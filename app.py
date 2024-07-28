
import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Load data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Preprocess data
df = preprocessor.preprocess(df, region_df)

# Sidebar setup
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)


#Medal wise analysis


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medals by Each Country")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)




#overall wise analysis




if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() - 1  # Number of unique years minus one
    cities = df['City'].nunique()  # Number of unique host cities
    sports = df['Sport'].nunique()  # Number of unique sports
    events = df['Event'].nunique()  # Number of unique events
    athletes = df['Name'].nunique()  # Number of unique athletes
    nations = df['region'].nunique()  # Number of unique regions/nations

    st.title("Top Statistics")

    # CSS for vertical lines
    st.markdown("""
    <style>
    .separator {
        border-left: 1px solid #000;
        height: 100px;
        position: absolute;
        left: 50%;
        top: 0;
    }
    .column-separator {
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # First row with three columns and vertical lines
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.header("Editions")
        st.subheader(editions)
    with col2:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.header("Hosts")
        st.subheader(cities)
    with col3:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.header("Sports")
        st.subheader(sports)

    # Separation line between rows
    st.markdown("<hr>", unsafe_allow_html=True)

    # Second row with three columns and vertical lines
    col4, col5, col6 = st.columns([1, 1, 1])
    with col4:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.header("Events")
        st.subheader(events)
    with col5:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.header("Nations")
        st.subheader(nations)
    with col6:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.header("Athletes")
        st.subheader(athletes)

    # Add spacing between sections
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Generate the data over time DataFrame
    nations_over_time = helper.data_over_time(df, 'region')

    # Create the line plot using correct column names
    fig = px.line(nations_over_time, x="Year", y="Count")
    st.title("Participating nations over the years")
    # Display the figure in Streamlit
    st.plotly_chart(fig)

    # Add spacing between sections
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Generate the data over time DataFrame for events
    events_over_time = helper.data_over_time(df, 'Event')

    # Create the line plot using correct column names
    fig = px.line(events_over_time, x="Year", y="Count")

    # Display the title and the figure in Streamlit
    st.title("Events over the years")
    st.plotly_chart(fig)

    # Add spacing between sections
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Generate the data over time DataFrame for athletes
    athletes_over_time = helper.data_over_time(df, 'Name')
    # Create the line plot using correct column names
    fig = px.line(athletes_over_time, x="Year", y="Count")
    # Display the title and the figure in Streamlit
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    # Add spacing between sections
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    # Add spacing between sections
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.title("Most Successful Athletes")

    

    # List of sports
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    # Select sport
    selected_sport = st.selectbox('Select a Sport', sport_list)

    # List of medals
    medal_list = ['Gold', 'Silver', 'Bronze', 'All']
    selected_medal = st.selectbox('Select a Medal Type', medal_list)

    # List of genders
    gender_list = df['Sex'].unique().tolist()
    gender_list.sort()
    gender_list.insert(0, 'All')
    selected_gender = st.selectbox('Select Gender', gender_list)

    # Filter data based on selected sport
    if selected_sport == 'Overall':
        filtered_df = df
    else:
        filtered_df = df[df['Sport'] == selected_sport]

# Filter data based on selected medal type
    if selected_medal != 'All':
        filtered_df = filtered_df[filtered_df['Medal'] == selected_medal]

    # Filter data based on selected gender
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Sex'] == selected_gender]

    # Call helper function to get the most successful athletes
    x = helper.most_successful(filtered_df, selected_sport)

    # Display the results
    st.table(x)


#country wise analysis


if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()


    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    # Add spacing between sections
    st.markdown("<br><br><br>", unsafe_allow_html=True)


    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    # Add spacing between sections
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)



if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')



    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)

    # Plotting the line chart
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


    st.title("Athletes with Most Appearances")
    
    # Fetch data using the helper function
    appearances_df = helper.most_appearances(df)
    
    # Display the results in a table
    st.table(appearances_df)








