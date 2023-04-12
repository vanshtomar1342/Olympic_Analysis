import numpy as np
def medal_(df):
    medal = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_analysis = medal.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_analysis['Total'] = medal_analysis.Gold + medal_analysis.Silver + medal_analysis.Bronze
    return medal_analysis

def  country_year_list(df):
    #For country list
    c = df.region.dropna()
    country = np.unique(c).tolist()
    country.sort()
    country.insert(0, 'overall')

    #For years list
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')

    return country,years

def medal_analysis(df2,country,year):
        df = df2.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
        a = False
        if year == 'overall' and country == 'overall':
            df1 = df
        if year == 'overall' and country != 'overall':
            a = True
            df1 = df[df.region == country]
        if year != 'overall' and country == 'overall':
            df1 = df[df['Year'] == int(year)]
        if year != 'overall' and country != 'overall':
            df1 = df[(df['region'] == country) & (df.Year == int(year))]
        if a == True:
            medal = df1.groupby('Year')[['Gold', 'Silver', 'Bronze', 'Total']].sum().sort_index().reset_index()
        else:
            medal = df1.groupby('region')[['Gold', 'Silver', 'Bronze', 'Total']].sum().sort_values('Gold',
                                                                                                   ascending=False).reset_index()
        return medal


def nations_graph(df):
    plot_df = df.groupby('Year')['region'].nunique().reset_index()
    return plot_df

def events_graph(df):
    plot_df = df.groupby('Year')['Event'].nunique().reset_index()
    return plot_df

def athletes_graph(df):
    plot_df = df.groupby('Year')['Name'].nunique().reset_index()
    return plot_df

def highest_medal(df,sport):
    df1=df.dropna(subset=['Medal'])
    if sport!='overall':
        df1=df1[df1['Sport']==sport]
    medal=df1.groupby('Name')['Medal'].count().sort_values(ascending=False).reset_index().head(15).merge(df,on='Name',how='left')[['Name','Sport','Medal_x','region']].drop_duplicates().reset_index(drop=True)
    return medal

def country_wise(df,country):
    df1 = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    df1.dropna(subset=['Medal'],inplace=True)
    df2=df1[df1['region']==country]
    ans=df2.groupby(['Year'])['Medal'].count().reset_index()
    return ans

def highest_medal_country_wise(df,country):
    df1=df.dropna(subset=['Medal'])
    df1=df1[df1['region']==country]
    medal=df1.groupby('Name')['Medal'].count().sort_values(ascending=False).reset_index().head(15).merge(df,on='Name',how='left')[['Name','Sport','Medal_x']].drop_duplicates().reset_index(drop=True)
    return medal

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df