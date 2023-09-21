from flask import Flask, request
import webbrowser
from suds.client import Client
from suds.wsse import Security, UsernameToken

app = Flask(__name__)

app_id = "4926"
app_key = "a6c8cced-d3b0-4b81-9fb2-f7652994bf33"
public_key = "fc436b34-4031-459f-9313-97741552099f"

tradera_api_url = "https://api.tradera.com/restrictedservice.asmx?wsdl"
tradera_api = None

@app.route('/tradera_callback', methods=['GET'])
def tradera_callback():
    global tradera_api

    user_id = request.args.get('userId')
    token = request.args.get('token')

    if not user_id or not token:
        return "Error: User ID and Token not received."

    if tradera_api is None:
        tradera_api = Client(tradera_api_url, username=app_id, password=app_key)

    security = Security()
    token = UsernameToken(user_id, token)
    security.tokens.append(token)

    tradera_api.set_options(wsse=security)

    # Perform an example search
    try:
        search_params = tradera_api.factory.create('ns0:SearchItemsRequest')
        search_params.Query = 'laptop'
        search_params.Offset = 0
        search_params.ItemsPerPage = 10

        headers = {
            'X-Tradera-UserID': user_id,
            'X-Tradera-UserToken': token.plain(),
        }

        response = tradera_api.service.SearchItems(
            search_params,
            AppId=app_id,
            AppKey=app_key,
            UserId=user_id,
            Token=token.plain(),
            _soapheaders=headers,
        )

        print(response)
        return "User ID and Token received. You can close this window."
    except Exception as e:
        return f"Error performing search: {e}"

def start_login_process():
    login_url = f"https://api.tradera.com/tokenlogin.aspx?appId={app_id}&pkey={public_key}&AcceptUrl=https://localhost:5000/tradera_callback"
    webbrowser.open(login_url)

if __name__ == "__main__":
    start_login_process()
    app.run(ssl_context='adhoc', debug=True)
