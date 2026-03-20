from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr
import pandas as pd
from datetime import datetime
from controllers.mailing import Mailing

utils = Utils()
dates = Dates()

pp = utils.pretty_print
throw = utils.throw

class Employee_Controller:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.core_hr = Core_Hr (dbms)
        self.mailing = Mailing (dbms)

    @classmethod
    def init_birth_day (cls, dbms, object):
        instance = cls (dbms, object)
        try:
            employee_lst = instance.core_hr.get_list ("Employee", filters={"status__in": ["Active", "Suspended", "On Leave"]})
            emp_df = utils.to_data_frame (employee_lst)

            now = pd.Timestamp.now()
            last_7_days = now - pd.Timedelta(days=7)

            emp_df["d_o_b"] = pd.to_datetime(emp_df["d_o_b"], errors="coerce")
            emp_lst = emp_df[
                (emp_df["d_o_b"].dt.month == now.month)
            ].to_dict (orient="records")

            for emp in emp_lst:
                if DataConversion.is_today (DataConversion.safe_get (emp, "d_o_b")):
                    # send email
                    full_name = DataConversion.safe_get (emp, 'full_name', f'{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}')
                    instance.mailing.send_mail (recipient=[], subject="Birth Greetings", body=f"""
                        <!DOCTYPE html>
                        <html lang='en'>
                            <head>
                                <meta charset='UTF-8' />
                                <meta name='viewport' content='width=device-width, initial-scale=1.0' />
                                <title>Birthday Greetings</title>
                            </head>

                            <body style='margin:0;padding:0;background-color:#f1f5f9;'>
                                <table width='100%' cellpadding='0' cellspacing='0' role='presentation'>
                                    <tr>
                                        <td align='center' style='padding:40px 16px;'>

                                        <!-- Card -->
                                            <table
                                                width='100%'
                                                cellpadding='0'
                                                cellspacing='0'
                                                role='presentation'
                                                style='
                                                max-width:520px;
                                                background-color:#ffffff;
                                                border-radius:12px;
                                                box-shadow:0 8px 20px rgba(0,0,0,0.06);
                                                overflow:hidden;
                                                text-align:center;
                                            '>

                                                <tr>
                                                    <td
                                                        style='
                                                        background-color:#0f766e;
                                                        padding:32px 24px;
                                                        '>
                                                        <h1
                                                        style='
                                                            margin:0;
                                                            font-family:Arial,Helvetica,sans-serif;
                                                            font-size:24px;
                                                            color:#ffffff;
                                                            font-weight:600;
                                                            letter-spacing:0.3px;
                                                        '>
                                                        Birthday Greetings
                                                        </h1>
                                                    </td>
                                                </tr>

                                                <tr>
                                                    <td
                                                        style='
                                                        padding:36px 32px;
                                                        font-family:Arial,Helvetica,sans-serif;
                                                        color:#374151;
                                                        '>

                                                        <p style='font-size:16px;margin:0 0 16px;'>
                                                        Dear <strong>{full_name}</strong>,
                                                        </p>

                                                        <p
                                                        style='
                                                            font-size:15px;
                                                            line-height:24px;
                                                            margin:0 0 16px;
                                                            color:#4b5563;
                                                        '>
                                                        On behalf of the Examinations Council of Zambia, we are pleased
                                                        to extend our warmest birthday wishes to you.
                                                        </p>

                                                        <p
                                                        style='
                                                            font-size:15px;
                                                            line-height:24px;
                                                            margin:0;
                                                            color:#4b5563;
                                                        '>
                                                        May the year ahead bring you good health, continued success,
                                                        and personal fulfillment.
                                                        </p>

                                                    </td>
                                                </tr>

                                                <!-- Divider -->
                                                <tr>
                                                    <td style='padding:0 32px;'>
                                                        <div style='height:1px;background-color:#e5e7eb;'></div>
                                                    </td>
                                                </tr>

                                                <!-- Footer -->
                                                <tr>
                                                    <td
                                                        style='
                                                        padding:24px;
                                                        font-family:Arial,Helvetica,sans-serif;
                                                        font-size:13px;
                                                        color:#6b7280;
                                                        text-align:center;
                                                        '>
                                                        Yours sincerely,<br />
                                                        <strong>Examinations Council of Zambia</strong>
                                                    </td>
                                                </tr>

                                            </table>

                                        </td>
                                    </tr>
                                </table>
                            </body>
                        </html>
                    """)
        except Exception as e:
            pp (f"ERROR: {e}")
            pass