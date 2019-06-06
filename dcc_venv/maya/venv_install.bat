:: #########################################################
:: setup .mod file #########################################
:: #########################################################

:: TOOL_NAME is determined by the current folder name
for %%I in (.) do set TOOL_NAME=%%~nxI

:: Check if modules folder exists
if not exist %UserProfile%\Documents\maya\modules mkdir %UserProfile%\Documents\maya\modules

:: Delete .mod file if it already exists
if exist %UserProfile%\Documents\maya\modules\%TOOL_NAME%.mod del %UserProfile%\Documents\maya\modules\%TOOL_NAME%.mod

:: Create file with contents in users maya/modules folder
(echo + %TOOL_NAME% 1.0 %CD%& echo scripts: .maya_venv/Lib/site-packages)>%UserProfile%\Documents\maya\modules\%TOOL_NAME%.mod 

:: end print 
@echo off
echo .mod file created at %UserProfile%\Documents\maya\modules\%TOOL_NAME%.mod

