import asyncio
from pytgcalls import idle
from config import call_py, bot


async def main():
    print("STARTING RIOUBOT CLIENT")
    await bot.start()
    print("STARTING PYTGCALLS CLIENT")
    await call_py.start()
    print(
        """
    ------------------------
   | Rio Music Actived! |
    ------------------------
"""
    )
    await idle()
    await pidle()
    print("STOPPING USERBOT")
    await bot.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
