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

async def create_routine_pages_demo() -> None:

    # Get the routines defined in the function get_routines()
    routines: list[Routine] = get_routines()

    # Define the time frame for creating routine pages
    # Starting from Monday, April 1, 2024, and spanning 2 weeks
    time_frame = TimeFrame(first_date=datetime.date(year=2024, month=4, day=1), length=datetime.timedelta(weeks=2))

    # Generate Notion pages based on the routines and the specified time frame
    pages: list[NotionPage] = routines_to_pages(routines, time_frame)

    # Import Notion integration key from .env file, create a NotionAPI object, and use it to create all the Notion pages
    dotenv.load_dotenv()
    notion_api = NotionAPI(os.getenv("NOTION_INTEGRATION_KEY"))
    await create_pages_batch(notion_api, pages)

    return


# Subclass of NotionIcon to define custom icons
class MyNotionIcon(NotionIcon):
    MEETING = "meeting_green"
    TEACHING = "gradebook_blue"
    GYM = "gym_yellow"


# Function to define and return a list of routine tasks
def get_routines() -> list[Routine]:

    # Load parent database ID from .env file
    dotenv.load_dotenv()
    PARENT_DB_ID: str = os.getenv("NOTION_DATABASE_ID")

    # Define names of the properties
    PROP_TITLE: str = "Name"
    PROP_TAGS: str = "Tags"
    PROP_DATE: str = "Date"

    # Define time zones
    TZ_CDT = datetime.timezone(offset=datetime.timedelta(hours= -5))
    TZ_CST = datetime.timezone(offset=datetime.timedelta(hours= -6))
    TZ = TZ_CDT

    # Create a prototype Notion page for meetings
    prototype_page_meeting = NotionPage(
        parent_db_id=PARENT_DB_ID,
        title=NotionPropPlainTitle(name=PROP_TITLE, title="Meeting"),
        props=[NotionPropMultiSelect(name=PROP_TAGS, options=["Research"])],
        icon=MyNotionIcon.MEETING
    )
    # Define a routine for the meeting
    routine_meeting = Routine(
        prototype_page=prototype_page_meeting,
        repeat=EVERY_THU,
        date_prop_name=PROP_DATE,
        start_time=datetime.time(hour=9, tzinfo=TZ),
        duration=datetime.timedelta(hours=1.5)
    )

    # Create a prototype Notion page for classes
    prototype_page_class = NotionPage(
        parent_db_id=PARENT_DB_ID,
        title=NotionPropPlainTitle(name=PROP_TITLE, title="Class"),
        props=[NotionPropMultiSelect(name=PROP_TAGS, options=["Teaching"])],
        icon=MyNotionIcon.TEACHING
    )
    # Define routines for the class
    routine_class_A = Routine(
        prototype_page=prototype_page_class,
        repeat=EVERY_MON | EVERY_WED,
        date_prop_name=PROP_DATE,
        start_time=datetime.time(hour=13, tzinfo=TZ),
        duration=datetime.timedelta(hours=1)
    )
    routine_class_B = Routine(
        prototype_page=prototype_page_class,
        repeat=EVERY_FRI,
        date_prop_name=PROP_DATE,
        start_time=datetime.time(hour=15, tzinfo=TZ),
        duration=datetime.timedelta(hours=1)
    )

    # Create a prototype Notion page for the gym
    prototype_page_gym = NotionPage(
        parent_db_id=PARENT_DB_ID,
        title=NotionPropPlainTitle(name=PROP_TITLE, title="Gym"),
        props=[NotionPropMultiSelect(name=PROP_TAGS, options=["Personal"])],
        icon=MyNotionIcon.GYM
    )
    # Define a routine for the gym
    routine_gym = Routine(
        prototype_page=prototype_page_gym,
        repeat=EVERY_SAT,
        date_prop_name=PROP_DATE,
        start_time=None,
        duration=None
    )

    # Return a list of all defined routines
    return [
        routine_meeting,
        routine_class_A,
        routine_class_B,
        routine_gym
    ]