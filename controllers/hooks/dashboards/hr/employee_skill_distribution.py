from datetime import datetime
import pandas as pd
from controllers.core_functions.hr import Core_Hr
from analytics.hr import HR_Analytics
from controllers.utils import Utils
from controllers.utils.dates import Dates
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class Employee_skill_distribution_dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.core = Core_Hr(dbms,object.user, object)
        self.past_7_days = dates.add_days(dates.today(), -7)
        self.analytics =  HR_Analytics(dbms, object)
        self.employees = []
        self.total_employees = 0

    @classmethod
    def dashboard(cls, dbms, object):
        cls.__init__ (cls, dbms=dbms, object=object)
        return utils.respond(utils.ok,{
            "get_employee_infor": cls.get_employee_turn_over(cls),
            "departmental_skill_gap": cls.departmental_skill_gap(cls),
            "employee_certifications": cls.employee_certifications(cls),
            "open_training_programs": cls.open_training_programs(cls),
            "skilled_employees": cls.skilled_employees(cls),
            "get_departments": cls.total_departments(cls),
            "self_appraisal": cls.appraisal_stat(cls),
            "appraisal_stats": cls.appraisal_stats(cls),
            
        })
        
    def get_employee_turn_over(self):
        get_user_infor = self.dbms.get_list("Employee")
        if get_user_infor.status == utils.ok:
            df = utils.to_data_frame(get_user_infor.data.rows)
            grouped_df = df.groupby('designation')['id'].count().reset_index()
            grouped_df = grouped_df.rename(columns={'id': 'employee_count'})
            data = grouped_df.to_dict(orient='records')
        return utils.respond(utils.ok, data)
    def departmental_skill_gap(self):
        staffing_plan = self.core.get_staffing_plan()
        if staffing_plan.status == utils.ok:
            df = utils.to_data_frame(staffing_plan.data.rows)
            submitted_plans = df[df['status'] == 'Submitted']
            skill_gap = submitted_plans.groupby(['department', 'designation']).size().reset_index(name='Count')
            skill_gap_pivot = skill_gap.pivot(index='department', columns='designation', values='Count').fillna(0)
            result = skill_gap_pivot.to_dict(orient='index')
            return result
        else:
            return None
    def employee_certifications(self):
        get_employee_profile = self.dbms.get_list("Employee_File", fetch_linked_tables=True)
        if get_employee_profile.status == utils.ok:
            df = utils.to_data_frame(get_employee_profile.data.rows)
            file_names = df['file_content'].apply(lambda x: [item['file_name'] for item in x] if x else [])
            file_names = file_names.explode()
            result = file_names.value_counts().reset_index()
            result.columns = ['file_name', 'count']
            return result.to_dict(orient='records')
        else:
            return None
    def open_training_programs(self):
        get_training_program = self.dbms.get_list("Attendee")
        if get_training_program.status == utils.ok:
            df = utils.to_data_frame(get_training_program.data.rows)
            program_counts = df['parent'].value_counts().reset_index()
            program_counts.columns = ['Training_Program', 'Number_of_Attendees']
            return program_counts.to_dict(orient='records')
        else:
            return None
    def skilled_employees(self):
        get_employee_profile = self.dbms.get_list("Employee_File", fetch_linked_tables=True)
        if get_employee_profile.status == utils.ok:
            df = utils.to_data_frame(get_employee_profile.data.rows)
            df['file_name'] = df['file_content'].apply(lambda x: [item['file_name'] for item in x] if x else [])
            qualification_order = ['Diploma', 'Degree', 'Masters', 'Doctor', 'PHD']
            if not df.empty:
                df['highest_qualification'] = df['file_name'].apply(lambda x: max(x, key=lambda y: qualification_order.index(y) if y in qualification_order else float('inf')) if x else None)
            highest_qualification = df['highest_qualification'].value_counts().index[0]
            if highest_qualification not in qualification_order:
                return {
                    'error': f"Highest qualification '{highest_qualification}' is not in the qualification order list."
                }
            total_employees = len(df[df['highest_qualification'] == highest_qualification])
            
            return {
                'highest_qualification': highest_qualification,
                'total_employees': total_employees
            }
        else:
            return None
    def total_departments(self):
        get_departments = self.dbms.get_list("Department")
        if get_departments.status == utils.ok:
            return len(get_departments.data.rows)
        else:
            return 0
    def appraisal_stat(self):
        appraisal = self.dbms.get_list("Appraise_Your_Self", fetch_linked_tables=True)
        if appraisal.status == utils.ok:
            df = utils.to_data_frame(appraisal.data.rows)
            behavioral_imperatives_df = pd.json_normalize(df['behavioral_imperative'].explode())
            performance_kpis_df = pd.json_normalize(df['performance_kpi'].explode())
            avg_behavioral_imperatives = behavioral_imperatives_df['rating_b'].mean()
            avg_performance_kpis = performance_kpis_df['rating_po'].mean()
            chart_data = {
                'values': [
                    {'name': 'Skills', 'data': [avg_behavioral_imperatives, 0, 0]},
                    {'name': 'Performance', 'data': [0, avg_performance_kpis, 0]}
                ],
                'labels': [
                    f'Soft Skill ({avg_behavioral_imperatives:.2f})',
                    f'Performance ({avg_performance_kpis:.2f})',
                    'Certification (0)'
                ]
            }

            return chart_data
        else:
            return None
    def appraisal_stats(self):
        appraisal = self.dbms.get_list("Appraise_Your_Self", fetch_linked_tables=True)
        if appraisal.status == utils.ok:
            df = utils.to_data_frame(appraisal.data.rows)
            behavioral_imperatives_df = pd.json_normalize(df['behavioral_imperative'].explode())
            performance_kpis_df = pd.json_normalize(df['performance_kpi'].explode())
            avg_behavioral_imperatives = behavioral_imperatives_df['rating_b'].mean()
            avg_performance_kpis = performance_kpis_df['rating_po'].mean()
            skills_vs_performance = {
                'values': [
                    {'name': 'Skills', 'data': [avg_behavioral_imperatives, 0, 0]},
                    {'name': 'Performance', 'data': [0, avg_performance_kpis, 0]}
                ],
                'labels': [
                    f'Soft Skill ({avg_behavioral_imperatives:.2f})',
                    f'Performance ({avg_performance_kpis:.2f})',
                    'Certification (0)'
                ]
            }
            ratings = behavioral_imperatives_df['rating_b']
            beginner_count = len(ratings[ratings <= 2])
            intermediate_count = len(ratings[(ratings > 2) & (ratings <= 4)])
            advanced_count = len(ratings[ratings > 4])

            total_count = len(ratings)
            skill_proficiency_levels = {
                'values': [
                    {'name': 'Beginner', 'data': [beginner_count / total_count * 100]},
                    {'name': 'Intermediate', 'data': [intermediate_count / total_count * 100]},
                    {'name': 'Advanced', 'data': [advanced_count / total_count * 100]}
                ],
                'labels': ['Skill Level']
            }

            return {
                'skills_vs_performance': skills_vs_performance,
                'skill_proficiency_levels': skill_proficiency_levels
            }
        else:
            return None