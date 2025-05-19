import logging
from pathlib import Path


def setup_logging(log_file: str = "logs/scraper.log") -> None:
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)  # Ordner erstellen, falls nicht da

    logging.basicConfig(
        level=logging.INFO, # Niedrigstes Log-Level
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
