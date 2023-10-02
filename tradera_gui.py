import xml.etree.ElementTree as ET
from collections import namedtuple

import json
import streamlit as st
from tradera_api import tradera_api_call

# Importera API variabler 
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

ApiParameters = namedtuple("ApiParameters", [
    "app_id",
    "app_key",
    "sandbox",
    "max_result_age",
    "search_words",
    "category_id",
    "search_in_description",
    "price_minimum",
    "price_maximum",
    "order_by",
    "item_status",
    "item_type",
    "only_auctions_with_buy_now",
    "items_per_page",
    "page_number",
    "item_condition",
    "seller_type"
])

# Default settings, ändras inte i GUI
app_id = config['app_id']
app_key = config['app_key']
sandbox = 0
max_result_age = 24

## GUI
# Fält för input, i ordningen de syns i GUI
search_words = st.text_input("Search Words:")

# Skapa 2 kolumner för category setting
cat_input, cat_json_col = st.columns(2)

with cat_input:
    category_id = st.number_input("Category ID:", value=302393)

# Drop down, meny med "advanced settings" som en drop down.  
with st.expander("Advanced settings"):
    search_in_description = st.radio("Search In Description", ["false", "true"], index=0, horizontal=True)
    price_minimum = st.slider("Price Minimum", 0, 1000, 0, 1)
    price_maximum = st.slider("Price Maximum", 0, 100000, 100000, 1000)
    order_by = st.selectbox("Sortera efter:", ["Relevance", "BidsAscending", "BidsDescending", "PriceAscending", "PriceDescending", "EndDateAscending", "EndDateDescending"])
    item_status = st.selectbox("Item Status", ["Active", "Ended"], index=0)
    item_type = st.selectbox("Item Type", ["All", "Auction", "BuyItNow"])
    only_auctions_with_buy_now = st.radio("Only Auctions With Buy Now", ["false", "true"], index=0, horizontal=True)
    items_per_page = st.slider("Items Per Page", 1, 500, 500)
    page_number = st.number_input("Page Number", 1)
    item_condition = st.selectbox("Item Condition", ["All", "OnlySecondHand", "OnlyNew"], index=0)
    seller_type = st.selectbox("Seller Type", ["All", "Private", "Company"], index=0)

if st.button("Search Auctions"):

    api_params = ApiParameters(
        app_id=app_id,
        app_key=app_key,
        sandbox=sandbox,
        max_result_age=max_result_age,
        search_words=search_words,
        category_id=category_id,
        search_in_description=search_in_description,
        price_minimum=price_minimum,
        price_maximum=price_maximum,
        order_by=order_by,
        item_status=item_status,
        item_type=item_type,
        only_auctions_with_buy_now=only_auctions_with_buy_now,
        items_per_page=items_per_page,
        page_number=page_number,
        item_condition=item_condition,
        seller_type=seller_type
    )

    response = tradera_api_call(api_params)
    st.write(response.status_code)

    # Bearbeta XML-responsen med korrekt namespace
    root = ET.fromstring(response.text)
    ns: dict = {'ns': 'http://api.tradera.com'}  # Använd namespace-prefixet för Tradera
    items = root.findall('.//ns:Items', namespaces=ns)

    # Visa auktionsinformation i Streamlit
    st.write("Resultat från Tradera.se API:")
    st.write(f"No Items: {root.find('.//ns:TotalNumberOfItems', namespaces=ns).text}")
    st.write(f"No sidor: {root.find('.//ns:TotalNumberOfPages', namespaces=ns).text}")
    st.write(len(items))
    for item in items:
        # Extrahera attribut med korrekt namespace
        item_id = item.find('ns:Id', namespaces=ns).text
        short_description = item.find('ns:ShortDescription', namespaces=ns).text
        seller_alias = item.find('ns:SellerAlias', namespaces=ns).text
        max_bid = item.find('ns:MaxBid', namespaces=ns).text
        end_date = item.find('ns:EndDate', namespaces=ns).text
        item_url = item.find('ns:ItemUrl', namespaces=ns).text

        # Visa information om varje auktion
        st.write(f"Auktions-ID: {item_id}")
        st.write(f"Kort beskrivning: {short_description}")
        st.write(f"Säljare: {seller_alias}")
        st.write(f"Max bud: {max_bid}")
        st.write(f"Slutdatum: {end_date}")
        st.write(f"Länk till auktion: {item_url}")
        st.link_button(":joy:", item_url)
        st.write("----")

print(f'{app_id}, {app_key}')