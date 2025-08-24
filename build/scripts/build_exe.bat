@echo off
echo ========================================
echo InvoiceArtisan Executable Builder
echo ========================================
echo.

echo Installing/updating dependencies...
python -m pip install -r requirements.txt

echo.
echo Building executable...
python build_exe.py

echo.
echo Build process completed!
echo Check the 'dist' folder for your executable.
echo.
pause
