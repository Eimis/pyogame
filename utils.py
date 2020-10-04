from datetime import timedelta
import os

from ogame import OGame
from ogame.constants import coordinates, ships, mission, speed

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

app = Celery('tasks', broker=os.environ.get('CELERY_BROKER_URL'))

app.conf.beat_schedule = {
    'send-expeditions': {
        'task': 'utils.send_expeditions',
        'schedule': crontab(minute='*/15'),  # every 15 mins
    },
}
app.conf.timezone = 'Europe/Vilnius'

logger = get_task_logger(__name__)


@app.task
def send_expeditions():

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

    for planet in empire.planet_ids():
        planet_ships = empire.ships(planet)

        if (
            bool(planet_ships.large_transporter.amount)
            and bool(planet_ships.explorer.amount)
            and expedition_count < AVAILABLE_EXPEDITIONS
        ):

            logger.info('Attempting to send Expedition for planet: '.format(planet))

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

            expedition_count += 1
        else:
            logger.info('No expeditions were started, current count: {0}'.format(
                expedition_count
            ))

            break
