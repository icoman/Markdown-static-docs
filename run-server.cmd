@echo off


SET MD_FOLDER=%CD%
:SET PY=c:\python27\python
SET PY=c:\python37\python
SET PORT=80
SET HOST=localhost
:loop
	if exist main.py %PY% main.py
	if exist main.exe main.exe
	if NOT "0" == "%ERRORLEVEL%" pause
goto loop


