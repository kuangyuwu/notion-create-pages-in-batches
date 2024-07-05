import datetime

from notion_page import NotionPage
from notion_property import NotionPropDate

EVERY_MON = {0}
EVERY_TUE = {1}
EVERY_WED = {2}
EVERY_THU = {3}
EVERY_FRI = {4}
EVERY_SAT = {5}
EVERY_SUN = {6}
EVERY_DAY = {0,1,2,3,4,5,6}

class Routine:

    def __init__(
            self,
            page: NotionPage,
            repeat: set[int],
            date_prop_name: str,
            start_time: datetime.time | None = None,
            duration: datetime.timedelta | None = None,
    ) -> None:
        self.page = page
        self.repeat = repeat
        self.date_prop_name = date_prop_name
        self.start_time = start_time
        self.duration = duration
        return
    
    def is_valid(self, date: datetime.date) -> bool:
        return date.weekday() in self.repeat
    
    def make_page(self, date: datetime.date) -> NotionPage:
        start_datetime = date if self.start_time is None else datetime.datetime.combine(date, self.start_time)
        date_prop = NotionPropDate(
            name=self.date_prop_name,
            start_datetime=start_datetime,
            duration=self.duration
        )
        return NotionPage(
            parent_db_id=self.page.parent_db_id,
            title=self.page.title,
            props=self.page.props + [date_prop],
            icon=self.page.icon
        )

class TimeFrame:

    def __init__(self, first_date: datetime.date, duration: datetime.timedelta) -> None:
        self.first_date = first_date
        self.duration = duration
    
    def __iter__(self):
        DAY = datetime.timedelta(days=1)
        num_day = self.duration // DAY
        return iter([self.first_date + DAY * i for i in range(num_day)])


def routines_to_pages(routines: list[Routine], time_frame: TimeFrame) -> list[NotionPage]:
    pages = []
    for date in time_frame:
        for routine in routines:
            if routine.is_valid(date):
                pages.append(routine.make_page(date))
    return pages