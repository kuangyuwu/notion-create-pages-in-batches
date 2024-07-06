import datetime
import dotenv
import os

from notion_api import NotionAPI
from notion_create_page import create_pages_batch
from notion_page import NotionPage
from notion_icon import NotionIcon
from notion_property import NotionPropMultiSelect, NotionPropPlainTitle
from routines import (
    EVERY_MON, EVERY_TUE, EVERY_WED, EVERY_THU, EVERY_FRI, EVERY_SAT, EVERY_SUN, EVERY_DAY,
    Routine, TimeFrame,
    routines_to_pages
)

async def create_routine_pages_demo(time_frame: TimeFrame) -> None:

    dotenv.load_dotenv()
    notion_api = NotionAPI(os.getenv("NOTION_INTEGRATION_KEY"))

    routines: list[Routine] = get_routines()
    pages: list[NotionPage] = routines_to_pages(routines, time_frame)

    await create_pages_batch(notion_api, pages)

    return

class MyNotionIcon(NotionIcon):
    MEETING = "meeting_green"
    TEACHING = "gradebook_blue"
    GYM = "gym_yellow"

def get_routines() -> list[Routine]:
    dotenv.load_dotenv()
    PARENT_DB_ID: str = os.getenv("NOTION_DATABASE_ID")
    PROP_TITLE: str = "Name"
    PROP_TAGS: str = "Tags"
    PROP_DATE: str = "Date"

    TZ_CDT = datetime.timezone(offset=datetime.timedelta(hours= -5))
    TZ_CST = datetime.timezone(offset=datetime.timedelta(hours= -6))
    TZ = TZ_CDT

    prototype_page_meeting = NotionPage(
        parent_db_id=PARENT_DB_ID,
        title=NotionPropPlainTitle(name=PROP_TITLE, title="Meeting"),
        props=[NotionPropMultiSelect(name=PROP_TAGS, options=["Research"])],
        icon=MyNotionIcon.MEETING
    )
    routine_meeting = Routine(
        prototype_page=prototype_page_meeting,
        repeat=EVERY_THU,
        date_prop_name=PROP_DATE,
        start_time=datetime.time(hour=13, tzinfo=TZ),
        duration=datetime.timedelta(hours=2)
    )

    prototype_page_class = NotionPage(
        parent_db_id=PARENT_DB_ID,
        title=NotionPropPlainTitle(name=PROP_TITLE, title="Class"),
        props=[NotionPropMultiSelect(name=PROP_TAGS, options=["Teaching"])],
        icon=MyNotionIcon.TEACHING
    )
    routine_class = Routine(
        prototype_page=prototype_page_class,
        repeat=EVERY_MON | EVERY_WED | EVERY_FRI,
        date_prop_name=PROP_DATE,
        start_time=datetime.time(hour=10, tzinfo=TZ),
        duration=datetime.timedelta(hours=1)
    )

    prototype_page_office_hours = NotionPage(
        parent_db_id=PARENT_DB_ID,
        title=NotionPropPlainTitle(name=PROP_TITLE, title="Office hours"),
        props=[NotionPropMultiSelect(name=PROP_TAGS, options=["Teaching"])],
        icon=MyNotionIcon.TEACHING
    )
    routine_office_hours_A = Routine(
        prototype_page=prototype_page_office_hours,
        repeat=EVERY_MON,
        date_prop_name=PROP_DATE,
        start_time=datetime.time(hour=11, tzinfo=TZ),
        duration=datetime.timedelta(hours=1)
    )
    routine_office_hours_B = Routine(
        prototype_page=prototype_page_office_hours,
        repeat=EVERY_WED,
        date_prop_name=PROP_DATE,
        start_time=datetime.time(hour=13, tzinfo=TZ),
        duration=datetime.timedelta(hours=1)
    )

    prototype_page_gym = NotionPage(
        parent_db_id=PARENT_DB_ID,
        title=NotionPropPlainTitle(name=PROP_TITLE, title="Gym"),
        props=[NotionPropMultiSelect(name=PROP_TAGS, options=["Personal"])],
        icon=MyNotionIcon.GYM
    )
    routine_gym = Routine(
        prototype_page=prototype_page_gym,
        repeat=EVERY_TUE | EVERY_FRI,
        date_prop_name=PROP_DATE,
        start_time=None,
        duration=None
    )

    return [
        routine_meeting,
        routine_class,
        routine_office_hours_A,
        routine_office_hours_B,
        routine_gym
    ]