@echo off
rem The one verification command for this workspace (Windows twin of verify.sh).
cd /d "%~dp0..\priorauth-api" && mvn -q test
