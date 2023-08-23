import pandas as pd
import streamlit as st
from db import DB
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

db = DB()
st.sidebar.title("Flights Analysis :small_airplane:")
st.sidebar.title(":blue[What you want to do..?]")

option = st.sidebar.selectbox("Menu",["Select One","Check flights","Flight's Analytics"])

if option == "Check flights":
    st.title("Check Flights")

    col1,col2 = st.columns(2)
    city = db.fetch_all_city()
    with col1:
        source = st.selectbox('Source',['BOM'])
    with col2:
        destination = st.selectbox('Destination',sorted(city))

    if st.button("Search"):
        result = db.fetch_all_flights(source,destination)
        st.dataframe(result)

elif option == "Flight's Analytics":
    st.title("Flight's Analytics :small_airplane:")

# company wise airline frequency pie chart
    company , frequency = db.airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=company,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        ))

    st.header("Company wise distribution of flights")
    st.plotly_chart(fig)

# number of flights per airport barchart
    city ,frequency1 = db.busy_airport()

    fig = px.bar(
        x= city,
        y = frequency1
    )
    st.header("Number of flights for each airport")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# daily average flights per airport bar chart
    city, average_freq = db.daily_average_flights()

    fig = px.bar(
        x=city,
        y=average_freq,
    )
    st.header("Daily avrage flights from each airport")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# Average price for each company Heatmap
    source_des, company, avg_price = db.average_price_company()
    dict1 = {'source_destination' : source_des , 'company': company , 'average_price':avg_price}
    data = pd.DataFrame(dict1)
    fig = go.Figure(data=go.Heatmap(
        z=data["average_price"],
        x=data["source_destination"],
        y=data["company"],
        colorscale = 'Viridis'))
    st.header("Average price for each company")
    st.plotly_chart(fig, theme=None,use_container_width=True)




