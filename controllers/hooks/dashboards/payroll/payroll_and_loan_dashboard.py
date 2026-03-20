from controllers.utils import Utils
from controllers.utils.dates import Dates
utils =Utils()
dates =Dates()
from datetime import datetime, timedelta
pp =utils.pretty_print
throw =utils.throw

# class payroll_loans_dashboard:
#     def __init__(self, dbms, object):
#         self.dbms =dbms
#         self.obj =object
#         self.Advances =self.dbms.get

    # @classmethod
def payroll_loans_dashboard(dbms, object):
    return_data =utils.from_dict_to_object({
        "advances_and_loans": utils.from_dict_to_object({}),
        "dept_advance_applications": utils.from_dict_to_object({}),
    })    
    
    disbursements_repayments_and_defaults =utils.from_dict_to_object({})
    fetch_advances =None
    fetch_advances_entries =None


    # DATA FECTHING
    try:
        fetch_advances =dbms.get_list("Advance_Application", fetch_linked_fields=True, fetch_linked_tables=True)
        fetch_advances_entries =dbms.get_list("Salary_Advance_Entries")
        # filters={"created_on__range": [dates.add_days(dates.today(), (-30*3)), dates.today()]}, 
        pp(fetch_advances, fetch_advances_entries)
    except Exception as e:
        pp("An error occurred: {e}")


    # RECENT 
    if fetch_advances.status == utils.ok:
        date_obj = (datetime.today() - timedelta(days=90)).date()
        filtered_to_3months = [advance for advance in fetch_advances.data.rows if advance.created_on > date_obj]
        recent_applications = []
        for application in filtered_to_3months:
            recent_applications.append(utils.from_dict_to_object({
                "image": "",
                "name": application.full_name,
                "designation": application.designation,
                "amount": application.amount_with_interest,
            }))

        return_data.recent_applications = recent_applications

        # departmental_applications = utils.group(fetch_advances.data.rows, "department")
        # for item in departmental_applications:
        #     index = item[0]
        #     department = item[1:]
        #     return_data.dept_advance_applications.labels.append(index)
        #     return_data.dept_advance_applications.value.append(len(department))


    # ADVANCE AND LOANS
    # if fetch_advances_entries.status ==utils.ok:
    #     utils.group(fetch_advances_entries.data.rows, "entry_type")
    #     advances_and_loans =utils.from_dict_to_object({})
    #     for index, application in fetch_advances.data.rows:
    #         advances_and_loans[index] =[]
    #         advances_and_loans[index].append(utils.from_dict_to_object({
    #             "collected_amount": sum(app.total_repaid or 0.00 for app in application),
    #             "disbursed_amount": sum(app.amount or 0.00 for app in application),
    #         }))

    #         return_data.advances_and_loans[index] =advances_and_loans

    # RECENT APPLICATIONS
    if fetch_advances_entries.status ==utils.ok:
        default_data =[]
        defaulted = [entry for entry in fetch_advances_entries.data.rows if entry.due_date is not None and entry.due_date > datetime.today().date()]
        repaid = [entry for entry in fetch_advances_entries.data.rows if entry.balance is not None and (entry.balance <= 0 or entry.balance - entry.balance == 0)]
        disbursements = [entry for entry in fetch_advances_entries.data.rows if entry.total_repaid is not None and entry.entry is not None and entry.total_repaid <= 0 and entry.entry > datetime.today().date()]

        trio_distribution =utils.from_dict_to_object({
            "labels": ["Disbursements", "Repaid", "defaulted"],
            "value": [len(fetch_advances_entries.data.rows), len(repaid), len(defaulted)]
        })
        disbursements_repayments_and_defaults.trio_distribution =trio_distribution

        disbursement_and_repayment =utils.from_dict_to_object({
            "labels": trio_distribution.labels[:-1],
            "value": trio_distribution.value[:-1]
        })

        disbursements_repayments_and_defaults.disbursement_and_repayment =disbursement_and_repayment

        for entry in defaulted:
            default_data.append(utils.from_dict_to_object({
                "icon": "",
                "name": entry.full_name,
                "currency": "",
                "amount": entry.balance,
            }))
        disbursements_repayments_and_defaults.default_data =default_data      
        
        return_data.disbursements_repayments_and_defaults =disbursements_repayments_and_defaults
        
    return utils.respond(utils.ok, return_data)