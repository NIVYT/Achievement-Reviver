# Release Notes

All notable changes to **Achievement Reviver** will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [2.0.0] - 2026-09-04

### Major Update & Reliability Overhaul

Version 2.0 brings major stability improvements, UI enhancements, and safeguards to guarantee seamless world revival across all Windows Minecraft Bedrock installations.

#### New Features & Improvements
- **Real World Thumbnails:** Integrated automatic extraction and rendering of `world_icon.jpeg` thumbnails for all detected Bedrock worlds.
- **Active Process Safeguard:** Automatically detects if `Minecraft.Windows.exe` is currently running before attempting any mutations, preventing save file locks and autosave overwrites.
- **`level.dat_old` Synchronization:** Synchronizes modifications to `level.dat_old` (with backup) to prevent Minecraft from rolling back survival state on load.
- **On-Demand World Refresh:** Added an interactive `Refresh` button in the UI to reload worlds instantly without restarting the application.
- **Drag & Window Controls Optimization:** Decoupled titlebar drag regions from window controls, guaranteeing 100% responsive minimize and close interactions in WebView2.
- **Unsigned Short Handling:** Fixed NBT short unpack handling to unsigned format (`<H`) for tag string length headers.
- **Installer & Spec v2.0:** Updated PyInstaller spec and Inno Setup configuration for automated compilation into `Achievement_Reviver_Setup_v2.0.exe`.

---

## [1.0.0] - 2026-09-04

### Initial Release

- **Inline Little-Endian NBT Engine:** Parses and modifies Bedrock `level.dat` files in-place with zero external binary dependencies and sub-millisecond execution.
- **Achievement Restoration:** Automatically clears `hasBeenLoadedInCreative`, `cheatsEnabled`, `commandsEnabled`, sets `GameType` to `0` (Survival), and sets `ForceGameType` to `1`.
- **Dual World Scanner:** Automatically detects worlds saved via both Bedrock GDK (`%APPDATA%\Minecraft Bedrock\Users`) and classic Microsoft Store UWP (`%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState`).
- **Failsafe Automatic Backups:** Creates `level.dat.bak` copy prior to any byte mutation.
- **Modern Desktop UI:** Frameless `pywebview` interface with Edge WebView2, skeleton animations, and system tray integration.
