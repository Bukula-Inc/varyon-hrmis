import re
from datetime import datetime, date, timedelta
import calendar
from math import floor
import numpy as np
from controllers.utils import Utils
from controllers.utils.dates import Dates
import html
from dateutil.relativedelta import relativedelta


utils = Utils ()
dates = Dates ()


class DataConversion:
    @staticmethod
    def convert_to_positive (val):
        """
        Converts negative numbers to positive.
        """
        val = DataConversion.convert_to_float (val)
        return abs (val)
    
    @staticmethod
    def convert_to_negative (val):
        """
        Converts positive numbers to negative.
        """
        val = DataConversion.convert_to_float (val)
        return -abs (val)
    
    @staticmethod
    def map_to_current_year(date_input):
        """
        Converts a datetime/date/string to the same month/day/time in the current year.
        """
        try:
            # Step 1: Normalize to datetime
            if isinstance(date_input, str):
                try:
                    parsed = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    parsed = datetime.strptime(date_input, "%Y-%m-%d")
            elif isinstance(date_input, datetime):
                parsed = date_input
            elif isinstance(date_input, date):
                # Convert date to datetime with time 00:00:00
                parsed = datetime.combine(date_input, datetime.min.time())
            else:
                return f"Unsupported input type: {type(date_input)}"

            # Step 2: Replace year with current year
            current_year = datetime.now().year
            new_date = parsed.replace(year=current_year)

            return new_date

        except ValueError as e:
            return f"Error: {e}"
    
    @staticmethod
    def get_weekends (date_str: str):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        day_name = date.strftime("%A")
        if date.weekday() == 5 or date.weekday() == 6:
            return True, day_name
        return False, day_name

    @staticmethod
    def divide_current_month_portions(portions):
        if not isinstance(portions, (int, float)) or portions <= 0:
            raise ValueError("Portions must be a positive number (int or float)")

        today = datetime.today()
        year = today.year
        month = today.month

        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])
        total_days = (last_day - first_day).days + 1

        n = floor(portions)
        step = total_days / portions

        date_ranges = []
        current_day_index = 0.0

        for i in range(n):
            start_index = floor(current_day_index)
            end_index = floor(current_day_index + step) - 1

            if end_index >= total_days:
                end_index = total_days - 1

            start_date = first_day + timedelta(days=start_index)
            end_date = first_day + timedelta(days=end_index)
            date_ranges.append((start_date.date(), end_date.date()))

            current_day_index += step
        return date_ranges


    @staticmethod
    def remove_NaN_and_None (list_, replace_with=""):
        df = utils.to_data_frame (list_)
        df = df.replace({np.nan: replace_with, None: replace_with})
        return_data = df.to_dict(orient="records")
        return return_data


    @staticmethod
    def parse_date(date_str):
        try:
            if isinstance(date_str, datetime):
                return date_str.date()
            elif isinstance(date_str, str):
                return datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return datetime.today().date()
    
    @staticmethod
    def is_number(value):
        """
        Check if a value is a number.
        """
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def convert_to_float(value):
        if value is None:
            return 0.0

        try:
            if isinstance(value, str):
                value = re.sub(r"[^\d.,\-]", "", value)
                value = value.replace(",", "")
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def convert_to_int(value):
        if value is None:
            return 0

        try:
            if isinstance(value, str):
                value = re.sub(r"[^\d\.\-]", "", value)
            return int(float(value))
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def safe_get(dictionary, key, default=None):
        """
            Safely retrieve a value from a dictionary.
            Args:
                dictionary (dict): The dictionary to retrieve from.
                key: The key to look for.
                default: The value to return if the key is not found or dictionary is invalid.
            Returns:
                The value from the dictionary, or the default if key is missing or error occurs.
        """
        if not isinstance(dictionary, dict):
            return default
        return dictionary.get(key, default)

    @staticmethod
    def safe_set(dictionary, key, value):
        """
            Safely set a key-value pair in a dictionary.

            Args:
                dictionary (dict): The dictionary to update.
                key: The key to set.
                value: The value to assign.

            Returns:
                dict: The updated dictionary. If input is not a dict, returns a new one with the key-value.
        """
        if not isinstance(dictionary, dict):
            dictionary = {}
        dictionary[key] = value
        return dictionary

    @staticmethod
    def safe_gt(a, b, datatype):
        """
            Safe greater than (a > b) comparison with datatype checking and fallback.

            Args:
                a: First value to compare.
                b: Second value to compare.
                datatype: Expected type for a and b (e.g., int, float, str).

            Returns:
                bool: True if a > b, False otherwise or on error.
        """
        try:
            if isinstance(a, datatype) and isinstance(b, datatype):
                return a > b
            try:
                a_converted = datatype(a)
                b_converted = datatype(b)
                return a_converted > b_converted
            except (ValueError, TypeError):
                pass
        except Exception:
            return False

    @staticmethod
    def safe_le(a, b, datatype):
        """
            Safe greater than (a <= b) comparison with datatype checking and fallback.

            Args:
                a: First value to compare.
                b: Second value to compare.
                datatype: Expected type for a and b (e.g., int, float, str).

            Returns:
                bool: True if a < b, False otherwise or on error.
        """
        try:
            if isinstance(a, datatype) and isinstance(b, datatype):
                return a <= b

            try:
                a_converted = datatype(a)
                b_converted = datatype(b)
                return a_converted <= b_converted
            except (ValueError, TypeError):
                pass
        except Exception:
            return False

    @staticmethod
    def safe_lt(a, b, datatype):
        """
            Safe greater than (a > b) comparison with datatype checking and fallback.

            Args:
                a: First value to compare.
                b: Second value to compare.
                datatype: Expected type for a and b (e.g., int, float, str).

            Returns:
                bool: True if a > b, False otherwise or on error.
        """
        try:
            if isinstance(a, datatype) and isinstance(b, datatype):
                return a < b

            try:
                a_converted = datatype(a)
                b_converted = datatype(b)
                return a_converted < b_converted
            except (ValueError, TypeError):
                pass
        except Exception:
            return False

    @staticmethod
    def safe_ge(a, b, datatype):
        """
            Safe greater than (a >= b) comparison with datatype checking and fallback.

            Args:
                a: First value to compare.
                b: Second value to compare.
                datatype: Expected type for a and b (e.g., int, float, str).

            Returns:
                bool: True if a > b, False otherwise or on error.
        """
        try:
            if isinstance(a, datatype) and isinstance(b, datatype):
                return a >= b

            try:
                a_converted = datatype(a)
                b_converted = datatype(b)
                return a_converted >= b_converted
            except (ValueError, TypeError):
                pass
        except Exception:
            return False

    @staticmethod
    def safe_e(a, b, datatype, to_lower=False):
        """
            Safe greater than (a > b) comparison with datatype checking and fallback.

            Args:
                a: First value to compare.
                b: Second value to compare.
                datatype: Expected type for a and b (e.g., int, float, str).

            Returns:
                bool: True if a > b, False otherwise or on error.
        """
        try:
            if isinstance(a, datatype) and isinstance(b, datatype):
                if to_lower:
                    return str (a).lower () == str (b).lower ()
                return a == b

            try:
                a_converted = datatype(a)
                b_converted = datatype(b)
                if to_lower:
                    str (a_converted).lower () == str (b_converted).lower ()
                return a_converted == b_converted
            except (ValueError, TypeError):
                pass
        except Exception:
            return False

    @staticmethod
    def safe_n(a, b, datatype):
        """
            Safe greater than (a > b) comparison with datatype checking and fallback.

            Args:
                a: First value to compare.
                b: Second value to compare.
                datatype: Expected type for a and b (e.g., int, float, str).

            Returns:
                bool: True if a > b, False otherwise or on error.
        """
        try:
            if isinstance(a, datatype) and isinstance(b, datatype):
                return a != b

            try:
                a_converted = datatype(a)
                b_converted = datatype(b)
                return a_converted != b_converted
            except (ValueError, TypeError):
                pass
        except Exception:
            return False

    @staticmethod
    def is_today (input_date):
        """
        Checks if the given date is today's date.

        Args:
            input_date (str | date | datetime): The date to check.

        Returns:
            bool: True if the date is today, False otherwise.
        """
        try:
            if isinstance(input_date, str):
                for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
                    try:
                        input_date = datetime.strptime(input_date, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    return False

            elif isinstance(input_date, datetime):
                input_date = input_date.date()

            elif not isinstance(input_date, date):
                return False

            return input_date == date.today()

        except Exception:
            return False

    @staticmethod
    def is_past_date(input_date):
        """
        Checks if the given date is earlier than today.

        Args:
            input_date (str | date | datetime): The date to check.

        Returns:
            bool: True if the date is before today, False otherwise.
        """
        try:
            if isinstance(input_date, str):
                for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
                    try:
                        input_date = datetime.strptime(input_date, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    return False

            elif isinstance(input_date, datetime):
                input_date = input_date.date()

            elif not isinstance(input_date, date):
                return False

            return input_date < date.today()

        except Exception:
            return False

    @staticmethod
    def is_future_date(input_date):
        """
        Checks if the given date is after today.

        Args:
            input_date (str | date | datetime): The date to check.

        Returns:
            bool: True if the date is after today, False otherwise.
        """
        try:
            if isinstance(input_date, str):
                for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
                    try:
                        input_date = datetime.strptime(input_date, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    return False

            elif isinstance(input_date, datetime):
                input_date = input_date.date()

            elif not isinstance(input_date, date):
                return False

            return input_date > date.today()

        except Exception:
            return False

    @staticmethod
    def find_index (lst, value):
        """
        Returns the index of the given value in the list.
        If the value is not found, returns -1.
        """
        try:
            return lst.index(value)
        except ValueError:
            return -1

    @staticmethod
    def convert_to_datetime(date_input):
        """
        Converts:
        - ISO format string ('YYYY-MM-DD') -> datetime object
        - datetime/date object -> ISO string
        - None -> None
        """
        if date_input is None:
            return None

        if isinstance(date_input, str):
            try:
                return datetime.strptime(date_input, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Invalid date string format: {date_input}. Expected 'YYYY-MM-DD'.")

        elif isinstance(date_input, (datetime, date)):
            return date_input.strftime('%Y-%m-%d')

        else:
            raise TypeError(f"Unsupported type for date conversion: {type(date_input)}")

    @staticmethod
    def convert_datetime_to_string(dt, fmt="%Y-%m-%d %H:%M:%S"):
        """
        Convert a datetime object to a string.

        Args:
            dt (datetime | date | str): The datetime to format.
            fmt (str): Format string to use for conversion.

        Returns:
            str: The formatted datetime string, or empty string on failure.
        """
        if isinstance(dt, str):
            return dt
        try:
            if isinstance(dt, date) and not isinstance(dt, datetime):
                dt = datetime.combine(dt, datetime.min.time())
            return dt.strftime(fmt)
        except Exception:
            return ""

    @staticmethod
    def get_year_bounds():
        current_year = date.today().year
        first_day = date(current_year, 1, 1)
        last_day = date(current_year, 12, 31)
        return first_day, last_day

    @staticmethod
    def get_previous_month_range(reference_date=None, return_as='date'):
        """
        Returns the first and last day of the previous month.

        Parameters:
            reference_date (datetime): Optional reference date (default: today)
            return_as (str): 'date' for datetime.date, 'string' for 'YYYY-MM-DD'

        Returns:
            tuple: (first_day, last_day) as either date or string
        """
        print (reference_date)
        if reference_date is None:
            reference_date = datetime.today()
        else:
            if isinstance (reference_date, str):
                reference_date = DataConversion.convert_to_datetime (reference_date)

        first_day_this_month = reference_date.replace(day=1)
        last_day_previous_month = first_day_this_month - timedelta(days=1)
        first_day_previous_month = last_day_previous_month.replace(day=1)

        if return_as == 'string':
            return (
                DataConversion.convert_datetime_to_string (first_day_previous_month, '%Y-%m-%d'),
                DataConversion.convert_datetime_to_string (last_day_previous_month, '%Y-%m-%d'),
            )

        return (
            first_day_previous_month.date(),
            last_day_previous_month.date()
        )

    @staticmethod
    def safe_list_append(lst, item):
        """
        Safely append an item to a list.

        Args:
            lst (list): The list to append to.
            item: The item to append.

        Returns:
            list: The updated list. If input is not a list, returns a new list with the item.
        """
        if not isinstance(lst, list):
            lst = []
        lst.append(item)
        return lst

    @staticmethod
    def safe_list_get(lst, index, default=None):
        """
        Safely get an item from a list by index.

        Args:
            lst (list): The list to access.
            index (int): The index to retrieve.
            default: The value to return if index is out of bounds or input is not a list.

        Returns:
            The item at index or default.
        """
        try:
            if isinstance(lst, list):
                return lst[index]
        except (IndexError, TypeError):
            pass
        return default
    
    @staticmethod
    def safe_list_remove(lst, item):
        """
        Safely remove an item from a list.

        Args:
            lst (list): The list to modify.
            item: The item to remove.

        Returns:
            list: The updated list. If input is not a list or item not in list, returns original list.
        """
        if isinstance(lst, list):
            try:
                lst.remove(item)
            except ValueError:
                pass
        return lst if isinstance(lst, list) else []

    @staticmethod
    def contains_html_chars(text):
        """
        Check if a string contains HTML entities like &amp;, &lt;, etc.

        Args:
            text (str): The input text.

        Returns:
            bool: True if HTML entities are found, else False.
        """
        if not isinstance(text, str):
            return False
        return html.unescape(text) != text

    @staticmethod
    def contains_special_chars(text):
        """
        Check if a string contains special characters.

        Args:
            text (str): The input text.

        Returns:
            bool: True if special characters are found, else False.
        """
        if not isinstance(text, str):
            return False
        return bool(re.search(r"[^a-zA-Z0-9\s]", text))

    @staticmethod
    def remove_special_chars(text):
        """
        Remove all special characters from a string (keeps letters, numbers, and spaces).

        Args:
            text (str): The input string.

        Returns:
            str: Cleaned string.
        """
        if not isinstance(text, str):
            return ""
        return re.sub(r"[^a-zA-Z0-9\s]", "", text)

    @staticmethod
    def find_and_replace_special_chars(text, replacement="_"):
        """
        Replace all special characters in a string with the given replacement.

        Args:
            text (str): The input string.
            replacement (str): The replacement character.

        Returns:
            str: Modified string.
        """
        if not isinstance(text, str):
            return ""
        return re.sub(r"[^a-zA-Z0-9\s]", replacement, text)

    @staticmethod
    def replace_all(text, find_str, replace_str):
        """
        Replace all occurrences of a substring with another.

        Args:
            text (str): Original string.
            find_str (str): Substring to find.
            replace_str (str): Replacement string.

        Returns:
            str: Modified string.
        """
        if not isinstance(text, str):
            return ""
        return text.replace(find_str, replace_str)

    @staticmethod
    def evaluate_expression(template: str, values: dict):
        expression = template.replace('%', '/').replace('x', '*')
        placeholders = re.findall(r'{(.*?)}', expression)
        for key in placeholders:
            if key not in values:
                raise ValueError(f"Missing value for placeholder: {key}")
            expression = expression.replace(f'{{{key}}}', str(values[key]))

        try:
            result = eval(expression)
            return result
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {expression}") from e
        
    @staticmethod
    def _parse_date_for_diff(d):
        """
        Internal helper to parse date or datetime from string, date, or datetime.
        """
        if isinstance(d, (datetime, date)):
            return datetime.combine(d, datetime.min.time()) if isinstance(d, date) and not isinstance(d, datetime) else d
        if isinstance(d, str):
            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
                try:
                    return datetime.strptime(d, fmt)
                except ValueError:
                    continue
        raise ValueError(f"Unsupported date format: {d}")

    @staticmethod
    def date_diff(d1, d2, unit:str='days'):
        """
        Return the difference between two dates in the specified unit.

        Args:
            d1, d2: str, date, or datetime
            unit: 'days', 'hours', 'months', or 'years'

        Returns:
            float or int: Difference in specified unit
        """
        unit = unit.lower ()
        d1 = DataConversion._parse_date_for_diff(d1)
        d2 = DataConversion._parse_date_for_diff(d2)

        if unit == 'days':
            return (d1 - d2).total_seconds() / 86400
        elif unit == 'hours':
            return (d1 - d2).total_seconds() / 3600
        elif unit == 'months':
            diff = relativedelta(d1, d2)
            return diff.years * 12 + diff.months
        elif unit == 'years':
            diff = relativedelta(d1, d2)
            return diff.years
        else:
            raise ValueError("Unit must be one of: 'days', 'hours', 'months', 'years'")

    @staticmethod
    def get_date_part(date_str=None, part: str="", human_readable=True):

        if not date_str:
            date_str = dates.today ()

        d = datetime.strptime(date_str, "%Y-%m-%d")
        match part.lower ():
            case "year":
                return d.year
            case "month":
                return d.strftime("%B") if human_readable else d.month
            case "day":
                return d.day
            case _:
                return f"{d.strftime("%B")} {d.year}"