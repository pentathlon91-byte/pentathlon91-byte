import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ReplayController:
    """
    Controls the historical replay timeline for the Kafka producer.

    It iterates through timestamps between a start and end datetime,
    advancing by a fixed interval (e.g., 1 minute), and computes the
    real-time sleep duration based on a speed multiplier.
    """

    def __init__(self, start: str, end: str, speed_multiplier: int, interval_minutes: int):
        self.start = datetime.fromisoformat(start)
        self.end = datetime.fromisoformat(end)
        self.speed_multiplier = speed_multiplier
        self.interval = timedelta(minutes=interval_minutes)

        self.simulated_interval_seconds = self.interval.total_seconds()

    def iter_timestamps(self):
        """
        Generator that yields timestamps from start to end,
        advancing by the configured interval.
        """
        current = self.start
        while current < self.end:
            yield current
            current += self.interval

    def real_sleep_seconds(self) -> float:
        """
        Computes how long the producer should sleep in real time
        to simulate the historical interval at the chosen speed.
        """
        return self.simulated_interval_seconds / self.speed_multiplier
