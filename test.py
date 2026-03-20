# # # import smtplib
# # # from email.message import EmailMessage

# # # def send_email(subject, body, to_email, from_email, password, smtp_server='mail.exams-council.org.zm', smtp_port=587):
# # #     msg = EmailMessage()
# # #     msg['Subject'] = subject
# # #     msg['From'] = from_email
# # #     msg['To'] = to_email
# # #     msg.set_content(body)

# # #     try:
# # #         with smtplib.SMTP(smtp_server, smtp_port) as server:
# # #             server.starttls()
# # #             server.login(from_email, password)
# # #             server.send_message(msg)
# # #             print("✅ Email sent successfully.")
# # #     except Exception as e:
# # #         print(f"❌ Failed to send email: {e}")

# # # # === Demo Email ===
# # # if __name__ == "__main__":
# # #     subject = "566666666666 Email from Python"
# # #     body = "Hello!\n\nThis is a test email sent using Python.\n\nBest regards,\nPython Script"
# # #     # to_email = "eczbright@gmail.com"
# # #     to_email = "bright@startappsolutions.com"
# # #     from_email = "hradmin@exams-council.org.zm"
# # #     password = "12345@abc"

# # #     send_email(subject, body, to_email, from_email, password)

# # le = 10
# # for i in range (le):
# #     print (f"\n\n\n {i} \n\n\n")

# from datetime import datetime, date
# from dateutil.relativedelta import relativedelta

# def parse_date(d):
#     """Helper to parse date/datetime objects from strings."""
#     if isinstance(d, (date, datetime)):
#         return datetime.combine(d, datetime.min.time()) if isinstance(d, date) and not isinstance(d, datetime) else d
#     # Try parsing date/time string
#     for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
#         try:
#             return datetime.strptime(d, fmt)
#         except ValueError:
#             continue
#     raise ValueError(f"Unsupported date format: {d}")

# def date_diff(d1, d2, unit='days'):
#     """
#     Return the difference between two dates in the specified unit.

#     Args:
#         d1, d2: date, datetime, or string ('YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS')
#         unit: 'days', 'hours', 'months', or 'years'

#     Returns:
#         Difference as float (for days/hours), or int (for months/years)
#     """
#     d1 = parse_date(d1)
#     d2 = parse_date(d2)

#     if unit == 'days':
#         delta = d1 - d2
#         return delta.total_seconds() / 86400  # 86400 seconds in a day

#     elif unit == 'hours':
#         delta = d1 - d2
#         return delta.total_seconds() / 3600  # 3600 seconds in an hour

#     elif unit == 'months':
#         diff = relativedelta(d1, d2)
#         return diff.years * 12 + diff.months

#     elif unit == 'years':
#         diff = relativedelta(d1, d2)
#         return diff.years

#     else:
#         raise ValueError("Unit must be one of: 'days', 'hours', 'months', or 'years'")
# print(date_diff("2025-09-23", "2024-09-23", unit='years'))     # 1
# print(date_diff("2025-09-23", "2024-06-23", unit='months'))    # 15
# print(date_diff("2025-09-23", "2025-09-01", unit='days'))      # 22.0
# print(date_diff("2025-09-23 12:00:00", "2025-09-22 00:00:00", unit='hours'))  # 36.0

# num = -2000
# positive_num = abs(num)
# print(positive_num)
from datetime import datetime

def get_date_part(date_str, part, human_readable=True):
    d = datetime.strptime(date_str, "%Y-%m-%d")

    match part:
        case "year":
            return d.year
        case "month":
            return d.strftime("%B") if human_readable else d.month
        case "day":
            return d.day
        case _:
            return None

# Example usage
print(get_date_part("2025-12-20", "year"))                 # 2025
print(get_date_part("2025-12-20", "month"))                # December
print(get_date_part("2025-12-20", "month", False))         # 12
print(get_date_part("2025-12-20", "day"))                  # 20
