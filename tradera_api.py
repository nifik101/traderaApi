import requests


def tradera_api_call(api_params) -> requests.models.Response:
    """tradera_api_call Skapa SOAP api call med 'requests' module.
    
    Har statisk 'url' och 'header'

    Args:
        api_params (ApiParameters): _description_

    Returns:
        requests.models.Response: _description_
    """

    url = "http://api.tradera.com/v3/searchservice.asmx"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
    }
    
    data = f'''<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
        <soap12:Header>
            <AuthenticationHeader xmlns="http://api.tradera.com">
                <AppId>{api_params.app_id}</AppId>
                <AppKey>{api_params.app_key}</AppKey>
            </AuthenticationHeader>
            <ConfigurationHeader xmlns="http://api.tradera.com">
                <Sandbox>{api_params.sandbox}</Sandbox>
                <MaxResultAge>{api_params.max_result_age}</MaxResultAge>
            </ConfigurationHeader>
        </soap12:Header>
        <soap12:Body>
            <SearchAdvanced xmlns="http://api.tradera.com">
                <request>
                    <SearchWords>{api_params.search_words}</SearchWords>
                    <CategoryId>{api_params.category_id}</CategoryId>
                    <SearchInDescription>{api_params.search_in_description}</SearchInDescription>
                    <PriceMinimum>{api_params.price_minimum}</PriceMinimum>
                    <PriceMaximum>{api_params.price_maximum}</PriceMaximum>
                    <OrderBy>{api_params.order_by}</OrderBy>
                    <ItemStatus>{api_params.item_status}</ItemStatus>
                    <ItemType>{api_params.item_type}</ItemType>
                    <OnlyAuctionsWithBuyNow>{api_params.only_auctions_with_buy_now}</OnlyAuctionsWithBuyNow>
                    <ItemsPerPage>{api_params.items_per_page}</ItemsPerPage>
                    <PageNumber>{api_params.page_number}</PageNumber>
                    <ItemCondition>{api_params.item_condition}</ItemCondition>
                    <SellerType>{api_params.seller_type}</SellerType>
                </request>
            </SearchAdvanced>
        </soap12:Body>
    </soap12:Envelope>'''

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as err:
        print("Request exception ERROR:", err.response)
