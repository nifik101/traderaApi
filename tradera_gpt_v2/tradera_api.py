import requests


def tradera_search(query, categoryId, pageNumber, orderBy):
    
    app_id = 4971
    app_key = "0d66bbf2-cdd2-4ad2-9b44-542f2ce0652c"
  
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

