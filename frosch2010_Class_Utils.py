import asyncio

class Timer:

    def __init__(self, timeout, callback, parms):
        self._timeout = timeout
        self._callback = callback
        self._parms = parms
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback(self._parms[0], self._parms[1], self._parms[2])

    def cancel(self):
        self._task.cancel()