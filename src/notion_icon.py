from enum import Enum
from typing import Any

# Enum class representing different Notion icons
class NotionIcon(Enum):
    
    # Method to generate the JSON representation of the Notion icon
    def json(self) -> dict[str, Any]:
        return {
            "type": "external",
            "external": {"url": f"https://www.notion.so/icons/{self.value}.svg"}
        }