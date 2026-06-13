import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

stream_event = pd.read_csv('sample_stream_events.csv')
user = pd.read_csv('users.csv')
merged = stream_event.merge(
    user,
    on = 'user_id',
    how = 'left'
)
merged.head()

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
    stream_event['label']
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
        stream_event,
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
        stream_event['risk_score'].describe(),
        use_container_width=True
    )
st.divider()

st.title("Risk Score by Label")

tab1, tab2 = st.tabs(["Chart", "Dataframe"])

with tab1:

    fig = px.box(
        stream_event,
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
        stream_event
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
        stream_event,
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
        stream_event[
            [
                'user_id',
                'bytes_out',
                'risk_score',
                'label'
            ]
        ].head(20),
        use_container_width=True
    )

st.title("Data Security Risk Patterns")
st.divider()
#Risk 1
risk1 = merged[
    merged['status_y'] != 'active'
]

risk1_summary = (
    risk1.groupby(
        ['user_id', 'status_y', 'dept_y']
    )
    .agg(
        jumlah_event=('event_id', 'count'),
        total_bytes_out=('bytes_out', 'sum'),
        avg_risk_score=('risk_score', 'mean'),
        max_risk_score=('risk_score', 'max')
    )
    .reset_index()
    .sort_values(
        'jumlah_event',
        ascending=False
    )
)
#Risk 2
risk2 = merged[
    (merged['data_classification'].isin(
        ['confidential', 'restricted']
    ))
    &
    (
        merged['bytes_out']
        >
        merged['bytes_out'].quantile(0.95)
    )
]

risk2_summary = (
    risk2.groupby(
        [
            'user_id',
            'asset_id',
            'data_classification',
            'action'
        ]
    )
    .agg(
        jumlah_event=('event_id', 'count'),
        total_bytes_out=('bytes_out', 'sum'),
        avg_risk_score=('risk_score', 'mean')
    )
    .reset_index()
    .sort_values(
        'total_bytes_out',
        ascending=False
    )
)

#Risk 3
merged['is_external_ip'] = (
    ~merged['source_ip']
    .astype(str)
    .str.startswith('10.10.')
)

risk3 = merged[
    (merged['action'] == 'permission_change')
    &
    (merged['is_external_ip'])
]

risk3_summary = (
    risk3.groupby(
        [
            'user_id',
            'source_ip',
            'dept_y',
            'role_y',
            'status_y'
        ]
    )
    .agg(
        jumlah_event=('event_id', 'count'),
        avg_risk_score=('risk_score', 'mean'),
        max_risk_score=('risk_score', 'max')
    )
    .reset_index()
    .sort_values(
        'jumlah_event',
        ascending=False
    )
)
tab1, tab2, tab3 = st.tabs([
    "Risk 1: Terminated User",
    "Risk 2: Large Sensitive Download",
    "Risk 3: External Permission Change"
])

with tab1:

    st.subheader("Akses oleh User Terminated")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Terminated Users",
        risk1['user_id'].nunique()
    )

    col2.metric(
        "Total Events",
        len(risk1)
    )

    col3.metric(
        "Avg Risk Score",
        round(risk1['risk_score'].mean(), 2)
    )

    st.dataframe(
        risk1_summary.head(10),
        use_container_width=True
    )

with tab2:

    st.subheader(
        "Large Download from Confidential/Restricted Data"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Users",
        risk2['user_id'].nunique()
    )

    col2.metric(
        "Events",
        len(risk2)
    )

    col3.metric(
        "Total Bytes Out",
        f"{risk2['bytes_out'].sum():,.0f}"
    )

    st.dataframe(
        risk2_summary.head(10),
        use_container_width=True
    )

with tab3:

    st.subheader(
        "Permission Change from External IP"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Users",
        risk3['user_id'].nunique()
    )

    col2.metric(
        "External IP",
        risk3['source_ip'].nunique()
    )

    col3.metric(
        "Events",
        len(risk3)
    )

    st.dataframe(
        risk3_summary.head(10),
        use_container_width=True
    )
