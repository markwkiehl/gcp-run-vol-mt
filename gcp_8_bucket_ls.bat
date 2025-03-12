@echo off
cls
echo %~n0%~x0   version 0.0.0
echo.

rem Created by Mechatronic Solutions LLC
rem Mark W Kiehl
rem
rem LICENSE: MIT


rem Batch files: https://steve-jansen.github.io/guides/windows-batch-scripting/
rem Batch files: https://tutorialreference.com/batch-scripting/batch-script-tutorial
rem Scripting Google CLI:  https://cloud.google.com/sdk/docs/scripting-gcloud

rem Verify that CLOUDSDK_PYTHON has already been set permanently for the user by gcp_part1.bat
IF NOT EXIST "%CLOUDSDK_PYTHON%" (
echo ERROR: CLOUDSDK_PYTHON path not found.  %CLOUDSDK_PYTHON%
echo Did you previously run gcp_part1.bat ?
EXIT /B
)


rem Make sure GOOGLE_APPLICATION_CREDENTIALS is not set so that Google ADC flow will work properly.
IF NOT "%GOOGLE_APPLICATION_CREDENTIALS%"=="" (
echo .
echo ERROR: GOOGLE_APPLICATION_CREDENTIALS has been set!
echo GOOGLE_APPLICATION_CREDENTIALS=%GOOGLE_APPLICATION_CREDENTIALS%
echo The environment variable GOOGLE_APPLICATION_CREDENTIALS must NOT be set in order to allow Google ADC to work properly.
echo Press RETURN to unset GOOGLE_APPLICATION_CREDENTIALS, CTRL-C to abort. 
pause
@echo on
SET GOOGLE_APPLICATION_CREDENTIALS=
CALL SETX GOOGLE_APPLICATION_CREDENTIALS ""
@echo off
echo Restart this file %~n0%~x0
EXIT /B
)



SETLOCAL

rem Define the working folder to Google Cloud CLI (gcloud) | Google Cloud SDK Shell
rem derived from the USERPROFILE environment variable.
rem This requires that the Google CLI/SKD has already been installed.
SET PATH_GCLOUD=%USERPROFILE%\AppData\Local\Google\Cloud SDK
IF NOT EXIST "%PATH_GCLOUD%\." (
	echo ERROR: PATH_GCLOUD path not found.  %PATH_GCLOUD%
	echo Did you install Google CLI / SKD? 
	EXIT /B
)
rem echo PATH_GCLOUD: %PATH_GCLOUD%

rem The current working directory for this script should be the same as the Python virtual environment for this project.
SET PATH_SCRIPT=%~dp0


echo.
echo PROJECT LOCAL VARIABLES:
echo.

rem import the GCP project constants from file gcp_constants.bat
if EXIST "gcp_constants.bat" (
  for /F "tokens=*" %%I in (gcp_constants.bat) do set %%I
) ELSE (
  echo ERROR: unable to find gcp_constants.bat
  EXIT /B
)


rem ----------------------------------------------------------------------
rem Edit the project variables below

rem set GCP_PROJ_ID=data-platform-v0-0
echo GCP_PROJ_ID: %GCP_PROJ_ID%

rem Google Run Jobs mount volume name
echo GCP_RUN_JOB_VOL_NAME: %GCP_RUN_JOB_VOL_NAME%

rem Google Run Jobs mount volume path
echo GCP_RUN_JOB_VOL_MT_PATH: %GCP_RUN_JOB_VOL_MT_PATH%

rem Google Storage Bucket
echo GCP_GS_BUCKET: %GCP_GS_BUCKET%  (gs://%GCP_GS_BUCKET%)



rem ----------------------------------------------------------------------

rem Show the bucket contents with the Cloud Console URL
echo.
echo.
echo View the bucket file contents in the Cloud Console with the URL: 
echo https://console.cloud.google.com/storage/browser/%GCP_GS_BUCKET%?project=%GCP_PROJ_ID%
echo.
echo.


rem Show the bucket file contents
echo.
echo Show the bucket file contents with the command: "gcloud storage ls gs://%GCP_GS_BUCKET%"
echo Contents of bucket "gs://%GCP_GS_BUCKET%":
CALL gcloud storage ls gs://%GCP_GS_BUCKET%



ENDLOCAL

echo.
echo This batch file %~n0%~x0 has ended normally (no errors).  
echo You can repeat running this batch file as frequently as you wish.
echo When you are ready to delete the Google Project and all of the related contents, execute "gcp_9_cleanup.bat".

