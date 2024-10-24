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
    # https://mavlink.io/en/messages/common.html#MAV_CMD_NAV_TAKEOFF
    mission_items.append(mission_raw.MissionItem(
        # start seq at 0
        0,
        # MAV_FRAME command. 3 is WGS84 + relative altitude
        3,
        # command. 16 is a basic waypoint
        22,
        # first one is current
        1,
        # auto-continue. 1: True, 0: False
        1,
        # param1
        0,
        # param2 - Acceptance radius
        10,
        # param3 - 0 (pass through the waypoint normally)
        0,
        # param4 - Desired yaw angle at waypoint
        float('nan'),
        # param5 - latitude
        0,
        # param6 - longitude
        0,
        # param7 - altitude
        10.0,
        # mission_type.
        0
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
