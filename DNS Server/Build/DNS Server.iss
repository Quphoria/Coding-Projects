; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Python DNS Server"
#define MyAppVersion "1.5"
#define MyAppPublisher "Samuel Simpson"
#define MyAppExeName "pythonw.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{1A190DF6-915C-4B8F-AF9D-783541ECA9D0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=C:\Users\Owner\Desktop\Coding Projects\DNS Server\Source\LICENSE.txt
InfoBeforeFile=C:\Users\Owner\Desktop\Coding Projects\DNS Server\Source\PRE_INSTALL.txt
InfoAfterFile=C:\Users\Owner\Desktop\Coding Projects\DNS Server\Source\POST_INSTALL.txt
OutputDir=C:\Users\Owner\Desktop\Coding Projects\DNS Server\Build
OutputBaseFilename=DNSServerSetup
SetupIconFile=C:\Users\Owner\Desktop\Coding Projects\DNS Server\Source\installer.ico
Compression=lzma
SolidCompression=yes
DisableDirPage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

;[Tasks]
;Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Owner\Desktop\Coding Projects\DNS Server\Source\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

;[Icons]
;Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Parameters: """{app}\dns_server.py"""
;Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Parameters: """{app}\dns_server.py"""; Tasks: desktopicon

[Run]
;Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser; Parameters: """{app}\dns_server.py"""
Filename: "{app}\NSSM\nssm.exe"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: runascurrentuser; Parameters: "install ""{#MyAppName}"" ""{app}\{#MyAppExeName}"" """"""{app}\dns_server.py"""""""
Filename: "{app}\NSSM\nssm.exe"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: runascurrentuser; Parameters: "set ""{#MyAppName}"" ObjectName ""NT Authority\Network Service"""
Filename: "{app}\NSSM\nssm.exe"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: runascurrentuser; Parameters: "set ""{#MyAppName}"" AppStdout ""{app}\Logs\service.log"""
Filename: "{app}\NSSM\nssm.exe"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: runascurrentuser; Parameters: "set ""{#MyAppName}"" AppStderr ""{app}\Logs\service.log"""
Filename: "icacls"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: runascurrentuser; Parameters: """{app}"" /grant ""NT Authority\Network Service"":(OI)(CI)F /T"
Filename: "{app}\NSSM\nssm.exe"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser; Parameters: "start ""{#MyAppName}"""

[UninstallRun]
Filename: "{app}\NSSM\nssm.exe"; Flags: runascurrentuser; Parameters: "stop ""{#MyAppName}"""
Filename: "{app}\NSSM\nssm.exe"; Flags: runascurrentuser; Parameters: "remove ""{#MyAppName}"" confirm"
