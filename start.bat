:: This script allows the user to launch the bot without needing to learn command line
:: This script allows the user to choose between global and virtual python environment
:: Turn ECHO off
@echo off
setlocal
:: Turn ECHO on
:: echo on

echo This script will launch SpiritMS Script Spider.
echo Please select the environment to run the source code with:
echo A: Virtual Python Environment (Default)
echo B: Global Python Environment
choice /c AB /t 10 /d A /m "What is your choice"
if errorlevel 2 call :global
if errorlevel 1 call :virtual
:: Turn ECHO off
:: @echo off
endlocal

:: function to run from venv
echo You have selected A: Virtual Python Environment
:virtual
call venv\scripts\activate.bat
venv\scripts\python main.py
EXIT 0

:: function to run from global environment
:global
echo You have selected B: Global Python Environment
python main.py
EXIT 0