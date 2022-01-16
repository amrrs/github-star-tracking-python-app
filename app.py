import streamlit as st 
import requests
import pandas as pd 
from pandas import json_normalize
import plotly.express as px 

def create_stargazers_count(user,repo):
    """this function creates the stargazers count dataframe"""

    star_count_url = "https://api.github.com/repos/"+user+"/"+repo
    response = requests.request("GET", star_count_url)
    total_star_count = response.json()['stargazers_count']
    loops = int(total_star_count / 100) + 1
    star_trends_url = "https://api.github.com/repos/"+user+"/"+repo+"/stargazers"
    star_trends_resp = []
    headers = {
    "Accept": "application/vnd.github.v3.star+json",
    "content-type": "application/json"
    }
    for page in range(loops):
        response = requests.request("GET", star_trends_url+"?per_page=100"+"&page="+str(page+1), headers=headers).json()
        star_trends_resp.extend(response)

    df = json_normalize(star_trends_resp)

    df['starred_date'] = pd.to_datetime(df['starred_at']).dt.date

    star_trend_df = df.groupby(['starred_date'])['starred_date'].count().cumsum().reset_index(name="count")

    return star_trend_df


st.title("⭐️ Github Star Tracking ⭐️")

st.subheader("with interactive ⭐️ History chart")

st.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpngimg.com%2Fuploads%2Fgithub%2Fgithub_PNG93.png&f=1&nofb=1",
width=200)

st.markdown("### Github Repo Details")

first,second = st.columns(2)

with first:
    user = st.text_input(label="Enter the github user name", value =  "amrrs")

with second:
    repo = st.text_input(label="Enter the github repo name (without the user name)", value =  "coinmarketcapr")

st.write("You are going to see the star trends for this repo:" + user+"/"+repo +"/")


with st.spinner("Downloading Data from Github.....Stars are coming....."):
    df = create_stargazers_count(user,repo)

st.markdown("### Github Stars Trend")

chart = px.line(data_frame=df, x = 'starred_date', y = 'count')

st.plotly_chart(chart)
