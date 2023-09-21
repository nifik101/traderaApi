import streamlit as st
import xml.etree.ElementTree as ET
from tradera_api import tradera_search  # Importera tradera_search-funktionen från tradera_api.py
from datetime import datetime, time

# Skapa ett Streamlit-gränssnitt
st.title("Tradera.se Auktionsfiltrering")

# Lägg till Streamlit-komponenter för att ange sökkriterier
default_query = "macbook pro 2012 500 gb" # sätter default i Sökfras string 

user_query = st.text_input("Ange sökfras:", value=default_query)
user_categoryId = st.selectbox("Ange kategori ID:", [302393])
user_pageNumber = st.text_input("Ange sidnummer:", value=1)
user_orderBy = st.selectbox("Sortera efter:", ["Relevance", "Date"])

# Lägg till komponenter för att ange tidintervallet
start_time = st.time_input("Ange starttid (HH:MM):", time(2, 0))
end_time = st.time_input("Ange sluttid (HH:MM):", time(6, 0))

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
        end_date_str = item.find('ns:EndDate', namespaces=ns).text
        item_url = item.find('ns:ItemUrl', namespaces=ns).text
        
        # Konvertera EndDate till datetime-objekt
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        
        # Kontrollera om EndDate ligger inom det angivna tidsintervallet
        if start_time <= end_date.time() <= end_time:
            # Visa information om varje auktion som passerar filtret
            st.write(f"Auktions-ID: {item_id}")
            st.write(f"Kort beskrivning: {short_description}")
            st.write(f"Säljare: {seller_alias}")
            st.write(f"Max bud: {max_bid}")
            st.write(f"Slutdatum: {end_date.strftime('%Y-%m-%d %H:%M:%S %z')}")
            st.write(f"Länk till auktion: {item_url}")
            st.write("----")
