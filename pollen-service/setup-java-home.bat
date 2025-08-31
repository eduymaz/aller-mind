@echo off
REM Script to set up JAVA_HOME for the Allermind Pollen Service

REM Update these paths to match your Java installation
SET JAVA_HOME=C:\Program Files\Java\jdk-21
SET PATH=%JAVA_HOME%\bin;%PATH%

echo JAVA_HOME is set to: %JAVA_HOME%
echo.
echo To make this permanent, set system environment variables:
echo 1. Right-click 'This PC' and select 'Properties'
echo 2. Click 'Advanced system settings'
echo 3. Click 'Environment Variables'
echo 4. Add JAVA_HOME with value: %JAVA_HOME%
echo 5. Add %%JAVA_HOME%%\bin to PATH
echo.
echo Current Java version:
java -version
