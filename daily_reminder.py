import asyncio

class DailyReminder:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.cd = 0
        self.prev = None