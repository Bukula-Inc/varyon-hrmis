from controllers.utils import Utils

utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def update_docs(dbms, old_company, new_comapny, doc, field, filter, muilt, second_field,):

    if filter ==0:
        fetch_docs =dbms.get_doc(doc, old_company.data.name, privilege=True, fetch_by_field=field)
        if fetch_docs.status == utils.ok and old_company.data.name != new_comapny.name:
            try:
                doc_data = fetch_docs.data 
                if muilt ==1: 
                    doc_data[second_field] =new_comapny.name
                doc_data[field] = new_comapny.name

                docs_update = dbms.update(doc, doc_data, privilege=True, update_submitted=True)
                return docs_update
            except Exception as e:
                    pp(f"An Error Occured when updating {doc_data.name}")
        
        else:
            return fetch_docs
    else :
        fetch_docs = dbms.get_list(doc, filters={field: old_company.data.name}, privilege=True,)
        if fetch_docs.status == utils.ok and old_company.data.name != new_comapny.name:
            for doc_data in fetch_docs.data.rows:
                try:
                    doc_data[field] = new_comapny.name
                    if muilt ==1: 
                        doc_data[second_field] =new_comapny.name
                    if doc =="Lite_User":
                        if doc_data.has_changed_default_password and not doc_data.has_changed_default_password:
                            doc_data.has_changed_default_password =0

                    doc_data_update = dbms.update(doc, doc_data, privilege=True, update_submitted=True)
                except Exception as e:
                    pp(f"An Error Occured when updating {doc_data.name}")

        else:
            return fetch_docs



def before_company_update(dbms, object):
    body = object.body

    models_list =[
        utils.from_dict_to_object({"model":"Lite_User", "field": "default_company", "filter": 1,  "muilt_fields": 0, "second_field": ""}),
        utils.from_dict_to_object({"model":"Hr_Setting", "field":"name", "muilt_fields": 0, "filter": 0, "second_field": ""}),
        utils.from_dict_to_object({"model":"Payroll_Setup", "field":"name", "muilt_fields": 0, "filter": 0, "second_field": ""}),
        utils.from_dict_to_object({"model":"Bonus_Setting", "field":"name", "muilt_fields": 0, "filter": 0, "second_field": ""}),
        utils.from_dict_to_object({"model":"Training_Program", "field":"company", "muilt_fields": 0, "filter":0, "second_field": ""}),
        utils.from_dict_to_object({"model":"Self_Appraisal", "field":"company", "second_field": "appraisal_setup", "muilt_fields": 1, "filter":1}),
        utils.from_dict_to_object({"model":"Leave_Application", "field":"company", "muilt_fields": 0, "filter":0, "second_field": ""}),
        utils.from_dict_to_object({"model":"Overtime_Configuration", "field":"name", "muilt_fields": 0, "filter":0, "second_field": ""}),
        utils.from_dict_to_object({"model":"Employee_Grade", "field":"company", "muilt_fields": 0, "filter":1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Commission_Setup", "field":"name", "muilt_fields": 0, "filter":0, "second_field": ""}),
        utils.from_dict_to_object({"model":"Work_Plan", "field":"company", "muilt_fields": 0, "filter":1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Job_Advertisement", "field":"company", "muilt_fields": 0, "filter":1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Job_Offer", "field":"company", "muilt_fields": 0, "filter":1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Gratuity_Configuration", "field":"name", "muilt_fields": 0, "filter":0, "second_field": ""}),
        utils.from_dict_to_object({"model":"Final_Statement", "field":"company", "muilt_fields": 0, "filter":1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Exit_Interview", "field":"company", "muilt_fields": 0, "filter":1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Employee", "field":"company", "muilt_fields": 0, "filter":1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Employee", "field":"company", "muilt_fields": 0, "filter":1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Employee_File", "field":"company", "muilt_fields": 0, "filter": 1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Employee_Attendance", "field":"name", "muilt_fields": 0, "filter": 1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Disciplinary_Committee", "field":"company", "muilt_fields": 0, "filter": 1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Hr_Contract", "field":"company", "muilt_fields": 0, "filter": 1, "second_field": ""}),
        utils.from_dict_to_object({"model":"Appointment_Letter", "field":"company", "muilt_fields": 0, "filter": 1, "second_field": ""}),
        # utils.from_dict_to_object({"model":"Disciplinary_Committee", "field":"company", "muilt_fields": 0, "filter": 1, "second_field": "" }),
        # utils.from_dict_to_object({"model":"Disciplinary_Committee", "field":"company", "muilt_fields": 0, "filter": 1, "second_field": "" }),
    ]


    old_company = dbms.get_doc("Company", body.id, privilege=True, fetch_by_field="id")
    if old_company.status == utils.ok:
        # update_docs(dbms, old_company=old_company, new_comapny=body, doc=models_list[1].model, field=models_list[1].field, filter=models_list[1].filter, muilt=models_list[1].muilt_fields, second_field=models_list[1].second_field)
        for doc in models_list:            
            updated_doc =update_docs(dbms, old_company=old_company, new_comapny=body, doc=doc.model, field=doc.field, filter=doc.filter, muilt=doc.muilt_fields, second_field=doc.second_field)
        # throw("old_company")Overtime_Configuration
        # update = dbms.update("Company", body, privilege=True, skip_hooks=True)
