from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PricePoint:
    zone: str
    period_start_utc: datetime
    kind: str            # day_ahead_price_eur_per_mwh | imbalance_price_eur_per_mwh
    value: float | None
