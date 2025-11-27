#!/bin/bash
set -e

echo "Creando entorno virtual..."
python3 -m venv venv

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Actualizando pip..."
pip install --upgrade pip

echo "Instalando dependencias..."
pip install matplotlib numpy pandas scipy seaborn chardet picnik-integrator rxnmodel pyinstaller #despues intentar quitar pillow para si por eso salen ventanas en la aplicacion

echo "Limpiando builds anteriores..."
rm -rf build dist ventana_principal.spec

echo "Compilando con PyInstaller..."
./venv/bin/pyinstaller --onefile --windowed \
  --collect-all matplotlib \
  --hidden-import=matplotlib.backends.backend_tkagg \
  --hidden-import=seaborn \
  --hidden-import=scipy \
  --hidden-import=pandas \
  --hidden-import=numpy \
  --hidden-import=chardet \
  --hidden-import=tkinter \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=picnik_integrator \
  --hidden-import=rxn_models\
  ventana_principal.py

echo "Ejecutable creado en dist/ventana_principal"

deactivate

