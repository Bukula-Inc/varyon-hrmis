# to adjust stock
from controllers import utils
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils import dict_to_object

utils = Utils()
dates = Dates()

def calculate_sales_commission(base_inclusive_total_amount, commission_rate):
    return base_inclusive_total_amount * commission_rate

def calculate_referral_commission(base_inclusive_total_amount, referral_commission_rate):
    return base_inclusive_total_amount * referral_commission_rate

def calculate_bonus_commission(base_inclusive_total_amount, sales_target, bonus_amount):
    if base_inclusive_total_amount >= sales_target:
        return bonus_amount
    else:
        return 0

def calculate_residual_commission(base_total_outstanding_amount, residual_commission_rate):
    return base_total_outstanding_amount * residual_commission_rate

def calculate_override_commission(base_total_outstanding_amount, override_commission_rate):
    return base_total_outstanding_amount * override_commission_rate

def calculate_flat_rate_commission(flat_rate):
    return flat_rate

data = {
    "currency": "USD",
    "convertion_rate": 1.0,
    "po_no": "PO001",
    "from_quotation": True,
    "payment_term": "30 days",
    "customer": "John Doe",
    "customer_tax_identification_no": "123456789",
    "customer_email": "johndoe@example.com",
    "customer_contact_no": "1234567890",
    "customer_physical_address": "123 Main St",
    "customer_postal_address": "123 Main St",
    "customer_currency": "ZMW",
    "sales_person": "kaizahc@gmail.com",
    "company": "ABC Corp",
    "company_tax_identification_no": "987654321",
    "company_physical_address": "456 Elm St",
    "company_postal_address": "456 Elm St",
    "update_stock": True,
    "is_return": False,
    "credit_note": False,
    "description": "Product sale",
    "total_qty": 10,
    "base_sub_total_amount": 1000,
    "base_total_discount_amount": 100,
    "base_tax_exclusive_total_amount": 900,
    "base_total_taxes_amount": 180,
    "base_inclusive_total_amount": 1080,
    "base_total_paid_amount": 0,
    "base_total_outstanding_amount": 1080,
    "sub_total_amount": 1000,
    "total_discount_amount": 100,
    "tax_exclusive_total_amount": 900,
    "total_taxes_amount": 180,
    "inclusive_total_amount": 1080,
    "total_paid_amount": 0,
    "total_outstanding_amount": 1080,
    "inclusive_in_words": "One thousand eighty dollars",
    "receivables_account": "1234567890"
}

base_inclusive_total_amount = float(data["base_inclusive_total_amount"]) 

def commission_calculations(dbms, object):
   

    system_settings = dbms.system_settings

    setup_settings = dbms.get_doc("Commission_Setup", name=system_settings.default_company, user=object.user)
    settings = setup_settings.data

  
    if setup_settings.status != utils.ok:
        utils.throw("Failed to get commission settings")

    for config in settings.configuration:
     
        for emp in settings.employees:
          
            if emp.user == data["sales_person"]:
                commission_amount = 0
                emp_commission_structure = emp.commission_structure

             
                if config.commission_structure == emp_commission_structure:
                   
                    if config.commission_rate_type == "Fixed Amount":
                        commission_rate = float(config.commission_rate)
                    elif config.commission_rate_type == "Percentage":
                        commission_rate = float(config.commission_rate) / 100
                    else:
                        commission_rate = 0

           
                    utils.pretty_print(commission_rate)
                        
                    if emp_commission_structure == "Percentage of sales revenue":
                        commission_amount = calculate_sales_commission(base_inclusive_total_amount, commission_rate)
                    elif emp_commission_structure == "Referral Commission":
                        commission_amount = calculate_referral_commission(base_inclusive_total_amount, commission_rate)
                    elif emp_commission_structure == "Bonus Commission":
                        sales_target = float(config.minimum_payment_threshold)
                        bonus_amount = commission_rate
                        commission_amount = calculate_bonus_commission(base_inclusive_total_amount, sales_target, bonus_amount)
                        utils.pretty_print(commission_amount)
                    elif emp_commission_structure == "Residual commission":
                        commission_amount = calculate_residual_commission(float(data["base_total_outstanding_amount"]), commission_rate)
                    elif emp_commission_structure == "Override Commission":
                        commission_amount = calculate_override_commission(float(data["base_total_outstanding_amount"]), commission_rate)
                    elif emp_commission_structure == "Flat rate per sale":
                        commission_amount = calculate_flat_rate_commission(commission_rate)

                    # Ensure commission_amount is correctly formatted and within acceptable limits
                    # commission_amount = str(commission_amount)
                    if commission_amount > 0.01:
                        # commission_amount = commission_amount[:255]

                        # Create and save the commission entry
                        entry = utils.from_dict_to_object({})
                        entry.sales_person = data["sales_person"]
                        entry.reference = data["po_no"]
                        entry.inclusive_amount = base_inclusive_total_amount
                        entry.commission_amount = commission_amount
                        entry.commission_type = emp_commission_structure
                        entry.service_or_product = data["description"]
                        entry.status = "Submitted"

                        create_entry = dbms.create("Commission_Entry", entry, object.user)
                        if create_entry.status != utils.ok:
                            return create_entry

    return utils.respond(utils.ok, "Commission calculations and entries successfully processed")
