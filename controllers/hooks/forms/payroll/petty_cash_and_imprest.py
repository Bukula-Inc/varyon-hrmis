from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion
import re


utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def staff_expense_retirement_validation(dbms, body):

    retired_amount =0
    model =None
    doc_name =None
    doc_data =None
    if not body:
        throw(f"No data was received for validations.")
    retirement_type =DataConversion.safe_get(body, "retirement_type", None)
    if not retirement_type:
        throw(f"Please pick a retirement type from the retirement type field")
    if retirement_type =="Petty Cash":
        doc_name =DataConversion.safe_get(body, "petty_cash", None)
        if not doc_name:
            throw(f"Please provide the petty cash document you wish to retire.")
        model ="Petty_Cash"
        fetch_petty_cash =dbms.get_doc(model, doc_name)
        employee_data =None
        if fetch_petty_cash.status !=utils.ok:
            throw(f"Failed to fetch the petty cash document {doc_name} dur to : {fetch_petty_cash}")
        doc_data  =DataConversion.safe_get(fetch_petty_cash, "data", None)
        if not DataConversion.safe_get(body, "employee_no", None):
            DataConversion.safe_set(body, "employee_no", DataConversion.safe_get(doc_data, "initiator", None))
            fetch_employee =dbms.get_doc("Employee", DataConversion.safe_get(body, "employee_no", None))
            if fetch_employee.status !=utils.ok:
                throw(f"An error occurred while verifying the employee's data in the system: {fetch_employee}")
            employee_data =DataConversion.safe_get(fetch_employee, "data", None)
        if not DataConversion.safe_get(body, "surname", None):
            DataConversion.safe_set(body, "surname", DataConversion.safe_get(doc_data, "initiator_last_name", None))
        if not DataConversion.safe_get(body, "other_name", None):
            DataConversion.safe_set(body, "other_name", DataConversion.safe_get(doc_data, "initiator_first_name", None))
        if not DataConversion.safe_get(body, "position", None):
            DataConversion.safe_set(body, "position", DataConversion.safe_get(employee_data, "designation", None))
        if not DataConversion.safe_get(body, "department", None):
            DataConversion.safe_set(body, "department", DataConversion.safe_get(doc_data, "department", None))
        if not DataConversion.safe_get(body, "section", None):
            DataConversion.safe_set(body, "section", DataConversion.safe_get(employee_data, "section", None))
        if not DataConversion.safe_get(body, "obtained_amount", None):
            DataConversion.safe_set(body, "obtained_amount", DataConversion.safe_get(doc_data, "balance", None))

    else:
        doc_name =""
        if retirement_type =="Imprest Form-20-A":
            doc_name ="imprest_a"
        elif retirement_type =="Imprest Form-20-B":
            doc_name ="imprest_b"
        elif retirement_type =="Imprest Form-20-C":
            doc_name ="imprest_c"

        model =re.sub(r"[ -]", "_", retirement_type)
        if not DataConversion.safe_get(body, doc_name, None):
            throw(f"""Please provide the {retirement_type} document""")
        fetch_imprest =dbms.get_doc(model, DataConversion.safe_get(body, doc_name, None))
        if fetch_imprest.status !=utils.ok:
            throw(f"""The {retirement_type} document of the name {DataConversion.safe_get(body, doc_name, None)} was not found: {fetch_imprest}""")
        doc_data =DataConversion.safe_get(fetch_imprest, "data", None)
        if not DataConversion.safe_get(body, "duration_of_tour_to", None):
            DataConversion.safe_set(body, "duration_of_tour_to", DataConversion.safe_get(doc_data, "duration_to_date", None))
        if not DataConversion.safe_get(body, "duration_of_tour_from", None):
            DataConversion.safe_set(body, "duration_of_tour_from", DataConversion.safe_get(doc_data, "duration_from_date", None))
        if not DataConversion.safe_get(body, "registration_vehicle", None):
            DataConversion.safe_set(body, "registration_vehicle", DataConversion.safe_get(doc_data, "registration_number_of_vechile", None))
        if not DataConversion.safe_get(body, "vehicle_model", None):
            DataConversion.safe_set(body, "vehicle_model", DataConversion.safe_get(doc_data, "vechile_make", None))
        
        if not DataConversion.safe_get(body, "places_visited", None) and DataConversion.safe_get(doc_data, "visited_province_and_district", None):
            visited_province_and_district =[]
            for place in DataConversion.safe_get(doc_data, "visited_province_and_district", None):
                visited_province_and_district.append(utils.from_dict_to_object({
                    "place": f"""{DataConversion.safe_get(place,"province", "")}, {DataConversion.safe_get(place,"district", "")}"""
                }))
            body.places_visited =visited_province_and_district

        if not DataConversion.safe_get(body, "areas_of_expense", None) and DataConversion.safe_get(doc_data, "retirement_item", None):
            retirement_item =[]
            for expense in retirement_item:
                DataConversion.safe_list_append(retirement_item, utils.from_dict_to_object({"subsistance_allowance": DataConversion.safe_get(expense, "description", ""), "usage_length": 1, "unit_price_of_usage": DataConversion.safe_get(expense, "amounts", 0.00), "total_spent": DataConversion.safe_get(expense, "amounts", 0.00)}))
                                
                retired_amount += DataConversion.safe_get(expense, "amounts", 0.00)
            
            body.areas_of_expense =retirement_item
        
    areas_of_expense =DataConversion.safe_get(body, "areas_of_expense", None)
    row_count =1
    if not areas_of_expense:
        throw(f"Please provide a list of the expense the {retirement_type} was used on.")
    if not DataConversion.safe_get(body, "retired_amount", None):
        for expense in areas_of_expense:
            if not DataConversion.safe_get(expense, "subsistance_allowance", None):
                throw(f"""You did not provide a <strong class='text-red font-semibold'>Description</strong> for row {row_count}""")
            if not DataConversion.safe_get(expense, "usage_length", None):
                throw(f"""You did not provide a <strong class='text-red font-semibold'>Quantity</strong> for row {row_count}""")
            if not DataConversion.safe_get(expense, "unit_price_of_usage", None):
                throw(f"""You did not provide a <strong class='text-red font-semibold'>Price</strong> for row {row_count}""")
            if not DataConversion.safe_get(expense, "total_spent", None):
                DataConversion.safe_set(expense, "total_spent", DataConversion.convert_to_float(DataConversion.safe_get(expense, "usage_length", 1)) * DataConversion.convert_to_float (DataConversion.safe_get(expense, "unit_price_of_usage", 0)))
            retired_amount +=DataConversion.convert_to_float(DataConversion.safe_get(expense, "total_spent", 0.00))
        DataConversion.safe_set(body, "retired_amount", retired_amount)

    if not DataConversion.safe_get(body, "balance_left", None):
        DataConversion.safe_set(body, "balance_left", DataConversion.convert_to_float(DataConversion.safe_get(body, "obtained_amount", None)) -DataConversion.convert_to_float(DataConversion.safe_get(body, "retired_amount", None)))
    if not DataConversion.safe_get(body, "owed_to", None) and DataConversion.safe_get(body, "balance_left", None) !=0:
        if DataConversion.convert_to_float(DataConversion.safe_get(body, "balance_left", None)) < 0:
            DataConversion.safe_set(body, "owed_to", f"""Officer {DataConversion.safe_get(body, "employee_no", None)}""")
        elif DataConversion.convert_to_float(DataConversion.safe_get(body, "balance_left", None)) > 0:
            DataConversion.safe_set(body, "owed_to", f"""Examination Council of Zambia""")

    return utils.from_dict_to_object({"retirement_body":body, "retiring_doc": doc_data})

def before_petty_cash_save(dbms, object):
    body =object.body

    if not body.initiator:
        throw(f"Initiator was not provided.")
    if not body.requested_amount:
        throw(f"Requested Amount was not provided.")
    if not body.purpose:
        throw(f"Purpose was not provided.")
    if not body.requested_amount_in_word:
        throw(f"Requested amount in word, was not provided.")
    if not body.requested_amount:
        throw(f"Requested amount was not provided.")
    # if not body.initiator:
    #     throw(f"Initiator was not provided.")
    # if not body.initiator:
    #     throw(f"Initiator was not provided.")
    # if not body.initiator:
    #     throw(f"Initiator was not provided.")
    # if not body.initiator:
    #     throw(f"Initiator was not provided.")
    # if not body.initiator:
    #     throw(f"Initiator was not provided.")
    # if not body.initiator:
    #     throw(f"Initiator was not provided.")
    # if not body.initiator:
    #     throw(f"Initiator was not provided.")
    # if not body.initiator:
    #     throw(f"Initiator was not provided.")
    # if not body.initiator:
    #     throw(f"Initiator was not provided.")

    object.body.balance =body.requested_amount
    DataConversion.safe_set (object.body, "not_retired", 0)

def before_imprest_save(dbms, object):
    body =object.body

    if not body.initiator:
        throw(f"Initiator was not provided.")
    if not body.requested_amount:
        throw(f"Requested Amount was not provided.")
    if not body.job_title:
        throw(f"Job_Title was not provided.")
    if not body.country:
        throw(f"Country was not provided.")
    if not body.duration_from_date:
        throw(f"Duration from date was not provided.")
    if not body.duration_to_date:
        throw(f"Duration to date was not provided.")
    if not body.nature_of_offical_duty:
        throw(f"Nature of offical duty was not provided.")
    if not body.mode_of_travel:
        throw(f"Mode of travel was not provided.")
    row_count =1
    for retirement_item in body.retirement_item:
        if not retirement_item.description:
            throw(f"Description was not provided at row {row_count}.")
        if not retirement_item.amounts:
            throw(f"Amounts was not provided at row {row_count}.")
        row_count +=1
            
    DataConversion.safe_set (object.body, "not_retired", 0)
    object.body.balance =body.requested_amount


def before_petty_cash_and_imprest_submit(dbms, object):
    # pp(object)
    object.doc_status ="Unretired"
    DataConversion.safe_set (object.body, "not_retired", 1)
    # throw(",.....,")

# def before_imprest_submit(dbms, object):
#     object.body.balance =body.requested_amount


def before_retirement_save(dbms, object):
    validation =staff_expense_retirement_validation(dbms, DataConversion.safe_get(object, "body", None))
    object.body =DataConversion.safe_get(validation, "retirement_body", None)

def before_retirement_submit(dbms, object):
    core_payroll =Core_Payroll(dbms, object)

    retirement_recalculation =core_payroll.retirement_recalculation(object.body)

    object.doc_status =retirement_recalculation.status
    object.body =retirement_recalculation.body


