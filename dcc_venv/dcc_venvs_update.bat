@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION
FOR /D %%G in (dcc_venv\*) do (
    set FOLDER=%%~nxG
    if not "!FOLDER:~0,1!" == "_" (
        call :UPDATE_VENV %%~nxG
    )
)

PAUSE
EXIT


:UPDATE_VENV
set DCC=%1
set VENV_FOLDER=.%DCC%_venv

CALL %VENV_FOLDER%\Scripts\activate.bat

IF EXIST %VENV_FOLDER%\src (
    echo Upgrading DEV - %DCC%
    python dcc_venv\_python_\create_requirements_d.py dcc_venv\%DCC%\requirements.txt
    pip install --upgrade --force-reinstall -r dcc_venv\%DCC%\requirements_DEV.txt
    del dcc_venv\%DCC%\requirements_DEV.txt
    
) ELSE (
    echo Upgrading Standard Packages - %DCC%
    pip install --upgrade --force-reinstall -r dcc_venv\%DCC%\requirements.txt
)

