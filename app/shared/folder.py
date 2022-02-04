from pathlib import Path
from datetime import datetime
import os

def timestamp_directory(report_type:str) -> str:
    """ Return the path to a timestamp based directory relative to the app root"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')

    directory = Path( os.path.dirname(__file__ ) + "/../../" ).resolve()
    path = Path(f"{directory}/__reports__/{report_type}/{timestamp}")
    os.makedirs(path, exist_ok=True)
    return path.resolve()
