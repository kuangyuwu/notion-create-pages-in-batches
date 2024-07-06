import asyncio
import datetime

from demo_config import create_routine_pages_demo
from routines import TimeFrame

async def main() -> None:
    time_frame = TimeFrame(first_date=datetime.date(year=2024, month=7, day=8), length=datetime.timedelta(weeks=1))
    await create_routine_pages_demo(time_frame)
    return

if __name__ == "__main__":
    asyncio.run(main())