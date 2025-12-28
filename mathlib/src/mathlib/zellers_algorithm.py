import math

DAYS_OF_THE_WEEK = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    0: "Saturday"
}


def zellers_algorithm(month: int, day: int, year: int, return_str = False):

    if month == 1 or month == 2:
        month = month + 12
        year = year - 1

    J = math.floor(year/100)
    K = year % 100

    day_of_the_week = (day 
                       + math.floor(13 * (month + 1) / 5) 
                       + K 
                       + math.floor(K / 4) 
                       + math.floor(J / 4) 
                       - 2 * J) % 7

    if return_str:
        return DAYS_OF_THE_WEEK[day_of_the_week]
    
    return day_of_the_week