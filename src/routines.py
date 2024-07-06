import datetime

from notion_page import NotionPage
from notion_property import NotionPropDate

# Constants representing days of the week
EVERY_MON = {0}
EVERY_TUE = {1}
EVERY_WED = {2}
EVERY_THU = {3}
EVERY_FRI = {4}
EVERY_SAT = {5}
EVERY_SUN = {6}
EVERY_DAY = {0,1,2,3,4,5,6}

# Class representing a routine task
class Routine:

    # Initialize the Routine class with a prototype page, repeat days, date property name, start time, and duration
    def __init__(
            self,
            prototype_page: NotionPage,
            repeat: set[int],
            date_prop_name: str,
            start_time: datetime.time | None = None,
            duration: datetime.timedelta | None = None,
    ) -> None:
        self.prototype_page = prototype_page
        self.repeat = repeat
        self.date_prop_name = date_prop_name
        self.start_time = start_time
        self.duration = duration
        return
    
    # Check if the routine is valid on a given date
    def is_valid(self, date: datetime.date) -> bool:
        return date.weekday() in self.repeat
    
    # Create a Notion page for the routine on a given date
    def make_page(self, date: datetime.date) -> NotionPage:
        # Create a date property for the Notion page
        start_datetime = date if self.start_time is None else datetime.datetime.combine(date, self.start_time)
        date_prop = NotionPropDate(
            name=self.date_prop_name,
            start_datetime=start_datetime,
            duration=self.duration
        )
        # Return a new Notion page with the date property added to the prototype page properties
        return NotionPage(
            parent_db_id=self.prototype_page.parent_db_id,
            title=self.prototype_page.title,
            props=self.prototype_page.props + [date_prop],
            icon=self.prototype_page.icon
        )

# Class representing a time frame for creating routine pages
class TimeFrame:

    # Initialize the TimeFrame class with a start date and a duration
    def __init__(self, first_date: datetime.date, length: datetime.timedelta) -> None:
        self.first_date = first_date
        self.length = length
    
    # Iterator method to generate dates within the time frame
    def __iter__(self):
        DAY = datetime.timedelta(days=1)
        num_day = self.length // DAY  # Calculate the number of days in the time frame
        return iter([self.first_date + DAY * i for i in range(num_day)])

# Function to convert a list of routines and a time frame into a list of Notion pages
def routines_to_pages(routines: list[Routine], time_frame: TimeFrame) -> list[NotionPage]:
    pages = []
    for date in time_frame:  # Iterate over each date in the time frame
        for routine in routines:  # Iterate over each routine
            # If the routine is valid on the date, create a Notion page and add it to the list
            if routine.is_valid(date):
                pages.append(routine.make_page(date))
    return pages