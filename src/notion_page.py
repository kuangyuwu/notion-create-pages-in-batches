from typing import Any

from notion_icon import NotionIcon
from notion_property import NotionProp, NotionPropPlainTitle

class NotionPage:

    def __init__(
            self,
            parent_db_id: str,
            title: NotionPropPlainTitle,
            props: list[NotionProp],
            icon: NotionIcon | None = None
    ) -> None:
        self.parent_db_id = parent_db_id
        self.title = title
        self.props = props
        self.icon = icon

    def json(self) -> dict[str, Any]:
        json = {
            "parent": {
                "type": "database_id",
                "database_id": self.parent_db_id,
            },
            "properties": {
                prop.name: prop.json()
                for prop in self.props
            }
        }
        json["properties"][self.title.name] = self.title.json()
        if self.icon is not None:
            json["icon"] = self.icon.json()
        return json
    
    def __repr__(self) -> str:
        return f"NotionPage({self.title.title})"