import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

ROAD_SEGMENTS = [
    "A12-45", "A12-46",
    "A90-12", "A90-13",
    "GRA-07", "GRA-08", "GRA-09"
]

VEHICLES = [f"vehicle_{i:03d}" for i in range(1, 201)]

def _base_speed_for_hour(hour: int) -> float:
    """
    Returns a baseline speed depending on the hour of day.
    00:00-05:00: UNIFORM[60, 80]
    07:00-09:00: UNIFORM[10, 30]
    11:00-15:00: UNIFORM[35, 55]
    17:00-19:00: UNIFORM[10, 25]
    All other hours: UNIFORM[40, 70]
    """
    if 0 <= hour < 5:
        return random.uniform(60, 80)

    if 7 <= hour < 9:
        return random.uniform(10, 30)

    if 11 <= hour < 15:
        return random.uniform(35, 55)

    if 17 <= hour < 19:
        return random.uniform(10, 25)

    return random.uniform(40, 70)

def _event_type_from_speed(speed: float) -> str:
    """
    Classifies the event type based on speed.
    - "congestion" if speed < 15
    - "anomaly" if speed > 90
    - "speed_update" otherwise
    """
    if speed < 15:
        return "congestion"
    if speed > 90:
        return "anomaly"
    return "speed_update"

def generate_events_for_timestamp(ts: datetime, events_per_minute: int):
    """
    Generates a list of synthetic traffic events for a given timestamp.

    Parameters
    ----------
    ts : datetime
        Historical timestamp for the event.
    events_per_minute : int
        Number of events to generate for this timestamp.

    Returns
    -------
    List[dict]
        A list of synthetic traffic events.
    """
    events = []
    hour = ts.hour

    for _ in range(events_per_minute):
        vehicle = random.choice(VEHICLES)
        road = random.choice(ROAD_SEGMENTS)

        speed = _base_speed_for_hour(hour)
        speed += random.uniform(-5, 5)
        speed = max(speed, 0)

        event_type = _event_type_from_speed(speed)

        event = {
            "timestamp": ts.isoformat(),
            "vehicle_id": vehicle,
            "road_segment": road,
            "speed": round(speed, 2),
            "event_type": event_type
        }

        events.append(event)

    return events
