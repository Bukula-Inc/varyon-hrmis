from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates
import pandas as pd
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class Employee_Grievance_outcome:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.get_system_settings()
        if system_settings.get("status") == utils.ok:
            self.settings = Generate_Object(system_settings.get("data"))
            
    @classmethod        
    def discipline_outcome(cls, dbms, object):
        cls.__init__(cls, dbms, object)

        result_data =utils.from_dict_to_object({
            "resolution_time": 0,
            "relution_distrubtion": utils.from_dict_to_object({}),
            "departmental_displinary": utils.from_dict_to_object({}),
        })
        departmental_displinary =utils.from_dict_to_object({
            "labels" :[],
            "value" :[]
        })

        verbal_warning =None,
        written_warning =None,
        suspension =None,
        total_length =0

        fetch_case_outcomes =cls.dbms.get_list("Case_Outcome", fetch_linked_fields=True, fetch_linked_tables=True)
        
        if fetch_case_outcomes.status ==utils.ok:
            df_case_outcome =utils.to_data_frame(fetch_case_outcomes.data.rows)

            df_case_outcome['last_modified'] = pd.to_datetime(df_case_outcome['last_modified'])
            df_case_outcome['violation_date'] = pd.to_datetime(df_case_outcome['violation_date'])
            df_case_outcome['date_difference'] = (df_case_outcome['last_modified'] - df_case_outcome['violation_date']).dt.days

            total_length = int(df_case_outcome['date_difference'].iloc[0])
            result_data.resolution_time =total_length   

            verbal_warning_list = list(filter(lambda x: x['verbal_warning'] == 1, fetch_case_outcomes.data.rows)) or None
            written_warning = list(filter(lambda x: x['written_warning'] == 1, fetch_case_outcomes.data.rows)) or None
            suspension = list(filter(lambda x: x['suspension'] == 1, fetch_case_outcomes.data.rows)) or None

            relution_distrubtion =utils.from_dict_to_object({
                "verbal_warning_list": len(verbal_warning_list or []),
                "written_warning": len(written_warning or []),
                "suspension": len(suspension or []),             
            })

            # DEPARTMAENTAL DIPLINARY FREQUENCY
            fetch_emp_diplinary =cls.dbms.get_list("Employee_Disciplinary", fetch_linked_fields=True, fetch_linked_tables=True)
            if fetch_emp_diplinary.status ==utils.ok:
                emp_displinary_list =fetch_emp_diplinary.data.rows
                departmental_emp_displinary_list =utils.group(emp_displinary_list, "issue_raiser_department")
                for key, dedl in departmental_emp_displinary_list.items():
                    departmental_displinary.labels.append(key)
                    departmental_displinary.value.append(len(dedl))
                

            result_data.relution_distrubtion =relution_distrubtion
            result_data.departmental_displinary =departmental_displinary

        return utils.respond(utils.ok, result_data)


















































        # get_discipline = dbms.get_list("Case_Outcome", privilege=True, limit=6)
        # if get_discipline:
        #     outcome_list = []
        #     for d in get_discipline:
        #         outcome_info = [
        #             {'type': 'Verbal Warning', 'value': d['verbal_warning']},
        #             {'type': 'Written Warning', 'value': d['written_warning']},
        #             {'type': 'Suspension', 'value': d['suspension']},
        #             {'type': 'Termination', 'value': d['termination']}
        #         ]
        #         outcome_list.append(outcome_info)
        #         pp(outcome_list)
        #     return utils.respond(utils.ok, {"rows": outcome_list})
        # else:
        #     return None

    
    






