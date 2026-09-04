# Release Notes

All notable changes to **Achievement Reviver** are documented below.

---

## [2.0.0] - 2026-09-04

<div align="center">

![Build](https://img.shields.io/badge/Release-v2.0.0-6366f1?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows)
![Minecraft](https://img.shields.io/badge/Minecraft-Bedrock-5C8A32?style=flat-square&logo=minecraft)

</div>

### Highlights

| Feature | Description |
| :--- | :--- |
| 🖼️ **World Thumbnails** | Automatically loads in-game screenshots (`world_icon.jpeg`) |
| 🔒 **Process Guard** | Halts if `Minecraft.Windows.exe` is running to prevent file locks |
| 🔄 **Rollback Proof** | Syncs both `level.dat` and `level.dat_old` with `.bak` safety backups |
| 🔍 **Dual Scanner** | Auto-detects saves from both Bedrock GDK & classic Store UWP |
| ⚡ **Zero Latency** | Custom Little-Endian NBT stream patcher (<1ms execution) |

> [!TIP]
> Close Minecraft before reviving a world to avoid file access conflicts.

---

## [1.0.0] - 2026-09-04

- Initial release with inline Little-Endian NBT patching engine.
- Bedrock flag resets: `hasBeenLoadedInCreative`, `cheatsEnabled`, `commandsEnabled`, and Survival mode lock.
- PyInstaller and Inno Setup build configurations.
