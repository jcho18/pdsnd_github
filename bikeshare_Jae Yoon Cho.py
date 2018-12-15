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

    valid_input = False
    valid_city = False
    valid_day = False
    valid_month = False
    valid_option = False
    valid_5line = False

    while not valid_input:    
        print('Hello! Let\'s explore some US bikeshare data!') 
        while not valid_city:   
            # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
            print('Would you like to see data for Chicago, New York, or Washington?')
            
            city = input()

            if city.lower() != 'chicago' and city.lower() != 'new york city' and city.lower() != 'new york' and city.lower() != 'washington':
                print('Invalid Input')
                continue
            else:
                valid_city = True

        while not valid_option:
        # get user input for month (all, january, february, ... , june)
            print('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter?')
            option = input()
            if option.lower() != 'month' and option.lower() != 'day' and option.lower() != 'both' and option.lower() != 'none':
                print('Invalid Input')
                continue
            else:
                valid_option = True

        if option.lower() == 'month' or option.lower() == 'both':
            # get user input for day of week (all, monday, tuesday, ... sunday)
            if option.lower() == 'month':
                day = 0
            while not valid_month:
                print('Which month? Please type your response as an integer (e.g., 1=Jan).')
                month = input()
                if not 1 <= int(month) <= 12:
                    print('Invalid Input')
                    continue
                else:
                    valid_month = True

        if option.lower() == 'day' or option.lower() == 'both':
            # get user input for day of week (all, monday, tuesday, ... sunday)
            if option.lower() == 'day':
                month = 0
            while not valid_day:
                print('Which day? Please type your response as an integer (e.g., 1=Sunday).')
                day = input()
                if not 1 <= int(day) <= 7:
                    print('Invalid Input')
                    continue
                else:
                    valid_day = True

        if option.lower() == 'none':
            month = 0
            day = 0

        valid_input = True

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

    days = {'1': 'Sunday', '2': 'Monday', '3': 'Tuesday', '4': 'Wednesday', '5': 'Thursday', '6': 'Friday',\
        '7': 'Saturday'}

    if city.lower() == 'chicago':
        # load Chicago
        df = pd.read_csv('chicago.csv', skipinitialspace=True)
    elif city.lower() == 'new york city' or city.lower() == 'new york':
        # load NYC
        df = pd.read_csv('new_york_city.csv', skipinitialspace=True)
    elif city.lower() == 'washington':
        # load Washington
        df = pd.read_csv('washington.csv', skipinitialspace=True)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name

    if int(month) != 0:
        df = df[df['Month'] == int(month)]
    if int(day) != 0:
        df = df[df['Day'] == days[day]]

    #print(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    df['Hour'] = df['Start Time'].dt.hour
    if len(df['Month'].value_counts()) == 0 or len(df['Day'].value_counts()) == 0:
        print('No Records in this Month or Day')
        return

    # display the most common month
    most_freq_month_count = df['Month'].value_counts().idxmax()
    print('Most popular month:', most_freq_month_count)


    # display the most common day of week
    most_freq_day_count = df['Day'].value_counts().idxmax()
    print('Most popular day:', most_freq_day_count)


    # display the most common start hour
    most_freq_hour_count = df['Hour'].value_counts().idxmax()
    print('Most popular hour:', most_freq_hour_count)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if len(df['Month'].value_counts()) == 0 or len(df['Day'].value_counts()) == 0:
        print('No Records in this Month or Day')
        return

    # display most commonly used start station
    most_freq_start = df['Start Station'].value_counts().idxmax()

    # display most commonly used end station
    most_freq_end = df['End Station'].value_counts().idxmax()

    # display most frequent combination of start station and end station trip
    most_freq_comb = df.groupby(['Start Station', 'End Station']).size().nlargest(1).idxmax()

    print('Most Commonly Start Station:', most_freq_start)
    print('Most Commonly End Station:', most_freq_end)
    print('Most Frequent Combintion:', most_freq_comb)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    if len(df['Month'].value_counts()) == 0 or len(df['Day'].value_counts()) == 0:
        print('No Records in this Month or Day')
        return

    df['Duration'] = df['End Time'].values - df['Start Time'].values

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time:', df['Duration'].sum())

    # display mean travel time
    print('Mean Travel Time:', df['Duration'].mean())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if len(df['Month'].value_counts()) == 0 or len(df['Day'].value_counts()) == 0:
        print('No Records in this Month or Day')
        return
        
    # Display counts of user types
    
    user_type_count = df['User Type'].value_counts()
    print('Counts of User Types')
    print(user_type_count)

    # Display counts of gender
    if 'Gender' in df: # Washington does not have a Gender column
        user_type_count = df['Gender'].value_counts()
        print('Counts of Gender')
        print(user_type_count)

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df: # Washington does not have a Gender column
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].value_counts().idxmax()

        print('Earliest Birth:', earliest_birth)
        print('Most Recent Birth:', recent_birth)
        print('Most Common Birth:', common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    display_data(df)

def display_data(df):
    "Display Raw Data"

    k1, k2 = 0, 5 # number to slice

    valid_input = False
    valid_input2 = False
    while not valid_input:   

        print('Display Raw Data? (5 lines) -- Y/N') 
        
        display = input()

        if display.lower() != 'y' and display.lower() != 'n':
            print('Invalid Input -- input Y or N')
            continue
        elif display.lower() == 'y':
            while True:
                print(df[k1 : k2])
                print('Display 5 more lines? -- Y/N') 
                display2 = input()
                if display2.lower() == 'n':
                    valid_input = True
                    break
                if len(df[k1 : k2].index) == 0:
                    print('No more data to display')
                    return
                k1 += 5
                k2 += 5
            

        elif display.lower() == 'n':
            valid_input = True
   


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
   main()