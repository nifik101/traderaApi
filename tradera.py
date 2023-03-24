import requests

app_id = '4926'
app_key = 'a6c8cced-d3b0-4b81-9fb2-f7652994bf33'

# url = 'https://api.tradera.com/v3/search?q=iphone%2012'
url = 'https://api.tradera.com/v3/searchservice.asmx/Search?query=iphone&categoryId=26&pageNumber=1&orderBy=Relevance'
params = {'appId': app_id, 'appKey': app_key}

response = requests.get(url, params=params)

if response.status_code == 200:
    # Process the response data
    data = response.json()
    print(data)
else:
    # Handle the error
    print('Error:', response.status_code)
