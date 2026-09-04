# Achievement Reviver

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows%2010%20%2F%2011-0078D6?style=flat-square&logo=windows)
![Minecraft](https://img.shields.io/badge/Minecraft-Bedrock%20Edition-5C8A32?style=flat-square&logo=minecraft)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=flat-square&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

**Restore Xbox Achievements and pure Survival mode to your Minecraft Bedrock worlds in one click.**

</div>

---

## 📖 Overview

In **Minecraft Bedrock Edition**, toggling cheats on or switching to Creative mode flags your world permanently, disabling Xbox Live Achievements forever. 

**Achievement Reviver** solves this without third-party save bloat or complex external hex editors. It scans your local Minecraft Bedrock installation, parses the world's binary NBT data with a custom little-endian stream engine, removes the cheat flags, and locks the mode back to Survival.

---

## ✨ Features (v2.0)

- **⚡ Instant In-Place NBT Patching:** Sub-millisecond byte modification directly targeting the required NBT tags without re-serializing or risking compound corruption.
- **🖼️ Real World Thumbnails:** Automatically extracts and renders in-game screenshot thumbnails (`world_icon.jpeg`) for every detected Bedrock world.
- **🛡️ Failsafe Automatic Backups:** Automatically generates an uncompressed `level.dat.bak` duplicate before any file mutation.
- **🔒 Active Process Protection:** Checks if `Minecraft.Windows.exe` is running to prevent file locks or autosave overwrites.
- **🔄 `level.dat_old` Synchronization:** Patches both primary and backup `level.dat` files to guarantee Bedrock doesn't revert flags on restart.
- **🔍 Dual-Path World Discovery:** Automatically detects worlds saved across both:
  - **Bedrock GDK / Unified Launcher:** `%APPDATA%\Minecraft Bedrock\Users\<User>\games\com.mojang\minecraftWorlds`
  - **Classic Microsoft Store / UWP:** `%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds`
- **🎨 Modern Desktop UI:** Custom frameless interface powered by `pywebview` (Microsoft Edge WebView2) featuring real-time refresh, smooth skeleton loaders, responsive states, and system tray integration.
- **📦 Single Executable & Installer:** Available both as a standalone portable package and a lightweight Inno Setup installer.

---

## ⚙️ How It Works

Bedrock Edition stores world metadata inside `level.dat` using an 8-byte header (format version and payload size) followed by uncompressed little-endian NBT compounds.

Achievement Reviver reads the binary stream and performs byte-level adjustments on the following tags:

| NBT Tag | Type | Value Set | Purpose |
| :--- | :--- | :--- | :--- |
| `hasBeenLoadedInCreative` | `TAG_Byte` (1) | `0` | Clears the creative mode taint on the world. |
| `cheatsEnabled` | `TAG_Byte` (1) | `0` | Disables cheat mode flags. |
| `commandsEnabled` | `TAG_Byte` (1) | `0` | Disables command flags. |
| `GameType` | `TAG_Int` (3) | `0` | Enforces the primary game mode to Survival. |
| `ForceGameType` | `TAG_Byte` (1) | `1` | Enforces Survival on joining players. |

---

## 🚀 Getting Started

### Option A: Using the Installer
1. Download the latest `Achievement_Reviver_Setup_v2.0.exe` from the [Releases](../../releases) tab.
2. Run the installer (installs to `%LOCALAPPDATA%\Achievement Reviver`).
3. Launch **Achievement Reviver** from your Start Menu or Desktop.

### Option B: Running from Source
Ensure you have **Python 3.10+** installed on Windows.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NIVYT/Achievement-Reviver.git
   cd Achievement-Reviver
   ```

2. **Install dependencies:**
   ```bash
   pip install pywebview pystray Pillow
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

---

## 🛠️ Building & Packaging

### 1. Build Executable with PyInstaller
```bash
pyinstaller Achievement-Reviver.spec
```
The compiled output will be generated in `dist/Achievement-Reviver/`.

### 2. Build Inno Setup Installer
Ensure [Inno Setup 6](https://jrsoftware.org/isdl.php) is installed.
1. Open `installer_builder.iss` in Inno Setup Compiler.
2. Click **Compile** (or run `& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_builder.iss`).
3. The ready-to-distribute installer will be created inside `./Inno_Output/`.

---

## ⚠️ Notes & Best Practices

> [!IMPORTANT]
> **Close Minecraft before reviving a world:** Achievement Reviver automatically detects if Minecraft is running and prompts you to exit the game to prevent save file conflicts.

> [!TIP]
> If you ever need to restore your world to its previous state, simply rename the created `level.dat.bak` back to `level.dat` in your world's directory.

---

## 📄 License

This project is open-source software licensed under the [MIT License](LICENSE).

Copyright (c) 2026 **NIVYT**.
