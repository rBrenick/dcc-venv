
@ECHO OFF

FOR /D %%G in ("%UserProfile%\Documents\MB\*") do (
    call :SETUP_MOBU_STARTUP %%~nxG
)

goto END

:SETUP_MOBU_STARTUP
set MOBU_VERSION=%1
echo Setting up Motionbuilder Version - %MOBU_VERSION%

:: TOOL_NAME is determined by the current folder name
for %%I in (.) do set TOOL_NAME=%%~nxI

set dst_folder=%UserProfile%\Documents\MB\%MOBU_VERSION%\config\PythonStartup
set dst=%dst_folder%\%TOOL_NAME%_startup.py

if not exist %dst_folder% mkdir %dst_folder%

:: Create file with contents in users maya/modules folder
(echo import runpy& echo runpy.run_path("%CD%\.mobu_venv\Lib\site-packages\userSetup.py", init_globals=globals(^)^))>%dst%

:END
