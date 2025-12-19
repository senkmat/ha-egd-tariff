from datetime import time

# EG.D – A1B6DP5 – Brno
# ZATÍM zjednodušený model:
# NT: 22:00–06:00 + 2h přes den (např. 12–14)

TARIFFS = {
    "A1B6DP5": {
        "Brno": [
            (time(22, 0), time(23, 59)),
            (time(0, 0), time(6, 0)),
            (time(12, 0), time(14, 0)),
        ]
    }
}
