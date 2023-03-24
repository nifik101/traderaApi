import requests

url = 'https://api.tradera.com/v3/searchservice.asmx/Search'
params = {
    'query': 'iphone',
    'categoryId': '26',
    'pageNumber': '1',
    'orderBy': 'Relevance'
}
headers = {
    # 'Content-Type': 'application/json',
    'AppId': '4926',
    'AppKey': 'a6c8cced-d3b0-4b81-9fb2-f7652994bf33'
}
response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
    except ValueError:
        print('Error: Response is empty')
        data = None

    if data:
        # Process the response data
        print(data)
else:
    # Handle the error
    print('Error:', response.status_code)
