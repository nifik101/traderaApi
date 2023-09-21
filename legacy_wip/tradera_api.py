from typing import Dict
import json
from suds.client import Client
from suds.wsse import Security, UsernameToken


class TraderaAPI:
    def __init__(self, app_id: str, app_key: str, user_id: str, token: str):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('suds.client').setLevel(logging.DEBUG)

        self.app_id = app_id
        self.app_key = app_key
        self.public_api_url = "https://api.tradera.com/publicservice.asmx?WSDL"
        self.restricted_api_url = "https://api.tradera.com/restrictedservice.asmx?WSDL"

        self.user_id = user_id
        self.token = token

        self.public_client = Client(self.public_api_url)
        self.restricted_client = Client(self.restricted_api_url)

    def set_user_token(self, user_id: str, token: str, app_id: str, app_key: str):
        self.user_id = user_id
        self.token = token
        self.app_id = app_id
        self.app_key = app_key

        security = Security()
        token = UsernameToken(self.app_id, self.app_key, self.user_id, self.token)
        security.tokens.append(token)
        self.restricted_client.set_options(wsse=security)

    def search_items(self, query: str, page: int = 1, items_per_page: int = 10) -> Dict:
        if not self.user_id or not self.token:
            raise Exception("User ID and Token must be set before calling search_items")

        search_params = {
            "Query": query,
            "Offset": (page - 1) * items_per_page,
            "ItemsPerPage": items_per_page,
        }

        response = self.restricted_client.service.SearchItems(
            search_params, AppId=self.app_id, AppKey=self.app_key, UserId=self.user_id, Token=self.token
        )

        return json.loads(response)

if __name__ == "__main__":
    app_id = "4926"
    app_key = "a6c8cced-d3b0-4b81-9fb2-f7652994bf33"

    tradera_api = TraderaAPI(app_id, app_key)

    # After obtaining the user_id and token from the tokenlogin.aspx page
    user_id = "YOUR_USER_ID"
    token = "YOUR_TOKEN"
    tradera_api.set_user_token(user_id, token, app_id, app_key)

    # Example usage: searching for items with specific query, category, and time range
    search_results = tradera_api.search_items(
        query="laptop",
        category_id=123,  # Replace with a valid category ID
        min_end_time="2023-04-01T00:00:00",
        max_end_time="2023-04-01T05:00:00"
    )

    print(search_results)
