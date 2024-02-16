import streamlit as st
import pandas.io.sql as sqlio
import altair as alt
from streamlit_folium import st_folium
from db import conn_str
import pandas as pd
from pandas.tseries.offsets import DateOffset

st.title("Seattle Events")
df = sqlio.read_sql_query("SELECT * FROM events", conn_str)

all_categories = ['All'] + list(df['category'].unique())
all_locations = ['All'] + list(df['location'].unique())

category = st.sidebar.selectbox('Select Category', all_categories)
location = st.sidebar.selectbox('Select Location', all_locations)


start_date, end_date = st.sidebar.date_input('Select Date Range', value=[pd.to_datetime('2024-01-01'), pd.to_datetime('2024-12-31')])

start_datetime = pd.to_datetime(start_date).tz_localize('UTC').tz_convert('US/Pacific')
end_datetime = pd.to_datetime(end_date).tz_localize('UTC').tz_convert('US/Pacific') + DateOffset(hours=23, minutes=59, seconds=59)

filtered_df = df.copy()
if category != 'All':
    filtered_df = filtered_df[filtered_df['category'] == category]
if location != 'All':
    filtered_df = filtered_df[filtered_df['location'] == location]

filtered_df = filtered_df[(filtered_df['date'] >= start_datetime) & (filtered_df['date'] <= end_datetime)]

st.write(filtered_df)


number_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('count()', title='Number of Events'),
    y=alt.Y('category', sort='-x', title='Category')
).properties(
    title='Most Common Event Categories in Seattle'
).interactive()

st.altair_chart(number_chart, use_container_width=True)


df['date'] = pd.to_datetime(df['date'], utc=True)
df['date'] = df['date'].dt.tz_convert('US/Pacific')
df['month'] = df['date'].dt.month_name() 
df['weekday'] = df['date'].dt.weekday


month_df = df['month'].value_counts().reset_index()
month_df.columns = ['Month', 'Number of Events']
month_df = month_df.sort_values(by='Month', key=lambda x: pd.to_datetime(x, format='%B')) 


month_chart = alt.Chart(month_df).mark_bar().encode(
    x=alt.X('Month', sort=list(month_df['Month']), axis=alt.Axis(title='Month', labelAngle=0)),  
    y='Number of Events',
    tooltip=['Month', 'Number of Events']
).properties(
    title='Number of Events per Month'
).interactive()
st.altair_chart(month_chart, use_container_width=True)

location_count = df['location'].value_counts().reset_index()
location_count.columns = ['Location', 'Number of Events']

location_chart = alt.Chart(location_count).mark_bar().encode(
    x=alt.X('Location', sort='-y'),
    y='Number of Events',
    color='Location',
    tooltip=['Location', 'Number of Events']
).properties(
    title='Common Event Locations in Seattle'
)
st.altair_chart(location_chart, use_container_width=True)
