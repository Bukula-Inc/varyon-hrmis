import pandas as pd
from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils ()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

class HR_Analytics:
    def __init__(self,dbms,object=None):
        self.dbms = dbms
        self.object = object

    def group_leave_by_type(self, data):
        df = utils.to_data_frame(data)
        df["total_days"] = pd.to_numeric(df["total_days"])
        df["used_leave_days"] = pd.to_numeric(df["used_leave_days"])
        df["remaining_leave_days"] = pd.to_numeric(df["remaining_leave_days"])
        df["leave_days_in_working_hours"] = pd.to_numeric(df["leave_days_in_working_hours"])

        grouped_data = df.groupby('leave_type').agg(
            total_days=('total_days', 'sum'),
            used_days=('used_leave_days', 'sum'),
            remaining_days=('remaining_leave_days', 'sum'),
            leave_days_in_working_hours=('leave_days_in_working_hours', 'sum'),
        )
        leave_type_details = grouped_data.to_dict(orient='index')
        leave_type_details["overall_totals"] = {
            'total_days': int(grouped_data['total_days'].sum()),
            'used_days': int(grouped_data['used_days'].sum()),
            'remaining_days': int(grouped_data['remaining_days'].sum()),
            'leave_days_in_working_hours': int(grouped_data['leave_days_in_working_hours'].sum())
        }
        return utils.respond(utils.ok, leave_type_details)

    def group_work_plan(self, data):
        df = utils.to_data_frame(data)
        df['created_on'] = pd.to_datetime(df['created_on'], errors='coerce')
        if df['created_on'].isnull().any():
            print("Warning: Some 'created_on' values couldn't be converted to datetime.")
        df['expected_end_date'] = pd.to_datetime(df['expected_end_date'], errors='coerce')
        df['quarter'] = df['created_on'].dt.to_period('Q').astype(str)
        df['Delayed'] = (df['progress_tracker'] == 'Completed') & (df['completed_on'].notna()) & (pd.to_datetime(df['completed_on']) > df['expected_end_date'])
        df['OnTime'] = (df['progress_tracker'] == 'Completed') & (df['completed_on'].notna()) & (pd.to_datetime(df['completed_on']) <= df['expected_end_date'])
        df['Need Some More Time'] = (df['progress_tracker'] != 'Completed') & (df['progress_tracker'] != 'Pending')
        df['Completed'] = df['progress_tracker'] == 'Completed'
        df['Pending'] = df['progress_tracker'] == 'Pending'
        result = df.groupby('quarter').agg({
            'Pending': 'sum',
            'Completed': 'sum',
            'Need Some More Time': 'sum',
            'Delayed': 'sum',
            'OnTime': 'sum'
        }).reset_index().to_dict(orient='records')
        if result:
            return utils.respond(utils.ok, result)
        return utils.respond(utils.unprocessable_entity, "Failed to Analyze")

    def groupbyEmp (self, data):
        df = utils.to_data_frame(data)
        df['adjusted'] = df['progress_tracker'] == 'Need Some More Time'
        df['completed'] = df['progress_tracker'] == 'Completed'
        df['pending'] = df['progress_tracker'] == 'Pending'
        df['in_progress'] = df['progress_tracker'] == 'In Progress'
        by_emp = df.groupby ("planer_of_work_plan").agg ({
            'pending': 'sum',
            'completed': 'sum',
            'adjusted': 'sum',
            'in_progress': 'sum',
            }).reset_index().to_dict(orient='records')

        return utils.from_dict_to_object ({
            "by_emp": by_emp,
        })

    def group_leave_applications_by_status(self, data, only_totals=False):
        df = utils.to_data_frame(data)
        grouped_dict = None
        if only_totals:
            grouped_dict = df.groupby('status').size().to_dict()
        else:
            grouped_dict = df.groupby('status').apply(lambda group: group.to_dict(orient='records')).to_dict()
        return utils.respond(utils.ok, grouped_dict)

    def group_employees_by_department(self, data, only_totals=False):
        df = utils.to_data_frame(data)
        grouped_dict = None
        if only_totals:
            grouped_dict = df.groupby('department').size().to_dict()
        else:
            grouped_dict = df.groupby('department').apply(lambda group: group.to_dict(orient='records')).to_dict()
        return utils.respond(utils.ok, grouped_dict)
    

    def group_employees_by_designation(self, data, only_totals=False):
        df = utils.to_data_frame(data)
        grouped_dict = None
        if only_totals:
            grouped_dict = df.groupby('designation').size().to_dict()
        else:
            grouped_dict = df.groupby('designation').apply(lambda group: group.to_dict(orient='records')).to_dict()
        return utils.respond(utils.ok, grouped_dict)
    

    def group_employees_by_employment_type(self, data, only_totals=False):
        df = utils.to_data_frame(data)
        grouped_dict = None
        if only_totals:
            grouped_dict = df.groupby('employment_type').size().to_dict()
        else:
            grouped_dict = df.groupby('employment_type').apply(lambda group: group.to_dict(orient='records')).to_dict()
        return utils.respond(utils.ok, grouped_dict)
    

    def group_employees_by_gender(self, data, only_totals=False):
        df = utils.to_data_frame(data)
        grouped_dict = None
        if only_totals:
            grouped_dict = df.groupby('gender').size().to_dict()
        else:
            grouped_dict = df.groupby('gender').apply(lambda group: group.to_dict(orient='records')).to_dict()
        return utils.respond(utils.ok, grouped_dict)
    

    def group_employees_by_status(self, data, only_totals=False):
        df = utils.to_data_frame(data)
        grouped_dict = None
        if only_totals:
            grouped_dict = df.groupby('status').size().to_dict()
        else:
            grouped_dict = df.groupby('status').apply(lambda group: group.to_dict(orient='records')).to_dict()
        return utils.respond(utils.ok, grouped_dict)
    