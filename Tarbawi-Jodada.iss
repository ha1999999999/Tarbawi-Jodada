; ملف Inno Setup اختياري لبناء المثبت على Windows
#define MyAppName "مولّد الجذاذة – التربية الإسلامية"
#define MyAppVersion "0.1.0"
#define MyAppExeName "Tarbawi-Jodada.exe"
[Setup]
AppId={{8A4E5B22-0A10-4D89-9F9F-EDU001TARBAWI}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\Tarbawi-Jodada
DefaultGroupName={#MyAppName}
OutputDir=..\release
OutputBaseFilename=Tarbawi-Jodada-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
[Files]
Source: "..\dist\Tarbawi-Jodada.exe"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "تشغيل التطبيق"; Flags: nowait postinstall skipifsilent
