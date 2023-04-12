import streamlit as st
import scipy
import pandas as pd
import plotly.express as px
import preprocess,helper
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import seaborn as sns


df_events=pd.read_csv('athlete_events.csv')
df_region=pd.read_csv('noc_regions.csv')

df=preprocess.preprocess(df_events,df_region)
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

user_=st.sidebar.radio(
   'Select an option',
    ('Medal analysis','Overall analysis','Country-wise analysis','Athlete-wise analysis')
)

#st.dataframe(df)
if user_=='Medal analysis':
    st.header('Medal Analysis')
    country,years = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal=helper.medal_analysis(df,selected_country,selected_year)
    if selected_year == 'overall' and selected_country == 'overall':
        st.title("Overall Records")
    elif selected_year != 'overall' and selected_country == 'overall':
        st.title(str(selected_year) + " olympics"+' Medal Records')
    elif selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country +' '+ "performance over the years")
    elif selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal)

if user_ == 'Overall analysis':
    editions = df['Year'].nunique()-1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("Olympic Statis")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Total Editions")
        st.title(editions)
    with col2:
        st.header("Total Hosts")
        st.title(cities)
    with col3:
        st.header("Total Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Total Events")
        st.title(events)
    with col2:
        st.header("Total Nations")
        st.title(nations)
    with col3:
        st.header("Total Athletes")
        st.title(athletes)


    plot_df=helper.nations_graph(df)
    fig = px.line(plot_df, x='Year', y='region')
    st.title("Participant Counts over the years")
    st.plotly_chart(fig)

    plot_df = helper.events_graph(df)
    fig = px.line(plot_df, x='Year', y='Event')
    st.title("Event Counts over the years")
    st.plotly_chart(fig)

    plot_df = helper.athletes_graph(df)
    fig = px.line(plot_df, x='Year', y='Name')
    st.title("Athlete Counts over the years")
    st.plotly_chart(fig)

    st.title("No. of Events per sport over the years")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title("Highest Ranking acc to Medal")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.highest_medal(df, selected_sport)
    st.table(x)

if user_== 'Country-wise analysis':

    st.sidebar.title('Country-wise analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.remove('India')
    country_list.insert(0,'India')

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.country_wise(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.highest_medal_country_wise(df, selected_country)
    st.table(top10_df)

if user_== 'Athlete-wise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df,x='Height',y='Weight', hue='Medal', style='Sex', s=60)
    st.pyplot(fig)



