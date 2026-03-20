



export const extend_payroll_fields = async (controller, fields) =>{
    const Core_Payroll = await import("../../../functions/core_payroll/index.js")
    lite.core_payroll = new Core_Payroll.default()
    await lite.core_payroll.init()
    return lite.core_payroll.extend_payroll_fields(fields)
}

export const extend_total_fields = async (controller, fields) =>{
    const Core_Payroll = await import("../../../functions/core_payroll/index.js")
    lite.core_payroll = new Core_Payroll.default()
    await lite.core_payroll.init()
    return lite.core_payroll.extend_total_fields(fields)
}


export const on_payroll_load = async (params)=>{
    const Core_Payroll = await import("../../../functions/core_payroll/index.js")
    lite.core_payroll = new Core_Payroll.default()
    await lite.core_payroll.init()

    await lite.core_payroll.populate_employees(params);
    return
   
}

export const calculate_payroll = async (params)=>{
    await lite.core_payroll.recalculate_payroll(params)
    return
}

export const on_payroll_new_employee_row_added = async ({ controller, row_id }) => {
    const row = controller.get_table_row("employee_info", row_id);
    var table_content = []
    
    if (row.employee.fieldname === "employee") {
        const tb_rows = controller.get_table_rows("employee_info")
        const result = await lite.core_payroll.populate_employee({ controller: controller, employeeId: row.employee.value });  
    }

    if(lite.utils.array_has_data(table_content)){
        console.log("table content has data")
    // controller.populate_child_table("employee_info", table_content)
    }

};

export const on_payroll_row_removed = async ({controller})=>{
    const table_rows = controller.get_table_rows("employee_info")
    if(lite.utils.array_has_data(table_rows)){
        $.each(table_rows,async (_,row)=>{
            await lite.core_payroll.recalculate_payroll({controller:controller, row_id:row.employee.row_id, value:0})
        })
    }
}

export const on_end_time_field_change = async (params) => {
    const controller = lite.page_controller.form_controller;
    const field_start_time = controller.get_form_data()?.values?.start_time;
    const field_end_time = controller.get_form_data()?.values?.end_time;
    const employee_salary = lite.employee_info.basic_pay;
    const working_days = lite.employee_info.working_days;
    
    const get_overtime_setup_response = await lite.connect.x_post("get_overtime_setup", {name: lite.user.company.name})
    if (get_overtime_setup_response.status === lite.status_codes.ok) {
    if (get_overtime_setup_response.data.calculation_type === "Salary Based") {
    const number_of_hours = get_overtime_setup_response.data.number_of_hours 
    if (field_start_time && field_end_time){
    if (employee_salary && working_days && number_of_hours > 0) {
    const startTime = parseTime(field_start_time);
    const endTime = parseTime(field_end_time);
    
    const total_hours_worked = working_days * number_of_hours;
    const per_rate = employee_salary / total_hours_worked;
    const totalHours = calculateTotalHours(startTime, endTime);
    const total_minutes_worked = totalHours.hours * 60 + totalHours.minutes;
    const total_earning = total_minutes_worked * per_rate / 60;
    controller.set_form_value(controller.get_form_field("total_earning"), parseFloat(total_earning).toFixed(2));
    
    }
    
    }  
} else {
    
    const fixed_rate = get_overtime_setup_response.data.fixed_rate
            if (field_start_time && field_end_time && fixed_rate > 0) {
        const startTime = parseTime(field_start_time);
        const endTime = parseTime(field_end_time);
        const totalHours = calculateTotalHours(startTime, endTime);
        const total_minutes_worked = totalHours.hours * 60 + totalHours.minutes;
        const total_earning = total_minutes_worked * fixed_rate / 60;
        controller.set_form_value(controller.get_form_field("total_earning"), parseFloat(total_earning).toFixed(2));
            
            }
        }
    }  else{
        lite.alerts.toast({
            toast_type: lite.status_codes.internal_server_error,
            title: `Request Failed`,
            message: `Failed to fetch overtime settings`,
        })
    }
 }

const parseTime = (timeString) => {
    const [hour, minute] = timeString.split(":").map(Number);
    return { hour, minute };
};

const calculateTotalHours = (startTime, endTime) => {
    let hourDiff = endTime.hour - startTime.hour;
    let minDiff = endTime.minute - startTime.minute;

    if (minDiff < 0) {
        hourDiff--;
        minDiff += 60;
    }

    return {
        hours: hourDiff,
        minutes: minDiff
    };
};





export const basic_pay_changed = async (params)=>{
    // console.log("basic_pay_changed")
}

export const apply_for_advance = async (params) => {
    const controller = params.controller 
    const values = params.values
    const response = await lite.connect.x_post ("apply_for_advance", {employee: values.applicant, company: lite.user.company.name, application: values.name})
    if (response.status === lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type: lite.status_codes.ok,
            title: `Successful`,
            message: `${response.data}`,
        })
        controller.init_form()
    }else {
        lite.alerts.toast({
            toast_type: lite.status_codes.unauthorized,
            title: `Error Occurred`,
            message: `${response.data}`,
        })
    }
}

export const approve_advance = async (params) => {
    const controller = params.controller 
    const values = params.values
    const response = await lite.connect.x_post ("approve_for_advance", {employee: values.staff_number, company: lite.user.company.name, application: values.name})
    if (response.status === lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type: lite.status_codes.unauthorized,
            title: `Successful`,
            message: `${response.data}`,
        })

        controller.init_form()
    }else {
        lite.alerts.toast({
            toast_type: lite.status_codes.unauthorized,
            title: `Info`,
            message: `${response.data}`,
        })
    }
}

export const calculate_partial_payments = async (params) => {
    console.log("test")
    const controller = lite.page_controller.form_controller
    const amount = parseInt (params.controller.get_form_data ()?.values?.amount_v)
    controller.set_form_value (controller.get_form_field ("amount"), amount)
    const {
        employment_type,
        date_of_joining,
        basic_pay
    } = lite.system_settings.employee_info

    const config = await lite.connect.x_post ("get_advance_config", {name: lite.user?.company?.name})
    
    if (config.status == lite.status_codes.ok) {
        const configs = config.data
        const percentage = (parseInt (configs.amount_rate) / 100) * parseInt (basic_pay)
        if (percentage < amount) {
            lite.alerts.toast({
                toast_type: lite.status_codes.unauthorized,
                title: `Policy Error`,
                message: `You Are Eligible For The Amount!`,
            })
            return
        }
        if (configs.eligibility.length > 0) {
            const eligibility = configs.eligibility.filter(object => object.employment_type === employment_type)
            if (eligibility.length > 0){
                const eligibility_row = eligibility[0]
                switch (lite.utils.lower_case(String (eligibility_row.time_measure))) {
                    case "day":
                        if (!lite.utils.days_since (new Date(date_of_joining), parseInt (eligibility_row.period_of_service))) {
                            lite.alerts.toast({
                                toast_type: lite.status_codes.unauthorized,
                                title: `You Not Eligible For Advance`,
                                message: `You Will Be Notified When You Become Eligible!`,
                            })
                            return
                        }
                        break
                    case "weeks":
                        if (!lite.utils.weeks_since (new Date(date_of_joining), parseInt (eligibility_row.period_of_service))) {
                            lite.alerts.toast({
                                toast_type: lite.status_codes.unauthorized,
                                title: `You Not Eligible For Advance`,
                                message: `You Will Be Notified When You Become Eligible!`,
                            })
                            return
                        }
                        break
                    case "months":
                        if (!lite.utils.months_since (new Date(date_of_joining), parseInt (eligibility_row.period_of_service))) {
                            lite.alerts.toast({
                                toast_type: lite.status_codes.unauthorized,
                                title: `You Not Eligible For Advance`,
                                message: `You Will Be Notified When You Become Eligible!`,
                            })
                            return
                        }
                        break
                    case "years":
                        if (!lite.utils.years_since (new Date(date_of_joining), parseInt (eligibility_row.period_of_service))) {
                            lite.alerts.toast({
                                toast_type: lite.status_codes.unauthorized,
                                title: `You Not Eligible For Advance`,
                                message: `You Will Be Notified When You Become Eligible!`,
                            })
                            return
                        }
                        break
                    default:
                        break
                }
            }else {
                lite.alerts.toast({
                    toast_type: lite.status_codes.unauthorized,
                    title: `You Not Eligible For Advance`,
                    message: `You Will Be Notified When You Become Eligible!`,
                })

                return
            }
        }else {
            lite.alerts.toast({
                toast_type: lite.status_codes.unauthorized,
                title: `No Advance`,
                message: `We Have Not Advance Policy!`,
            })

            return
        }
        
        if (params.value == 1) {
            const interest_rate = parseInt (configs.interest_rate) || 0
            const partial_payment_rate = configs.partial_payment
            if (configs.allow_partial_payments) {
                const calculated_advance = loan_calculator (parseInt (amount), interest_rate, partial_payment_rate)
                controller.populate_child_table ("calculated_value", calculated_advance)
            }else {
                lite.alerts.toast({
                    toast_type: lite.status_codes.unauthorized,
                    title: `Partial Payment Are Not Allowed`,
                    message: `No Partial Payments Are Not Allowed`,
                })
            }
        }else {
            let amount_s = parseInt (basic_pay)
            if (configs.allow_partial_payments) {
                const interest_rate = parseInt (configs.interest_rate) || 0
                amount_s += (interest_rate / 100) * amount

            }
            controller.set_form_value (controller.get_form_field ("amount"), amount)
            controller.populate_child_table ("calculated_value", [])
        }
    }else {
        lite.alerts.toast({
            toast_type: lite.status_codes.unauthorized,
            title: `Failed`,
            message: `Failed to Load Advance Policy`,
        })
    }

}
export const calc_percentage_advance = async (params) => {
    const controller = lite.page_controller.form_controller
    let amount = parseInt (params.controller.get_form_data ()?.values?.amount_v)
    const {
        basic_pay
    } = lite.system_settings.employee_info

    const config = await lite.connect.x_post ("get_advance_config", {name: lite.user?.company?.name})
    
    if (config.status == lite.status_codes.ok) {
        const configs = config.data
        const percentage = (parseInt (configs.amount_rate) / 100) * parseInt (basic_pay)
        if (percentage < amount) {
            lite.alerts.toast({
                toast_type: lite.status_codes.unauthorized,
                title: `Policy Error`,
                message: `You Are Eligible For The Amount!`,
            })
            return
        }
        if (configs.allow_partial_payments) {
            const interest_rate = parseInt (configs.interest_rate) || 0
            amount += (interest_rate / 100) * amount
        }
        controller.set_form_value (controller.get_form_field ("amount"), amount)
        controller.populate_child_table ("calculated_value", [])
    }else {
        lite.alerts.toast({
            toast_type: lite.status_codes.unauthorized,
            title: `Failed`,
            message: `Failed to Load Advance Policy`,
        })
    }

}
// allocate_salary_component
export const allocate_salary_component = async ({form_controller, values}) =>{

    let item_content = {
        component_type: values?.component_type || "",
        name: values?.name || "",
    }
    
    const quick_modal = await lite.modals.quick_form("payroll", "salary_component_allocation", async (values,setup)=>{
        
        const loader_id = lite.alerts.loading_toast({
            title: `Saving Content in Employee`, 
            message:`Please wait while we save data`
        })
        lite.modals.close_modal(quick_modal.modal_id)
        const save = await lite.connect.x_post("allocate_employee_salary_component", values)
        lite.alerts.destroy_toast(loader_id)
        if(save.status === lite.status_codes.ok){
            lite.alerts.toast({
                toast_type:lite.status_codes.ok,
                title:"Alloction was Successfully",
                message:`Alloction was Successfully`
            })
        }else {
            lite.alerts.toast({
                toast_type:lite.status_codes.no_content,
                title:"Allocation was Failed",
                message:`Failed to Allocate`
            })
        }
    },null, item_content)
}
const loan_calculator = (amount, interestRate, paymentPercentage, startDate = new Date()) => {
    const monthlyInterestRate = (interestRate / 100) / 12;
    const monthlyPayment = (amount * monthlyInterestRate * (1 + monthlyInterestRate)) / (1 - Math.pow(1 + monthlyInterestRate, -1 / (paymentPercentage / 100)))
    const totalMonths = Math.ceil(Math.log(monthlyPayment / (monthlyPayment - amount * monthlyInterestRate)) / Math.log(1 + monthlyInterestRate))
    
    return Array(totalMonths).fill(0).map((_, i) => {
        const interest = amount * monthlyInterestRate
        let principal = monthlyPayment - interest
        if (amount - principal < 0) {
            principal = amount
        }
        amount -= principal
        if (amount < 0) {
            amount = 0.00
        }
        const month = new Date(startDate.getTime() + i * 30 * 24 * 60 * 60 * 1000)
    
        return {
            month_v: `${month.toLocaleString('default', { month: 'short' })} ${month.getFullYear()}`,
            payment: +`${parseFloat(monthlyPayment.toFixed(2)) || 0.0}`,
            interest: +`${parseFloat(interest.toFixed(2)) || 0}`,
            principal: +`${parseFloat(principal.toFixed(2)) || 0}`,
            balance: +`${amount == 0.00? '0' : amount.toFixed(2)}`,
            month: month,
            state: "Unsettled"
        }
    })
}
export const get_salary_components_payroll = async ({controller}) => {
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
                        component: ele.name
                    })
                }else if (ele.component_type == "Earning") {
                    earnings.push ({
                        component: ele.name
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

export const apply_to_all_employees = async ({values}) => {
    const loader_id = lite.alerts.loading_toast({
        title: `GETTING STATUTORY COMPONENTS`, 
        message:"Please wait while We're fetching."
    })
    const save = await lite.connect.x_post ("link_component_to_all_employees", values)
    if (save.status == lite.status_codes.ok) {
        lite.alerts.destroy_toast(loader_id)
        const success_id =lite.alerts.toast({ toast_type: lite.status_codes.ok, title: "SUCCESSFUL", message: `Successfully allocated Component` });
        lite.alerts.destroy_toast(success_id)
    }else {
        lite.alerts.destroy_toast(loader_id)
        const error_id =lite.alerts.toast({ toast_type: lite.status_codes.no_content, title: "FAILED TO ALLOCATE", message: `Allocating Component Failed` });
        lite.alerts.destroy_toast(error_id)
    }
}
