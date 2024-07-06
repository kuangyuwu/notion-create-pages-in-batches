import asyncio

from demo_config import create_routine_pages_demo

async def main() -> None:
    await create_routine_pages_demo()
    return

if __name__ == "__main__":
    asyncio.run(main())