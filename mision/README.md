## Entorno de desarrollo

### Programas a instalar

1. Instalar Python 3.12

    https://www.python.org/downloads/

2. Instalar dependencias

   1. Abrir terminal
   2. Instalar dependencias con pip
   ```bash
    py -3.12 -m pip install mavsdk
   ``` 
   3. Tomar nota de que version de mavsdk se instaló, es 2.8.4 al momento de escribir este documento.

3. Mavproxy

    https://firmware.ardupilot.org/Tools/MAVProxy/

4. Mavsdk-server

    _(Si `mavsdk.System()` en Python funciona saltar este paso)_

   1. Revisar qué version de MAVSDK server es compatible con la libreria de Python, para la 2.8.4 es **v2.12.10**
   https://github.com/mavlink/MAVSDK-Python/blob/2.8.4/MAVSDK_SERVER_VERSION

   2. Descargar el ejecutable del servidor correspondiente (**v2.12.10**) en https://github.com/mavlink/MAVSDK/releases, para Windows es el `mavsdk-windows-x64-release.zip`

   3. Extraer el `mavsdk_server_bin.exe` a `%APPDATA%\..\Local\Programs\Python\Python312\Lib\site-packages\mavsdk\bin`

   4. Renombrar el archivo a `mavsdk_server.exe`


### Inicializar mavproxy

```bash
mavproxy --no-console --master="com28",57600 --out=udp:127.0.0.1:14560 --out=udp:127.0.0.1:14540
```

### Ejecutar script python

```bash
py -3.12 prueba1.py
```