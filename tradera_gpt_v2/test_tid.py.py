import xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st


def find_element(root):
    items = root.findall(".//tradera:EndDate", namespaces=namespaces)
    value = []
    
    for i in items:
        time = i.text
        # value.append(time)
    return time

st.title("Tidsintervallväljare i Streamlit")

start_time = st.time_input("Ange starttid (HH:MM):") # st.session_state.start_time
end_time = st.time_input("Ange sluttid (HH:MM):") # st.session_state.end_time

st.write("Vald starttid:", start_time.strftime("%H:%M"))
st.write("Vald sluttid:", end_time.strftime("%H:%M"))


tree = ET.parse("sample.xml")
root = tree.getroot()

namespaces = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'tradera': 'http://api.tradera.com', # ns att använda i XPath, .//tradera:XPath
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}

if st.button("Kolla tid"):
    tiden = find_element(root)
    tid = datetime.fromisoformat(tiden).replace(tzinfo=None).time()
    
    if start_time <= tid <= end_time:
        st.write("Tiden är mellan start_time och end_time.")
    else:
        st.write("Tiden är inte mellan start_time och end_time.")

if st.button("Hämta EndDate"):
    data = find_element(root)
    st.write(data)

if st.button("vissa tid och typ"):
    st.write(f'{start_time} ät typ: {type(start_time)}')