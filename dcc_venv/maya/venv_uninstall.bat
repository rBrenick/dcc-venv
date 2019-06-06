:: TOOL_NAME is determined by the current folder name
for %%I in (.) do set TOOL_NAME=%%~nxI

:: Delete .mod file if it already exists
IF EXIST %UserProfile%\Documents\maya\modules\%TOOL_NAME%.mod (
    del %UserProfile%\Documents\maya\modules\%TOOL_NAME%.mod
    echo .mod file removed from %UserProfile%\Documents\maya\modules\%TOOL_NAME%.mod
)
