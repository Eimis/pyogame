import os
from ogame import OGame
from ogame.constants import coordinates, ships, mission, speed


def send_expedition():

    empire = OGame(
        'Leda',
        os.environ.get('OGAME_USERNAME'),
        os.environ.get('OGAME_PASSWORD'),
    )

    expedition_count = len([
        fleet.mission == mission.expedition
        for fleet in empire.fleet()
        if fleet.mission == mission.expedition]
    )

    AVAILABLE_EXPEDITIONS = 5

    if expedition_count < AVAILABLE_EXPEDITIONS:
        for planet in empire.planet_ids():
            planet_ships = empire.ships(planet)

            if (
                bool(planet_ships.large_transporter.amount)
                and bool(planet_ships.explorer.amount)
            ):

                empire.send_fleet(
                    mission=mission.expedition,
                    id=id,
                    where=coordinates(8, 208, 16),
                    ships=[
                        ships.large_transporter(planet_ships.large_transporter.amount),
                        ships.explorer(planet_ships.explorer.amount),
                    ],
                    resources=[0, 0, 0],  # optional default no resources
                    speed=speed.max,      # optional default speed.max
                    holdingtime=2
                )
