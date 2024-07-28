
import numpy as np
import pandas as pd


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country




def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_over_time.columns = ['Year', 'Count']  # Rename columns appropriately
    nations_over_time = nations_over_time.sort_values('Year')  # Sort by 'Year'
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    count_df = temp_df['Name'].value_counts().reset_index().head(20)
    count_df.columns = ['Name', 'Medals']
    count_df['Medals'] = count_df['Medals'].astype(str)

    merged_df = pd.merge(count_df, df, left_on='Name', right_on='Name', how='left').drop_duplicates(subset='Name')
    result_df = merged_df[['Name', 'Medals', 'Sport', 'region']]
    result_df.rename(columns={'Name': 'Athlete'}, inplace=True)

    return result_df


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df



def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    count_df = temp_df['Name'].value_counts().reset_index().head(10)
    count_df.columns = ['Name', 'Medals']
    count_df['Medals'] = count_df['Medals'].astype(str)

    merged_df = pd.merge(count_df, df, left_on='Name', right_on='Name', how='left').drop_duplicates(subset='Name')
    result_df = merged_df[['Name', 'Medals', 'Sport', 'region']]
    result_df.rename(columns={'Name': 'Athlete'}, inplace=True)

    return result_df


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    # Rename columns to ensure they have distinct names before merge
    men.rename(columns={'Name': 'Male'}, inplace=True)
    women.rename(columns={'Name': 'Female'}, inplace=True)

    # Merge the two DataFrames on 'Year'
    final = men.merge(women, on='Year', how='left')

    # Fill NaN values with 0
    final.fillna(0, inplace=True)

    return final


def most_appearances(df):
    # Count the number of appearances by each athlete
    appearances_df = df.groupby('Name')['Games'].nunique().reset_index()
    appearances_df = appearances_df.sort_values(by='Games', ascending=False).head(20)
    return appearances_df




