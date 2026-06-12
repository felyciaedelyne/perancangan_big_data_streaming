import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

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
        
st.title("Hasil Distribusi Data dan Data Discovery")
st.divider()

st.title("1. Data Information (df.info)")
st.divider()

df = pd.read_csv("sample_stream_events.csv")
df = df.head(100)

dtypes_df = pd.DataFrame({
    "dtype": df.dtypes,
    "missing_values": df.isnull().sum(),
    "unique_values": df.nunique()
})
st.dataframe(dtypes_df)
st.divider()

st.write("""
         <p style='font-size:18px; text-align:center;'> 
         <b>Action Distribution</b></p>
         """, unsafe_allow_html=True)

all_action = sorted(df['action'].unique())

with st.container(border=True):
    actions = st.multiselect(
        "Action",
        all_action,
        default=all_action
    )

    freq_action = (
        df[
            df['action'].isin(actions)
        ]['action']
        .value_counts()
        .reset_index()
    )

    freq_action.columns = [
        'Action',
        'Frequency'
    ]

    tab1, tab2 = st.tabs([
        "Chart",
        "Dataframe"
    ])

    # Bar Chart
    with tab1:

        fig = px.bar(
            freq_action,
            x='Action',
            y='Frequency',
            color='Action',
            text='Frequency'
        )

        fig.update_layout(
            xaxis_title="Action",
            yaxis_title="Frequency"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Dataframe
    with tab2:

        st.dataframe(
            freq_action,
            use_container_width=True
        )
st.divider()

st.write("<p style='font-size:18px; text-align:center;'><b>Status Distribution</b></p>", unsafe_allow_html=True)
 
all_status = sorted(df['status'].unique())
 
with st.container(border=True):
    statuses = st.multiselect("Status", all_status, default=all_status)
 
    freq_status = (
        df[df['status'].isin(statuses)]['status']
        .value_counts()
        .reset_index()
    )
    freq_status.columns = ['Status', 'Frequency']
 
    tab1, tab2 = st.tabs(["Chart", "Dataframe"])
 
    with tab1:
        fig = px.bar(freq_status, x='Status', y='Frequency', color='Status', text='Frequency')
        fig.update_layout(xaxis_title="Status", yaxis_title="Frequency")
        st.plotly_chart(fig, use_container_width=True)
 
    with tab2:
        st.dataframe(freq_status, use_container_width=True)
 
st.divider()

st.write("""
         <p style='font-size:18px; text-align:center;'> 
         <b>Distribusi Klasifikasi</b></p>
         """, unsafe_allow_html=True)

all_class = sorted(df['data_classification'].unique())

with st.container(border=True):
    classification = st.multiselect(
        "Data Classification",
        all_class,
        default=all_class
    )

    freq_class = (
        df[
            df['data_classification'].isin(classification)
        ]['data_classification']
        .value_counts()
        .reset_index()
    )

    freq_class.columns = [
        'Data Classification',
        'Frequency'
    ]

    tab1, tab2 = st.tabs([
        "Chart",
        "Dataframe"
    ])

    # Bar Chart
    with tab1:

        fig = px.bar(
            freq_class,
            x='Data Classification',
            y='Frequency',
            color='Data Classification',
            text='Frequency'
        )

        fig.update_layout(
            xaxis_title="Data Classification",
            yaxis_title="Frequency"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Dataframe
    with tab2:

        st.dataframe(
            freq_class,
            use_container_width=True
        )
st.divider()

st.write("""
         <p style='font-size:18px; text-align:center;'> 
         <b>Top 5 Users by Number of Events</b></p>
         """, unsafe_allow_html=True)

top_user = (
    df['user_id']
    .value_counts()
    .head(5)
    .reset_index()
)

top_user.columns = [
    'User ID',
    'Frequency'
]

tab1, tab2 = st.tabs([
    "Chart",
    "Dataframe"
])

# Chart
with tab1:

    fig = px.bar(
        top_user,
        x='User ID',
        y='Frequency',
        color='User ID',
        text='Frequency'
    )

    fig.update_layout(
        xaxis_title="User ID",
        yaxis_title="Number of Events"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Dataframe
with tab2:

    st.dataframe(
        top_user,
        use_container_width=True
    )
st.divider()

st.write("""
         <p style='font-size:18px; text-align:center;'> 
         <b>Top 5 Used Assets</b></p>
         """, unsafe_allow_html=True)

top_asset = (
    df['asset_id']
    .value_counts()
    .head(5)
    .reset_index()
)

top_asset.columns = [
    'Asset ID',
    'Frequency'
]

tab1, tab2 = st.tabs([
    "Chart",
    "Dataframe"
])

# Chart
with tab1:

    fig = px.bar(
        top_asset,
        x='Asset ID',
        y='Frequency',
        color='Asset ID',
        text='Frequency'
    )

    fig.update_layout(
        xaxis_title="Asset ID",
        yaxis_title="Number of Events"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Dataframe
with tab2:

    st.dataframe(
        top_asset,
        use_container_width=True
    )

