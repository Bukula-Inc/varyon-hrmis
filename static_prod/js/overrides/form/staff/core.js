

const controller =lite.page_controller.form_controller

export const create_jobapplication = (params) => {
    let values = params.values
    values.job_opening = values.name
    values.designation = values.designation
    values.currency = values.currency
    values.lower_range = values.lower_range
    values.upper_range = values.upper_range
   

    delete values.company
    delete values.department
    delete values.description
    
   

   

    lite.session.set_session("clone_doc", values)
    lite.utils.redirect("staff","staff_job_application","new-form","Job_Application")
}


export const time_difference = (params)=>{
    
    const controller = lite.page_controller.form_controller
    let values = { ...params.controller.get_form_data()?.values }
    

    let date1 = new Date(values?.from_date);
    let date2 = new Date(values?.to_date);
     
    // to calculate the time difference of two dates
    let Difference_In_Time = date2.getTime() - date1.getTime();
     
    // to calculate the no. of days between two dates
    let Difference_In_Days = Math.round(Difference_In_Time / (1000 * 60 * 60 * 24));

    
    
    controller.set_form_value(controller.get_form_field("total_days"), Difference_In_Days)    
}

export const req_requested_amount =(data)=>{
    const req_item = controller.get_form_data ()?.values?.purchase_requisition_item;
    let requested_amount =0
    let total_amount =0
    for(let i=0; i<req_item.length; i++){
        total_amount =(parseFloat(req_item[i].unit_price)*parseFloat(req_item[i].qty))
        requested_amount +=total_amount
        controller.set_form_value ($(`#total_amount`), parseFloat(total_amount).toFixed(2))
        controller.set_form_value(controller.get_form_field("total_amount"),parseFloat(total_amount).toFixed(2))
    }
    controller.set_form_value(controller.get_form_field("requested_amount"),parseFloat(requested_amount).toFixed(2))   
    controller.set_form_value(controller.get_form_field("approved_amount"),parseFloat(requested_amount).toFixed(2))   
}

export const retire_imprest = (params) => {
    let values = params.values
    values.imprest = values.name
    values.currency = values.request_currency
    values.balance = values.balance
    lite.session.set_session("clone_doc", values)
    lite.utils.redirect("staff","staff_imprest","new-form","Imprest Retirement",null,true)
}

export const recalculate_imprest = async (params) =>{
    const controller = params.controller
    const values = controller.get_form_data().values
    let requested_amount = lite.utils.string_to_float(values.requested_amount)
    let approved_amount = lite.utils.string_to_float(values.approved_amount)
    let credit_amount = 0, debit_amount = 0
    if(requested_amount && !approved_amount){
        approved_amount = requested_amount
    }
    if(approved_amount && !requested_amount){
        requested_amount = approved_amount
    }
    controller.set_form_value(controller.get_form_field("approved_amount"), approved_amount,null, false)
    if(approved_amount > 0){
        const approved_amount_in_reporting_currency = await lite.currency.convert_currency(values.request_currency, values.reporting_currency,approved_amount,null)
        if(approved_amount_in_reporting_currency.status === lite.status_codes.ok){
            const cr = approved_amount_in_reporting_currency.data
            controller.set_form_value(controller.get_form_field("approved_amount_in_reporting_currency"), cr.converted_amount,null, false)
            controller.set_form_value(controller.get_form_field("requested_to_credit_convertion_rate"), cr.exchange_rate,null, false)
        }
        if(values.credit_account && values.credit_account_currency){
            const converted = await lite.currency.convert_currency(values.request_currency, values.credit_account_currency,approved_amount)
            if(converted.status === lite.status_codes.ok){
                const cr = converted.data
                credit_amount = cr.converted_amount
                controller.set_form_value(controller.get_form_field("credit_amount"), credit_amount,null, false)
                controller.set_form_value(controller.get_form_field("credit_to_reporting_convertion_rate"), converted.converted_amount, null, false)
            }
        }
        if(values.debit_account && values.debit_account_currency){
            const converted = await lite.currency.convert_currency(values.credit_account_currency, values.debit_account_currency,credit_amount)
            if(converted.status === lite.status_codes.ok){
                const dr = converted.data
                debit_amount = dr.converted_amount
                controller.set_form_value(controller.get_form_field("debit_amount"), credit_amount, null, false)
                controller.set_form_value(controller.get_form_field("credit_to_debit_convertion_rate"), dr.exchange_rate, null, false)
            }
        }
        controller.set_form_value(controller.get_form_field("balance"), approved_amount, null, false)
    }
}

export const validate_imprest = (params) =>{
    const values = params.values
    const req_amount = lite.utils.string_to_float(values.requested_amount)
    if(!req_amount){
        lite.alerts.toast({toast_type: lite.status_codes.not_found,title:"Requested Amount Required", message:"Please provide the amount you are requesting for requested."})
        return false
    }
}


export const recalculate_imprest_retirement = async (params)=>{
    const {controller} = params
    const {values} = controller.get_form_data()
    const {currency, retirement_item, reporting_currency} = values
    if (values.imprest){
        const imprest = await lite.connect.get_doc("Imprest", values.imprest)
        if(imprest.status === lite.status_codes.ok){
            let balance = imprest.data.balance
            let new_balance = 0
            let total_retired = 0
            if(lite.utils.array_has_data(retirement_item)){
               
                $.each(retirement_item,(_,itm)=>{
                    const {amount, debit_account, credit_account, debit_account_currency, credit_account_currency} = itm
                    total_retired += lite.utils.string_to_float(amount)
                    if(amount && debit_account && credit_account && debit_account_currency && credit_account_currency){
                        
                    }
                })
                new_balance = balance - total_retired
                controller.set_form_value(controller.get_form_field("total_items"), retirement_item?.length, lite.utils.thousand_separator(retirement_item?.length, 0), false)
                controller.set_form_value(controller.get_form_field("balance"), new_balance, lite.utils.currency(new_balance, lite.currency_decimals,currency), false)
                controller.set_form_value(controller.get_form_field("total_retirement"), total_retired, lite.utils.currency(total_retired, lite.currency_decimals,currency), false)
            }
        }
        
    }
    
}
export const get_full_name = (params) => {
    const controller = lite.page_controller.form_controller
    let values = { ...params.controller.get_form_data()?.values }     
    let name = `${values?.first_name} ${values?.last_name}`
    controller.set_form_value(controller.get_form_field("full_name"), name)
}

export const apply_for_training_program = (params) => {
  
    lite.utils.redirect("staff","scholarship","new-form","scholarship")
}


export const on_approval_preload = async(params)=>{
    const {status, data, error_message} = await lite.connect.core("get_approval_doc_config", {doc: lite.utils.get_url_parameters("doc")})
    return data
}
export const staff_survey_feedback = async (params) =>{
    const page = lite.utils.get_url_parameters("page")  
    const controller = lite.page_controller.form_controller
    const q_tions = await lite.connect.x_post("staff_survey_feedback", params.value)
    console.log(q_tions);
    
   if (q_tions.status = lite.status_codes.ok){
        if (page === "new-form"){ const survey_queestion = q_tions.data.welfare_questions
            controller.populate_child_table ("question_ans", survey_queestion || [])
        }
        if (page === "new-form"){ const questionnair = q_tions.data.questionnaire
            controller.populate_child_table ("staff_welfare_questionnair", questionnair || [])
        }
   }
}
export const interview_rating_staff = async ({controller, value}) => {
    const loader_id = lite.alerts.loading_toast({title: `Processing Interview Rate`, message:"Please wait while Your submit your rating."})
    const res = await lite.connect.x_post ("interview_rating_by_staff", {emp: value})
    console.log(res);
    lite.alerts.destroy_toast(loader_id)
    if (res.status != lite.status_codes.ok) {lite.alerts.toast({toast_type:lite.status_codes.ok, title:"Rates Not Found", message:`You have no rates to submit`})
            return
    }else {
        controller.populate_child_table ("practical_rating", res.data.practical_rating)
        controller.populate_child_table ("competess_rating", res.data.competess_rating)
        controller.populate_child_table ("skills_rating", res.data.data)
        controller.populate_child_table ("qualifications", res.data.qualification)
        controller.set_form_value(controller.get_form_field("applicant"), res.data?.applicant_name)
        return
    }
}

export const recalculate_imprest_retirement_expenses =async(params)=>{
    const {controller, value} =params
    const form_values =controller.get_form_data()?.values
    let summed_total_amount =lite.utils.string_to_float(form_values.retired_amount) || 0
    const child_items = params.controller.get_table_rows("areas_of_expense")
    let total_amount =lite.utils.string_to_float(form_values.retired_amount) || 0;
    $.each (child_items, async (_, itemRow) => {
        const prev_total =lite.utils.string_to_float(itemRow?.total_spent?.value) || 0
        total_amount =(lite.utils.string_to_float(itemRow?.usage_length?.value || 0.00)) *(lite.utils.string_to_float(itemRow?.unit_price_of_usage?.value || 0.00) || 0.00)
        summed_total_amount +=lite.utils.string_to_float(total_amount || 0.00) -(lite.utils.string_to_float(prev_total) || 0.00)
        params.controller.set_form_table_value("areas_of_expense", itemRow?.total_spent?.row_id, itemRow?.total_spent?.field, !isNaN (total_amount) ? total_amount : (lite.utils.string_to_float(total_amount) || 0.00))
        console.log(itemRow?.usage_length?.value, itemRow?.unit_price_of_usage?.value)
    }) 
    const balance =(lite.utils.string_to_float(form_values?.pending) || 0) -(lite.utils.string_to_float(summed_total_amount) || 0)
    
    controller.set_form_value(controller.get_form_field("retired_amount"), !isNaN (summed_total_amount) ? summed_total_amount : lite.utils.string_to_float (summed_total_amount))
    controller.set_form_value(controller.get_form_field("balance_left"), balance || 0)
}

export const popluate_imprest_data =async(params)=>{
    const {controller, value} =params
    console.log("We are good to go...");  
}