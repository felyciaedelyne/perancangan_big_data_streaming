import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('sample_stream_events.csv')

st.set_page_config(
    page_title='Event Stream - Visualisasi Distribusi', 
    layout='wide'
)

st.markdown(
"""
<style>
div[data-testid="stSidebarNav"] {display: none;}
.stButton > button {
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
""", 
unsafe_allow_html=True)

with st.sidebar:
    st.title('Event Streaming')
    st.divider()

    if st.button('**Profile Proyek**', width="stretch"):
        st.switch_page('st_page1.py')
    
    if st.button('**Hasil Distribusi Data**', width="stretch"):
        st.switch_page('pages/st_page2.py')
    
    if st.button('**EDA dengan Visualisasi**', width="stretch"):
        st.switch_page('pages/st_page3.py')

    if st.button('**Streaming Data Insights**', width="stretch"):
        st.switch_page('pages/st_page4.py')
        
st.title("Streaming Data Insights")
st.divider()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("event_alert_stream.csv")

st.set_page_config(
    page_title='Event Stream Dashboard',
    layout='wide'
)

stream_df = pd.read_csv(
    'event_alert_stream.csv'
)

st.title('Event Stream Monitoring Dashboard')


col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Total Events",
 len(stream_df)
)

col2.metric(
    "Critical Alerts",
    len(
        stream_df[
            stream_df['alert_level'] == 'CRITICAL'
        ]
    )
)

col3.metric(
    "High Alerts",
    len(
        stream_df[
            stream_df['alert_level'] == 'HIGH'
        ]
    )
)

col4.metric(
    "Unique Users",
    df['user_id'].nunique()
)
st.divider()
st.title("Alerts Distribution")

fig, ax = plt.subplots()

df['alert_level'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%',
    ax=ax
)
ax.set_ylabel('')

st.pyplot(fig)
st.divider()

st.title("Top Risky User")
top_users = (
    df.groupby('user_id')['risk_score']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(top_users)
st.divider()
st.title("Department Risk Score")

dept_risk = (
    df.groupby('dept')['risk_score']
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(dept_risk)
st.divider()

st.title("Data Classification Access")

st.bar_chart(
    df['data_classification']
    .value_counts()
)
st.divider()

st.title("Critical Alert Table")
critical_df = df[
    df['alert_level'] == 'CRITICAL'
]

st.dataframe(
    critical_df
)
st.divider()

st.title("Top 10 Security Alerts")
top_alert = (
    df.sort_values(
        by='risk_score',
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_alert[
        [
            'event_id',
            'user_id',
            'action',
            'asset_id',
            'risk_score',
            'alert_level'
        ]
    ]
)

st.title("Latest Events")

st.dataframe(
    df.tail(20)
)
