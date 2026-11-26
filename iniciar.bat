@echo off
:: Cambia el directorio de trabajo a la carpeta donde esta este archivo .bat
cd /d "%~dp0"

:: Carga las configuraciones relativas de WinPython
call "PythonPortable\scripts\env.bat"

:: Ejecuta tu aplicacion
streamlit run app.py

:: Pausa en caso de que la app se cierre por un error para que puedas leerlo
pause