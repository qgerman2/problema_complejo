import asyncio
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk import mission_raw
from mavsdk.mission import (MissionItem, MissionPlan)

# Descargar mision actual e imprimir parametros


async def run():

    drone = System(mavsdk_server_address='localhost', port=50051)
    await drone.connect(system_address="udp://:14540")

    status_text_task = asyncio.create_task(print_status_text(drone))

    # Descargar mision
    print("Descargando mision...")
    mision = await drone.mission_raw.download_mission()
    for item in mision:
        print(item)

    status_text_task.cancel()


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


asyncio.run(run())
