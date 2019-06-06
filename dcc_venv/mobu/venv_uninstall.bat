
@ECHO OFF
echo MOBU INSTALL THINGS

FOR /D %%G in ("%UserProfile%\Documents\MB\*") do (
    call :REMOVE_MOBU_STARTUP %%~nxG
)

goto END

:REMOVE_MOBU_STARTUP
set MOBU_VERSION=%1
echo Removing startup for Motionbuilder Version - %MOBU_VERSION%

:: TOOL_NAME is determined by the current folder name
for %%I in (.) do set TOOL_NAME=%%~nxI

set dst_folder=%UserProfile%\Documents\MB\%MOBU_VERSION%\config\PythonStartup
set dst=%dst_folder%\%TOOL_NAME%_startup.py


:: Delete startup file if it exists
if exist %dst% del %dst%


:END
