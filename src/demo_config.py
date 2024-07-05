import datetime
import dotenv
import os

from notion_api import NotionAPI
from notion_create_page import create_pages_batch
from notion_page import NotionPage
from notion_icon import NotionIcon
from notion_property import (
    NotionPropMultiSelect, NotionPropPlainTitle
)
from routines import (
    EVERY_MON, EVERY_TUE, EVERY_WED, EVERY_THU, EVERY_FRI, EVERY_SAT, EVERY_SUN, EVERY_DAY,
    Routine, TimeFrame,
    routines_to_pages
)

async def create_routine_pages_demo(time_frame: TimeFrame) -> None:
    notion_api = get_demo_notion_api()
    routines = get_demo_routines()
    pages = routines_to_pages(routines, time_frame)
    await create_pages_batch(notion_api, pages)
    return

def get_demo_notion_api() -> NotionAPI:
    dotenv.load_dotenv()
    NOTION_INTEGRATION_KEY: str = os.getenv("DEMO_NOTION_INTEGRATION_KEY")
    return NotionAPI(NOTION_INTEGRATION_KEY)

class DemoNotionIcon(NotionIcon):
    MEETING = "meeting_green"
    TEACHING = "gradebook_blue"
    GYM = "gym_yellow"

def get_demo_routines() -> list[Routine]:
    dotenv.load_dotenv()
    PARENT_DB_ID: str = os.getenv("DEMO_NOTION_DATABASE_ID")
    DEMO_PROP_TITLE: str = "Name"
    DEMO_PROP_TAGS: str = "Tags"
    DEMO_PROP_DATE: str = "Date"

    TZ_CDT = datetime.timezone(offset=datetime.timedelta(hours= -5))
    TZ_CST = datetime.timezone(offset=datetime.timedelta(hours= -6))
    TZ = TZ_CDT

    demo_routine_meeting = Routine(
        page=NotionPage(
            parent_db_id=PARENT_DB_ID,
            title=NotionPropPlainTitle(name=DEMO_PROP_TITLE, title="Meeting"),
            props=[
                NotionPropMultiSelect(name=DEMO_PROP_TAGS, options=["Research"]),
            ],
            icon=DemoNotionIcon.MEETING
        ),
        repeat=EVERY_THU,
        date_prop_name=DEMO_PROP_DATE,
        start_time=datetime.time(hour=13, tzinfo=TZ),
        duration=datetime.timedelta(hours=2)
    )

    demo_routine_class = Routine(
        page=NotionPage(
            parent_db_id=PARENT_DB_ID,
            title=NotionPropPlainTitle(name=DEMO_PROP_TITLE, title="Class"),
            props=[
                NotionPropMultiSelect(name=DEMO_PROP_TAGS, options=["Teaching"]),
            ],
            icon=DemoNotionIcon.TEACHING
        ),
        repeat=EVERY_MON | EVERY_WED | EVERY_FRI,
        date_prop_name=DEMO_PROP_DATE,
        start_time=datetime.time(hour=10, tzinfo=TZ),
        duration=datetime.timedelta(hours=1)
    )

    demo_routine_office_hours_A = Routine(
        page=NotionPage(
            parent_db_id=PARENT_DB_ID,
            title=NotionPropPlainTitle(name=DEMO_PROP_TITLE, title="Office hours"),
            props=[
                NotionPropMultiSelect(name=DEMO_PROP_TAGS, options=["Teaching"]),
            ],
            icon=DemoNotionIcon.TEACHING
        ),
        repeat=EVERY_MON,
        date_prop_name=DEMO_PROP_DATE,
        start_time=datetime.time(hour=11, tzinfo=TZ),
        duration=datetime.timedelta(hours=1)
    )

    demo_routine_office_hours_B = Routine(
        page=NotionPage(
            parent_db_id=PARENT_DB_ID,
            title=NotionPropPlainTitle(name=DEMO_PROP_TITLE, title="Office hours"),
            props=[
                NotionPropMultiSelect(name=DEMO_PROP_TAGS, options=["Teaching"]),
            ],
            icon=DemoNotionIcon.TEACHING
        ),
        repeat=EVERY_WED,
        date_prop_name=DEMO_PROP_DATE,
        start_time=datetime.time(hour=13, tzinfo=TZ),
        duration=datetime.timedelta(hours=1)
    )

    demo_routine_gym = Routine(
        page=NotionPage(
            parent_db_id=PARENT_DB_ID,
            title=NotionPropPlainTitle(name=DEMO_PROP_TITLE, title="Gym"),
            props=[
                NotionPropMultiSelect(name=DEMO_PROP_TAGS, options=["Personal"]),
            ],
            icon=DemoNotionIcon.GYM
        ),
        repeat=EVERY_THU,
        date_prop_name=DEMO_PROP_DATE,
        start_time=None,
        duration=None
    )

    return [
        demo_routine_meeting,
        demo_routine_class,
        demo_routine_office_hours_A,
        demo_routine_office_hours_B,
        demo_routine_gym
    ]