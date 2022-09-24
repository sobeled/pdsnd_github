import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
         try:
             city = input("Please input one of the following cities - Chicago, New York City or Washington: ").lower()
             if city in CITY_DATA:
                 print("Thank you!")
                 break
             else:
                 print('That is not a valid city name. Please type Chicago, New York, or Washinton.')
         finally:
             print("")

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['all','january', 'february', 'march', 'april', 'may', 'june']
        month = input("Please enter a month on which to filter (All, January, February, etc.): ").lower()
        if month in months:
            print("Thank you!")
            break
        else:
            print("That is not a valid month. Please type a valid month (January, February, etc.)")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = input("Please enter a day of the week on which to filter (All, Sunday, Monday, etc.): ").lower()
        if day in days:
            print("Thank you!")
            break
        else:
            print("That is not a valid day. Please type a valid day (Sunday, Monday, etc.)")

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
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
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = days.index(day) + 1

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()



    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of the Week:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station: ',common_start)


    # display most commonly used end station
    common_end = df['End Station'].value_counts().idxmax()
    print('Most Common End Station: ',common_end)

    # display most frequent combination of start station and end station trip
    station_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Frequent Station Combination: ',station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total Travel Time: ",total_time," seconds")

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean Travel Time: ",mean_time," seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender only if the data is available
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print(genders)
    else:
        print("No gender data avialable.")

    # Display earliest, most recent, and most common year of birth only if the data is avialable
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print("Earliest year of birth: ",earliest_year)
        print("Most recent year of birth: ",recent_year)
        print("Most common year of birth: ",common_year)
    else:
        print("No birth year data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Asks if the user would like to see 5 line of raw data at a time
        data_count = 0
        while True:
            ask_data = input("Would you like to see 5 lines of raw data? Enter Yes or No: ").lower()
            if ask_data == "yes":
                print(df.iloc[data_count:data_count + 5])
                data_count += 5
            else:
                break
        # Asks if the user would like to restart the program            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
