import requests

CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
ACCEPT_URL = 'http://localhost:8000/accept'
SCOPE = 'YOUR_DESIRED_SCOPE'

# Step 1: Redirect user to Tradera.se login page for authentication
def get_authorization_url():
    url = 'https://api.tradera.com/tokenlogin.aspx'
    params = {
    'consumerKey': CONSUMER_KEY,
    'acceptUrl': ACCEPT_URL,
    'scope': SCOPE,
    }
    response = requests.get(url, params=params)
    return response.url

# Step 3: Get token from cookie when user returns to the Accept URL
def get_token_from_cookie(cookie):
    token = None
    for item in cookie:
        if item.name == 'TRADERA_TAUTH':
            token = item.value
        break
    return token

# Example usage
auth_url = get_authorization_url()
print(f'Redirect user to: {auth_url}')

# User logs in and is redirected back to the Accept URL with cookie set
cookie = requests.cookies.RequestsCookieJar() 
cookie.set('TRADERA_TAUTH', 'TOKEN_VALUE')
r = requests.get(ACCEPT_URL, cookies=cookie)

# Get token from cookie
access_token = get_token_from_cookie(r.cookies)

print(f'Access token: {access_token}')


