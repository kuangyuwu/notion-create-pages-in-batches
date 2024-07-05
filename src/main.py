import asyncio
import datetime

from demo_config import create_routine_pages_demo
from routines import TimeFrame

async def main() -> None:
    await create_routine_pages_demo(
        TimeFrame(
            first_date=datetime.date(year=2024, month=7, day=8),
            duration=datetime.timedelta(weeks=1)
        )
    )
    return

if __name__ == "__main__":
    asyncio.run(main())