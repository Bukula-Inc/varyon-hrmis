import pandas as pd
from datetime import datetime, timedelta
from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class HR_Recruitment_Analytics:
    def __init__(self, dbms, object=None):
        self.dbms = dbms
        self.object = object

    def get_employee_metrics(self, data):
        df = utils.to_data_frame(data)
        total = len(df)
        type_metrics = {}
        active_count = len(df[df['status'] == 'Active'])
        terminated_count = len(df[df['status'] == 'Terminated'])
        retired_count = len(df[df['status'] == 'Retired'])
        resigned_count = len(df[df['status'] == 'Resigned'])

        filtered_df = df[df['employment_type'].notna()]
        if filtered_df['employment_type'].nunique() > 0:
            types = filtered_df['employment_type'].unique()
            type_metrics = {}
            for e_type in types:
                type_metrics[e_type] = len(filtered_df[filtered_df['employment_type'] == e_type])

        # Calculate duration-based metrics for active employees
        # active_employees = df[df['status'] == 'Active']
        # current_date = datetime.now()

        # # Employees who have been in the company for more than 1 year but less than 2 years
        # one_year = len(active_employees[(active_employees['date_of_joining'] <= current_date - timedelta(days=365)) & 
        #                                 (active_employees['date_of_joining'] > current_date - timedelta(days=2*365))])

        # # Employees who have been in the company for more than 2 years but less than 3 years
        # two_year = len(active_employees[(active_employees['date_of_joining'] <= current_date - timedelta(days=2*365)) & 
        #                                 (active_employees['date_of_joining'] > current_date - timedelta(days=3*365))])

        # # Employees who have been in the company for more than 3 years
        # three_year_plus = len(active_employees[active_employees['date_of_joining'] <= current_date - timedelta(days=3*365)])

        return utils.respond(utils.ok, {
            'total': total,
            'active': active_count,
            'terminated': terminated_count,
            'retired': retired_count,
            'resigned': resigned_count,
            'type_metrics': type_metrics,
            # 'one_year': one_year,
            # 'two_year': two_year,
            # 'three_year_plus': three_year_plus
        })

    def staff_planning(self, data):
        df = utils.to_data_frame(data)
        total = len(df)
        draft_count = len(df[df['status'] == 'Draft'])
        submitted_count = len(df[df['status'] == 'Submitted'])
        active_count = len(df[df['status'] == 'Active'])

        departments = df['department'].unique()
        department_metrics = {}

        for dept in departments:
            department_metrics[dept] = len(df[df['department'] == dept])

        return utils.respond(utils.ok, {
            'total': total,
            'draft': draft_count,
            'submitted': submitted_count,
            'active': active_count,
            'department_metrics': department_metrics
        })

    def staffing(self, data):
        df = utils.to_data_frame(data)
        df["vacancies"] = df["vacancies"].astype(int)
        df["total_cost"] = df["total_cost"].astype(float)
        total_vacancies = df['vacancies'].sum()
        designations = df['designation'].unique()
        designation_metrics = {}

        for designation in designations:
            designation_df = df[df['designation'] == designation]
            designation_metrics[designation] = utils.from_dict_to_object({
                'vacancies': designation_df['vacancies'].sum(),
                'total_cost': designation_df['total_cost'].sum()
            })

        return utils.respond(utils.ok, {
            'vacancies': total_vacancies,
            'designations': designations,
            'designation_metrics': designation_metrics
        })

    def job_openings(self, data):
        df = utils.to_data_frame(data)
        df["vacancies"] = df["vacancies"].astype(int)
        df["lower_range"] = df["lower_range"].astype(float)
        df["upper_range"] = df["upper_range"].astype(float)
        total_openings = len(df)
        departments = df['department'].unique()
        department_metrics = {}

        for dept in departments:
            dept_df = df[df['department'] == dept]
            department_metrics[dept] = utils.from_dict_to_object({
                'vacancies': dept_df['vacancies'].sum(),
                'lowest': dept_df['lower_range'].min(),
                'highest': dept_df['upper_range'].max(),
            })

        total_vacancies = df['vacancies'].sum()

        return utils.respond(utils.ok, {
            'openings': total_openings,
            'vacancies': total_vacancies,
            'department_metrics': department_metrics
        })

    def job_applications(self, data):
        df = utils.to_data_frame(data)
        total_applications = len(df)
        df["lower_range"] = df["lower_range"].astype(float)
        df["upper_range"] = df["upper_range"].astype(float)
        total_unique_applicants = df['applicant_name'].nunique()
        active_count = len(df[df['status'] == 'active'])
        rejected_count = len(df[df['status'] == 'rejected'])
        designations = df['designation'].unique()
        designation_metrics = {}

        for desig in designations:
            desig_df = df[df['designation'] == desig]
            applications = len(desig_df)
            designation_metrics[desig] = utils.from_dict_to_object({
                'applications': applications,
                'lowest': desig_df['lower_range'].min(),
                'highest': desig_df['upper_range'].max(),
                'average': desig_df[['lower_range', 'upper_range']].mean().mean()
            })

        return utils.respond(utils.ok, {
            'applications': total_applications,
            'applicants': total_unique_applicants,
            'active': active_count,
            'rejected': rejected_count,
            'designation_metrics': designation_metrics
        })

    def interview_type(self, data):
        df = utils.to_data_frame(data)
        total_types = len(df)
        draft_count = len(df[df['status'] == 'Draft'])
        active_count = len(df[df['status'] == 'Active'])

        return utils.respond(utils.ok, {
            'total': total_types,
            'draft': draft_count,
            'active': active_count
        })

    def interview_schedule(self, data):
        df = utils.to_data_frame(data)
        total_schedules = len(df)
        interview_types = df['interview_type'].unique()
        interview_type_metrics = {}

        for i_type in interview_types:
            interview_type_metrics[i_type] = utils.from_dict_to_object({
                'schedules': len(df[df['interview_type'] == i_type]),
            })

        job_applications = df['application'].unique()
        job_application_metrics = {}

        for app in job_applications:
            app_df = df[df['application'] == app]
            job_application_metrics[app] = utils.from_dict_to_object({
                'total': len(app_df),
                'interview_types': app_df['interview_type'].unique()
            })

        return utils.respond(utils.ok, {
            'total': total_schedules,
            'interview_type_metrics': interview_type_metrics,
            'job_application_metrics': job_application_metrics
        })

    def interviews(self, data):
        df = utils.to_data_frame(data)
        total_interviews = len(df)
        draft_count = len(df[df['status'] == 'Draft'])
        active_count = len(df[df['status'] == 'Active'])

        return utils.respond(utils.ok, {
            'total': total_interviews,
            'draft': draft_count,
            'active': active_count
        })

    def job_offers(self, data):
        df = utils.to_data_frame(data)
        total_offers = len(df)
        draft_count = len(df[df['status'] == 'Draft'])
        submitted_count = len(df[df['status'] == 'Submitted'])
        total_applicants = df['job_application'].nunique()

        job_applications = df['job_application'].unique()
        job_application_metrics = {}

        for app in job_applications:
            app_df = df[df['job_application'] == app]
            job_application_metrics[app] = utils.from_dict_to_object({
                'total': len(app_df),
                'draft': len(app_df[app_df['status'] == 'Draft']),
                'submitted': len(app_df[app_df['status'] == 'Submitted']),
            })

        return utils.respond(utils.ok, {
            'total': total_offers,
            'applicants': total_applicants,
            'draft': draft_count,
            'submitted': submitted_count,
            'job_application_metrics': job_application_metrics
        })

    def appointment_letters(self, data):
        df = utils.to_data_frame(data)
        total_appointments = len(df)
        draft_count = len(df[df['status'] == 'Draft'])
        submitted_count = len(df[df['status'] == 'Submitted'])
        total_applicants = df['job_application'].nunique()

        job_applications = df['job_application'].unique()
        job_application_metrics = {}

        for app in job_applications:
            app_df = df[df['job_application'] == app]
            job_application_metrics[app] = utils.from_dict_to_object({
                'total': len(app_df),
                'draft': len(app_df[app_df['status'] == 'Draft']),
                'submitted': len(app_df[app_df['status'] == 'Submitted']),
            })

        return utils.respond(utils.ok, {
            'total': total_appointments,
            'applicants': total_applicants,
            'draft': draft_count,
            'submitted': submitted_count,
            'job_application_metrics': job_application_metrics
        })