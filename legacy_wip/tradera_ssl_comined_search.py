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


class TraderaAPI:
    import logging
    def __init__(self, app_id: str, app_key: str):
        self.app_id = app_id
        self.app_key = app_key
        self.public_api_url = "https://api.tradera.com/publicservice.asmx?wsdl"
        self.restricted_api_url = "https://api.tradera.com/restrictedservice.asmx?wsdl"

        self.public_client = Client(self.public_api_url)
        self.restricted_client = Client(self.restricted_api_url)

        self.set_client_auth(self.restricted_client)

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
        response = self.restricted_client.service.SearchItems(
            **search_params,
            AppId=self.app_id,
            AppKey=self.app_key,
            UserId=self.user_id,
            Token=self.token,
            _soapheaders=headers
        )
        self.set_client_auth(self.public_client)

    @staticmethod
    def searchByQuery(appID, appKey, query):
        """Searches for items matching the given query using the Tradera API."""
        service_url = 'https://api.tradera.com/v3/PublicService.asmx?WSDL'
        client = Client(service_url)

        # Set up authentication headers
        auth_header = Element('AuthenticationHeader')
        app_id = Element('AppId').setText(appID)
        app_key = Element('AppKey').setText(appKey)
        auth_header.append(app_id)
        auth_header.append(app_key)
        client.set_options(soapheaders=auth_header)

        # Set up the search query
        search_query = Element('SearchQuery')
        search_query.append(Element('Query').setText(query))

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



    def search_items(self, query: str, page: int = 1, items_per_page: int = 10) -> Dict:
        if not self.user_id or not self.token:
            raise Exception("User ID and Token must be set before calling search_items")

        search_params = {
            "Query": query,
            "Offset": (page - 1) * items_per_page,
            "ItemsPerPage": items_per_page,
        }

        search_query = Element('SearchQuery')
        for key, value in search_params.items():
            search_query.append(Element(key).setText(str(value)))

        headers = {"X-Tradera-UserID": self.user_id, "X-Tradera-UserToken": self.token}
        response = self.restricted_client.service.SearchItems(
            search_query, AppId=self.app_id, AppKey=self.app_key, UserId=self.user_id, Token=self.token, _soapheaders=headers
        )

        return response


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
        search_results = tradera_api.search_items(
            query="laptop",
            page=1,
            items_per_page=10
        )

        # print(search_results)
        return "User ID and Token received. You can close this window."
    except Exception as e:
        return f"Error performing search: {e}"


def start_login_process():
    login_url = f"https://api.tradera.com/tokenlogin.aspx?appId={app_id}&pkey={public_key}&AcceptUrl=https://localhost:5000/tradera_callback"
    webbrowser.open(login_url)

if __name__ == "__main__":
    # Generate a self-signed certificate for the local server
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'localhost'),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    ).sign(private_key, hashes.SHA256())
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Save SSL certificate and private key to disk
    with open('cert.pem', 'wb') as f:
        f.write(cert_pem)

    with open('key.pem', 'wb') as f:
        f.write(key_pem)

    # Use the SSL certificate and private key to start the Flask app with an ad-hoc SSL context
    ssl_context = ('cert.pem', 'key.pem')
    start_login_process()
    app.run(ssl_context=ssl_context, debug=True)




