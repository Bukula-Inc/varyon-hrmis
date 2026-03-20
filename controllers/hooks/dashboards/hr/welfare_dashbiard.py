# from turtle import pd
from controllers.utils import Utils
from controllers.utils.dates import Dates
import pandas as pd
from controllers.core_functions.hr import Core_Hr

utils = Utils()
dates = Dates()

pp = utils.pretty_print
throw = utils.throw
class employee_welfare_dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.core_hr = Core_Hr(dbms=dbms)
        self.past_7_days = dates.add_days(dates.today(), -7)
        self.settings = dbms.system_settings

    @classmethod
    def welfare_dashboard(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        return utils.respond(utils.ok,{
            "get_welfare_applications":cls.welfare_applications(cls),
            "on_going_training_program":cls.on_going_training_programs(cls),
            "get_training_program_expenses": cls.get_training_program_expenses(cls),
            "get_training_program_expenses": cls.get_training_program_expenses(cls),
            "total_approved_rejceted": cls.total_approved_rejceted(cls),
            "participants": cls.participants(cls),
            "welfare_stats": cls.welfare_stats(cls)
        })


    def welfare_applications(self):
        get_welfare_applications = self.dbms.get_list("Employee_Welfare", filters={"created_on__gt": self.past_7_days})
        if get_welfare_applications.status == utils.ok:
            df = utils.to_data_frame(get_welfare_applications.data.rows)
            if not df.empty:
                required_columns = ['employee_name', 'welfare_type', 'welfare_expense', 'staff_covered_expense']
                available_columns = df.columns.tolist()
                missing_columns = [col for col in required_columns if col not in available_columns]
                
                if missing_columns:
                    return {"status": 422, "error_message": f"Missing columns: {missing_columns}"}
                
                result_df = df[required_columns]
                return result_df.to_dict(orient='records')
            else:
                return []
        else:
            return None
 
    def on_going_training_programs(self):
        training_program = self.dbms.get_list("Training_Program", filters = {"status__in": ["Submitted", "Approved"]})
        if training_program.status == utils.ok:
            df = utils.to_data_frame(training_program.data.rows)
            if not df.empty:
                name_counts = df['name'].value_counts().to_dict()
                return name_counts
            else:
                return {}
        else:
            return None
    def welfare_stats(self):
        get_welfares = self.dbms.get_list("Recovery_Of_Medical_Bills")
        total_employees = self.dbms.get_list("Employee", filters={"status": "Active"})

        if get_welfares.status == utils.ok and total_employees.status == utils.ok:
            df = utils.to_data_frame(get_welfares.data.rows)
            df_employees = utils.to_data_frame(total_employees.data.rows)

            if not df.empty:
                total_welfare = len(df)
                approved_programs = len(df[df['status'] == 'Approved'])
                rejected_programs = len(df[df['status'] == 'Rejected'])
                employees_participated = df['employee'].nunique()
                participation_rate = (employees_participated / len(df_employees)) * 100 if len(df_employees) > 0 else 0

                return {
                    'total_welfare': total_welfare,
                    'approved_programs': approved_programs,
                    'rejected_programs': rejected_programs,
                    'participation_rate': round(participation_rate, 2)
                }
            else:
                return {
                    'total_welfare': 0,
                    'approved_programs': 0,
                    'rejected_programs': 0,
                    'participation_rate': 0
                }
        else:
            return None

    def get_training_program_expenses(self):
        training_program_expenses = self.dbms.get_list("Program_Expense", filters = {"status__in": ["Submitted", "Approved"]})
        if training_program_expenses.status == utils.ok:
            df = utils.to_data_frame(training_program_expenses.data.rows)
            df['created_on'] = pd.to_datetime(df['created_on'])
            df['quarter'] = df['created_on'].dt.quarter
            df['year'] = df['created_on'].dt.year

            quarterly_expenses = {
                'first_quarter': df[df['quarter'] == 1]['amount'].sum(),
                'second_quarter': df[df['quarter'] == 2]['amount'].sum(),
                'third_quarter': df[df['quarter'] == 3]['amount'].sum(),
                'fourth_quarter': df[df['quarter'] == 4]['amount'].sum(),
            }

            yearly_expenses = df['amount'].sum()

            return {
                'quarterly_expenses': quarterly_expenses,
                'yearly_expenses': yearly_expenses
            }
        else:
            return None
    def total_approved_rejceted(self):
        training_program_expenses = self.dbms.get_list("Program_Expense")
        if training_program_expenses.status == utils.ok:
            df = utils.to_data_frame(training_program_expenses.data.rows)
            total_approved = df[df['status'] == 'Approved']['amount'].sum()
            total_rejected = df[df['status'] == 'Rejected']['amount'].sum()

            return {
                'total_approved': total_approved,
                'total_rejected': total_rejected
            }
        else:
            return None
    def participants(self):
        attendees = self.dbms.get_list("Attendee") 
        employees = self.dbms.get_list("Employee", filters={"status": "Active"}) 
        if attendees.status == utils.ok and employees.status == utils.ok:
            df_attendees = utils.to_data_frame(attendees.data.rows)
            df_employees = utils.to_data_frame(employees.data.rows)
            unique_attendees = df_attendees['employee'].unique()
            total_participants = len(unique_attendees)
            never_participated = df_employees[~df_employees['name'].isin(unique_attendees)]
            num_never_participated = len(never_participated)
            num_not_in_attendees = len(df_employees) - total_participants
            return {
                'ytd_total_participants': total_participants,
                'ytd_num_never_participated': num_never_participated,
                'ytd_num_not_in_attendees': num_not_in_attendees
            }
        else:
            return None
