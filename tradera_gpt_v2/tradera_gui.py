import streamlit as st
import xml.etree.ElementTree as ET
from tradera_api import tradera_search  # Importera tradera_search-funktionen från tradera_api.py

# Skapa ett Streamlit-gränssnitt
st.title("Tradera.se Auktionsfiltrering")

# Lägg till Streamlit-komponenter för att ange sökkriterier
default_query = "macbook pro 2012 500 gb" # sätter default i Sökfras string 

user_query = st.text_input("Ange sökfras:", value=default_query)
# user_categoryId = st.text_input("Ange kategori ID:")
user_categoryId = st.selectbox("Ange kategori ID:", [302393])
user_pageNumber = st.text_input("Ange sidnummer:", value=1)
user_orderBy = st.selectbox("Sortera efter:", ["Relevance", "Date"])

# Anropa tradera_search-funktionen med användarens sökkriterier
if st.button("Sök på Tradera"):
    result = tradera_search(query=user_query, categoryId=user_categoryId, pageNumber=user_pageNumber, orderBy=user_orderBy)
    
    # Bearbeta XML-responsen med korrekt namespace
    root = ET.fromstring(result)
    ns = {'ns': 'http://api.tradera.com'}  # Använd namespace-prefixet för Tradera
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
        st.write("----")


# Debug sektion, för att göra tester
if st.button("Debug test"):
    result = tradera_search(query=user_query, categoryId=user_categoryId, pageNumber=user_pageNumber, orderBy=user_orderBy)
    # Bearbeta XML-responsen
    root = ET.fromstring(result)
    ns = {'ns': 'http://api.tradera.com'}

    st.write("Tradera API-svar:")  # Skriv ut Tradera API-svar för felsökning

    # Exempel: Hämta och skriv ut antalet resultat från responsen
    items = root.findall('.//ns:Items', namespaces=ns)
    for item in items:

        st.write(item.find('.//ns:SellerAlias', namespaces=ns).text)


# Vissar rå-datan typ ofiltrerad
if st.button("Visa rådata"):
    result = tradera_search(query=user_query, categoryId=user_categoryId, pageNumber=user_pageNumber, orderBy=user_orderBy)
    st.write(result)
