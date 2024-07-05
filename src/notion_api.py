from typing import Literal

class NotionAPI:
     
    def __init__(self, integration_key: str) -> None:
        self.__integration_key = integration_key

    def headers(self, method: Literal["DELETE", "GET", "PATCH", "POST"]) -> dict[str, str]:
        headers = {
            "Notion-Version": "2022-06-28",
            "Authorization": "Bearer " + self.__integration_key
        }
        if method == "PATCH" or method == "POST":
            headers["Content-Type"] = "application/json"
        return headers