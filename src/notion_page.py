from typing import Any

from notion_icon import NotionIcon
from notion_property import NotionProp, NotionPropPlainTitle

class NotionPage:

    # Initialize the NotionPage class with parent database ID, title, properties, and icon (optional)
    def __init__(
            self,
            database_id: str,
            title: NotionPropPlainTitle,
            props: list[NotionProp],
            icon: NotionIcon | None = None
    ) -> None:
        self.database_id = database_id
        self.title = title
        self.props = props
        self.icon = icon

    # Generate a JSON representation of the Notion page
    def json(self) -> dict[str, Any]:
        json = {
            # Include the parent database ID
            "parent": {
                "type": "database_id",
                "database_id": self.database_id,
            },
            # Generate JSON for each property and include it in the properties dictionary
            "properties": {
                prop.name: prop.json()
                for prop in self.props
            }
        }
        # Add the title property to the properties dictionary
        json["properties"][self.title.name] = self.title.json()
        # Add the icon to the JSON if it is not None
        if self.icon is not None:
            json["icon"] = self.icon.json()
        return json
    
    # Provide a string representation of the NotionPage object
    def __repr__(self) -> str:
        return f"NotionPage({self.title.title})"