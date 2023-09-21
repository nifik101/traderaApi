from flask import Flask, request
import webbrowser
from typing import Dict, List
import json
from suds.client import Client
from suds.wsse import Security, UsernameToken
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element


class TraderaAPI:
    import logging

    def __init__(self, app_id: str, app_key: str):
        self.app_id = app_id
        self.app_key = app_key
        self.api_url = "https://api.tradera.com/v3/PublicService.asmx?WSDL"
        self.client = Client(self.api_url)
        self.set_client_auth(self.client)

    def set_client_auth(self, client: Client):
        security = Security()
        token = UsernameToken(self.app_id, self.app_key)
        security.tokens.append(token)
        client.set_options(wsse=security)

    def set_user_token(self, user_id: str, token: str):
        self.user_id = user_id
        self.token = token

        headers = {"X-Tradera-UserID": self.user_id, "X-Tradera-UserToken": self.token}
        search_params = {
            "Query": "",
            "Offset": 0,
            "ItemsPerPage": 10,
        }
        self.client.set_options(soapheaders=headers)

    @staticmethod
    def searchByQuery(appID, appKey, query):
        """Searches for items matching the given query using the Tradera API."""
        service_url = 'https://api.tradera.com/v3/PublicService.asmx?WSDL'
        client = Client(service_url)

        # Set up authentication headers
        auth_header = Element('AuthenticationHeader')
        app_id = Element('AppId')
        app_id.text = appID
        app_key = Element('AppKey')
        app_key.text = appKey
        auth_header.append(app_id)
        auth_header.append(app_key)
        client.set_options(soapheaders=auth_header)

        # Set up the search query
        search_query = Element('SearchQuery')
        query_elem = Element('Query')
        query_elem.text = query
        search_query.append(query_elem)

        # Call the searchByQuery method
        result = client.service.searchByQuery(search_query)

        try:
            # Call the searchByQuery method
            result = client.service.searchByQuery(search_query)
            return result
        except Exception as e:
            logging.error(f"Error occurred while searching for {query}: {e}")
            return None

        return result




app = Flask(__name__)

app_id = "4926"
app_key = "a6c8cced-d3b0-4b81-9fb2-f7652994bf33"
public_key = "fc436b34-4031-459f-9313-97741552099f"

tradera_api = TraderaAPI(app_id, app_key)


@app.route('/tradera_callback', methods=['GET'])
def tradera_callback():
    global tradera_api
    user_id = request.args.get('userId')
    token = request.args.get('token')

    if not user_id or not token:
        return "Error: User ID and Token not received."

    tradera_api.set_user_token(user_id, token)

    # Perform an example search
    try:
        search_results = TraderaAPI.searchByQuery(appID=app_id, appKey=app_key, query="laptop")
        # Process the search results
        # ...
        return "User ID and Token received. You can close this window."
    except Exception as e:
        return f"Error performing search: {e}"


def start_login_process():
    login_url = f"https://api.tradera.com/tokenlogin.aspx?appId={app_id}&pkey={public_key}&AcceptUrl=https://localhost:5000/tradera_callback"
    webbrowser.open(login_url)


if __name__ == "__main__":
    start_login_process()
    app.run(ssl_context='adhoc', debug=True)

