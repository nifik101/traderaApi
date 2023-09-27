import requests


def tradera_search(categoryId, pageNumber, orderBy, query):
    
    app_id = 5050
    app_key = "d5fbd47a-1508-4f9e-8fb0-0110cb924829"
  
    url = "http://api.tradera.com/v3/searchservice.asmx"
    
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "\"http://api.tradera.com/Search\""
    }
    
    data = f'''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Header>
        <AuthenticationHeader xmlns="http://api.tradera.com">
          <AppId>{app_id}</AppId>
          <AppKey>{app_key}</AppKey>
        </AuthenticationHeader>
        <ConfigurationHeader xmlns="http://api.tradera.com">
          <Sandbox>0</Sandbox>
          <MaxResultAge>0</MaxResultAge>
        </ConfigurationHeader>
      </soap:Header>
      <soap:Body>
        <Search xmlns="http://api.tradera.com">
          <query>{query}</query>
          <categoryId>{categoryId}</categoryId>
          <pageNumber>{pageNumber}</pageNumber>
          <orderBy>{orderBy}</orderBy>
        </Search>
      </soap:Body>
    </soap:Envelope>'''
    
    response = requests.post(url, headers=headers, data=data)
    
    # Nu har du svaret från Tradera API i response.text
    return response.text


def tradera_http_request():
  pass
