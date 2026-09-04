; ===================================================
; Achievement Reviver - Professional Inno Script
; ===================================================

#define MyAppName "Achievement Reviver"
#define MyAppVersion "2.0"
#define MyAppPublisher "NIVYT"
#define MyAppExeName "Achievement-Reviver.exe"

[Setup]
AppId={{C4B7D2E1-5A8F-4B9C-92D3-81E4F5A6B7C8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={localappdata}\{#MyAppName}
DisableProgramGroupPage=yes

PrivilegesRequired=lowest
OutputDir=.\Inno_Output
OutputBaseFilename=Achievement_Reviver_Setup_v2.0
SetupIconFile=logo.ico
Compression=lzma2/ultra
SolidCompression=yes
WizardStyle=modern

UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\Achievement-Reviver\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Achievement-Reviver\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconIndex: 0
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconIndex: 0; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent