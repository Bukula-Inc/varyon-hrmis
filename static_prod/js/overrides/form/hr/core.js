import HR_HTML_Generator from "../../../page/html/hr_html_generator.js"

export const add_paye_to_all_employees = async ({form_controller}) => {
    const loader_id = lite.alerts.loading_toast({
        title: `Adding Paye To Employees`,
        message:`Please wait while we add paye Employee`
    })
    const add_paye_to_all_employees_ = await lite.connect.x_fetch ("add_paye_to_all_employees")
    lite.alerts.destroy_toast(loader_id)
    if(add_paye_to_all_employees_.status === lite.status_codes.ok){
        lite.alerts.toast({
            toast_type:lite.status_codes.ok,
            title:"Added Paye Status",
            message:`Add Paye was Successfully`
        })
    }
}

export const normalize_emp_info = async ({form_controller}) => {
    const loader_id = lite.alerts.loading_toast({
        title: `Normalization Submission`,
        message:`Please wait while we Normalize Employee`
    })
    const normalize_emp_information = await lite.connect.x_fetch ("normalize_emp_information")
    lite.alerts.destroy_toast(loader_id)
    if(normalize_emp_information.status === lite.status_codes.ok){
        lite.alerts.toast({
            toast_type:lite.status_codes.ok,
            title:"Normalization Status",
            message:`Normalization was Successfully`
        })
    }else {
        lite.alerts.toast({
            toast_type:lite.status_codes.no_content,
            title:"SNormalization Failed",
            message:`Failed to Normalize`
        })
    }

}

export const separate_with_separated_employees = async ({form_controller}) => {
    const get_separated_employees = await lite.connect.x_fetch ("get_separated_employees")
    const separated_employees = {
        employees: get_separated_employees?.data || []
    }
    const quick_modal = await lite.modals.quick_form("hr", "separate_with_separated_employees", async (values,setup)=>{
        const loader_id = lite.alerts.loading_toast({
            title: `Separating With Separated Employees`,
            message:`Please wait while we do the separation`
        })
        lite.modals.close_modal(quick_modal.modal_id)
        const save = await lite.connect.x_post("separate_with_separated_employees", values)
        lite.alerts.destroy_toast(loader_id)
        if(save.status === lite.status_codes.ok){
            lite.alerts.toast({
                toast_type:lite.status_codes.ok,
                title:"Separation was Successfully",
                message:`Separation was Successfully`
            })
        }else {
            lite.alerts.toast({
                toast_type:lite.status_codes.no_content,
                title:"Separation was Failed",
                message:`Failed to Separate`
            })
        }
    },null,separated_employees)
}

export const prepopulated_behavioral_imperatives = async ({controller}) => {
    if (lite.form_state == "new" ) {
        const res = await lite.connect.x_fetch ("behavioral_imperative",)
        console.log(res);
        
        if (res.status == lite.status_codes.ok) {
            controller.populate_child_table ("behavioral_imperative", res.data.behavioral_imperative)
        }
        else {
            lite.alerts.toast(
                {
                    toast_type:lite.status_codes.no_content,
                    title:"There Is An Issue",
                    message:`Failed to fetch Behavioral Imperatives`
                }
            )
        }
    }
}

export const reinstate_employee = async ({form_controller}) => {
    const values = form_controller.get_form_data ()?.values
    const loader_id = lite.alerts.loading_toast({
        title: `GETTING STATUTORY COMPONENTS`,
        message:"Please wait while We're fetching."
    })
    const res = await lite.connect.x_post ("reinstate_employee", {emp: values?.name})
    lite.alerts.destroy_toast(loader_id)

    if (res.status == lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type: lite.status_codes.ok,
            title: "REINSTATE SUCCEEDED",
            message: "Employee Reinstated Successfully"
        })
        form_controller.init_form ()
        return
    }
    return
}
export const get_job_opening = async ({controller, value}) => {
    if (value != lite.form_data.job_opening) {
        const opening = await lite.connect.x_post ('get_job_opening_application', {job_opening:value})
        if (opening.status == lite.status_codes.ok) {
            const qualifications = opening.data.qualification
            const skill = opening.data.skill
            controller.populate_child_table ("attachments", qualifications)
            controller.populate_child_table ("job_skills", skill)
        }
    }
}
export const commutated_leave_days = ({ controller }) => {
    const values = controller.get_form_data()?.values;
    
    if (values?.commutable_days < values?.commutated_days) {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "DAYS ERROR",
            message: "Commutable Days are Less than Commuted Day"
        });
        controller.set_form_value(controller.get_form_field("amount"), '0.00')
        controller.set_form_value(controller.get_form_field("commutated_days"), '0')
    }
    if (values?.basic_pay && values?.working_days && values?.commutated_days) {
        const commuted_leave_days_amount = (parseFloat(values.basic_pay) / parseFloat(values.working_days)) * parseFloat(values.commutated_days);
        const formatted_amount = lite.utils.thousand_separator(parseFloat(commuted_leave_days_amount), lite?.currency_decimals);
        
        controller.set_form_value(controller.get_form_field("amount"), formatted_amount);
    }
};

export const get_emp_by_policy = async ({controller, value}) => {
    let name =null
    
    if(lite?.utils?.get_url_parameters("page") == "info"){
        name =controller?.get_form_data()?.values?.name
    }
    const res = await lite.connect.x_post ("filter_emps_by_policys_category", {policy: value, doc_name: name})
    
    const employees = []
    if (res.status == lite.status_codes.ok) {
        if (res.data.data.length > 0) $.each (res.data.data, (_, emp) => {
            employees.push (emp)
        })
    }

    controller.set_form_value (controller.get_form_field ("main_leave_type"), "")
    controller.populate_child_table ("leave_allocation_employees", employees)
}

export const get_leave_type = async ({controller, value}) => {
    if (value !== lite.form_data.main_leave_type) {
        const employees = []
        const res = await lite.connect.x_post ("get_leave_type", {type: value})
        if (res.status == lite.status_codes.ok) {
            if (res.data.data.length > 0) $.each (res.data.data, (_, emp) => {
                employees.push (
                    {
                        employee: emp.name,
                        employee_name: emp.full_name,
                        employee_designation: emp.designation,
                        department: emp.department,
                        leave_type: value,
                    }
                )
            })
        }
        controller.set_form_value (controller.get_form_field ("main_policy"), "")
        controller.populate_child_table ("leave_allocation_employees", employees)
    }
}

export const years_checker = ({controller}) => {
    let values = controller.get_form_data()?.values
    let date1 = new Date(values?.d_o_b);
    let date2 = new Date(values?.date_of_joining);

    if (!date1 || isNaN(date1.getTime())) {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID DATE FORMAT",
            message: "Please Enter a valid Date of Birth"
        });
        return false;
    }

    if (!date2 || isNaN(date2.getTime())) {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID DATE FORMAT",
            message: "Please Enter a valid Date of Joining"
        });
        return false;
    }
    if (dateDiffInYears (date1, date2) < 18) {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: "INVALID AGE",
            message: `Age restriction: Individual is below 18`
        })
        return
    }
}
export const on_bonus_percentage = ({controller}) => {
    const values = controller.get_form_data ()?.values
    const bonus_amount =  values?.bonus_amount
    const employees = controller.get_table_rows("bonus_employees")
    $.each (employees, (_, el) => {
        const amount = (parseFloat(el?.is_percentage.value) / 100) * bonus_amount
        controller.set_form_table_value("bonus_employees", el.bonus_amount?.row_id, el?.bonus_amount?.field,  parseFloat(amount).toFixed(2))
    })
}
export const on_bonus_amount_to_percentage = ({controller, value}) => {
    const values = controller.get_form_data ()?.values
    const bonus_amount =  values?.bonus_amount
    const employees = controller.get_table_rows("bonus_employees")
    $.each (employees, (_, el) => {
        const amount = (parseFloat(value) / bonus_amount) * 100
        controller.set_form_table_value("bonus_employees", el.is_percentage?.row_id, el?.is_percentage?.field,  parseFloat(amount).toFixed(2))
    })
    
}
export const interview_rating_validation = ({controller}) => {
    const value = controller.get_form_data()?.values
    // const form_controller = lite.page_controller.form_controller
    let skills_rates = value.skills_rating
    skills_rates.forEach((skill) => {
        if (skill.rating > 10){
            lite.alerts.toast({toast_type: lite.status_codes.forbidden,title: "WRONG RATING", message: "You can only rate out of 10"}); 
            controller.set_form_value(controller.get_form_field("skills_rating"), "0") 
        }
    });
}
export const on_load_emp_load = async ({controller}) => {
    if (!controller.is_new_form) {
        $ ("#create_user").hide ()
        $ ("#main_role").hide ()
        $ ("#temporal_user").hide ()
        $ ("#basic-pay").hide ()
        const loader_id = lite.alerts.loading_toast({
            title: `GETTING STATUTORY COMPONENTS`, 
            message:"Please wait while We're fetching."
        })
        const salary_components = await lite.connect.x_fetch ("get_salary_components")
        if (salary_components.status == lite.status_codes.ok) {
            lite.alerts.destroy_toast(loader_id)
            const success_id =lite.alerts.toast({ toast_type: lite.status_codes.ok, title: "SUCCESSFUL", message: "Fetch Was Successful" });
            lite.alerts.destroy_toast(success_id)
            let deductions = []
            let earnings = []
            if (salary_components.data) {
                $.each (salary_components.data, (_, ele) => {
                    if (ele.component_type == "Deduction") {
                        deductions.push ({
                            deduction: ele.name
                        })
                    }else if (ele.component_type == "Earning") {
                        earnings.push ({
                            earning: ele.name
                        })
                    }
                })
            }
            controller.populate_child_table ("earnings", earnings)
            controller.populate_child_table ("deductions", deductions)
        }else {
            lite.alerts.destroy_toast(loader_id)
            const success_id =lite.alerts.toast({ toast_type: lite.status_codes.no_content, title: "COULDN't FETCH", message: `No Statutory Components Found` });
            lite.alerts.destroy_toast(success_id)
        }
    }
} 

export const recalculate_expense_total = ({controller}) => {
    const form_controller = lite.page_controller.form_controller
    const expenses = controller.get_form_data ()?.values.expenses
    let total = 0
    $.each (expenses, (_, expense) => {
        total += parseInt (expense.amount)
    })

    form_controller.set_form_value(form_controller.get_form_field ("training_expense"), total)

}
export const on_exit_interview_questionnair = async (params) => {  
    const page = lite.utils.get_url_parameters("page")  
    const controller = lite.page_controller.form_controller
    const response = await lite.connect.x_post('questions', { name: params.value })  
            
    if (response.status == lite.status_codes.ok) {
        if (page === "new-form"){const objectives_data = response.data
            controller.populate_child_table ("questions", objectives_data || [])
        }else {
            controller.populate_child_table ("Questions", null)
        }
            
    }
}

export const pull_questiones = async (params) => {  
    const value = params.value
    const page = lite.utils.get_url_parameters("page")  
    const controller = lite.page_controller.form_controller    
    controller.set_form_value(controller.get_form_field ("name"), value)
    const response = await lite.connect.x_post('questions', { name: params.value })  
            
    if (response.status == lite.status_codes.ok) {
        if (page === "new-form"){const objectives_data = response.data
            controller.populate_child_table ("questions", objectives_data || [])
        }
            
    }
}

export const create_case_outcome_from_grievance = (params) => {
    const values = params.values
   
    const value = {
        subject: values.grievance_against,
        name: values.name,
        date_of_warning: values.grievance_date,
        type_displineray: "Clean Resolve",
    }
    lite.session.set_session("clone_doc", value)
    lite.utils.redirect("hr","case_outcome","new-form","case outcome")
}
export const generate_final_statement = (params) => {
    const values = params.values
   
    const value = {
        employee_id: values.employee,
        name: values.name,
        department: values.department,
        designation: values.designation,
        company: values.company,
        transaction_date: lite.utils.today()
    }
    lite.session.set_session("clone_doc", value)
    lite.utils.redirect("hr","final_statement","new-form","Final Statement")
} 

export const do_exit_interview = (params) => {
    const values = params.values
   
    const value = {
        employee: values.employee,
        employee_name: values.employee_name,
        department: values.department,
        designation: values.designation,
        company: lite.user.company.name,
    }
    lite.session.set_session("clone_doc", value)
    lite.utils.redirect("hr","exit_interview","new-form","exit interview")
}

export const count_week_days = (startDate, endDate, holidays = [], remove_saturday=true, remove_sunday=true) => {
    const start = new Date(startDate)
    const end = new Date(endDate)
    const holidayDates = holidays.map(date => new Date(date))
    function* dateGenerator() {
        while (start <= end) {
            yield new Date(start)
            start.setDate(start.getDate() + 1)
        }
    }
    return [...dateGenerator()].filter(date => {
        const isNotHoliday = !holidayDates.some(holiday => date.getTime() === holiday.getTime())
        if (remove_saturday && remove_sunday) {
            const isWeekday = date.getDay() !== 0 && date.getDay() !== 6
            return isWeekday && isNotHoliday
        }else if (remove_sunday) {
            const isWeekday = date.getDay() !== 0
            return isWeekday && isNotHoliday
        }else if (remove_saturday) {
            const isWeekday = date.getDay() !== 6
            return isWeekday && isNotHoliday
        }else {
            return isNotHoliday
        }
    }).length
}

export const on_create_user = async ({controller, value}) => {
    const form_controller = lite.page_controller.form_controller
    const form_values = controller.get_form_data ()?.values
    if (!form_values?.email) {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: "REQUIRED",
            message: `Email is equal required`
        })
        return
    }
    if (!form_values?.last_name) {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: "REQUIRED",
            message: `Last Name is equal required`
        })
        return
    }
    if (!form_values?.first_name) {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: "REQUIRED",
            message: `First Name is equal required`
        })
    }
    if (!form_values?.department) {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: "REQUIRED",
            message: `Department is equal required`
        })
        return
    }

    const user = {
        "email" : form_values?.email,
        "department": form_values?.department,
        "first_name": form_values?.first_name,
        "contact_no": form_values?.contact,
        "middle_name": form_values?.middle_name ? form_values?.middle_name : "",
        "last_name": form_values?.last_name,
        "main_role": value
    }
    const loader_id = lite.alerts.loading_toast({
        title: `Creating ${user.first_name} Employee`, 
        message: `Please wait while the system is Creating ${user.first_name} information.`
    })
    const r = await lite.connect.x_post ("create_user_form_employee", user)
    if (r.status == lite.status_codes.ok) {
        lite.alerts.destroy_toast(loader_id)
        lite.alerts.toast({
            toast_type: lite.status_codes.created,
            title: "Created",
            message: r.data
        })
        form_controller.set_form_value(form_controller.get_form_field ("user"), user.email)
        form_controller.set_form_value(form_controller.get_form_field ("temporal_user"), user.email)
        return
    }else {
        lite.alerts.destroy_toast(loader_id)
        lite.alerts.toast({
            toast_type: lite.status_codes.bad_request,
            title: "Failed",
            message: r.data
        })
        return
    }
}

export const func = (data) => {
    const controller = lite.page_controller.form_controller
    const staffing_details = controller.get_table_rows("staffing_details")

    let total = 0
    $.each(staffing_details, (index, staff_details_row)=> {
        const value = parseFloat(staff_details_row?.vacancies?.value) *parseFloat(staff_details_row?.estimated_cost?.value) * 12
        if(!isNaN(value)){
            total+=value
            controller.set_form_value(staff_details_row?.total_cost.field, parseFloat(value).toFixed(2))

        }else{
            controller.set_form_value(staff_details_row?.total_cost.field, '0.00')
        }

        if(!isNaN(value)){
            controller.set_form_value(staff_details_row?.total_cost.field, value)
    
            }else{
                controller.set_form_value(staff_details_row?.total_cost.field, '0.00')
            }
    })
     
    controller.set_form_value(controller.get_form_field("total_estimated"), total)
    
}

export const get_emp_name = (params) => {
    const controller = lite.page_controller.form_controller
    let values = { ...params.controller.get_form_data()?.values}
    const middle_name = values.middle_name ? values?.middle_name : ""
    let name = `${values?.first_name} ${middle_name} ${values?.last_name}`
    controller.set_form_value(controller.get_form_field("full_name"), name)
}

export const on_employee_grade_change = async ({value}) => {
    const controller = lite.page_controller.form_controller
    const grade = await lite.connect.get_doc("Employee_Grade", value)

    if (grade.status===lite.status_codes.ok){
        const grade_data=grade.data
        const basic_pay_field = controller.get_form_field("basic_pay") || controller.get_form_field("revised_basic")
        controller.set_form_value(basic_pay_field,grade_data.basic_pay)

        if (!lite.utils.is_empty_array(grade_data.earnings)){
            let earnings = []
            $.each(grade_data.earnings,(_,e)=>{
                earnings.push({earning:e.component})
            })
             controller.populate_child_table("earnings",earnings)
            
        }

        if (!lite.utils.is_empty_array(grade_data.deductions)){
            let deductions = []
            $.each(grade_data.deductions,(_,d)=>{
                deductions.push({deduction:d.component})
            })
            controller.populate_child_table("deductions",deductions)
            
        }

    
    }
 
}
    

export const leave_hours = ({controller}) => {
    const vls = controller.get_form_data ()?.values
    if (lite.form_data.to_time == vls.to_time) return
    console.log('====================================');
    console.log(vls);
    console.log('====================================');
    if (vls.from_time && vls.to_time) {
        const from_time = new Date(`1970-01-01T${vls.from_time}:00`)
        const to_time = new Date(`1970-01-01T${vls.to_time}:00`)
        const difference_in_milliseconds = to_time - from_time
        if (difference_in_milliseconds < 0) {
            lite.alerts.toast ({
                toast_type: lite.status_codes.no_content,
                title: "Time Mismatch",
                message: `Time from time (${from_time}) is greater than to time (${to_time}).`
            })
        }
        controller.set_form_value (controller.get_form_field ("total_days"), difference_in_milliseconds)
        const difference_n_milliseconds = Math.floor(difference_in_milliseconds / 60000)
        const hours = Math.floor(difference_n_milliseconds / 60)
        const minutes = difference_n_milliseconds % 60
        controller.set_form_value (controller.get_form_field ("time_duration_formatted"), `${hours} Hrs and ${minutes} Min`)
    }
    return
}

export const leave_days = async (params) => {
    if (lite.form_data.to_date == params.value) return
    const controller = lite.page_controller.form_controller
    let values = { ...params.controller.get_form_data()?.values }
    if (!values?.leave_type) {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: "LEAVE TYPE MISSING",
            message: `Select A Leave Type`
        })
        return
    }
    const levty = await lite.connect.get_doc ("Leave_Type", values?.leave_type)
    if (levty?.status == lite.status_codes.ok) {
        // add logic to handle Leave days Type
        const holidays = await lite.connect.x_fetch ("get_holidays")
        if (holidays.status == lite.status_codes.ok) {
            const holiday = holidays.data.data
            const leave_days_calc = count_week_days (new Date(values?.from_date), new Date(values?.to_date), holiday)
            controller.set_form_value(controller.get_form_field("total_days"), leave_days_calc)
            controller.set_form_value (controller.get_form_field ("time_duration_formatted"), `${leave_days_calc} Days`)
        }else {
            lite.alerts.toast({
                toast_type: lite.status_codes.forbidden,
                title: "Holidays Error",
                message: `System Did Find Any Holidays`
            })
        }
    }
    return
}

export const leave_date_validate = (params) => {
    const controller = lite.page_controller.form_controller
    let values = { ...params.controller.get_form_data()?.values }
    if (values.leave_mode == "Hourly Leave") return
    let date1 = new Date(values?.from_date)
    let date2 = new Date(values?.to_date)
    if (date1 < date2) {
        return true
    } else if (date1 > date2) {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID DATE FORMAT",
            message: `${values?.from_date} is after ${values?.to_date}`
        })
        return false
    } else {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "VALID DATE FORMAT",
            message: `${values?.from_date} is equal to ${values?.to_date}`
        })
        return false
    }

}

export const allocate_leave = (params) => {
    let values = params.values
    lite.session.set_session("clone_doc", {leave_allocation_employees: [{employee: values.name}]})
    lite.utils.redirect("hr","leave_allocation","new-form","Leave Allocation")
}

export const create_employee_separation = (params) => {
    const values = params.values
    lite.session.set_session("clone_doc", {employee: values.name})
    lite.utils.redirect("hr","employee_separation","new-form","employee separation")
}

export const create_employee_promotion = (params) => {
    let values = params.values
    values.employee = values.name
    values.employee_name = values.full_name
    values.salary_currency = values.currency
    values.current_basic = values.basic_pay
    delete values.gender
    delete values.salutation
    delete values.designation
    delete values.branch
    delete values.d_o_b
    delete values.nrc_no
    delete values.employment_type
    delete values.status
    delete values.date_of_joining
    delete values.report_to
    delete values.leave_approver
    delete values.shift_approver
    delete values.requisition_approver
    delete values.basic_pay
    delete values.currency
    delete values.account_no
    delete values.sort_code
    delete values.employee_grade
    delete values.tax_band
    delete values.earnings
    delete values.deductions
    lite.session.set_session("clone_doc", values)
    lite.utils.redirect("hr","employee_promotion", "new-form", "Employee Promotion")
}


export const renew_contract = (params) => {
    let values = params.values
    values.company = values.company
    values.contract_type = values.contract_type
    values.effective_date = values.effective_date
    values.end_date = values.end_date
    values.employee = values.employee
    values.name = values.name
    values.period = values.period
    lite.session.set_session("clone_doc", values)
    lite.utils.redirect("hr","contract","new-form","Contract")
}


export const terminate_contract = async (params) =>  {
    const values = params.values
    const value = {
        employee: values.employee,
        employee_name: values.full_name,
        department: values.department,
        designation: values.designation,
        last_day_of_work: values.end_date,
        company: lite.user.company.name,
    }
    lite.session.set_session("clone_doc", value)
    lite.utils.redirect("hr","employee_separation","new-form","Employee Separation")
}
export const appraisal_setup = (params) => {
    let values = params.values
    values.name = values.name
    values.first_name = values.full_name
    values.department = values.department
    lite.session.set_session("clone_doc", {"appraisee": values.name})
    lite.utils.redirect("hr","appraisal","new-form","Appraisal")
}

export const create_interview = (params) => {
    let values = params.values
    values.interviewer_schedule = values.name
    values.interview_type = values.interview_type
    values.schedule = values.schedule
    values.from_time = values.from_time
    values.to_time = values.to_time
    values.application = values.application
    values.interview_status = values.interview_status
    values.interviewer = values.interviewer
    
    lite.session.set_session("clone_doc", values)
    lite.utils.redirect("hr","interview","new-form","Interview")
}

export const open_case_outcome = async(params) => {
    let values = params.values,
        id =null
    ;
    values.employee_disciplinary = values.name
    const case_out_come =await lite?.connect?.x_post("fetch_case_out_come_id", values.name)
    console.log(case_out_come);
    

    if(case_out_come.status ==lite?.status_codes.ok){
        id =case_out_come.data.rows
        console.log(case_out_come, id);
        
        lite.utils.redirect("hr","case_outcome","info","Case Outcome", `doc=${id}`)
    } else{
        lite.alerts.toast({
            toast_type: case_out_come.status,
            title: "Error Fetching The Id",
            message: case_out_come.error_message || "Case out come doc not found"
        })
    } 
    
    

}

export const create_training_feedback = (params) => {
    let values = params.values
    values.training_event = values.name
    values.event = values.name
    values.trainer_name = values.trainer
    values.event_course = values.course

    delete values.training_program
    delete values.company
    delete values.event_status
    delete values.type
    delete values.level
    delete values.has_certificate
    delete values.trainer_email
    delete values.contact
    delete values.supplier
    delete values.location
    delete values.start_time
    delete values.end_time
    delete values.introduction
    delete values.employees
   
    
    lite.session.set_session("clone_doc", values)
    lite.utils.redirect("hr","training_feedback","new-form","Training Feedback")
}


export const create_jobopening = (params) => {
    let values = params.values
    values.name = values.name
    values.department = values.department
    values.company = values.company
    values.designation = values.designation
    values.to_time = values.to_time
    values.application = values.application
    values.interview_status = values.interview_status
    values.interviewer = values.interviewer

    delete values.total_estimated
    
    lite.session.set_session("clone_doc", values)
    lite.utils.redirect("hr","job_opening","new-form","Job_Advertisement")
}

export const consider_applicant = async (params) => {
    let values = params.values
    const controller = params.form_controller 
    const application = await lite.connect.x_post ("get__job_application_details", {application: values.applicant})
    if (application.status == lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type: lite.status_codes.ok,
            title: "Applicant Considered",
            message: `An Email Has Been Sent to The Applicant For Further Steps`
        })
    }
}
export const reverse_job_cons = async (params) => {
    let values = params.values
    const controller = params.form_controller 
    const application = await lite.connect.x_post ("reverse_job_consideration", {application: values.applicant})
    if (application.status == lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type: lite.status_codes.ok,
            title: "Applicant Considered",
            message: `An Email Has Been Sent to The Applicant For Further Steps`
        })
    }
}

export const create_job_offer = async (params) => {
    let values = params.values
    const data = {"interview": values.name, "applicant_name": values.applicant,"applicant_email": values.email,"designation": values.designation,}
    lite.session.set_session("clone_doc", data)
    lite.utils.redirect("hr","job_offer","new-form","job offer")
}

export const employee_date_validate = (params) => {

    const controller = lite.page_controller.form_controller
    let values = { ...params.controller.get_form_data()?.values }

    let date1 = new Date(values?.d_o_b);
    let date2 = new Date(values?.date_of_joining);
    // Compare the dates using standard comparison operators
    if (dateDiffInYears (date1, date2) < 18) {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID AGE",
            message: `Age restriction: Individual is below 18.`
        })
        return false
    }else if (date1 < date2) {
        return true
        
    } else if (date1 > date2) {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID DATE FORMAT",
            message: ` Date of Birth cannot be greater than Date of Joining`
        })
        return false
    
    } else {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID DATE FORMAT",
            message: `Date of Birth cannot cannot be equal to Date of Joining`
        })
        return false
    }
      
}



export const validateTime =(params)=> {

    const controller = lite.page_controller.form_controller
    let values = { ...params.controller.get_form_data()?.values }

    // Convert string representations of time to Date objects
    const startDate = new Date(`1970-01-01 ${values?.start_time}`);
    const endDate = new Date(`1970-01-01 ${values?.end_time}`);

        // Compare the Date objects
    if (startDate < endDate) {
        return true
        
    } else if (startDate > endDate) {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID ",
            message: ` Start Time cannot be greater than End Time`
        })
        return false
    
    } else {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID ",
            message: `Start Time cannot be equal to End Time`
        })
        return false
    }


}




export const interview_time_validation = (params) => {

    const controller = lite.page_controller.form_controller
    let values = { ...params.controller.get_form_data()?.values }

    // Convert string representations of time to Date objects
    const startDate = new Date(`1970-01-01 ${values?.from_time}`);
    const endDate = new Date(`1970-01-01 ${values?.to_time}`);

        // Compare the Date objects
    if (startDate < endDate) {
       return true
        
    } else if (startDate > endDate) {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID ",
            message: ` Start Time cannot be greater than End Time`
        })
        return false
    
    } else {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID ",
            message: `Start Time cannot be equal to End Time`
        })
        return false
    }

}

export const interview_schedule_time_validation = (params) => {

    const controller = lite.page_controller.form_controller
    let values = { ...params.controller.get_form_data()?.values }
    if (values?.schedule_for != "For Single Applicant") return
    // Convert string representations of time to Date objects
    const startTime = new Date(`2000-01-01 ${values?.from_time}`);
    const endTime = new Date(`2000-01-01 ${values?.to_time}`);

        // Compare the Date objects
    if (startTime < endTime) {
        return true
    } else if (startTime > endTime) {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID ",
            message: ` Start Time cannot be greater than End Time`
        })
        return false
    } else {
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "INVALID ",
            message: `Start Time cannot be equal to End Time`
        })
        return false
    }
}

// leave policy
export const on_leave_policy_leave_type_changed = async ({ controller, value }) => {

    const fd = controller.get_form_data ()?.values
    let policy = undefined
    let table = undefined
    const grade_leaves = controller.get_table_rows("leave_policy_grade")
    const policy_leaves = controller.get_table_rows("policy_designation")
    const default_leaves = controller.get_table_rows("policy_details")
    if (grade_leaves && grade_leaves.length > 0) {
        table = "leave_policy_grade"
        policy = grade_leaves
    }else if (policy_leaves && policy_leaves.length > 0) {
        table = "policy_designation"
        policy = policy_leaves
    }else if (default_leaves) {
        table = "policy_details"
        policy = default_leaves
    }

    if (policy && table) {
        $.each (policy, async (_, leave_type) => {
            if (leave_type?.leave_type?.value) {
                const r = await lite.connect.get_doc("Leave_Type", leave_type.leave_type.value)
                if (r.status === lite.status_codes.ok) {
                    const lt = r.data
                    let days = leave_type.total_days_allocated_per_month.value
                    switch (lt.accrual_frequency) {
                        case 'Dose Not Accrua':
                            days = leave_type.total_days_allocated_per_month.value
                            break;
                        case 'Monthly':
                            days = leave_type.total_days_allocated_per_month.value * 12
                            break;
                        case 'Quarterly':
                            days = leave_type.total_days_allocated_per_month.value * (12 / 3)
                            break;
                        case 'Two Months':
                            days = leave_type.total_days_allocated_per_month.value * (12 / 2)
                            break;

                        case 'Six Months':
                            days = leave_type.total_days_allocated_per_month.value * (12 /6)
                            break;
                        default:
                            break;
                    }
                    controller.set_form_table_value(table, leave_type?.annual_allocation?.row_id, leave_type?.annual_allocation?.field, days)
                }else {
                    lite.alerts.toast({
                        toast_type: lite.status_codes.no_content,
                        title: "No Leave Type Is Selected",
                        message: `Please Select A Leave Type`
                    })
                    return
                }
            }
            return
        })
    }
}

export const months_to_numbers = ({controller}) => {
    const popBy = controller.get_form_data ().values.populate_by
    if (popBy == "Leave Type") leave_by_type (controller)
    else if (popBy == "Leave Policy") leave_by_policy (controller)
}

export const create_leave_allocation = (params) => {
    let values = params.values
    values.main_policy = values.name
    values.employee_name = values.full_name
    values.populate_by = "Leave Policy"
    delete values.title
    delete values.policy_details
    delete values.leave_type
    delete values.total_days_allocated_per_month
    delete values.annual_allocation

    lite.session.set_session("clone_doc", values)
    lite.utils.redirect("hr","leave_allocation","new-form","Leave Allocation")
}

export const create_employee_files = (params) => {
    let values = params.values
    values.employee = values.name
    values.employee_name = values.full_name
    values.department = values.department
    values.designation = values.designation
    delete values.gender
    delete values.salutation
    delete values.branch
    delete values.d_o_b
    delete values.nrc_no
    delete values.employment_type
    delete values.status
    delete values.date_of_joining
    delete values.report_to
    delete values.leave_approver
    delete values.shift_approver
    delete values.requisition_approver
    delete values.basic_pay
    delete values.currency
    delete values.account_no
    delete values.sort_code
    delete values.employee_grade
    delete values.tax_band
    delete values.earnings
    delete values.deductions
   
    lite.session.set_session("clone_doc", values)
    lite.utils.redirect("hr","employee_files","new-form","Employee Files")
}


export const create_training_event = (params) => {
    let values = params.values;

    // Map values directly
    values.training_program = values.name;
    values.trainer = values.trainer;
    values.trainer_email = values.trainer_email;
    values.contact = values.contact;
    values.supplier = values.supplier;
    
    // Handle attendees if present in params
    if (values.attendee && Array.isArray(values.attendee)) {
        values.attendees = values.attendee.map(att => ({
            employee: att.employee,
            email: att.email,
        }));
    }

    // Remove unwanted properties
    delete values.description;
    delete values.training_status;
    
    // Store the new Training Event document in the session
    lite.session.set_session("clone_doc", values);
    // Redirect to create a new form for the Training Event
    lite.utils.redirect("hr", "training_event", "new-form", "Training Event");
};


export const reject = async (params) =>{
    const controller = params.form_controller
    const id = params?.values?.id
    const rejected = await lite.connect.x_post ("reject", {id:id})
    if(rejected.status == lite.status_codes.ok){
        controller.init_form()
    }
}

export const create_employee = async (params) => {
    console.log(params);
    const id = params?.values?.id
    const applicant_infor  = await lite.connect.x_post("create_employee_from_applicant", {id:id})
    
}

export const on_interview_schedule_change = async ({value}) => {
    const controller = lite.page_controller.form_controller
    const job_application_response = await lite.connect.x_post ("get_job_application", {name: value})
    if (job_application_response.status === lite.status_codes.ok) {
        controller.populate_child_table ("skills", job_application_response.data._skills, true)
        controller.populate_child_table ("qualifications", job_application_response.data.documents, true)
        controller.set_form_value(controller.get_form_field("from_time"), job_application_response.data.interview_schedule_times.from_time);
        controller.set_form_value(controller.get_form_field("to_time"), job_application_response.data.interview_schedule_times.to_time);
    }
    return
}

export const approve_application = async (params) =>{
    const controller = params.form_controller 
    const id = params?.values?.id
    const closed = await lite.connect.x_post("approve_application", {id:id})
    if(closed.status == lite.status_codes.ok){
        controller.init_form()
    }
}

export const request_for_absence = async () => {
    const controller = lite.page_controller.form_controller;
    const field_start_date = controller.get_form_data()?.values?.start_date;
    const field_end_date = controller.get_form_data()?.values?.end_date;

    if (field_start_date && field_end_date) {
        const startDate = new Date(field_start_date);
        const endDate = new Date(field_end_date);

        if (endDate >= startDate) {
            const timeDifference = endDate.getTime() - startDate.getTime();
            const daysDifference = Math.abs(timeDifference / (1000 * 3600 * 24));
            const hoursDifference = Math.abs(timeDifference / (1000 * 3600));
            controller.set_form_value(controller.get_form_field("days"), daysDifference);
            controller.set_form_value(controller.get_form_field("hours"), hoursDifference);
        } 
    } else {
        console.error("Start date or end date is missing.");
    }
}

export const on_field_change_bonus_type = async (params) => {
    const controller = lite.page_controller.form_controller
    const response = await lite.connect.x_post('get_bonus_type', {name: params.value}) 
    if (response.status == lite.status_codes.ok) {
        const bonus_type = response.data
        controller.populate_child_table ("eligible_employees", bonus_type?.eligibility_criteria || [])
        controller.set_form_value(controller.get_form_field("amount_fixed"), bonus_type?.amount_fixed || 0.00);
        controller.set_form_value(controller.get_form_field("amount_percentage"), bonus_type?.amount_percentage || 0.00)
        controller.set_form_value(controller.get_form_field("bonus_frequency"), bonus_type?.bonus_frequency || '')
        controller.set_form_value(controller.get_form_field("is_percentage"), bonus_type?.is_percentage == 1 ? 'YES' : 'NO')
        controller.set_form_value(controller.get_form_field("payment_timing"), bonus_type?.payment_timing || '')
    }
}

export const on_final_statement = async (params) => {
    const controller = lite.page_controller.form_controller
    const loader_id = lite.alerts.loading_toast({
        title: `Retriving Employee Information`, 
        message:"Please wait while employee info is beening retrived."
    })
    
    const get_asset_data = await lite.connect.x_post('get_employee_assets', {employee: params?.value })
    if (get_asset_data.status == lite.status_codes.ok) {
        const data = get_asset_data?.data?.data ?? 0
        const leave = data?.leave_summary ?? 0
        const assets = data?.assets ?? 0
        const earnings = data?.earnings ?? 0
        const deduction = data?.deductions ?? 0

        
        const get_calculated_totals = await lite.connect.x_post('final_statement_calculated_totals', {employee: params?.value })              

        if (get_calculated_totals.status ==lite.status_codes.ok) {    
            controller.populate_child_table ("calculated_totals", get_calculated_totals.data)
        }
        let total_payable_leave = 0
        let total_payable = 0
        let total_receivables = 0
        let ASSETS = []
        let EARNINGS = []
        let DEDUCTIONS = []
        $.each (leave.paid_leave, (_, ele) => {
            const paid_leave = leave[ele]
            if (paid_leave) {
                total_payable_leave += paid_leave.remaining_days
            }
        })

        if ( assets && assets.asset_list.length > 0 && assets.asset_list[0].length > 0) {
            $.each (assets.asset_list[0], (_, asset) => {
                ASSETS.push ({
                    assets_component: asset.asset,
                    assets_reference_document_type: asset.doctype,
                    assets_reference_document: asset.name,
                    assets_amount: asset.net_book_value,
                })
            })
        }

        $.each (deduction, (_, deduction) => {
            let amount = 0
            if (deduction.value_type == "Fixed Amount") {
                amount += deduction.fixed_amount ?? 0
            }else if (deduction.value_type == "Percentage") {

                amount += (deduction.percentage ?? 0 / 100) * data.basic_pay
            }
            
            total_receivables += amount ?? 0
            
            DEDUCTIONS.push ({
                receivable_component: deduction.name,
                receivable_reference_document_type: deduction.doctype,
                receivable_reference_document: deduction.name,
                receivable_amount:  amount,
                receivable_status: "Unsettled"
            })
        })

        $.each (earnings, (_, earning) => {
            let amount = 0
            if (earning.value_type == "Fixed Amount") {
                amount += earning.fixed_amount ??0
            }else if (earning.value_type == "Percentage") {
                amount += (deduction.percentage ?? 0 / 100) * data.basic_pay ?? 0
            }
            
            total_payable += amount ?? 0
            EARNINGS.push ({
                component: earning.name,
                reference_document_type: earning.doctype,
                reference_document: earning.name,
                amount: amount,
                payable_status: "Unsettled"
                
            })
        })

        const today = new Date ()
        let redundancy = 0
        let gratuity = 0

        const type_ = controller.get_form_data ().values?.statement_for
        if (type_ === "Redundancy") {
            redundancy = calculate_redundancy (data?.date_of_joining, today.toISOString().split('T')[0], data?.basic_pay)
            
        }else if (type_ === "End of Contract") {
            gratuity = calculate_gratuity ()
        }
       

        controller.populate_child_table ("receivables", EARNINGS)
        controller.populate_child_table ("payable", DEDUCTIONS)
        controller.populate_child_table ("asset", ASSETS)
        const leave_amount_ = parseFloat(leave_amount (total_payable_leave, data.working_days, data.basic_pay).toFixed (3))
        controller.set_form_value(controller.get_form_field("advance"), data.advance.advance || '0.00')
        controller.set_form_value(controller.get_form_field("overtime"), data.overtime.overtime|| '0.00')
        controller.set_form_value(controller.get_form_field("total_payable"), total_payable || '0.00')
        controller.set_form_value(controller.get_form_field("total_receivable"), total_receivables || '0.00')
        controller.set_form_value(controller.get_form_field("total_asset"), assets?.total_assets || '0.00')
        controller.set_form_value(controller.get_form_field("leave_days"), leave_amount_ || '0.00')
        controller.set_form_value(controller.get_form_field("gratuity"), gratuity || '0.00')
        controller.set_form_value(controller.get_form_field("redundancy"), redundancy || '0.00')
        const sun_obj = __totals_ (total_receivables ?? 0, data.advance.advance ?? 0, data.overtime.overtime ?? 0, total_payable ?? 0, leave_amount_ ?? 0)
        $ ("#payable_t #amount-payable").html (sun_obj.total_payable)
        $ ("#receivable_t #amount-receivable").html (sun_obj.total_receivables)
        $ ("#total-amount-payable #amount-for-payable").html (sun_obj.overall_total)
        $.each ($ (".currency"), (_, item) => {
            $ (item).html (data?.currency)
        })
        lite.alerts.destroy_toast(loader_id)
        lite.alerts.toast({
            toast_type: lite.status_codes.ok,
            title: "The Data Retrival Is Done",
            message: `The employee infomation retrival procees has been completed.`
        })
    }
}

export const extend_appraisal_fields = async (controller, fields) =>{
    const Core_hr = await import("../../../functions/core_hr/index.js")
    lite.Core_hr = new Core_hr.default()
    await lite.Core_hr.init()
    return lite.Core_hr.extend_appraisal_fields(fields)
}  
export const extend_self_appraisal_fields = async (controller, fields) =>{
    const Core_hr = await import("../../../functions/core_hr/index.js")
    lite.Core_hr = new Core_hr.default()
    await lite.Core_hr.init()
    return lite.Core_hr.extend_self_appraisal_fields(fields)
} 

export const create_appointment_letter = (params) => {
    let values = params.values
    values.name = values.name
    const data = {name:values.name, }
    lite.session.set_session("clone_doc", data)
    lite.utils.redirect("hr","appointment_letter","new-form","appointment letter")
}

function leave_amount (days, working_days, basic_pay) {
    const pay = parseFloat (basic_pay)
    const work_d = parseInt (working_days)
    return (pay / work_d) * days
}

function __totals_ (receivables, loan, overtime, payable, leave) {
    
    const total_receivables = (receivables + loan) || 0
    const total_payable = (overtime || 0 + payable || 0 + leave || 0) || 0
    const overall_total = (total_payable || 0 - total_receivables || 0) || 0
    return {
        total_receivables,
        total_payable,
        overall_total
    }
}

function months_between (dt1, dt2) {
    const [date1, date2] = [dt1, dt2].map(
        (date) => new Date(date)
    );
    const monthDiff = (
        (date2.getFullYear() - date1.getFullYear()) * 12 +
        date2.getMonth() -
        date1.getMonth() -
        (date2.getDate() < date1.getDate() ? 1 : 0)
    );

    return monthDiff
}


export const on_contract_change = async (params) => {
    console.log("we are");
    
    const controller = lite.page_controller.form_controller;
    const formData = controller.get_form_data()?.values;
    const res = await lite.connect.get_doc ("Gratuity_Configuration", formData?.company)
    if (res.status != lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: "NO POLICY FOUND",
            message: "There are no gratuity policy!!"
        });
        return
    }

    const basic_salary = lite.utils.string_to_float (formData?.basic_salary) || 0.00,
        rate = lite.utils.string_to_float (res.data?.gratuity_rate),
        min_rate = lite.utils.string_to_float (res.data?.minimum_rate )

    const by = rate < min_rate ? min_rate/100 : rate/100
    
    const wyd = lite.utils.getDateDifference (formData?.effective_date, formData?.expiry_contract_date, "months", true)
    console.log(by, wyd);
    const gratuity_pay = basic_salary * wyd * by
    console.log(gratuity_pay, wyd, by)
    controller.set_form_value (controller.get_form_field ("gratuity_amount"), lite.utils.thousand_separator (gratuity_pay, 2))
    return
};


function dateDiffInYears (startDate, endDate) {
    const startYear = startDate.getFullYear()
    const endYear = endDate.getFullYear()
    let yearDiff = endYear - startYear
    if (
        endDate.getMonth() < startDate.getMonth() ||
        (endDate.getMonth() === startDate.getMonth() && endDate.getDate() < startDate.getDate())
    ) {
        yearDiff--
    }
    return yearDiff
}

function calculate_gratuity (started_on, last_day_of_work, basic_pay) {
    let gratuity = 0
    return gratuity
}

function calculate_redundancy (started_on, last_day_of_work, basic_pay) {
    let redundancy = 0.00
    if (started_on && last_day_of_work) {
        const dt1 = new Date (started_on)
        const dt2 = new Date (last_day_of_work)
        const dif = dateDiffInYears (dt1, dt2) > 0 ? dateDiffInYears (dt1, dt2) : 0
        redundancy = (parseInt(basic_pay) * 2) *  dif
    }
    return redundancy
}


export const create_user_accounts = async (params) => {
    const loader_id = lite.alerts.loading_toast({
        title: `User Creation Initialized`, 
        message:"Please wait while we are creating user."
    })
    const selectedItems = params.selected_rows
    if (selectedItems.length > 0) {
        const {status, data, error_message} = await lite.connect.x_post ("create_users_from_selected", {employees: selectedItems})
        lite.alerts.destroy_toast(loader_id)
        if (status == lite.status_codes.ok){
            lite.alerts.toast({ toast_type: lite.status_codes.ok, title: "User Creation Successful", message: "Users Have Been Created Successfully!!" });               
        }
    }else {
        const {status, data, error_message} = await lite.connect.x_fetch ("create_users_on_a_mass")
        lite.alerts.destroy_toast(loader_id)
        if (status == lite.status_codes.ok){
            lite.alerts.toast({ toast_type: lite.status_codes.ok, title: "User Creation Successful", message: "Users Have Been Created Successfully!!" });              
        }
    }
}

export const go_to_profile = ({values}) => {
    lite.session.set_session ("lite_emp_profile_id", values.name)
    lite.utils.redirect("hr","employee_profile","dashboard","Employee Profile")
}

export const deactivate_separated_employees = async (params) => {
    const loader_id = lite.alerts.loading_toast({
        title: `Deactivation Initialized`, 
        message:"Please wait while we are deactivating Employees form your Payroll."
    })
    const res = await lite.connect.x_fetch ("deactivate_separated_employees") 
    if (res.status == lite.status_codes.ok) {
        lite.alerts.destroy_toast(loader_id)
        lite.alerts.toast({ toast_type: lite.status_codes.ok, title: "Deactivation Was Successfully", message: "Successfully Deactivate Separated Employees" });               
    }else {
        lite.alerts.destroy_toast(loader_id)
        lite.alerts.toast({ toast_type: lite.status_codes.no_content, title: "INFO", message: "All Separated Employees Are Deactivated from Payroll" });               
    }
}

function leave_by_type (controller) {
    const leave_types_by_employee = controller.get_table_rows ("leave_allocation_employees")
    $.each (leave_types_by_employee, async (_, employee_leave_type) => {
        let date1 = new Date(employee_leave_type?.from_date?.value)
        let date2 = new Date(employee_leave_type?.to_date?.value)
        if (date1 < date2) {
            const Difference_In_Months = months_between (employee_leave_type?.from_date?.value, employee_leave_type?.to_date?.value)
            const leave_data = await lite.connect.x_post ("get_employee_analytics",{eid:employee_leave_type.employee?.value, leave_policy: employee_leave_type?.leave_policy?.value, leave_type: employee_leave_type.leave_type?.value})
            let total_new_leaves = 0
            let remaining_days = 0
            let overall_total = 0
            let overall_total_leaves = 0
    
            if (leave_data?.status == lite.status_codes.ok) {
                remaining_days += leave_data?.data?.emp?.overall_totals?.remaining_days
                if (leave_data.data.leave_type?.apply_on === employee_leave_type?.gender?.value || leave_data.data.leave_type?.apply_on == "Both") {
                    const overall_total_ = lite.utils.string_to_int(Difference_In_Months) * lite.utils.string_to_int (leave_data.data.leave_type?.total_days_allocated_per_month)
                    total_new_leaves += overall_total_
                    overall_total += overall_total_
                }
                overall_total_leaves +=  total_new_leaves + remaining_days
            }
            controller.set_form_table_value ("leave_allocation_employees", employee_leave_type?.overall_total_leaves?.row_id,employee_leave_type?.overall_total_leaves?.field, overall_total_leaves) 
            controller.set_form_table_value("leave_allocation_employees", employee_leave_type?.total_leaves_allocated?.row_id,employee_leave_type?.total_leaves_allocated?.field, overall_total)
        }
    })
}

function leave_by_policy (controller) {
    console.log('====================================');
    console.log(controller.get_table_rows ("leave_allocation_employees"));
    console.log('====================================');
}

export const on_from_date_plan = async (params) => {
    const values = params.controller.get_form_data()?.values;
    let from_date = values.from_date;
    let to_date = values.to_date;
    if (new Date(from_date) >= new Date(to_date)) {
        lite.alerts.toast({ toast_type: lite.status_codes.unauthorized, title: "Date Validation", message: "To Date must be greater than From Date" });
        params.controller.set_form_value(params.controller.get_form_field("to_date"),null );
        return; 
    }
    const holidays = await lite.connect.x_fetch("get_holidays");
    if (holidays.status === lite.status_codes.ok) {
        const holiday = holidays.data.data;
        params.controller.set_form_value(
            params.controller.get_form_field("days"),
            count_week_days(new Date(values?.from_date), new Date(values?.to_date), holiday)
        );
    }

    return;
};

// export const attendance_list_cards =()=>{
//     const hr_fun =new HR_HTML_Generator()    
    
//     $("#employee-attendant-info").append(hr_fun.attendance_list_cards([{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]))
// }

export const create_jobOpenning_from_staffPlan =async (params)=>{
    const values = params?.values
    if(values.create_job_offers !=1){
        const loader_id = lite.alerts.loading_toast({
            title: `Creating A Job Opening`, 
            message:"Please wait while a job opening is being created."
        })        
        const job_openning =await lite.connect.x_post("create_jobOpenning_from_staffPlan", values)
        lite.alerts.destroy_toast(loader_id)
        lite.alerts.toast({
            toast_type:job_openning.status,
            title:"Job Openings Created",
            message:`${job_openning.data.created_job_opennings} job Opennings were created.`
        })            
        form_controller?.init_form()
        // else{
        //     lite.alerts.toast({
        //         toast_type:job_openning.status,
        //         title:"An Error Occuered",
        //         message:job_openning.error_message
        //     })
        // }
    } else{
        lite.alerts.toast({
            toast_type:lite.status_codes.unprocessable_entity,
            title:"Job Openings Already Exists",
            message:`The job openings already exist`})
            form_controller.init_form()
    }
}

export const price_distribution =async (params)=>{
    console.log(";;;;;;");    
    const {controller, value} =params 
    let welfare_type =null,
        company_value =null,
        staff_value =null
    const values =controller?.get_form_data()?.values

    if(values?.welfare_type && values?.welfare_expense){
        const fetch_welfare_type =await lite?.connect?.get_doc("Welfare_Type", values?.welfare_type)        
        if (fetch_welfare_type.status ==lite?.status_codes.ok){
            welfare_type =fetch_welfare_type.data
        }else{
            console.log("");            
        }
        if(welfare_type !=null){
            company_value =values?.welfare_expense *(welfare_type?.company_percentage/100)
            staff_value =values?.welfare_expense *(welfare_type?.employee_percentage/100)
            

            if(company_value && staff_value){
                controller.set_form_value(controller.get_form_field("company_covered_expense"), company_value || 0.00)
                controller.set_form_value(controller.get_form_field("staff_covered_expense"), staff_value || 0.00)
            }

        }
    }   
    
}

export const work_plan_start_working = async ({form_controller, row_data, values}) => {
    const loader_id = lite.alerts.loading_toast({
        title: `Processing Task Commencement`,
        message:"Please wait while Your task is being commenced."
    })
    console.log('====================================');
    console.log(row_data);
    console.log('====================================');
    const res = await lite.connect.x_post ("work_plan_commence_work", {doc: values.name, title:row_data?.key_result?.value, type: "Start"})
    lite.alerts.destroy_toast(loader_id)
    if (res.status == lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type:lite.status_codes.ok,
            title:"Task Started Successfully",
            message:`The task ${row_data?.title?.value} has been commenced successfully`})
        form_controller.init_form()
    }else {
        lite.alerts.toast({
            toast_type:lite.status_codes.ok,
            title:"Task Start Field",
            message:`The task ${row_data?.title?.value} commencement failed`})
    }
}

export const work_plan_task_issue = async ({form_controller, row_data, values}) => {
    const formData = values
    const issue_content = {
        title: row_data?.title?.value,
        description: row_data?.description?.value,
        expected_start_date: row_data?.expected_start_date?.value,
        expected_end_date: row_data?.expected_end_date?.value,
        progress_tracker: row_data?.progress_tracker?.value,
    }
    const quick_modal = await lite.modals.quick_form("hr", "work_plan_issue", async (values,setup)=>{
        // lite.modals.close_modal(quick_modal.modal_id)
        values["work_plan"] = values?.name
        console.log('====================================');
        console.log(values);
        console.log('====================================');
        const save = await lite.connect.x_post("request_adjustment", values)
        lite.alerts.destroy_toast(loader_id)
        if(save.status === lite.status_codes.ok){
            lite.alerts.toast({
                toast_type:lite.status_codes.ok,
                title:"Request was Successfully",
                message:`Request is successful`
            })
        }else {
            lite.alerts.toast({
                toast_type:lite.status_codes.no_content,
                title:"Request Failed",
                message:`Failed to request`
            })
        }
    },null, issue_content)

    // const loader_id = lite.alerts.loading_toast({
    //     title: `Processing Task Issue`,
    //     message:"Please wait while Your submit your issued."
    // })
    // const res = await lite.connect.x_post ("work_plan_commence_work", {doc: values.name, title:row_data?.title?.value, type: "Issue"})
    // lite.alerts.destroy_toast(loader_id)
    // if (res.status == lite.status_codes.ok) {
    //     lite.alerts.toast({
    //         toast_type:lite.status_codes.ok,
    //         title:"Issue Submitted Successfully",
    //         message:`The issue for ${row_data?.title?.value} has been submitted successfully`})
    //     form_controller.init_form()
    // }else {
    //     lite.alerts.toast({
    //         toast_type:lite.status_codes.ok,
    //         title:"Task Issue Field",
    //         message:`The issue for ${row_data?.title?.value} has failed`})
    // }
}

export const work_plan_task_completion = async ({form_controller, row_data, values}) => {
    const loader_id = lite.alerts.loading_toast({
        title: `Processing Task Completion`,
        message:"Please wait while Your submit your completion."
    })
    const res = await lite.connect.x_post ("work_plan_commence_work", {doc: values.name, title:row_data?.title?.value, type: "complete"})
    lite.alerts.destroy_toast(loader_id)
    if (res.status == lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type:lite.status_codes.ok,
            title:"Task Completion Successfully",
            message:`The task ${row_data?.title?.value} has been completion successfully`})
        form_controller.init_form()
    }else {
        lite.alerts.toast({
            toast_type:lite.status_codes.ok,
            title:"Task Completion Failed",
            message:`The completion for ${row_data?.title?.value} has failed`})
    }
}

export const get_tasks = async ({controller, value}) => {
    const loader_id = lite.alerts.loading_toast({
        title: `Processing Task Completion`,
        message:"Please wait while Your submit your completion."
    })
    const res = await lite.connect.x_post ("get_work_plan", {emp: value})
    lite.alerts.destroy_toast(loader_id)
    if (res.status == lite.status_codes.ok) {
        controller.populate_child_table ("leave_plan_tasks", res.data)
        return
    }
}
export const interview_rating_by_staff = async ({controller, value}) => {
    const loader_id = lite.alerts.loading_toast({title: `Processing Interview Rate`, message:"Please wait while Your submit your rating."})
    const res = await lite.connect.x_post ("interview_rating", {emp: value})
    console.log(res);
    lite.alerts.destroy_toast(loader_id)
    if (res.status != lite.status_codes.ok) {lite.alerts.toast({toast_type:lite.status_codes.ok, title:"Rates Not Found", message:`You have no rates to submit`})
            return
    }else {
        controller.populate_child_table ("practical_skill", res.data.practical_rating)
        controller.populate_child_table ("competess_assessment", res.data.competess_rating)
        controller.populate_child_table ("skills_rating", res.data.data)
        controller.populate_child_table ("qualifications", res.data.qualification)
        controller.set_form_value(controller.get_form_field("applicant"), res.data?.applicant_name)
        return
    }
}


export const activate_work_plan = async ({form_controller}) => {
    const values = form_controller.get_form_data ()?.values
    const loader_id = lite.alerts.loading_toast({
        title: `Activation In Process`,
        message:"Please wait while activate your Work Plan."
    })
    const res = await lite.connect.x_post ("activate_work_plan", {doc: values.name})
    lite.alerts.destroy_toast(loader_id)
    if (res.status == lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type:lite.status_codes.ok,
            title:"Activation Successfully",
            message:`Work plan activated successfully`})
        form_controller.init_form()
    }else {
        lite.alerts.toast({
            toast_type:lite.status_codes.ok,
            title:"Activation Failed",
            message:`activation failed`})
    }
}
export const company_skill_levy = async (params) => { 
    const page = lite.utils.get_url_parameters("page");
    const controller = lite.page_controller.form_controller;
    if (lite.form_data && Object.keys(lite.form_data).length > 0) {
        return;  
    }
    const employees = await lite.connect.x_post('company_skill_levy', params.values); 

    if (employees.status == lite.status_codes.ok) {
        if (page === "new-form") {
            const employee_data = employees.data?.data;
            console.log(employee_data);        
            controller.populate_child_table("skill_levy_entitled", employee_data || []);
        } else {
            controller.populate_child_table("skill_levy_entitled", null);
        }
    }
};

export const limit_payment_duration =async (params)=>{
    const {controller, value} =params 
    const length_values ={
        "Day": 1,
        "Week": 2,
        "Months": 3,
        "Year": 4,
    }

    let welfare_type =null,
        pay_length_unit =null,
        payment_length =null
    ; 


    const values =controller?.get_form_data()?.values

    if(values?.welfare_type && values?.pay_length_unit){

        const fetch_welfare_type =await lite?.connect?.get_doc("Welfare_Type", values?.welfare_type)   

        if (fetch_welfare_type.status ==lite?.status_codes.ok){
            welfare_type =fetch_welfare_type.data
            
        }else{
            console.log("");            
        }
 
        if(welfare_type !=null){
            
            pay_length_unit =values?.pay_length_unit
            payment_length =values?.payment_length

            if(pay_length_unit){
                
                if(length_values[values.pay_length_unit] > length_values[welfare_type.limit_unit]){
                    controller.set_form_value(controller.get_form_field("pay_length_unit"), " ")   
                    console.log("Too Much...>>!!");          

                    if(values?.payment_length){
                        controller.set_form_value(controller.get_form_field("payment_length"), "")    
                    }   

                }else{

                    if(payment_length){

                        if(payment_length > welfare_type?.limit_qty){
                            console.log("Too Much....>>>!!!");
                            controller.set_form_value(controller.get_form_field("payment_length"), "")        
                        }
                    }
                }
            }
        }
    }
}

export const appraise_your_self = async ({controller, value}) => {
    if (lite.form_state == "new" ) {
    const res = await lite.connect.x_post ("get_appraisal_for", {emp: value})
        if (res.status == lite.status_codes.ok && res.data) {
            controller.populate_child_table ("performance_kpi", res.data.performance_kpi)
        }else {
            lite.alerts.toast(
                {
                    toast_type:lite.status_codes.no_content,
                    title:"No Performance Agreement Found",
                    message:`Staff ${value} Has no Any Performance Agreement`
                }
            )
        }
    }
}

export const rate_behavior  = async ({controller}) => {
    let total_score = 0.00
    let total_rows = 0
    const pov = controller.get_table_rows ("behavioral_imperative")
    $.each (pov, (_, itm) => {
        total_rows += 1
        total_score += lite.utils.string_to_float(itm.rating_b.value)
    })
    const total_score_ = (total_score/(total_rows*5)) * 40
    controller.set_form_value (controller.get_form_field ("behavioral_imperatives_score"), lite.utils.fixed_decimals (total_score_, 2))
}

export const rate_performance_obj = async ({controller}) => {
    let total_score = 0.00
    let total_rows = 0
    const pov = controller.get_table_rows ("performance_kpi")
    $.each (pov, (_, itm) => {
        total_rows += 1
        total_score += lite.utils.string_to_float(itm.rating_po.value)
    })
    const total_score_ = (total_score/(total_rows*5)) * 60
    controller.set_form_value (controller.get_form_field ("performance_objective_score"), lite.utils.fixed_decimals (total_score_, 2))
}
export const short_list_applicant = async (params) =>{
    const controller = params.form_controller
    const id = params?.values?.id
    const short_list = await lite.connect.x_post("create_short_", {id:id})
    if(short_list.status == lite.status_codes.ok){
        controller.init_form()
    }
}
export const schedule_interview = (params) => {
    let values = params.values
    const data = {
        schedule_for: "For Single Applicant",
        applicant: values.applicant_first_name +""+""+ values.applicant_first_name,
        applicant_email: values.applicant_email,
    }
    lite.session.set_session("clone_doc", data)
    lite.utils.redirect("hr", "interview_schedule", "new-form", "interview_schedule")
}
// export const get_designation_description = async (params) =>{
//     const controller = params.form_controller
//     const desig_descript = await lite.connect.x_post("get_designation_description", params.value)
//     if(closed.status == lite.status_codes.ok){
//         controller.init_form()
//     }

export const training_program_duration =(params)=>{
    const {controller} =params
    const fields =controller?.get_form_data()?.values
    let units =" Day"
    
    if (fields.start_date && fields.end_date){
        let duration =(parseInt(new Date(fields.end_date) -new Date(fields.start_date)) /(1000 * 60 *60 *24)) +1 
        if(duration < 0){duration =0}
        if(duration > 1){units =" Days"}else{units =" Day"}
        
        controller?.set_form_value(controller?.get_form_field("program_duration"), duration+units || 1 +units) 
    }    
}

export const populate_training_app =async (params)=>{
    const {controller} =params
    const fields =controller?.get_form_data()?.values
    const tp =await lite?.connect?.get_doc("Training_Program", fields?.name)
    
    if(tp.status ==lite?.status_codes?.ok){
        const tp_fields = tp.data
        

        controller?.set_form_value(controller?.get_form_field("description"), tp_fields.description || "") 
        controller?.set_form_value(controller?.get_form_field("reason"), tp_fields.reason || "") 

        controller.populate_child_table("attendee", tp_fields.attendee || []);
        controller.populate_child_table("expenses", tp_fields.expenses || []);

    } 
}

export const percent_over_limiter =(params)=>{

    console.log("Lets go...");
    
    
}

export const seperation_notice_period =(params)=>{
    console.log("we are getting...");
    let units =" Days"
    let notice_period =0
    
    const fields =params?.controller?.get_form_data()?.values

    if (fields.resignation_date && fields.last_day_of_work){
        
        notice_period =(parseInt(new Date(fields.last_day_of_work) -new Date(fields.resignation_date)) /(1000 * 60 *60 *24)) +1 
        console.log(notice_period);
        
        if(notice_period < 0){notice_period =0}
        if(notice_period > 1){units =" Days"}else{units =" Day"}
        
        params?.controller?.set_form_value(params?.controller?.get_form_field("notice_period"), notice_period+units || 1) 
    }else if(fields.resignation_date){     
        params?.controller?.set_form_value(params?.controller?.get_form_field("notice_period"), 30+units) 
    }
    
}

export const update_total = (params) => {
    const claim_data = params?.controller?.get_form_data()?.values;
    const { controller } = params;
    const get_claims = claim_data?.members || [];

    let total_amount = 0;

    get_claims.forEach(item => {
        const amount = parseFloat(item.amount);
        total_amount += isNaN(amount) ? 0 : amount;
    });
    controller?.set_form_value(controller?.get_form_field("total_amount"), total_amount);
};


export const policy_type = async (params) => {
    const controller = lite.page_controller.form_controller;
    const id = params?.value;
    let name =null
    if(lite?.utils?.get_url_parameters("page") =="info"){
        name =controller?.get_form_data()?.values?.name
    }    
    const policy_type = await lite.connect.x_post("policy_type", {id: id, doc_name: name});
    if (policy_type.status == lite.status_codes.ok) {
        controller.populate_child_table("policy_details", policy_type?.data?.policy_details || [],);
        return
    }
};