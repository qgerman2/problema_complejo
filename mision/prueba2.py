import asyncio
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk import mission_raw
from mavsdk.mission import (MissionItem, MissionPlan)

# Cargar una mision de despegue y aterrizaje


async def run():

    drone = System(mavsdk_server_address='localhost', port=50051)
    await drone.connect(system_address="udp://:14540")

    status_text_task = asyncio.create_task(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    # Crear mision
    mission_items = []
    # Accion de despegue
    # http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/mission.html#mavsdk.mission.MissionItem
    mission_items.append(mission_raw.MissionItem(
        seq=0,
        frame=0,
        command=16,
        current=1,
        autocontinue=1,
        param1=0.0,
        param2=0.0,
        param3=0.0,
        param4=0.0,
        x=-367818897,
        y=-730684843,
        z=16.489999771118164,
        mission_type=0
    ))

    mission_items.append(mission_raw.MissionItem(
        seq=1,
        frame=3,
        command=22,
        current=0,
        autocontinue=1,
        param1=0.0,
        param2=0.0,
        param3=0.0,
        param4=0.0,
        x=0,
        y=0,
        z=10.0,
        mission_type=0
    ))

    mission_items.append(mission_raw.MissionItem(
        seq=2,
        frame=3,
        command=21,
        current=0,
        autocontinue=1,
        param1=0.0,
        param2=0.0,
        param3=0.0,
        param4=1.0,
        x=-367818897,
        y=-730684843,
        z=0.0,
        mission_type=0
    ))

    print("-- Uploading mission")
    await drone.mission_raw.upload_mission(mission_items)
    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(20)

    print("-- Starting mission")
    await drone.mission.start_mission()

    status_text_task.cancel()


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


asyncio.run(run())
