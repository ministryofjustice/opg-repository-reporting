from pathlib import Path
from datetime import datetime
import os

def timestamp_directory(report_type:str) -> str:
    """ Return the path to a timestamp based directory relative to the app root"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')

    directory = root_directory()
    path = Path(f"{directory}/__reports__/{report_type}/{timestamp}")
    os.makedirs(path, exist_ok=True)
    return path.resolve()


def app_directory() -> Path:
    """ Return root application directory """
    return Path(__file__).parent.parent.parent.resolve()

def root_directory() -> Path:
    """ Return the root of this code base """
    return Path(__file__).parent.parent.parent.parent.resolve()