from pywebio import start_server
from pywebio.input import actions, input, NUMBER
from pywebio.output import put_error, put_info, put_text, put_html, put_markdown, put_table
from pywebio.platform.flask import webio_view
import argparse
from flask import Flask
import webbrowser
import time
import pandas as pd
import datetime
import os

app = Flask(__name__)

current_directory = os.getcwd()
print('## Current working directory: ', current_directory)

CITY_DATA = {'chicago': "chicago.csv",
             'new york': "new_york_city.csv",
             'washington': "washington.csv"}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply 
            no month filter
        (str) day - name of the day of week to filter by, or "all" to apply 
            no day filter
    """
    city = ""
    cities = ('chicago', 'new york', 'washington')
    while (city.title() != "Chicago", city.title() != "New York", city.title != "Washington"):
        city = input('Would you like to see data for Chicago, New York, or Washington?\n', type='text')
        if city.lower() in cities:
            break

    filter_type = ""
    filter_types = ('none', 'month', 'day', 'both')
    while (filter_type.lower() not in filter_types):
        filter_type = input('How would you like to filter the data, by month, day, both or not at all? Type "none" for no time filters.', type='text')

    # get user input for month (all, january, february, ... , june)
    if (filter_type == 'month' or filter_type == 'both'):
        if(filter_type == 'month'):
            day = 'all'
        month = ""
        months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
        while (month != 'january', month != 'february', month != 'march',
               month != 'april', month != 'may', month != 'may'):
            month = input('Please type in the month to filter the data by: January, February, March, April, May and June.',type='text').lower()
            if (month in months):
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if (filter_type == 'day' or filter_type == 'both'):
        if filter_type == 'day':
            month = 'all'

        day = ''
        days = ['all', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday']
        while (day != all and day not in days):
            day = days[int(input('Please select the day to filter the day by as integer(1 =Sunday, 2 = Monday etc.)', type=NUMBER))]

    if filter_type == 'none':
        month = 'all'
        day = 'all'

    put_markdown(f'### You have selected to view data for: **{city} (Filtered by: {filter_type})**')
    if month != 'all':
        put_markdown(f'Month Filter: {month}'.title())
    if day != 'all':
        put_markdown(f'Day Filter: {day}'.title())

    put_html('<br>')

    # format city to lowercase.
    city = city.lower()

    return city, month, day


def openurl():
    put_error('You selected not "Accept" the Terms, therefore, you barred access to the data.\nAlternatively, refresh and "Accept" the terms.')
    webbrowser.open('https://www.motivateco.com/', new=0)
    raise SystemExit


def welcome():
    """This function is displays the welcome page to our web app."""
    put_markdown('# **Explore US Bikeshare Data**')
    intro = 'This web app assist you in uncovering bike share usage patterns, using data provided by Motivate, a bike share system provider for many major cities in the United States \nYou will be able to compare the system usage between three large cities: Chicago, New York City, and Washington'
    put_text(intro)
    put_html('<hr>')
    confirm_desc = 'By select the "Accept" you accept the the data provided\
    in app will only be used for education and training purposes and \
        will not be distributed.'
    confirm = actions(confirm_desc, ['Accept', 'Cancel'],
                      help_text='Select "Accept" to continue and "Cancel" to exit')
    if confirm != 'Accept':
        openurl()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
            month filter
        (str) day - name of the day of week to filter by, or "all" to apply
            no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of the week if applicable
    if day != 'all':
        # filter by the day of the week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    put_markdown('### Calculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # computes the most common start hour
    common_start_hour = df['start_hour'].mode()[0]

    # computes the 'count' for the most common hour
    hour_count = 0
    for t in df['start_hour']:
        if t == common_start_hour:
            hour_count += 1

    # computing values for Filter

    put_table([
        ['Most popular hour', 'Count'],
        [common_start_hour, hour_count]
    ])

    put_markdown("\n**This took %s seconds.**" % (time.time() - start_time))
    put_html('<br>')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    put_markdown('### Calculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # computes the most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    # computes the 'count' for the most commonly used start station
    count_start_station = 0
    for ss in df['Start Station']:
        if ss == common_start_station:
            count_start_station += 1

    # computes the most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    # computes the 'count' for the most commonly used end station
    count_end_station = 0
    for es in df['End Station']:
        if es == common_end_station:
            count_end_station += 1

    # computes the most frequent combination of start station and
    # end station trip
    df['trip'] = df['Start Station'] +' to '+ df['End Station']
    common_trip = df['trip'].mode()[0]

    # computes the 'count' for the most frequent combination of
    # start station and end station trip
    count_trip = 0
    for trip in df['trip']:
        if trip == common_trip:
            count_trip += 1

    put_table([
        [' ', 'Most Popular', 'Count'],
        ['Start Station', common_start_station, count_start_station],
        ['End Station', common_end_station, count_end_station],
        ['Trip', common_trip, count_trip]
    ])

    put_markdown("\n**This took %s seconds.**" % (time.time() - start_time))
    put_html('<br>')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    put_markdown('### Calculating Trip Duration...')
    start_time = time.time()

    # since the Start Time column was converted to datetime during the
    # load data function, we also nhave to convert the End Time column.
    df['End Time'] = pd.to_datetime(df['End Time'])

    # computes total travel time
    df['travel_time'] = (df['End Time'] - df['Start Time'])
    sum_travel_time = df['travel_time'].sum()

    # computes mean travel time
    avg_travel_time = df['travel_time'].mean()

    # computes the count for travel time
    count_travel_time = df['travel_time'].count()

    put_table([
        ['Total Trips Duration', 'Count', 'AVG Trip Duration'],
        [sum_travel_time, count_travel_time, avg_travel_time]
    ])
    put_markdown("\n**This took %s seconds.**" % (time.time() - start_time))
    put_html('<br>')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    put_markdown('### Calculating User Stats...')
    start_time = time.time()

    # computes counts of user types
    user_types = df['User Type'].value_counts()
    put_markdown('**User Type Distribution:**')
    if 'Dependent' in user_types:
        put_table([
            ['Subscriber', 'Customer', 'Dependent'],
            [user_types[0], user_types[1], user_types[2]]
        ])
    else:
        put_table([
            ['Subscriber', 'Customer'],
            [user_types[0], user_types[1]]
        ])

    # computes counts of gender
    if 'Gender' in df.columns:
        """The Washington Dataset does not have 'gender' data,
        therefore, we need to validate the Gender column. """
        index = pd.Index(df['Gender'])
        gender_distr = index.value_counts()
        if gender_distr is None:
            put_error('There is no Gender Distribution data')
        else:
            put_markdown('**Gender Distribution:**')
            put_table([
                ['Male', 'Female'],
                [gender_distr[0], gender_distr[1]]
            ])
    else:
        put_error('There is no Gender Distribution data')

    # computes earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        """The Washington Dataset does not have 'birth year' data,
        therefore, we need to validate the Birth Year column. """
        x = datetime.datetime.now()
        put_markdown('**Age Distribution**')
        put_table([
            ['', 'Birth Year', 'Age'],
            ['Te youngest communter', int((df['Birth Year']).max()),(x.year - int((df['Birth Year']).max()))],
            ['The oldest commuter', int((df['Birth Year']).min()),(x.year - int((df['Birth Year']).min()))],
            ['Most commuters', int(df['Birth Year'].mode()[0]), (x.year - int(df['Birth Year'].mode()[0]))]   
        ])
    else:
        put_error('There is no Birth Year data')

    put_markdown("\n**This took %s seconds.**" % (time.time() - start_time))
    put_html('<br>')


def raw_data(df):
    """This will allow the user to view the raw data used in for determining the Stats"""
    start_time = time.time()
    raw_data_confirm = "Would you like to see the raw data used to generate these bikeshare usage patterns?"
    confirm = actions(raw_data_confirm, ['Yes', 'No'],)
    if confirm == 'Yes':
        put_markdown('### Raw Data...')
        start_row = 0
        end_row = 5
        max_rows = len(df)

        put_text(df[start_row:end_row])
        while end_row < max_rows:
            load_next = 'Load next set of rows?'
            user_input = actions(load_next, ['Yes', 'No'],)
            if user_input == 'Yes':
                start_row += 5
                end_row += 5
                put_text(df[start_row:end_row])
            else:
                print(" ")
                break

    put_markdown("\n**This took %s seconds.**" % (time.time() - start_time))
    put_html('<br>')


def main():
    welcome()
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = actions('Would you like to restart?', ['Yes', 'No'], help_text='Select "Yes" to Restart Data Filter or "No" to exit')
        if restart == 'Yes':
            put_html('<br><br>')
            put_html('<hr size="2" width="90%" color="black">')
            put_info('New Selection')
            continue
        if restart == 'No':
            put_html('<br><br><br>')
            put_info('End of Report')
            raise SystemExit


app.add_url_rule('/tool', 'webio_view', webio_view(main),
                 methods=['GET', 'POST', 'OPTIONS'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port)
