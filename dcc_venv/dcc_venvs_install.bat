
set MODE=%1
set DEV_MODE=0
if %MODE% == DEV (
    set DEV_MODE=1
)

@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION
FOR /D %%G in (dcc_venv\*) do (
    set FOLDER=%%~nxG
    if not "!FOLDER:~0,1!" == "_" (
        call :SETUP_VENV %%~nxG
    )
)


PAUSE
EXIT


:SETUP_VENV
set DCC=%1
set VENV_FOLDER=.%DCC%_venv

echo Setting up %DCC% virtualenv

:: Remove existing venv
call dcc_venv\dcc_venvs_uninstall %DCC% INSTALLER

:: create new venv
echo Creating %VENV_FOLDER% ...
python -m venv %VENV_FOLDER%
CALL %VENV_FOLDER%/Scripts/activate.bat


if %DEV_MODE% == 0 (
    pip install -r dcc_venv\%DCC%\requirements.txt
)

if %DEV_MODE% == 1 (
    python dcc_venv\_python_\create_requirements_dev.py dcc_venv\%DCC%\requirements.txt
    pip install -r dcc_venv\%DCC%\requirements_DEV.txt
    del dcc_venv\%DCC%\requirements_DEV.txt

)

call dcc_venv\%DCC%\venv_install

echo f | xcopy dcc_venv\_python_\dcc_startup.py %VENV_FOLDER%\Lib\site-packages\userSetup.py


(echo start cmd /k call %VENV_FOLDER%/Scripts/activate.bat)>venv_activate__%DCC%.bat

:: final message ###########################################################################################

echo.
echo.
echo %DCC% Packages Installed
echo.
