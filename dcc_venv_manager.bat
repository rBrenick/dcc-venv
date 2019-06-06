@ECHO OFF
:BEGIN
CLS

ECHO Welcome to the DCC Virtual Environment Manager
ECHO Here are the options
ECHO.


ECHO    1. Setup environment (Artist)
ECHO    2. Get Latest Tools
ECHO.
ECHO Advanced:
ECHO    3. Setup environment (Tool Dev)
ECHO    4. Make New Tool
ECHO    5. Uninstall

ECHO.
SET /P AREYOUSURE=Choice: 
IF /I "%AREYOUSURE%" EQU "1" GOTO :Install
IF /I "%AREYOUSURE%" EQU "2" GOTO :GetLatest
IF /I "%AREYOUSURE%" EQU "3" GOTO :InstallDev
IF /I "%AREYOUSURE%" EQU "4" GOTO :MakeNewTool
IF /I "%AREYOUSURE%" EQU "5" GOTO :Uninstall


:Install
CALL dcc_venv\dcc_venvs_install.bat ARTIST
GOTO END

:InstallDev
CALL dcc_venv\dcc_venvs_install.bat DEV
GOTO END

:Uninstall
CALL dcc_venv\dcc_venvs_uninstall.bat x STANDALONE
GOTO END


:GetLatest
CALL dcc_venv\dcc_venvs_update.bat
GOTO END


:MakeNewTool
Powershell.exe -executionpolicy remotesigned -File  _install_\create_new_tool.ps1


:END
PAUSE