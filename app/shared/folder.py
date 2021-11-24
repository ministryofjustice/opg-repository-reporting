from pathlib import Path
from datetime import datetime
import os

def timestamp_directory(type:str = "dependencies") -> str:
    ts = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')

    dir = Path( os.path.dirname(__file__ ) + "/../../" ).resolve()
    path = Path(f"{dir}/__reports__/{type}/{ts}")
    os.makedirs(path, exist_ok=True)
    return path.resolve()
