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


    while True:
        city = str(input("\nWould you like to see data for Chicago, New York City, or Washington?")).strip().lower()

        if city not in ("chicago", "new york city", "washington"):
            print("\nPlease try again")
            continue
        else:
            print("\nYou want to see data for: {}".format(city.title()))
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("\nSpecify the name of the month to filter by (i.e January, All): ").strip().lower())
        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("\nPlease specify the month name")
            continue
        else:
            print("\nYou want to filter by: {}".format(month.title()))
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("\nSpecify the name of day to filter by (i.e Monday, All): ").strip().lower())
        if day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday" , "sunday", "all"):
            print("\nPlease specify the day name")
        else:
            print("\nYou want to filter by: {}".format(day.title()))
            break

    print("\nFilters applied: \nCity: {}, \nMonth: {}, \nDay: {}".format(city.title(), month.title(), day.title()))


    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start time to column to datatime type
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month from Start Time
    df["Month"] = df["Start Time"].dt.month

    # extract weekday from Start Time
    df["Day of Week"] = df["Start Time"].dt.weekday_name

    # extract hour from the Start Time
    df["Hour"] = df["Start Time"].dt.hour

    # filter by month
    if month != "all":
        # use the index
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        # month outputted as integer
        month = months.index(month) + 1

        df = df[df["Month"] == month]

    # filter by day of week
    if day != "all":
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        df = df[df["Day of Week"]== day.title()]


    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_values = {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June"}
    common_month = df["Month"].mode()[0]
    print("\nMost common month was: {}".format(month_values[str(common_month)]))

    # display the most common day of week
    common_day = df["Day of Week"].mode()[0]
    print("\nMost common day was: {}".format(common_day))


    # display the most common start hour
    common_start_hour = df["Hour"].mode()[0]
    print("\nMost common start hour was: {}".format(common_start_hour))


    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df["Start Station"].mode()[0]
    print("\nMost common start station was: {}".format(start_station))

    # display most commonly used end station
    end_station = df["End Station"].mode()[0]
    print("\nMost common end station was: {}".format(end_station))


    # display most frequent combination of start station and end station trip
    stations_comb = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index(name="counts")
    print("\nThe start station for most frequent combination was: {} and the end station was: {}".format(stations_comb["Start Station"][0],
                                                                                                    stations_comb["End Station"][1]))


    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()

    # Calculate time with % and // to return the travel time in  D:H:M:S format
    # Inspired from: https://github.com/sauravraghuvanshi/Udacity-programming-for-Data-Science-With-Python-Nanodegree/blob/master/Project-2/bikeshare.py
    total_travel_time_conv = str(int(total_travel_time//86400)) + "d " + str(int(total_travel_time % 86400) // 3600) + "h " + str(int((((total_travel_time % 86400) % 3600)//60))) + "m " + str(int(((total_travel_time % 86400) % 3600) % 60)) + "s"
    print("\nTotal travel time was {}".format(total_travel_time_conv))

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    mean_travel_time_conv = str(int(mean_travel_time // 60)) + "m " + str(int(mean_travel_time % 60)) + "s "
    print("\nMean travel time was: {}".format(mean_travel_time_conv))

    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # extract values from value_counts(): https://stackoverflow.com/questions/35523635/extract-values-in-pandas-value-counts

    for i, n in zip(df["User Type"].value_counts().keys().tolist(), df["User Type"].value_counts().tolist()):
        print("\nUser type:", i, "has a count of:", n)

    # Display counts of gender
    if "Gender" in df.columns:
        gender = df["Gender"].value_counts().keys().tolist()
        counts = df["Gender"].value_counts().tolist()
        nan_values = df["Gender"].isna().sum()
        print("\nBreakdown of gender: \n{} : {} \n{} : {} \nMissing values: {}".format(gender[0], counts[0], gender[1], counts[1], nan_values))

    else:
        print("\nNo gender data to share'")


    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest = df["Birth Year"].min()
        most_recent = df["Birth Year"].max()
        most_common = df["Birth Year"].mode()[0]
        print("\nEarliest year of birth: {}. \nMost recent year of birth: {}. \nMost common year of birth: {}".format(int(earliest), int(most_recent), int(most_common)))
    else:
        print("This dataset has no column named 'Birth Year'.")

    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)


def show_data(df):
    """
    Iterate through 5 entries at a time

    Returns:
        Print five rows of data to terminal

    """
    user_input = input("\n Would you like to see the individual raw data? Enter 'yes' or 'no'\n").strip().lower()
    if user_input in ("yes"):
        i = 0
        while True:
            print(df.iloc[i:i+5])
            i += 5
            more_data = input("\nWould you like to see more data? Enter 'yes' or 'no'\n").strip().lower()
            if more_data not in ('yes'):
                break


def main():
    """Main body of program"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Yes or No?\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
