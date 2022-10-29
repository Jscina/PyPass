; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "PyPass"
#define MyAppVersion "6.0"
#define MyAppPublisher "Jscin"
#define MyAppURL "https://www.jscin.com/"
#define MyAppExeName "PyPass.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".pypass"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{71BB8DA4-3492-4C4D-90C7-B58981202EB7}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ChangesAssociations=yes
DisableProgramGroupPage=yes
LicenseFile=C:\GitHub_Windows_Repos\PyPass\_BuildFolder\LICENSE.txt
InfoBeforeFile=C:\GitHub_Windows_Repos\PyPass\_BuildFolder\infobefore.txt
InfoAfterFile=C:\GitHub_Windows_Repos\PyPass\_BuildFolder\infoafter.txt
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputDir=PyPass
OutputBaseFilename=PyPass Setup
SetupIconFile=C:\GitHub_Windows_Repos\PyPass\_BuildFolder\setup.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\GitHub_Windows_Repos\PyPass\Staging\PyPass\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\GitHub_Windows_Repos\PyPass\Staging\PyPass\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
; NOTE: The secret key here is only a placeholder, DO NOT USE IN PRODUCTION
Root: HKCU; Subkey: "Environment"; ValueType:string; ValueName: "PYPASS_SECRET"; ValueData: "gizNQcBJHfECgTa2-vmzGIftwH3nfq_MzjGmaBYCOsA="; Flags: preservestringtype

[Setup]
; Tell Windows Explorer to reload the environment
ChangesEnvironment=true

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

