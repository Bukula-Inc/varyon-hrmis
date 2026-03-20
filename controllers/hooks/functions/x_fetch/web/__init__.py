from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def get_web_content(dbms, object):
    content = utils.from_dict_to_object({})
    module_pricing = dbms.get_list("Module_Pricing", privilege=True, fetch_linked_fields=True,fetch_linked_tables=False)
    module_pricing.status == utils.ok or throw("Failed to fetch web content.")
    module_grouping = dbms.get_list("Module_Group", privilege=True)
    module_grouping.status == utils.ok or throw("Failed to fetch web content.")
    billing_config = dbms.get_doc("Billing_Config", "Billing Config", privilege=True, fetch_linked_fields=True)
    billing_config.status == utils.ok or throw("Failed to fetch web content.")
    tax_template = dbms.get_list("Tax_Template", privilege=True, fetch_linked_fields=False,fetch_linked_tables=True)
    tax_template.status == utils.ok or throw("Failed to fetch web content.")
    license = dbms.get_doc("License","License", privilege=True)
    license.status == utils.ok or throw("Failed to fetch web content.")

    additiona_user_item = dbms.get_doc("Stock_Item",billing_config.data.additional_user_item, privilege=True,fetch_linked_fields=False, fetch_linked_tables=False)
    if additiona_user_item.status == utils.ok:
        billing_config.data.additional_user_item = additiona_user_item.data

    additional_storage_item = dbms.get_doc("Stock_Item", billing_config.data.additional_storage_item, privilege=True, fetch_linked_fields=False, fetch_linked_tables=False)
    if additional_storage_item.status == utils.ok:
        billing_config.data.additional_storage_item = additional_storage_item.data

    module_grouped = utils.array_to_dict(module_grouping.data.rows,"name")
    grouped_pricing = utils.group(module_pricing.data.rows,"module_group")
    for key in utils.get_object_keys(module_grouped):
        if grouped_pricing.get(key):
            module_grouped[key].modules = grouped_pricing.get(key)

    content = {
        "billing_config": billing_config.data,
        "module_group": list(module_grouped.values()),
        "taxes": utils.array_to_dict(tax_template.data.rows,"name"),
        "license":license.data
    }
    return utils.respond(utils.ok, content)



def get_job_openings(dbms, object):
    return_list = []
    core_hr = Core_Hr(dbms)
    get_inst = core_hr.company
    get_hr_settings = dbms.get_doc("Hr_Setting", name=get_inst)
    job_openings = dbms.get_list("Job_Advertisement", filters={"publish": 1, "docstatus": 1}, privilege=True)
    if job_openings.get("status") == utils.ok:
        job_openings = job_openings.get("data").get("rows")
        if job_openings:
            for job_opening in job_openings:
                if job_opening.publish_salary:
                    lower = f"{job_opening.lower_range} {job_opening.currency}" if job_opening.lower_range else ''
                    upper = f"{job_opening.upper_range} {job_opening.currency}" if job_opening.upper_range else ''
                    return_list.append({
                        "id": job_opening.id,
                        "job_title": job_opening.name,
                        "company": job_opening.company,
                        "description": job_opening.description,
                        "designation": job_opening.designation,
                        "salary": f"""{lower}{f' - {upper}' if upper else ''}""",
                    })
                else:
                    return_list.append({
                        "id": job_opening.id,
                        "job_title": job_opening.name,
                        "company": job_opening.company,
                        "description": job_opening.description,
                        "designation": job_opening.designation,
                    })
    medical_clearance = get_hr_settings.data.get("medical_clearance")
    outh_of_secrecy = get_hr_settings.data.get("medical_clearance")
    return utils.respond(utils.ok, {"job_openings": return_list, "medical_clearance": medical_clearance, "oath_of_secrecy":outh_of_secrecy})


