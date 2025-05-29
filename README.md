PyInstaller
PyInstaller incorpora el intérprete de Python y todas las dependencias del código dentro de un archivo ejecutable. Pero para poder utilizarlo, primero tenemos que instalarlo como si fuera una dependencia más de nuestro código Python. El comando para instalarlo es el siguiente:

$ pip install pyinstaller
Notar que aunque no lo haya mencionado, es preferible hacer dicha instalación dentro de un entorno virtual específico para el proyecto en cuestión.

Uso de PyInstaller
Una vez tenemos instalado PyInstaller, su uso es como el de una aplicación de línea de comandos. Es decir, lo utilizamos desde el CMD o PowerShell en Windows y desde la Terminal en macOS y Linux. Dentro del directorio raíz de nuestra aplicación, si nuestro fichero Python que contiene la entrada a nuestro programa se llama ejemplo.py, el comando para convertirlo en un fichero ejecutabe es el siguiente:

$ pyinstaller script.py
Al ejecutar dicho comando, PyInstaller nos mostrará un montón de mensajes por la consola mientras crea el fichero ejecutable.

Resultado de ejecutar PyInstaller
Al finalizar la ejecución, veremos que se nos han generado las siguientes dos carpetas:

build: Contiene metadatos generados por PyInstaller para crear el archivo ejecutable. Raramente vamos a necesitar estos archivos, así que podemos ignorar esta carpeta.
dist: Esta carpeta a su vez contiene otra carpeta con el nombre de nuestro script, ejemplo en nuestro caso; y es en esta carpeta es donde encontramos nuestro fichero ejecutable, junto con otras dependencias. Por tanto, esta última carpeta es lo que tenemos que distribuir. Aunque como veremos a continuación podemos indicar a PyInstaller que nos genere un sólo fichero ejecutable.
