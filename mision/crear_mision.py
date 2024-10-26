import asyncio
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk import mission_raw
from mavsdk.mission import (MissionItem, MissionPlan)

# Cargar una mision de despegue y aterrizaje

address = "tcp://:5762"


async def run():

    # CONECTAR

    print("Creando mavsdk server")
    drone = System()
    print("Conectando a dron", address)
    await drone.connect(address)
    print("Conectado")

    # CREAR MISION

    pos = {
        'latitude_deg': 0,
        'longitude_deg': 0,
        'absolute_altitude_m': 0
    }

    # crear waypoints de mision
    # https://mavlink.io/en/services/mission.html
    mission_items = []

    # WAYPOINT NORMAL
    # el item 0 de la mision es el home location

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
        x=int(pos["latitude_deg"]*10**7),
        y=int(pos["longitude_deg"]*10**7),
        z=pos["absolute_altitude_m"],
        mission_type=0
    ))

    # DESPEGUE
    # https://mavlink.io/en/messages/common.html#MAV_CMD_NAV_TAKEOFF

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

    # ATERRIZAJE
    # https://mavlink.io/en/messages/common.html#MAV_CMD_NAV_LAND

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
        x=int(pos["latitude_deg"]*10**7),
        y=int(pos["longitude_deg"]*10**7),
        z=0,
        mission_type=0
    ))

    print("-- Uploading mission")
    await drone.mission_raw.upload_mission(mission_items)

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting mission")
    await drone.mission.start_mission()


asyncio.run(run())
