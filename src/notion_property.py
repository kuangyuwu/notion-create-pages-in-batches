import datetime
from abc import ABC, abstractmethod
from typing import Any


# Abstract base class representing a property of a Notion page
class NotionProp(ABC):

    # Every child class has to be initialized with the name of the property
    def __init__(self, name: str) -> None:
        self.name = name
    
    # Abstract method to generate a JSON representation of the property
    @abstractmethod
    def json(self) -> dict[str, Any]:
        raise NotImplementedError("this method should be overwritten")

    def __repr__(self) -> str:
        return repr(self.json())


# Class representing a date property in Notion
class NotionPropDate(NotionProp):

    # Initialize the NotionPropDate class with the name of the date property, start datetime, and optional duration
    def __init__(
            self,
            name: str,
            start_datetime: datetime.date | datetime.datetime,
            duration: datetime.timedelta | None = None
    ) -> None:
        super().__init__(name)
        self.start_datetime = start_datetime
        self.duration = duration

    def json(self) -> dict[str, Any]:
        result = {
            "date": {
                "start": self.start_datetime.isoformat(),
            }
        }
        if self.duration is not None:
            end_datetime = self.start_datetime + self.duration
            result["date"]["end"] = end_datetime.isoformat()
        return result


# Class representing a multi-select property in Notion
class NotionPropMultiSelect(NotionProp):

    # Initialize the NotionPropMultiSelect class with the name of the multi-select property and a list of options
    def __init__(self, name: str, options: list[str]) -> None:
        super().__init__(name)
        self.options = options
    
    def json(self) -> dict[str, Any]:
        return {"multi_select": [{"name": option} for option in self.options]}


# Class representing a title property in Notion
class NotionPropPlainTitle(NotionProp):

    # Initialize the NotionPropPlainTitle class with the name of the title property and title
    def __init__(self, name: str, title: str) -> None:
        super().__init__(name)
        self.title = title

    def json(self) -> dict[str, Any]:
        return {
            "id": "title",
            "type": "title",
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": self.title,
                        "link": None
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": self.title,
                    "href": None
                }
            ]
        }
