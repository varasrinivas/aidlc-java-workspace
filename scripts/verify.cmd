@echo off
rem The one verification command for this workspace (Windows twin of verify.sh; the logic is in verify.ps1).
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify.ps1" %*
exit /b %ERRORLEVEL%
