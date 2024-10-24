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

3. Mavproxy

    https://firmware.ardupilot.org/Tools/MAVProxy/

4. Mavsdk-server

   1. Descargar
   https://github.com/mavlink/MAVSDK/releases/download/v2.12.12/mavsdk-windows-x64-release.zip
   2. Descomprimir `mav_server_bin.exe` en `C:\Users\[usuario]`

### Inicializar mavproxy y mavsdk-server

```bash
mavproxy --no-console --master="com28",57600 --out=udp:127.0.0.1:14560 --out=udp:127.0.0.1:14540

./mavsdk_server_bin.exe -p 50051 udp://:14540
```

### Ejecutar script python

```bash
py -3.12 prueba1.py
```