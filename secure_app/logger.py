import logging

logging.basicConfig(
    filename="access.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_access(identifier: str, outcome: str, app: str):
    logging.info(f"[{app}] Access to {identifier} | Result: {outcome}")
