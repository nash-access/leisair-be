import time
import sys
import os
from dotenv import load_dotenv
from celery import Celery
from celery.utils.log import get_task_logger
import logging
from leisair_ml.utils.mongo_handler import MongoDBHandler
from leisair_ml.services.vessel_detection import run
from pathlib import Path
from leisair_ml.utils.logger import custom_logger

load_dotenv()

# initialize mongo_handler
mongo_handler = MongoDBHandler()

# Create a custom logger
logger = custom_logger("leisair")
current_dir = Path(__file__).resolve().parent
root_dir = Path(__file__).resolve().parent
sys.path.append(str(root_dir))

logging.basicConfig(level=logging.INFO)
logger = get_task_logger(__name__)

celery_app = Celery("nash_worker", broker=os.environ.get("RABBIT_URL"))


celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_expires=3600,
    worker_log_color=False,
    worker_hijack_root_logger=False,
    accept_content=["json"],
    broker_connection_retry_on_startup=True,
)


@celery_app.task(name="tasks.process_file", bind=True)
def process_file(self, file_path: str):
    model_path = Path(os.environ.get("MODEL_PATH",current_dir))
    logger.info("Starting to process file: %s", file_path)
    run(
        weights=Path(model_path / "best.pt"),
        source=Path(file_path),
        data=Path(model_path / "LEISair 03_11_23 all classes.yaml"),
    )
