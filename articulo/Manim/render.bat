@echo off
chcp 65001 > nul
echo ========================================================
echo   AcadAId - Renderizador de Videos de Presentacion
echo ========================================================
echo.
set PYTHON_EXE=python
if exist ".venv\Scripts\python.exe" set PYTHON_EXE=".venv\Scripts\python.exe"

echo Seleccione una opcion:
echo [1] Previsualizacion rapida (480p) - Explicacion Conceptual
echo [2] Video Final 1080p - Explicacion Conceptual Completa
echo [3] Diapositiva Animada Limpia 1080p (Para insertar en Slides)
echo [4] Matriz de Pesos 3D de la Red Neuronal (1080p)
echo [5] LLM 3D: Palabras y Silabas con Auto-Atencion (1080p)
echo [6] MMR 3D: Relevancia Marginal Maxima en Investigacion Cientifica (1080p)
echo [7] MMR 3D en 4K Ultra HD (2160p - Maxima Resolucion)
echo [8] LLM 3D en 4K Ultra HD (2160p - Maxima Resolucion)
echo [9] Selector Interactivo (Elige cuales videos y resolucion 4K/1080p)
echo [10] Renderizar TODO en 4K Ultra HD (Maxima Resolucion)
echo [11] Salir
echo.
set /p opt="Opcion (1-11): "

if "%opt%"=="1" %PYTHON_EXE% render.py --scene conceptual --preview --open
if "%opt%"=="2" %PYTHON_EXE% render.py --scene conceptual --quality high --open
if "%opt%"=="3" %PYTHON_EXE% render.py --scene slide --quality high --open
if "%opt%"=="4" %PYTHON_EXE% render.py --scene weights3d --quality high --open
if "%opt%"=="5" %PYTHON_EXE% render.py --scene llm3d --quality high --open
if "%opt%"=="6" %PYTHON_EXE% render.py --scene mmr3d --quality high --open
if "%opt%"=="7" %PYTHON_EXE% render.py --scene mmr3d --quality 4k --open
if "%opt%"=="8" %PYTHON_EXE% render.py --scene llm3d --quality 4k --open
if "%opt%"=="9" %PYTHON_EXE% render.py --interactive
if "%opt%"=="10" %PYTHON_EXE% render.py --scene all --quality 4k
if "%opt%"=="11" exit

pause
