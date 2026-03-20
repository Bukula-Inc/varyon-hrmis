from controllers.utils import Utils
from controllers.utils.dates import Dates

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw


class BJ_Leave:
    def __init__(self, dbms, object):
        self.dbms =dbms
        self.object =object
        self.today =dates.today()

    def leave_allocation(self):
        today =dates.string_to_date(self.today)
        policy =None
        leave_allocation_employees =[]
        emps =None
        grade_allocation =None
        allocation =None
        emps_leave_entries =[]
        fetch_leave_policy =self.dbms.get_list("Leave_Policy", filters={"is_active":1}, fetch_linked_tables=True, fetch_linked_fields=True)
        if fetch_leave_policy.status ==utils.ok:
            policy =fetch_leave_policy.data.rows[0]
            # today.day ==1 and 
        if policy !=None:
            grouped_by_grade =utils.group(policy.leave_policy_grade, "employee_grade")
            grouped_by_leave_type =utils.group(policy.leave_policy_grade, "leave_type")
            grade_allocation =utils.from_dict_to_object({key:val[0].total_days_allocated_per_month for key, val in grouped_by_grade.items()})
            grade_leave_type =utils.from_dict_to_object({key:[leave_type.leave_type for leave_type in val] for key, val in grouped_by_grade.items()})
            leave_type_allocation =utils.from_dict_to_object({key:val[0].linked_fields.leave_type for key, val in grouped_by_leave_type.items()})
            list_of_grades =[grade for grade in grouped_by_grade]
            fetch_employees =self.dbms.get_list("Employee", filters={"employee_grade__in": list_of_grades or []}, fields=["name", "full_name", "department", "gender", "employee_grade"])

            pp("grade_allocation=>",grade_allocation, "grade_leave_type=>",grade_leave_type, "leave_type_allocation=>",leave_type_allocation)

            if fetch_employees.status !=utils.ok:
                return fetch_employees.status
            else:
                emps =fetch_employees.data.rows
                emps_by_grade =utils.group(emps, "employee_grade")

                if policy.enable_single_accrual ==1:
                
                    accruing_leave_type =policy.accruing_leave_type
                    for emp in emps:
                        leave_allocation_employees.append(utils.from_dict_to_object
                            ({
                                "employee_name": emp.full_name,
                                "from_date": None,
                                "to_date": None,
                                "total_leaves_allocated": grade_allocation[emp.employee_grade],
                                "gender": emp.gender,
                                "department": emp.department,
                                "employee": emp.name,
                                "leave_policy": policy.name,
                                "leave_type": accruing_leave_type,
                            }))                    

                        # {
                        #     "company_id": None,
                        #     "name": "",
                        #     "reference": "",
                        #     "total_days": 0,
                        #     "leave_type": accruing_leave_type,
                        #     "employee": emp.name,
                        #     "employee_name": emp.full_name,
                        #     "from_date": None,
                        #     "to_date": null,
                        #     "used_leave_days": 0,
                        #     "allocated_leave_days": 24,
                        #     "remaining_leave_days": 0,
                        #     "leave_days_in_working_hours": "0",
                        # }

                    allocation =utils.from_dict_to_object({
                        "name": "",
                        "company": None,
                        "populate_by": "Leave Policy",
                        "policy": policy.name,
                        "main_policy": accruing_leave_type,
                        "main_leave_type": "",
                        "leave_allocation_employees": leave_allocation_employees,
                    },)
           
                    try:
                        allocationed =self.dbms.create("Leave_Allocation", allocation, submit_after_create=True)
                        return allocationed.status
                    except Exception as e:
                        pp(e)
                else:
                    for key, leave in leave_type_allocation.items():
                        for emp in emps:
                            if key in grade_leave_type[emp.employee_grade] and leave_type_allocation[key].is_commutable ==1:
                                emps_leave_entries.append(utils.from_dict_to_object({
                                    "company_id": None,
                                    "name": "",
                                    "reference": "",
                                    "total_days": 0,
                                    "leave_type": key,
                                    "employee": emp.name,
                                    "employee_name": emp.full_name,
                                    "from_date": None,
                                    "to_date": None,
                                    "used_leave_days": 0,
                                    "allocated_leave_days": grade_allocation[emp.employee_grade],
                                    "remaining_leave_days": 0,
                                    "leave_days_in_working_hours": "0",
                                }))

                    try:
                        for entry in emps_leave_entries:
                            leave_entry =self.dbms.create("Leave_Entry", entry, submit_after_create=True)
                            pp(leave_entry)
                        return allocationed.status
                    except Exception as e:
                        pp(e)


            # try:
            #     allocationed =self.dbms.create("Leave_Allocation", allocation, submit_after_create=True)
            #     return allocationed.status
            # except Exception as e:
            #     pp(e)


    def leave_plan(self):
        fetch_leave_plan =self.dbms.get_list("Leave_Plan", filters={"auto_create_leave_application":1}, fetch_linked_tables=True)
        pp(fetch_leave_plan)
        if fetch_leave_plan.status ==utils.ok:
            for allocation in fetch_leave_plan.data.rows:
                print(type(allocation.days_before_from_date))
                pp(".................................")
                pp(dates.add_days(allocation.from_date, -1))
                pp(".................................")
                if dates.add_days(allocation.from_date, -int(allocation.days_before_from_date)) ==self.today:
                    pp(allocation)


    @classmethod
    def leave(cls, dbms, object):
        instance =cls(dbms, object)
        result =utils.from_dict_to_object({
            "leave_allocation": instance.leave_allocation(),
            # "instance.leave_plan": instance.leave_plan()
        })
        
        return utils.respond(utils.ok, result)