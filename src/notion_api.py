from typing import Literal

class NotionAPI:
    
    # Initialize the NotionAPI class with the integration key
    def __init__(self, integration_key: str) -> None:
        self.__integration_key = integration_key

    # Generate headers for the API request based on the HTTP method
    def _headers(self, method: Literal["DELETE", "GET", "PATCH", "POST"]) -> dict[str, str]:
        headers = {
            "Notion-Version": "2022-06-28",
            "Authorization": "Bearer " + self.__integration_key
        }
        # Add Content-Type header for PATCH and POST methods
        if method == "PATCH" or method == "POST":
            headers["Content-Type"] = "application/json"
        return headers