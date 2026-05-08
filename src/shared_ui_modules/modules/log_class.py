import logging
from pathlib import Path
import datetime

log_dir = Path("./logs")
log_dir.mkdir(parents=True, exist_ok=True)

current_timestamp = datetime.datetime.today()

file_name = log_dir / f"JHMR_LOG_{current_timestamp.day}-{current_timestamp.month:02d}-{current_timestamp.year}.log"

logging.basicConfig(level=logging.DEBUG)
file_handler = logging.FileHandler(file_name)
formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger = logging.getLogger("CUSTOMLOGGER")
logger.addHandler(file_handler)
