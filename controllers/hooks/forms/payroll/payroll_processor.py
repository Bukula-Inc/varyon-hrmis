from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.utils.dates import Dates
from controllers.core_functions.payroll.payroll_processor import Process_Payroll
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()

pp = utils.pretty_print
throw = utils.throw

def on_per_month_entry (dbms, object):
    object.doc_status = "Draft"

def on_payroll_processor_save(dbms, object):
    core_hr = Core_Hr (dbms)
    pay_pro = object.body
    DataConversion.safe_set (object.body, "has_error", 0)
    
    DataConversion.safe_set (object, "doc_status", "Draft")

def on_payroll_processor_update(dbms, object):
    pass

def on_payroll_processor_cancel(dbms, object):
    core_hr = Core_Hr (dbms)
    payroll_processor = DataConversion.safe_get (object, "body", utils.from_dict_to_object ())
    payslips = core_hr.get_list ("Payslip", filters={"payroll_processor": DataConversion.safe_get (payroll_processor, "name")})
    if payslips:
        payslip_ids =  utils.get_list_of_dicts_column_field(payslips, "id")
        dbms.cancel_doc ("Payslip", payslip_ids)

    employee_info = DataConversion.safe_get (payroll_processor, "employee_info", [])
    if len (employee_info) > 0:
        for emp in employee_info:
            employee = core_hr.get_doc ("Employee", DataConversion.safe_get (emp, "employee"))
            if employee:
                status = DataConversion.safe_get (emp, "status")
                if str (status).lower () != "active":
                    DataConversion.safe_set (employee, "is_separated_emp_paid", "Unsettled")
                    dbms.update ("Employee", employee, update_submitted=True)

def on_payroll_processor_submit(dbms, object):
    # object.doc_status = "Queued for Processing"
    initiate_Payroll_processor (dbms, object)

def initiate_Payroll_processor (dbms, object):
    core_hr = Core_Hr (dbms)
    payroll_processors = core_hr.get_list ("Payroll_Processor", filters={"status__in": ["Queued for Processing", "Partially Processed"]}, limit=1)
    if payroll_processors and len (payroll_processors) > 0:
        for processor in payroll_processors:
            try:
                emps = utils.array_to_dict (DataConversion.safe_get (processor, "employee_info", []), 'employee')
                try:
                    delattr (emps, "TOTALS")
                except:
                    pass
                DataConversion.safe_set (processor, "employee_info", utils.reverse_array_to_dict (emps))

                obj = utils.from_dict_to_object ({
                    "body": processor,
                })

                processor = Process_Payroll.payroll_processor_initializer (dbms=dbms, obj=obj)
                DataConversion.safe_set (obj.body, "total_successful_payslips", DataConversion.safe_get (processor, "successful", 0))
                DataConversion.safe_set (obj.body, "total_failed_payslips", DataConversion.safe_get (processor, "failed", 0))
                DataConversion.safe_set (obj.body, "transaction_journal", DataConversion.safe_get (processor, "journal"))
                
                has_error = 0
                payroll_processor_error = ""
                payroll_processor_error_obj = None

                status = "Processed Successfully"
                if processor.successful == 0:
                    status = "Processing Failed"
                    has_error = 1
                    payroll_processor_error = f"{DataConversion.safe_get (processor, 'failed_employees')}"
                    payroll_processor_error_obj = DataConversion.safe_get (processor, 'failed_employees')

                DataConversion.safe_set (obj.body, "status", status)
                DataConversion.safe_set (obj.body, "has_error", has_error) 
                DataConversion.safe_set (obj.body, "payroll_processor_error", payroll_processor_error)
                DataConversion.safe_set (obj.body, "payroll_processor_error_obj", payroll_processor_error_obj)

                r = dbms.update ("Payroll_Processor", obj.body, update_submitted=True)
                pp ("=========================>>>>>>>>>>>>>>>>>> Payroll Processed Successfully", r)

            except Exception as e:
                pp (f"An error occurred while processing payroll: {str(e)}")
                throw ("wwwwwwwwwwwwwwwwwwwwwwwww")