import pandas as pd


def preprocess(df_events,df_region):
    df_events=df_events[df_events.Season=='Summer']
    df_comb = pd.merge(df_events, df_region, on='NOC', how='left')
    df_comb.drop_duplicates(inplace=True)
    df1 = pd.get_dummies(df_comb.Medal)
    df = pd.concat([df_comb, df1], axis=1)
    df['Total']=df.Gold+df.Silver+df.Bronze
    return df