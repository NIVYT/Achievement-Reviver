import os
import sys
import struct
import threading
import time
import ctypes
import shutil
import base64
import subprocess
import webview
import pystray
from PIL import Image

try:
    myappid = 'achievementreviver.2.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def is_minecraft_running():
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        output = subprocess.check_output(
            'tasklist /FI "IMAGENAME eq Minecraft.Windows.exe" /NH',
            shell=True,
            text=True,
            startupinfo=startupinfo
        )
        return 'Minecraft.Windows.exe' in output
    except:
        return False

# ==========================================
# 💾 INLINE LITTLE-ENDIAN NBT ENGINE
# ==========================================
class NBTStream:
    def __init__(self, data):
        self.data = bytearray(data)
        self.offset = 0

    def read_byte(self):
        val = self.data[self.offset]
        self.offset += 1
        return val

    def write_byte_at(self, offset, val):
        self.data[offset] = val & 0xFF

    def read_short(self):
        val = struct.unpack_from('<H', self.data, self.offset)[0]
        self.offset += 2
        return val

    def read_int(self):
        val = struct.unpack_from('<i', self.data, self.offset)[0]
        self.offset += 4
        return val

    def write_int_at(self, offset, val):
        struct.pack_into('<i', self.data, offset, val)

    def skip(self, n):
        self.offset += n

    def scan_and_patch(self, targets):
        try:
            root_type = self.read_byte()
            if root_type != 10: return False
            name_len = self.read_short()
            self.skip(name_len)
            self._parse_compound(targets)
            return True
        except: return False

    def _parse_compound(self, targets):
        while self.offset < len(self.data):
            tag_type = self.read_byte()
            if tag_type == 0: break
            
            name_len = self.read_short()
            name = self.data[self.offset:self.offset+name_len].decode('utf-8', errors='ignore')
            self.skip(name_len)

            if name in targets:
                expected_type, target_val = targets[name]
                if tag_type == expected_type:
                    if tag_type == 1: self.write_byte_at(self.offset, target_val)
                    elif tag_type == 3: self.write_int_at(self.offset, target_val)
            
            self._skip_payload(tag_type, targets)

    def _skip_payload(self, tag_type, targets):
        if tag_type == 1: self.skip(1)
        elif tag_type == 2: self.skip(2)
        elif tag_type == 3: self.skip(4)
        elif tag_type == 4: self.skip(8)
        elif tag_type == 5: self.skip(4)
        elif tag_type == 6: self.skip(8)
        elif tag_type == 7: self.skip(self.read_int())
        elif tag_type == 8: self.skip(self.read_short())
        elif tag_type == 9: 
            sub_type = self.read_byte()
            for _ in range(self.read_int()): self._skip_payload(sub_type, targets)
        elif tag_type == 10: self._parse_compound(targets)
        elif tag_type == 11: self.skip(self.read_int() * 4)
        elif tag_type == 12: self.skip(self.read_int() * 8)

# ==========================================
# 🌐 BACKEND API ROUTER
# ==========================================
class Api:
    def __init__(self):
        self.discovered_worlds = {}
        self._window = None

    def set_window(self, window):
        self._window = window

    def minimize_window(self):
        if self._window: self._window.minimize()

    def close_window(self):
        if self._window:
            self._window.hide()
            
        def fast_kill():
            time.sleep(0.1)
            os._exit(0)
            
        threading.Thread(target=fast_kill, daemon=True).start()
        
    def scan_worlds(self):
        self.discovered_worlds.clear()
        worlds_list = []
        search_dirs = []

        # 1. Bedrock GDK / Unified Launcher path
        gdk_base = os.path.expandvars(r'%APPDATA%\Minecraft Bedrock\Users')
        if os.path.exists(gdk_base):
            try:
                for user_dir in os.listdir(gdk_base):
                    if user_dir.lower() == 'shared': continue
                    target = os.path.join(gdk_base, user_dir, 'games', 'com.mojang', 'minecraftWorlds')
                    if os.path.isdir(target):
                        search_dirs.append(target)
            except: pass

        # 2. Classic Microsoft Store / UWP path
        uwp_target = os.path.expandvars(r'%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds')
        if os.path.isdir(uwp_target):
            search_dirs.append(uwp_target)

        for target_path in search_dirs:
            try:
                for folder in os.listdir(target_path):
                    folder_path = os.path.join(target_path, folder)
                    if not os.path.isdir(folder_path): continue
                    level_dat = os.path.join(folder_path, 'level.dat')
                    
                    if os.path.exists(level_dat):
                        display_name = folder
                        levelname_txt = os.path.join(folder_path, 'levelname.txt')
                        if os.path.exists(levelname_txt):
                            try:
                                with open(levelname_txt, 'r', encoding='utf-8', errors='ignore') as f:
                                    display_name = f.read().strip()
                            except: pass
                        
                        # Load world thumbnail if present
                        icon_b64 = None
                        icon_file = os.path.join(folder_path, 'world_icon.jpeg')
                        if os.path.exists(icon_file):
                            try:
                                with open(icon_file, 'rb') as img_f:
                                    icon_b64 = "data:image/jpeg;base64," + base64.b64encode(img_f.read()).decode('ascii')
                            except: pass

                        self.discovered_worlds[folder] = level_dat
                        worlds_list.append({'id': folder, 'name': display_name, 'icon': icon_b64})
            except: pass
        return worlds_list

    def unlock_world(self, world_id):
        if is_minecraft_running():
            return {
                "status": "error",
                "message": "Minecraft is currently open! Please exit the game before reviving to prevent file corruption."
            }

        if world_id not in self.discovered_worlds:
            return {"status": "error", "message": "Selected world path missing."}

        file_path = self.discovered_worlds[world_id]
        backup_path = file_path + ".bak"

        try:
            shutil.copy2(file_path, backup_path)
            with open(file_path, 'rb') as f: raw_bytes = f.read()

            if len(raw_bytes) < 8: return {"status": "error", "message": "Invalid level.dat file structure."}

            header, nbt_payload = raw_bytes[:8], raw_bytes[8:]
            stream = NBTStream(nbt_payload)
            
            targets = {
                "hasBeenLoadedInCreative": (1, 0), 
                "cheatsEnabled": (1, 0),
                "commandsEnabled": (1, 0), 
                "GameType": (3, 0),
                "ForceGameType": (1, 1)  
            }

            if not stream.scan_and_patch(targets):
                return {"status": "error", "message": "NBT parsing failed."}

            with open(file_path, 'wb') as f:
                f.write(header + stream.data)

            # Also synchronize level.dat_old if it exists to prevent Bedrock rollback
            level_old = os.path.join(os.path.dirname(file_path), 'level.dat_old')
            if os.path.exists(level_old):
                try:
                    shutil.copy2(level_old, level_old + ".bak")
                    with open(level_old, 'wb') as f_old:
                        f_old.write(header + stream.data)
                except: pass

            return {"status": "success", "message": "World Revived! Mode set to Survival and Achievements re-enabled."}

        except Exception as e:
            if os.path.exists(backup_path): shutil.copy2(backup_path, file_path)
            return {"status": "error", "message": f"Error: {str(e)}"}

# ==========================================
# 🔒 APP WINDOW SYSTEM
# ==========================================
def on_loaded():
    time.sleep(0.2)
    try: window.show()
    except: pass

def on_closing():
    os._exit(0)

def setup_system_tray(window):
    try:
        image = Image.open(get_resource_path('logo.ico'))
        def show_app(icon, item): window.show()
        def quit_app(icon, item):
            icon.stop()
            os._exit(0)
            
        menu = pystray.Menu(
            pystray.MenuItem("Open Achievement Reviver", show_app, default=True),
            pystray.MenuItem("Exit Completely", quit_app)
        )
        tray_icon = pystray.Icon("Achievement_Reviver", image, "Achievement Reviver", menu)
        threading.Thread(target=tray_icon.run, daemon=True).start()
    except: pass

if __name__ == '__main__':
    api = Api()
    
    window = webview.create_window(
        title='Achievement Reviver',
        url=get_resource_path('index.html'),
        js_api=api,
        width=580,
        height=530,
        resizable=False,
        frameless=True, 
        easy_drag=False, 
        background_color='#f0f2f5',
        hidden=True 
    )
    
    api.set_window(window)
    window.events.loaded += on_loaded
    window.events.closing += on_closing
    
    if os.path.exists(get_resource_path('logo.ico')):
        setup_system_tray(window)
        
    webview.start(debug=False)