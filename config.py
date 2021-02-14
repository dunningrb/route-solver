import os
from pathlib import Path

ROOT_PATH = str(Path(os.path.dirname(os.path.realpath(__file__)))).replace("\\", "/")

CITY_GPS_PATH = f'{ROOT_PATH}/city-gps.txt'
ROAD_SEGMENTS_PATH = f'{ROOT_PATH}/road-segments.txt'

LOG_CONFIG = f'logging.ini'    # Config file for log files.
LOG_PATH = f'{ROOT_PATH}/'  # Path for log files.
LOG_FILEPATH = f'{LOG_PATH}/log.log'
LOG_DEFAULT = {'logfilepath': LOG_FILEPATH}     # defaults dict for logging.config.fileConfig().
