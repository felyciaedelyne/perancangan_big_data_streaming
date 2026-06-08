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
        
st.title("EDA dengan Visualisasi")
st.divider()

st.title("Label Distribution")

label_dist = (
    df['label']
    .value_counts()
    .reset_index()
)

label_dist.columns = ['Label', 'Frequency']

tab1, tab2 = st.tabs(["Chart", "Dataframe"])

with tab1:

    fig = px.pie(
        label_dist,
        names='Label',
        values='Frequency',
        hole=0.3
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:
    st.dataframe(label_dist, use_container_width=True)
st.divider()

st.title("Risk Score Distribution")

tab1, tab2 = st.tabs(["Chart", "Statistics"])

with tab1:

    fig = px.histogram(
        df,
        x='risk_score',
        nbins=20
    )

    fig.update_layout(
        xaxis_title='Risk Score',
        yaxis_title='Frequency'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:

    st.dataframe(
        df['risk_score'].describe(),
        use_container_width=True
    )
st.divider()

st.title("Risk Score by Label")

tab1, tab2 = st.tabs(["Chart", "Dataframe"])

with tab1:

    fig = px.box(
        df,
        x='label',
        y='risk_score',
        color='label'
    )

    fig.update_layout(
        xaxis_title='Label',
        yaxis_title='Risk Score'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:

    summary = (
        df
        .groupby('label')['risk_score']
        .describe()
        .reset_index()
    )

    st.dataframe(
        summary,
        use_container_width=True
    )
st.divider()

st.title("Bytes Out vs Risk Score")

tab1, tab2 = st.tabs(["Chart", "Dataframe"])

with tab1:

    fig = px.scatter(
        df,
        x='bytes_out',
        y='risk_score',
        color='label',
        hover_data=[
            'user_id',
            'action',
            'asset_id'
        ]
    )

    fig.update_layout(
        xaxis_title='Bytes Out',
        yaxis_title='Risk Score'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:

    st.dataframe(
        df[
            [
                'user_id',
                'bytes_out',
                'risk_score',
                'label'
            ]
        ].head(20),
        use_container_width=True
    )