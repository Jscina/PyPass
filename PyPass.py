import async_eel, asyncio
from Database import Database
from Accounts import Account

active_user: str | None = None

db = Database()

loop = asyncio.get_event_loop()

@async_eel.expose
async def test():
    return await db.get_accounts()
        
async def main():
    async_eel.init("www")
    # Start on the login screen
    await async_eel.start("login.html", blocking=False)


if __name__ == "__main__":
    asyncio.run_coroutine_threadsafe(main(), loop)
    loop.run_forever()