import asyncio
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk import mission_raw
from mavsdk.mission import (MissionItem, MissionPlan)

# Descargar mision actual e imprimir parametros

address = "tcp://:5762"


async def run():
    print("Creando mavsdk server")
    drone = System()
    print("Conectando a dron", address)
    await drone.connect(address)

    # Descargar mision
    print("Descargando mision...")
    mision = await drone.mission_raw.download_mission()
    for item in mision:
        print(item)

asyncio.run(run())
