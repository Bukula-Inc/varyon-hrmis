from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def validate_salary_increment(dbms,body, skip_for_approval=True):  
    core_hr = Core_Hr (dbms)
    successful = []
    grades_dict = {}
    grade_log = []
    emp_log = []

    DataConversion.safe_set (body, "saved", 1)
    salary_grades = DataConversion.safe_get (body, "salary_grades", [])
    increment_type = DataConversion.safe_get (body, "increment_type")
    if not body:
        throw(f""" Please Provide all <b class='text-rose-600'>Required Fields</b>. """)
    if not increment_type:
        throw(f""" Please Select <b class='text-rose-600'>Increment Type</b>. """)

    if not utils.get_text_from_html_string (DataConversion.safe_get (body, "description")):
        throw(f""" Please Provide <b class='text-rose-600'>Reason For Increment</b>. """)
    
    if not salary_grades or len (salary_grades) <= 0:
        throw(f""" Please Select <b class='text-rose-600'>Grades To Do Increments On</b>. """)
    
    for i, grade in enumerate (salary_grades):
        salary_grade = DataConversion.safe_get (grade, "salary_grade")
        current_basic_pay = DataConversion.convert_to_float (DataConversion.safe_get (grade, "current_basic_pay"))
        increment_amount = DataConversion.convert_to_float (DataConversion.safe_get (grade, "increment_amount"))
        if not salary_grade:
            throw(f""" Salary Grade <b class='text-rose-600'>Is Missing on Row (#{i+1})</b>. """)
        if not current_basic_pay:
            throw(f""" Current Basic <b class='text-rose-600'>Is Missing on Row (#{i+1})</b>. """)
        if not increment_amount:
            throw(f""" Increment By <b class='text-rose-600'>Is Missing on Row (#{i+1})</b>. """)
        DataConversion.safe_list_append (successful, grade)

    grades_dict = utils.array_to_dict (core_hr.get_list ("Employee_Grade", fetch_linked_tables=True), "name")
    sc_dict = utils.array_to_dict (core_hr.get_list ("Salary_Component"), "name")
    em_dict = {}
    df = utils.to_data_frame (core_hr.get_list ("Employee"))
    if "employee_grade" in df.columns:
        em_dict = (
            df.groupby("employee_grade")
            .apply(lambda x: x.to_dict(orient="records"))
            .to_dict()
        )
    
    for row in successful:
        salary_grade = DataConversion.safe_get (row, "salary_grade")
        current_basic_pay = DataConversion.convert_to_float(DataConversion.safe_get (row, "current_basic_pay"))
        increment_amount = DataConversion.convert_to_float (DataConversion.safe_get (row, "increment_amount"))
        grade = DataConversion.safe_get (grades_dict, salary_grade)

        if not grade:
            DataConversion.safe_list_append (grade_log, {
                "grade": salary_grade,
                "update_status": "Failed",
                "issue": f"Grade {salary_grade} Not Found In The System",
                "status": "Failed",
            })
            continue

        current_basic_pay = DataConversion.convert_to_float (DataConversion.safe_get (grade, "basic_pay"))
        new_basic = current_basic_pay

        if DataConversion.safe_e (increment_type, "Percentage", str, True):
            new_basic = ((increment_amount/100) * current_basic_pay) + current_basic_pay
        else: 
            new_basic = current_basic_pay + increment_amount
        
        emps = DataConversion.safe_get (em_dict, salary_grade)
        for emp in emps:

            emp_name = DataConversion.safe_get (emp, "name")
            deductions = utils.array_to_dict (DataConversion.safe_get (emp, "deductions", []), "deduction")
            earnings = utils.array_to_dict (DataConversion.safe_get (emp, "earnings", []), "earning")
            unstandardized_components = DataConversion.safe_get (emp, "unstandardized_components", [])
            if unstandardized_components == "":
                unstandardized_components = []
            new_unstandardized_components = []
            
            for cmt in unstandardized_components:
                pp ("PPPPPP")
                component_name = DataConversion.safe_get (cmt, "component_name")
                component_type = DataConversion.safe_get(cmt, "component_type")
                component_value = DataConversion.safe_get(cmt, "component_value")

                asc = DataConversion.safe_get(sc_dict, component_name)
                scName = DataConversion.safe_get (asc, "resenting")
                new_component = DataConversion.safe_get (sc_dict, scName)

                if scName in earnings:
                    DataConversion.safe_list_append (emp_log, {
                        "employee": emp_name,
                        "issue": f"Salary Component {scName or 'Unknown' } Is Already Part of the Earnings",
                        "status": "Failed",
                    })
                    DataConversion.safe_list_append (new_unstandardized_components, cmt)
                    continue

                if scName in deductions:
                    DataConversion.safe_list_append (emp_log, {
                        "employee": emp_name,
                        "issue": f"Salary Component {scName or 'Unknown'} Is Already Part of the Deductions",
                        "status": "Failed",
                    })
                    DataConversion.safe_list_append (new_unstandardized_components, cmt)
                    continue

                if not new_component:
                    DataConversion.safe_list_append (emp_log, {
                        "employee": emp_name,
                        "issue": f"Salary Component {scName} Missing Representing",
                        "status": "Failed",
                    })
                    DataConversion.safe_list_append (new_unstandardized_components, cmt)
                    continue
                
                if not DataConversion.safe_e (DataConversion.safe_get(new_component, "value_type"), "Percentage", str, True):
                    DataConversion.safe_list_append (emp_log, {
                        "employee": emp_name,
                        "issue": f"Salary Component {component_name} Missing Representing",
                        "status": "Failed",
                    })
                    DataConversion.safe_list_append (new_unstandardized_components, cmt)
                    continue

                if not asc and not DataConversion.safe_e (DataConversion.safe_get (asc, "is_to_catch_up", 0), 1, int) and not DataConversion.safe_e (component_type, "Fixed Amount"):
                    DataConversion.safe_list_append (new_unstandardized_components, cmt)
                    continue

                sc_pv = DataConversion.convert_to_float (DataConversion.safe_get (new_component, "percentage", 0))
                pv = (sc_pv/100) * new_basic

                if pv <= component_value:
                    DataConversion.safe_list_append (emp_log, {
                        "employee": emp_name,
                        "issue": f"Salary Component {component_name} is still Greater than New and Standard Component {scName}",
                        "status": "Failed",
                    })
                    DataConversion.safe_list_append (new_unstandardized_components, cmt)
                    continue

                DataConversion.safe_set (cmt, "component_type", "Percentage")
                DataConversion.safe_set (cmt, "component_name", scName)
                DataConversion.safe_set (cmt, "component_value", sc_pv)

                DataConversion.safe_list_append (new_unstandardized_components, cmt)
                if component_name in earnings:
                    earning_obj = DataConversion.safe_get (earnings, component_name, {})
                    DataConversion.safe_set (earning_obj, "earning", scName)
                    earn = utils.reverse_array_to_dict (earnings)
                    earnings = utils.array_to_dict (earn, "earning")

                elif component_name in deductions:
                    deduction_obj = DataConversion.safe_get (deductions, component_name, {})
                    DataConversion.safe_set (deduction_obj, "deduction", scName)
                    earn = utils.reverse_array_to_dict (deductions)
                    deductions = utils.array_to_dict (earn, "deduction")
            
            DataConversion.safe_set (emp, "basic_pay", new_basic)
            DataConversion.safe_set (emp, "unstandardized_components", new_unstandardized_components)
            DataConversion.safe_set (emp, "deductions", utils.reverse_array_to_dict (deductions))
            DataConversion.safe_set (emp, "earnings", utils.reverse_array_to_dict (earnings))
            if not skip_for_approval:
                r = dbms.update ("Employee", utils.from_dict_to_object (emp), update_submitted=True)
                pp ("<<<<<<<<<<<<<<<<<<<======== EMPLOYEE =======>>>>>>>>>>>>>>>>",r)
                if r.status != utils.ok:
                    DataConversion.safe_list_append (emp_log, {
                        "grade": emp_name,
                        "issue": f"Failed to update Employee {emp_name}",
                        "status": "Failed",
                    })
                    
        if not skip_for_approval:
            DataConversion.safe_set (grade, "basic_pay", new_basic)
            r = dbms.update ("Employee_Grade", utils.from_dict_to_object (grade), update_submitted=True)
            pp ("<<<<<<<<<<<<<<<<<<<======== Employee Grade =======>>>>>>>>>>>>>>>>",r)
            if r.status != utils.ok:
                DataConversion.safe_list_append (grade_log, {
                    "grade": salary_grade,
                    "issue": f"Failed to update Employee Grade {salary_grade}",
                    "status": "Failed",
                })

    DataConversion.safe_set (body, "grade_updates", grade_log)
    DataConversion.safe_set (body, "employee_updates", emp_log)
    return body

def before_salary_increment_save(dbms, object):
    DataConversion.safe_set(object, "body", validate_salary_increment(dbms, DataConversion.safe_get(object, "body", {})))

def before_salary_increment_submit(dbms, object):
    DataConversion.safe_set(object, "body", validate_salary_increment(dbms, DataConversion.safe_get(object, "body", {}) ,skip_for_approval=False))