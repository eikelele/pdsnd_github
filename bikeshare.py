import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    day_list = ['monday','tuesday','wednesday','thursday','friday', 'saturday','sunday','all']
    #Could use months / month_list as an global variable, but global variables should only be used when no other solution is possible!
    month_list = ['january','february','march','april','may', 'june','all']
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Please type in your city: ').lower())
            if city not in CITY_DATA:
                print('Not a valid city!\nTry Again!')
            else:
                break
        except Exception as e:
            print(e)
            break

    while True:
        try:
            month = str(input('Please type in your month: ').lower())
            if month not in month_list:
                print('Not a valid month!\nTry Again!')
            else:
                break
        except Exception as e:
            print(e)
            break

    while True:
        try:
            day = str(input('Please type in your weekday: ').lower())
            if day not in day_list:
                print('Not a valid day of week!\nTry Again!')
            else:
                break
        except Exception as e:
            print(e)
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    """If month != 'all' this month is the most common. So not needed."""

    common_month = df['month'].mode().item()
    if month == 'all':
        print('Most common month: {}'.format(month_dict[common_month]))
    else:
        print('Selected Month: {}'.format(month_dict[common_month]))

    # TO DO: display the most common day of week
    if day == 'all':
        print('Most common day of week: {}'.format(df['day_of_week'].mode().item()))
    else:
        print('Selected day of week: {}'.format(df['day_of_week'].mode().item()))
    # TO DO: display the most common start hour
    print('Most common start hour: {}'.format(df['hour'].mode().item()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."" int('\nCalculating The Most Popular Stations and Trip...\n')"""
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most commonly used start station: ' + df['Start Station'].mode().item())

    # TO DO: display most commonly used end station
    print('Most commonly used end station: ' + df['End Station'].mode().item())

    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = 'Most frequent combination: Start Station: ' + df['Start Station'] + ' | End Station: ' + df['End Station']
    most_common = df['combination'].mode().item()
    print(most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    if (df['Trip Duration'].isnull().sum()) == 0:
        print('Total Trip Duration: {} seconds'.format(df['Trip Duration'].sum()))
    else:
        df.fillna(0)
        print('Total Trip Duration: {} seconds'.format(df['Trip Duration'].sum()))
    # TO DO: display mean travel time
    print('Mean travel time per trip: {} seconds'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if city == 'chicago' or city == 'new york city':
        print(df['Gender'].value_counts())
    else:
        print('No gender data for Washington!')

    # TO DO: Display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york city':
        print('Earlist Birth Year: {}'.format(int(df['Birth Year'].min())))
        print('Most recent Birth Year: {}'.format(int(df['Birth Year'].max())))
        print('Most common Birth Year: {}'.format(int(df['Birth Year'].mode().item())))
    else:
        print('No birth data for Washington!')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df,month,day):
    index = 0
    """Displays random data if the user wants to. Else the look breaks."""

    while True:
        decision = str(input("Do you want to print raw data? Please type 'yes' or 'no': ").lower())
        if decision != 'yes' and decision != 'no':
            print("No valid input! Please type 'yes' or 'no'.")
        elif decision == 'yes':
            print(df.iloc[(index):(index+5)])
            index += 5
        elif decision == 'no':
            print('You stopped to output raw data. Thank you!')
            break





def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df,month,day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()