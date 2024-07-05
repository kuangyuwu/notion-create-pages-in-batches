import datetime
from abc import ABC, abstractmethod
from typing import Any, Optional


class NotionProp(ABC):

    def __init__(self, name: str) -> None:
        self.name = name
    
    @abstractmethod
    def json(self) -> dict[str, Any]:
        raise NotImplementedError("this method should be overwritten")

    def __repr__(self) -> str:
        return repr(self.json())


class NotionPropDate(NotionProp):

    def __init__(
            self,
            name: str,
            start_datetime: datetime.date | datetime.datetime,
            duration: Optional[datetime.timedelta] = None
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


class NotionPropMultiSelect(NotionProp):

    def __init__(self, name: str, options: list[str]) -> None:
        super().__init__(name)
        self.options = options
    
    def json(self) -> dict[str, Any]:
        return {"multi_select": [{"name": option} for option in self.options]}


class NotionPropPlainTitle(NotionProp):

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
