// core Js

import Core_Payroll from "../../../functions/core_payroll/index.js"


export const on_payroll_load = async (params)=>{
    lite.core_payroll = new Core_Payroll()
    await lite.core_payroll.populate_employees(params);
}

export const calculate_payroll = async (params) => {
    if(!lite.core_payroll){
        lite.core_payroll = new Core_Payroll()
    }
    await lite.core_payroll.recalculate_payroll(params)
    return
}

// export const on_payroll_new_employee_row_added = async ({ controller, row_id }) => {
//     const row = controller.get_table_row("employee_info", row_id);
//     var table_content = []

//     if (row.employee.fieldname === "employee") {
//         const tb_rows = controller.get_table_rows("employee_info")
//         const result = await lite.core_payroll.populate_employee({ controller: controller, employeeId: row.employee.value });  
//     }

//     if(lite.utils.array_has_data(table_content)){
//         console.log("table content has data")
//     controller.populate_child_table("employee_info", table_content)
//     }

// };

// export const on_payroll_row_removed = async ({controller})=>{
//     const table_rows = controller.get_table_rows("employee_info")
//     if(lite.utils.array_has_data(table_rows)){
//         $.each(table_rows,async (_,row)=>{
//             await lite.core_payroll.recalculate_payroll({controller:controller, row_id:row.employee.row_id, value:0})
//         })
//     }
// }

export const on_end_time_field_change = async (params) => {
    const controller = lite.page_controller.form_controller;
    const emp = controller.get_form_data()?.values?.applicant
    const field_start_time = controller.get_form_data()?.values?.start_time;
    const field_end_time = controller.get_form_data()?.values?.end_time;
    const emp_info = await lite.connect.get_doc ("Employee", emp)
    // const overtime = await lite.connect.get_doc ("Overtime_Setup", emp_info.data.company)
    // const ss = overtime.status == lite.status_codes.ok ? overtime.data : undefined
    const employee_salary = emp_info.data.basic_pay;
    const working_days = emp_info.data.working_days;
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
async function calc_max_take_home_rate (max_take_home_rate, applied_amount, basic_apy, emp, max_advances) {
    if (!max_take_home_rate) return false
    const current_advances = await lite.connect.x_post ("advance_calc", {applicant: emp, total_monthly_amount__gt: 0})
    if (current_advances.status != lite.status_codes.ok) return false
    if (typeof current_advances.data == "string") return false
    if (current_advances.data.length >= max_advances) {
        lite.alerts.toast({
            toast_type: lite.status_codes.unauthorized,
            title: `MAXIMUM ADVANCE`,
            message: `The maximum number of open Advance is Hit`,
        })
        return false
    }
    let total_monthly_pending_payments = applied_amount
    $.each (current_advances.data, (_, advance) => {
        total_monthly_pending_payments += advance?.total_monthly_amount
    })
    const amount_difference = basic_apy - total_monthly_pending_payments
    const take_home_percentage = (parseInt (max_take_home_rate) / 100) * parseFloat (basic_pay)
    if (amount_difference <= take_home_percentage) {
        lite.alerts.toast({
            toast_type: lite.status_codes.unauthorized,
            title: `AMOUNT ISSUE`,
            message: `The requested amount is Greater than you Pay`,
        })
        return false
    }
    return
}
export const advance_leave_validations = async ({controller, value}) => {
    value = parseFloat (value)
    const amount = value
    const form_data = controller.get_form_data ()?.values
    if (!form_data?.type_of_advance) {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: `ADVANCE TYPE MISSING`,
            message: `Please select advance type!`,
        })
        return
    }
    const advance_type = await lite.connect.get_doc ("Salary_Advance_Configuration", form_data?.type_of_advance)
    if (advance_type?.status != lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: `NOT FOUND`,
            message: `Advance type was Not found!`,
        })
        return
    }
    // first validate discipline and Probation
    const adType = advance_type.data
    if (!adType?.allow_on_probation && form_data?.emp_status == "Probation") {
        lite.alerts.toast({
            toast_type: lite.status_codes.unauthorized,
            title: `NOT ALLOWED`,
            message: `This Advance Type You Trying to Apply You're not Eligible!`,
        })
        return
    }
    if (!adType?.allow_on_discipline && form_data?.emp_status != "Probation" && form_data?.emp_status != "Active") {
        lite.alerts.toast({
            toast_type: lite.status_codes.unauthorized,
            title: `NOT ALLOWED`,
            message: `This  Type You Trying to Apply You're not Eligible!`,
        })
        return
    }

    // value Type validation
    if (adType?.amount_value == "Employee's Full Basic") {
        if (parseFloat (form_data?.basic_pay) < value) {
            lite.alerts.toast({
                toast_type: lite.status_codes.unauthorized,
                title: `AMOUNT ISSUE`,
                message: `The requested amount is Greater than you Pay`,
            })
            return
        }
    }else {
        const percentage = (parseInt (adType?.amount_rate) / 100) * parseFloat (form_data?.basic_pay)
        if (percentage < amount) {
            lite.alerts.toast({
                toast_type: lite.status_codes.unauthorized,
                title: `Policy Error`,
                message: `You Are Not Eligible For The Amount!`,
            })
            return
        }
    }
    if (adType?.is_interest_applicable) {
        value += (adType?.interest_rate / 100) * value
    }
    await calc_max_take_home_rate (
        adType?.max_take_home,
        value,
        form_data?.basic_pay,
        form_data?.applicant,
        adType?.maximum_open_advances,
    )

    if (adType?.eligibility_type != "All") {
        const eligibility = lite.utils.array_to_object (adType?.eligibility, "employment_type")
        const eligibility_criteria = eligibility[form_data?.employment_type]
        if (getDateDifference (form_data?.date_of_joining, eligibility_criteria?.time_measure) < eligibility_criteria?.period_of_service) {
            lite.alerts.toast({
                toast_type: lite.status_codes.unauthorized,
                title: `Policy Error`,
                message: `You Are Not Eligible For The Advance!`,
            })
            return
        }
    }
    const am = adType?.is_interest_applicable ? value : amount
    const mmp = adType?.repayment_plan == "Onces Off" ? am : am / parseInt (adType?.repayment_period_length)
    const show = !isNaN(am) && !isNaN (mmp) ? "Show" : ""
    controller.set_form_value (controller.get_form_field ("show_totals"), show)
    controller.set_form_value (controller.get_form_field ("amount_with_interest"), am)
    controller.set_form_value (controller.get_form_field ("total_monthly_amount"), (mmp))

}

// allocate_salary_component
export const allocate_salary_component = async ({form_controller, values}) =>{

    let item_content = {
        component_type: values?.component_type || "",
        name: values?.name || "",
    }
    
    const quick_modal = await lite.modals.quick_form("payroll", "salary_component_allocation", async (values,setup)=>{
        
        const loader_id = lite.alerts.loading_toast({
            title: `Allocating to Employee`,
            message:`Please wait while we do the allocation`
        })
        lite.modals.close_modal(quick_modal.modal_id)
        const save = await lite.connect.x_post("allocate_employee_salary_component", values)
        lite.alerts.destroy_toast(loader_id)
        if(save.status === lite.status_codes.ok){
            lite.alerts.toast({
                toast_type:lite.status_codes.ok,
                title:"Allocation was Successfully",
                message:`Allocation was Successfully`
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
        title: `ALLOCATING COMPONENT TO EMPLOYEE`,
        message:"Please wait while We're allocating component."
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

function getDateDifference (from_date, unit_type) {
    const fromDate = new Date(from_date)
    const toDate = new Date()
    const timeDifference = toDate - fromDate

    let result

    switch (unit_type.toLowerCase()) {
        case 'days':
            result = timeDifference / (1000 * 3600 * 24)
            break

        case 'weeks':
            result = timeDifference / (1000 * 3600 * 24 * 7)
            break

        case 'months':
            const monthsDifference = (toDate.getFullYear() - fromDate.getFullYear()) * 12
            result = monthsDifference + (toDate.getMonth() - fromDate.getMonth())
            break

        case 'years':
            result = toDate.getFullYear() - fromDate.getFullYear()
            break

        default:
            result = 0
            break
    }

    return result
}