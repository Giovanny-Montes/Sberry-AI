#!/bin/bash

# Actualizar el sistema
echo "Actualizando el sistema..."

sudo apt update

# Instalar las dependencias del sistema operativo
echo "Instalando dependencias del sistema operativo..."
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf \
libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
cmake libffi-dev libssl-dev

# Instalar Cython y virtualenv
echo "Instalando Cython y virtualenv..."
pip3 install --user --upgrade Cython==0.29.33 virtualenv

# Crear un entorno virtual llamado "app"
echo "Creando el entorno virtual 'app'..."
python3 -m virtualenv app

# Activar el entorno virtual
echo "Activando el entorno virtual..."
source app/bin/activate

# Crear el archivo requirements.txt con las dependencias
echo "Creando el archivo requirements.txt..."
cat <<EOL > requirements.txt
kivy==2.2.1
opencv-python==4.8.1
numpy==1.24.3
tensorflow==2.14.0
keras==2.14.0
Cython==0.29.33
EOL

# Instalar las dependencias de Python dentro del entorno virtual
echo "Instalando dependencias de Python en el entorno virtual..."
pip install -r requirements.txt

# Clonar el repositorio de Buildozer
echo "Clonando el repositorio de Buildozer..."
git clone https://github.com/kivy/buildozer

# Navegar al directorio buildozer
cd buildozer

# Construir e instalar Buildozer
echo "Instalando Buildozer..."
python setup.py build
pip install -e .

# Volver al directorio del proyecto
cd ..

# Compilar la aplicación para Android
echo "Compilando la aplicación para Android en modo depuración..."
buildozer -v android debug

echo "Proceso completado."
