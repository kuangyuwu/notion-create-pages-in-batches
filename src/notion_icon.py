from enum import Enum
from typing import Any


class NotionIcon(Enum):
    
    def json(self) -> dict[str, Any]:
        return {
            "type": "external",
            "external": {"url": f"https://www.notion.so/icons/{self.value}.svg"}
        }