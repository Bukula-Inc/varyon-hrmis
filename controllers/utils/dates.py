import calendar
from datetime import datetime, date, timedelta
import datetime as dt
from holidays import country_holidays

import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
from django.utils import timezone
class Dates:
    def __init__(self) -> None:
        pass



    def format_date_to_default(self, date_str):
        dt = str(date_str)
        try:
            date_obj = parser.parse(dt)
            return date_obj.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            return False


    def date_difference(self, date1, date2, date_format="%Y-%m-%d", unit="days", cd=False):
        """
        Calculate the difference between two dates in the specified unit.

        Args:
        - date1: The first date in string or datetime format.
        - date2: The second date in string or datetime format.
        - date_format (str): The format of the input dates. Default is "%Y-%m-%d".
        - unit (str): The unit for the difference ('days', 'months', or 'years').

        Returns:
        - int: The difference in the specified unit.
        """
        try:
            if isinstance(date1, str):
                date1 = datetime.strptime(date1, date_format)
            if isinstance(date2, str):
                date2 = datetime.strptime(date2, date_format)
        except ValueError as e:
            raise ValueError(f"Error parsing dates: {e}")

        delta = relativedelta(date2, date1)

        if unit.lower() == "days":
            return (date2 - date1).days
        elif unit.lower() == "months":
            total_months = delta.years * 12 + delta.months
            if cd:
                if date2.day < date1.day:
                    total_months -= 1
            return total_months
        elif unit.lower() == "years":
            return delta.years
        else:
            raise ValueError("Invalid unit. Choose 'days', 'months', or 'years'.")


    def today(self,return_date_object=False):
        date = datetime.now().strftime('%Y-%m-%d')
        if return_date_object:
            return self.string_to_date(date)
        return date

    def time(self):
        return dt.datetime.now().time()

    def time(self):
        current_time = dt.datetime.utcnow()
        return current_time.strftime("%H:%M:%S")
    
    def timestamp_to_full_date_time(self, tstmp):
        if tstmp:
            return dt.datetime.strptime(tstmp, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        return "-"
    
    def datestamp_to_full_date(self, tstmp):
        return dt.datetime.strptime(tstmp, '%Y%m%d').strftime('%Y-%m-%d')
    
    def unformated_date_timestamp(self):
        now = datetime.now()
        # Format the date and time as a string
        formatted_date = now.strftime("%Y%m%d%H%M%S")
        return formatted_date
    
    def add_minutes_to_time(self, time_str, minutes):
        current_time = dt.datetime.strptime(time_str, "%H:%M:%S")
        modified_time = current_time + dt.timedelta(minutes=10)
        updated = modified_time.strftime("%H:%M:%S")
        return  updated
    
    def get_current_year (self):
        return datetime.now().year
    
    def date_to_numeric(self, date_str):
        def ordinal_suffix(day):
            if 10 <= day % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
            return str(day) + suffix
        date_object = datetime.strptime(str(date_str), "%Y-%m-%d")
        formatted_date = ordinal_suffix(date_object.day) + " " + date_object.strftime("%b, %Y")
        return formatted_date
    
    def get_split_date(self):
        current_date = datetime.now()
        day = current_date.day
        month = current_date.month
        year = current_date.year
        return{
            "day":day if len(f"{day}") > 1 else f"0{day}",
            "month":month if len(f"{month}") > 1 else f"0{month}",
            "year":year,
            "time":self.time(),
            "timestamp":self.timestamp()
        }
        
    def timestamp(self):
        current_time = dt.datetime.utcnow()
        return current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def timestamp_without_colons(self, date_str=None):
        current_time = None
        if not date_str:
            current_time = dt.datetime.utcnow()
        else:
            input_date = dt.datetime.strptime(self.convert_date_to_YYYY_MM_DD(date_str), "%Y-%m-%d")
            input_date = input_date.replace(hour=0, minute=0, second=0)
            current_time = input_date
        return current_time.strftime("%Y%d%H%S")
    
    def timestamp_without_colons_for_smart_invoice(self, date_str=None):
        if not date_str:
            current_time = dt.datetime.utcnow()
        else:
            try:
                # Parse the input date string
                input_date = dt.datetime.strptime(date_str, "%Y-%m-%d")
                
                # Set the time to 00:00:00 if not provided
                input_date = input_date.replace(hour=0, minute=0, second=0)
                
                current_time = input_date
            except ValueError:
                raise ValueError("Invalid date format. Use 'yyyy-mm-dd'.")
        return current_time.strftime("%Y%m%d%H%M%S")
    
    def date_timestamp(self):
        current_time = dt.datetime.utcnow()
        return current_time.strftime("%Y%m%d")
    
    def hour_minute_second(self):
        current_time = dt.datetime.utcnow()
        return current_time.strftime("%H%M%S")
    
    def local_timestamp(self):
        current_time = datetime.utcnow()
        lusaka_time = current_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Africa/Lusaka'))
        return lusaka_time.strftime("%Y%m%d%H%M%S")
    
    def local_timestamp_starting_hour(self):
        current_time = datetime.utcnow()
        lusaka_time = current_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Africa/Lusaka'))
        stamp = f'{lusaka_time.strftime("%Y%m%d")}000000'
        return stamp

    def add_days(self, date, days_to_add, return_date_object=False):
        if isinstance(date, datetime):
            dt = date
        elif isinstance(date, str):
            dt = datetime.strptime(date, "%Y-%m-%d")
        else:
            raise ValueError("The 'date' parameter must be a string or a datetime object")
        new_date = dt + timedelta(days=days_to_add)
        final_date = new_date.strftime("%Y-%m-%d")
        if return_date_object:
            return self.string_to_date(final_date)
        return final_date

    def add_months(self, date, months):
        return

    def add_years(self, date, years):
        return
    
    def calculate_days(self,from_date,to_date):
        return (to_date - from_date).days
    
    def string_to_date(self,date_str):
        converted = datetime.strptime(date_str, "%Y-%m-%d").date()
        return converted
    
    def calculate_time_period(self, start_date, end_date):
        start_date =  datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        delta = end_date - start_date
        years = delta.days // 365
        remaining_days = delta.days % 365
        months = remaining_days // 30
        remaining_days = remaining_days % 30
        weeks = remaining_days // 7
        days = remaining_days % 7
        y_string = "Year" if years == 1 else "Years"
        m_string = "Month" if months == 1 else "Months"
        return f"{years} {y_string}, {months} {m_string}"
    
    def first_date_of_current_year(self):
        current_year = datetime.now().year
        first_date_of_year = datetime(current_year, 1, 1)
        return first_date_of_year
    
    def convert_time_to_24_hour_format(self, time_string):
        time_format = "%I:%M %p"
        input_time = datetime.strptime(time_string, time_format)
        output_time = input_time.strftime("%H:%M")

        return output_time
    
    def get_first_date_of_current_year(self):
        current_year = datetime.now().year
        first_date_of_year = datetime(current_year, 1, 1).strftime('%Y-%m-%d')
        return first_date_of_year
    
    def get_last_date_of_current_year(self):
        current_year = datetime.now().year
        last_date_of_year = datetime(current_year, 12, 31).strftime('%Y-%m-%d')
        return last_date_of_year
    
    def get_first_date_of_current_month(self):
        today = dt.date.today()
        return today.replace(day=1)
    

    def get_last_date_of_current_month(self):
        today = dt.date.today()
        return today.replace(day=calendar.monthrange(today.year, today.month)[1])

    def weeks_since (self, date, weeks):
        today = dt.date.today()
        delta = today - date
        return delta.days >= weeks * 7

    def days_since(self, date, days):
        today = dt.date.today()
        delta = today - date
        return delta.days >= days
    
    def days_between_two_dates(self,first_date, second_date):
        if not second_date:
            second_date = date.today()
        difference = second_date - first_date
        return abs(difference.days or 0)


    def years_since(self, date, years):
        today = dt.date.today()
        return (today.year - date.year) * 12 + (today.month - date.month) >= years * 12

    def months_since(self, date, months):
        today = dt.date.today()
        delta = today.year * 12 + today.month - (date.year * 12 + date.month)
        return delta >= months
    


    def is_first_day_of_current_month (self):
        today = dt.date.today()
        return today.day == 1
    
    def is_first_day_of_year(self):
        today = date.today()
        first_day_of_year = date(today.year, 1, 1)
        return today == first_day_of_year

    def _init_holidays (self, country):
        return self.generate_holidays (country)
        

    def generate_holidays(self, country):
        holidays = country_holidays(country, years=self.get_current_year ())
        holiday_dates = holiday_dates = [
            {
                'year': date.strftime('%Y'),
                'month': date.strftime('%B'),
                'day': date.strftime('%d'),
                "name_of_holiday": holiday,
                "date_formate": date,
            } for date, holiday in holidays.items()
        ]
        return holiday_dates
    
    def count_week_days(self, start_date: str, end_date: str, holidays:bool = False):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        def date_generator():
            while start <= end:
                yield start
                start += timedelta(days=1)
            holiday_dates = []
        if holidays:
            holiday_dates = [datetime.strptime(holiday, "%Y-%m-%d") for holiday in holidays]
        return sum (
            1 for date in date_generator()
            if date.weekday() not in [5, 6] and date not in holiday_dates
        )
    
    def get_human_word_date (self, date_string):
        if isinstance (date_string, str):
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
            return date_object.strftime("%d %B, %Y")
        else:
            return date_string.strftime("%d %B, %Y")

    def is_on_time (self, given_time: str, reverse: bool=False) -> bool:
        """
            Checks if the current time is less than or equal to the given time.
            given_time (str): to be convented Time in HH:MM format
            Args:
                Reverse (bool): change the mode of calculating 
            Returns:
                bool: True if current time is less than or equal to given time
        """
        given_time = datetime.datetime.strptime(given_time, "%H:%M").time()
        if reverse:
            return given_time <= self.time ()
        return self.time () <= given_time

    def days_in_month_as_weeks (self, year, month):
        cal = calendar.monthcalendar(year, month)
        weeks_format = []

        for week in cal:
            week_days = []
            for day in week:
                if day != 0:
                    week_days.append(day)
            weeks_format.append(week_days)

        return weeks_format
    
    def months_between(self, dt1, dt2):
        date1 = dt1
        date2 = dt2
        if isinstance (dt1, str):
            date1 = datetime.strptime(dt1, "%Y-%m-%d").date()
        if isinstance (dt2, str):
            date2 = datetime.strptime(dt2, "%Y-%m-%d").date()
        month_diff = (
            (date2.year - date1.year) * 12 +
            date2.month - date1.month -
            (date2.day < date1.day)
        )
        return month_diff
    


    def convert_seconds_to_time(self, execution_time):
        hours = int(execution_time // 3600)
        minutes = int((execution_time % 3600) // 60)
        seconds = int(execution_time % 60)
        milliseconds = int((execution_time % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    


    # financial reporting date utils
    def get_years_between_dates(self, start_date, end_date):
        start_year = datetime.strptime(start_date, "%Y-%m-%d").year
        end_year = datetime.strptime(end_date, "%Y-%m-%d").year
        return list(range(start_year, end_year + 1))
    

    # def get_current_and_last_year():
    #     current_year = date.today().year
    #     return [current_year, current_year - 1]


    def convert_date_to_YYYY_MM_DD(self, date_string):
        """
        Converts a date string in any format to YYYY-MM-DD.

        Args:
            date_string (str): The date string to convert.

        Returns:
            str: The date in YYYY-MM-DD format, or None if parsing fails.
        """
        date_formats = [
            "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y",
            "%d %B %Y", "%d %b %Y", "%B %d, %Y", "%b %d, %Y",
            "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M",
            "%d %B %Y %H:%M:%S", "%d %b %Y %H:%M:%S", "%B %d, %Y %H:%M:%S",
            "%d %B %Y %I:%M %p", "%d %b %Y %I:%M %p"
        ]

        for date_format in date_formats:
            try:
                date_obj = datetime.strptime(date_string, date_format)
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                pass  # Try the next format

        # If all formats fail, return None
        return None
