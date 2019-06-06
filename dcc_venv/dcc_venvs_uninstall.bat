SETLOCAL ENABLEDELAYEDEXPANSION

set DCC=%1
set MODE=%2
set INSTALLER_ACTIVE=0
if %MODE% == INSTALLER (
    set INSTALLER_ACTIVE=1
)


:: do all the dcc's if not currently installing a dcc
if %INSTALLER_ACTIVE% == 0 (

    FOR /D %%G in (dcc_venv\*) do (
        set FOLDER=%%~nxG
        if not "!FOLDER:~0,1!" == "_" (
            call :REMOVE_VENV %%~nxG
        )
    )
    
    echo.
    echo.
    echo Maya Packages Uninstalled
    echo.
    pause
    exit
)



:REMOVE_VENV
set DCC=%1
set VENV_FOLDER=.%DCC%_venv

call dcc_venv\%DCC%\venv_uninstall %DCC% INSTALLER

IF EXIST %VENV_FOLDER% (
    rmdir %VENV_FOLDER% /s /q
    echo Existing %VENV_FOLDER% deleted
)

IF EXIST venv_activate__%DCC%.bat (
    del venv_activate__%DCC%.bat
)
