import Core_Payroll from "../../../functions/core_payroll/index.js"

function display_payslips (rows, to_date) {
    let payslips = ''
    if (rows.length > 0) {
        const deduc = lite.core_payroll._deducs
        const earnings = lite.core_payroll._earnings
        const employees = lite.core_payroll.employees
        rows.pop ()
        rows.forEach(payslip => {
            payslips += generate_payslips (payslip, to_date, deduc, earnings, employees)
        })

    }
    return payslips
}

function generate_payslips (payslip, data, deductions, earnings, employees) {
    const earnings_keys = lite.utils.get_object_keys (earnings)
    const deductions_keys = lite.utils.get_object_keys (deductions)
    const net =  payslip?.net || 0,
        gross = payslip?.gross || 0,
        paye = payslip["PAYE"] || 0

    let ducs = ''
    let inco = ''
    const emp_no = payslip?.employee,
        employee = employees[emp_no],
        lds = employee?.leave_days || 0,
        wds = employee?.working_days || 0,
        leave_days_val = payslip.basic_pay / wds * lds
        const components_vals = employee?.components_vals || {}
    deductions_keys.forEach (deduc => {
        const val = payslip[deduc] || 0.00
        const deduction = deductions[deduc]
        
        const sc = !deduction.resenting || deduction.resenting == "" ? deduction?.name || deduc : deduction?.resenting
        const component_info = components_vals[sc] || {}
                
        if (val && val > 0) ducs += `
            <div class="grid grid-cols-12 gap-1 py-1 px-2">
                <div class="col-span-4 uppercase">${sc|| '-'}</div>
                <div class="col-span-3 capitalize text-center">{ ${component_info?.remaining_period || '0'} ${deduction?.unites || 'month'} }</div>
                <div class="col-span-3 capitalize text-center">${lite.utils.thousand_separator (component_info?.balance || 0, 2) || '-'}</div>
                <div class="col-span-2 capitalize text-center font-bold">${lite.utils.thousand_separator (val, 2) || '0.00'}</div>
            </div>
        `
    })

    earnings_keys.forEach (ear => {
        const val = payslip[ear] || 0.00
        const earning = earnings[ear]
        const sc = !earning.resenting || earning.resenting == "" ? earning?.name || ear : earning?.resenting
        const component_info = components_vals[ear] || {}
        if (val && val > 0) {
            inco += `
                <div class="grid grid-cols-12 gap-1 py-1 px-2">
                    <div class="col-span-5 uppercase">${sc || '-'}</div>
                    <div class="col-span-4 capitalize text-center"> { ${component_info?.remaining_period || '1'} ${earning?.unites || 'month'} } </div>
                    <div class="col-span-3 capitalize text-center font-bold">${lite.utils.thousand_separator (val, 2) || '0.00'}</div>
                </div>
            `
        }
    })

    return `
        <div class="payslip border rounded-md border-black w-full mx-auto text-[12px]">
            <div class="p-3 flex items-center justify-between gap-3">
                <div class="h-[60px] w-[60px] overflow-hidden flex-shrink-0">
                    <img src="/static/images/eczlogo.png"
                        class="logo h-full w-full object-contain" alt="">
                </div>
                <div class="flex-1 text-[14px]">
                    <div class="flex justify-between font-bold">
                        <div class="text-center flex-1 text-[16px]">EXAMINATIONS COUNCIL OF ZAMBIA</div>
                        <div class="text-[12px]">CURRENCY: ZMW</div>
                    </div>

                    <div class="flex justify-between border-t border-black pt-1 font-bold">
                        <div class="text-center flex-1 text-[14px]">Pay Statement For ${moment(data).format('Do MMM, YYYY')}</div>
                        <div class="text-[12px]">EXCH. RATE: 1.0</div>
                    </div>
                </div>
            </div>
            <div class="p-1 border border-slate-700/60 text-[11px]">
                <!-- Employee Info -->
                <div class="grid grid-cols-12 border border-black text-[10px]">
                    <div class="col-span-4 pl-1 border-r"><b>Emp Name:</b><br> ${payslip?.full_names || ''}</div>
                    <div class="col-span-2 pl-1 border-r"><b>Emp No:</b><br> ${emp_no || ''}</div>
                    <div class="col-span-2 pl-1 border-r"><b>NRC No:</b><br> ${employee?.id_no || ''}</div>
                    <div class="col-span-2 pl-1 border-r"><b>Eng. Date:</b><br> ${employee?.date_of_joining ? moment(data).format('Do MMM, YYYY'): ''}</div>
                    <div class="col-span-2 pl-1"><b>Basic:</b><br>${lite.utils.thousand_separator (payslip?.basic_pay, 2) ||0}</div>
                </div>
                <!-- Financial Summary -->
                <div class="grid grid-cols-7 border border-black text-[10px]">
                    <div class="pl-1 border-r"><b>Taxable:</b><br> ${lite.utils.thousand_separator (gross || 0, 2) ||0}</div>
                    <div class="pl-1 border-r"><b>Pay YTD:</b><br> ${lite.utils.thousand_separator (employee?.ytd_net + net || 0, 2) ||0}</div>
                    <div class="pl-1 border-r"><b>Tax Paid YTD:</b><br> ${lite.utils.thousand_separator (employee?.ytd_paye + paye || 0, 2) ||0}</div>
                    <div class="pl-1 border-r"><b>NAPSA YTD:</b><br> ${lite.utils.thousand_separator (employee?.ytd_napsa || 0, 2) ||0}</div>
                    <div class="pl-1 border-r"><b>Soc. Sec. No:</b><br> ${employee?.napsa ||0}</div>
                    <div class="pl-1 border-r"><b>Leave Days:</b><br> ${lite.utils.thousand_separator (lds, 2) ||0}</div>
                    <div class="pl-1"><b>Leave Value:</b><br> ${lite.utils.thousand_separator (leave_days_val, 2) ||0}</div>
                </div>
                <!-- More Summary -->
                <div class="grid grid-cols-12 border border-black text-[10px]">
                    <div class="col-span-2 pl-1 border-r"><b>Taxable This Month:</b></div>
                    <div class="col-span-3 pl-1 border-r"><b>Pension (PLA) YTD:</b><br> ${lite.utils.thousand_separator (employee?.ytd_private_pension || 0, 2) ||0}</div>
                    <div class="col-span-3 pl-1 border-r"><b>Gross Pay YTD:</b><br> ${lite.utils.thousand_separator (employee?.ytd_gross + gross || 0, 2) || 0}</div>
                    <div class="col-span-2 pl-1 border-r"><b>Print Date:</b><br> ${lite.utils.today ()}</div>
                    <div class="col-span-2 pl-1"><b>Incremental Month:</b><br> 1</div>
                </div>
                <!-- Deductions & Incomes -->
                <div class="salary-components mb-2 bg-slate-300">
                    <div class="grid grid-cols-2 bg-slate-400 gap-1 mt-1 text-[11px] font-bold">
                        <div class="px-2 grid grid-cols-12">
                            <div class="col-span-4">DEDUCTIONS</div>
                            <div class="col-span-3 text-center">Outstanding<br>Months</div>
                            <div class="col-span-3 text-center">Balance</div>
                            <div class="col-span-2 text-center">This Month</div>
                        </div>

                        <div class="px-2 grid grid-cols-12">
                            <div class="col-span-5">INCOMES</div>
                            <div class="col-span-4 text-center">Units</div>
                            <div class="col-span-3 text-center">This Month</div>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-1 mt-1 p-1">

                        <!-- Deductions -->
                        <div class="bg-white text-[10px]">
                            <div class="grid grid-cols-12 gap-1 py-1 px-2">
                                <div class="col-span-4 uppercase">PAYE</div>
                                <div class="col-span-3 capitalize text-center">{ 1 month }</div>
                                <div class="col-span-3 capitalize text-center">0.00</div>
                                <div class="col-span-2 capitalize text-center font-bold">${lite.utils.thousand_separator (paye || 0, 2)}</div>
                            </div>
                            ${ducs}
                        </div>

                        <!-- Incomes -->
                        <div class="bg-white text-[10px]">
                            <div class="grid grid-cols-12 gap-1 py-1 px-2">
                                <div class="col-span-5 uppercase"> Basic </div>
                                <div class="col-span-4 capitalize text-center"> { 1 month } </div>
                                <div class="col-span-3 capitalize text-center font-bold">${lite.utils.thousand_separator (payslip["basic_pay"] || 0, 2)}</div>
                            </div>
                            ${inco}
                        </div>

                    </div>
                </div>

                <!-- Totals -->
                <div class="grid grid-cols-2 border border-black text-[10px]">
                    <div class="grid grid-cols-8">
                        <div class="col-span-2 pl-1 border-r"><b>Grade:</b><br> ${employee?.employee_grade || ''}</div>
                        <div class="col-span-2 pl-1 border-r"><b>Pay Point:</b><br> - </div>
                        <div class="col-span-4 pl-1"><b>Total Deductions:</b><br> ${lite.utils.thousand_separator (payslip?.total_deductions || 0, 2) || '0.00'}</div>
                    </div>

                    <div class="grid grid-cols-8">
                        <div class="col-span-4"></div>
                        <div class="col-span-4 pl-1"><b>Total Incomes:</b><br> ${lite.utils.thousand_separator (payslip?.total_earnings || 0, 2) || '0.00'}</div>
                    </div>
                </div>

                <!-- Dept / Job / Bank -->
                <div class="grid grid-cols-3 border border-black text-[10px]">
                    <div class="pl-1 border-r"><b>Dept:</b><br>${employee?.department || ''}</div>
                    <div class="pl-1 border-r"><b>Job:</b><br>${payslip?.designation || ''}</div>
                    <div class="pl-1"><b>Net Pay:</b><br> ${lite.utils.thousand_separator (net || 0, 2) || '0.00'}</div>
                </div>

                <!-- Bank Info -->
                <div class="grid grid-cols-8 border border-black text-[10px]">
                    <div class="col-span-2 pl-1 border-r"><b>Bank Name:</b><br>${employee?.bank_name || ''}</div>
                    <div class="col-span-2 pl-1 border-r"><b>Acc No:</b><br>${employee?.account_no || ''}</div>
                    <div class="col-span-4 pl-1"><b>ECZ HQs:</b><br>ECZ</div>
                </div>
            </div>
        </div>
        <div class="h-[30px] w-full flex justify-center items-center"><div class="h-[3px] w-full rounded-full border-b border-dashed border-4 border-slate-300"></div></div>
    `
}

// export const calc_ot_amt = async ({controller}) => {
//     // if (lite.utils.object_has_data (lite.form_data)) return
//     const rows = controller.get_table_rows ("overtime_worked") || []
//     for (const row of rows) {

//         const basic = row?.emp_basic || 0.00,
//             wrk_hrs = row?.emp_wrk_hrs || 0.00,
//             wrk_days = row?.emp_wrk_days || 0.00,
//             rate = row?.rate || 0.00,
//             lunch = '13',
//             supper = '18',
//             hours_worked = getTimeDifferenceInHours (row?.from_time, row?.to_time)

//         const daily_rate = basic/wrk_days/wrk_hrs
//         const amount_earned = daily_rate*rate*hours_worked

//         controller.set_form_table_value ("overtime_worked", row?.row_id, "total_amount", amount_earned)
//         controller.set_form_table_value ("overtime_worked", row?.row_id, "total_hours", hours_worked)
//     }
// }

const timeToMinutes = (time) => {
    const [h, m] = time.split(":").map(Number)
    return (h * 60) + m
}

const overlaps = (startA, endA, startB, endB) => {
    return startA < endB && endA > startB
}


export const calc_ot_amt = async ({ controller }) => {
    const rows = controller.get_table_rows("overtime_worked") || []

    for (const row of rows) {

        const basic = row?.emp_basic || 0.00
        const wrk_hrs = row?.emp_wrk_hrs || 0.00
        const wrk_days = row?.emp_wrk_days || 0.00
        const rate = row?.rate || 0.00

        const from_time = row?.from_time
        const to_time = row?.to_time

        if (!from_time || !to_time) continue

        let hours_worked = getTimeDifferenceInHours(from_time, to_time)

        const start = timeToMinutes(from_time)
        const end = timeToMinutes(to_time)

        const lunch_start = timeToMinutes("13:00")
        const lunch_end   = timeToMinutes("14:00")

        const supper_start = timeToMinutes("18:00")
        const supper_end   = timeToMinutes("19:00")

        if (overlaps(start, end, lunch_start, lunch_end)) {
            hours_worked -= 1
        }

        if (overlaps(start, end, supper_start, supper_end)) {
            hours_worked -= 1
        }

        hours_worked = Math.max(0, hours_worked)

        const daily_rate = basic / wrk_days / wrk_hrs
        const amount_earned = daily_rate * rate * hours_worked

        controller.set_form_table_value(
            "overtime_worked",
            row?.row_id,
            "total_amount",
            amount_earned
        )

        controller.set_form_table_value(
            "overtime_worked",
            row?.row_id,
            "total_hours",
            hours_worked
        )
    }
}


export const get_ot_claim = async ({controller, value}) => {
    if (lite.utils.object_has_data (lite.form_data)) return
    const loader_id = lite.alerts.loading_toast({
        title: `FETCHING OVERTIME`,
        message:`Please wait while we the overtime information you worked`
    })
    const res = await lite.connect.x_post("get_ot_claim", {emp: value})
    lite.alerts.destroy_toast(loader_id)
    if(res.status === lite.status_codes.ok){
        lite.alerts.toast({
            toast_type:lite.status_codes.ok,
            title:"FETCHED",
            message:`Overtime Information Fetched Successfully`
        })
        
        controller.set_form_value (controller.get_form_field ("show"), "Yes")
        controller.populate_child_table ("overtime_worked", res.data)
    }
}

export const on_payroll_load = async (params)=>{
    const {controller} = params
    lite.core_payroll = new Core_Payroll()
    if (!lite.utils.object_has_data (lite.form_data)) {
        await lite.core_payroll.populate_employees(params)
    }else {
        await lite.core_payroll.init_pp ()
    }
    await lite.core_payroll.calc_payroll_totals(params)
    await lite.core_payroll.addEventListeners (controller)
    
    // if (controller?.page_type == "new-form" || controller?.page_type == "new" ||( controller.page_type == "info" && lite.form_data.status == "Draft")) {
    if (controller?.page_type == "new-form" || controller?.page_type == "new" || controller?.page_type == "new" ||( controller.page_type == "info" && lite.form_data.status == "Draft")) {
        $("#test-payslips").empty ().append (`
            <button id='analyze-payslip' class="flex items-center gap-2 h-[47px] text-16 w-[170px] btn bg-secondary_color text-theme_text_color shadow-md mr-2">
                <span class="material-symbols-outlined text-20">
                    compare
                </span>
                Test Payroll
            </button>
        `)

        const rows = controller.get_table_rows ("employee_info"),
            to_date = controller.get_form_data ()?.value

        $("#analyze-payslip").off ().on("click", async (e) => {
            $("#analyze-payslip").fadeOut()
            const $payroll_form = controller?.page_type == "new-form" || controller?.page_type == "new" ? $("#new-payroll-processor") : $ ("#payroll-processor-info")
            $payroll_form.addClass('relative')
            
            $payroll_form.addClass("relative").append(`
                <div id="test-payslip-display" class="z-[30000] absolute top-0 left-0 right-0 bottom-0 bg-default/20 backdrop-blur-[2px]">
                    <div id="overlay" class="w-full h-full flex p-2">
                        <div class="w-[30%] h-full"></div>
                        <div id="preview-area" class="w-[70%] h-full bg-white rounded-md p-3">
                            <div class="w-full h-full p-3">
                                <div class="h-[45px] w-full border-b flex justify-between items-center">
                                    <p class="font-extrabold">Trial Payroll Payslip Analysis</p>
                                    <p id="close-btn_p" class="px-3 py-1 bg-rose-600 text-white font-semibold rounded-md cursor-pointer">X</p>
                                </div>
                                <div id="display-payslip" class="h-[calc(100%-45px)] w-full overflow-y-auto py-3 flex flex-col gap-y-4">
                                    ${display_payslips(rows, to_date)}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `)

            $(document).on('click', '#close-btn_p', () => {
                $("#display-payslip").empty()
                $("#test-payslip-display").remove()
                $("#analyze-payslip").fadeIn()
            })
        })

    }
}

export const calculate_payroll = async (params) => {
    const {controller} = params
    if(!lite.core_payroll){
        lite.core_payroll = new Core_Payroll()
    }
    await lite.core_payroll.recalculate_payroll(params)
    await lite.core_payroll.addEventListeners (controller)
    return
}

export const recalculate_totals = async (params) => {
    const {controller} = params
    if(!lite.core_payroll){
        lite.core_payroll = new Core_Payroll()
    }
    await lite.core_payroll.calc_payroll_totals(params)
    await lite.core_payroll.addEventListeners (controller)
    return
}

export const resubmit_payroll = async (params) => {
    let values = params.values
    const data = {doc: values.name, }
    const res = await lite.connect.x_post ("resubmit_payroll", data)
    lite.alerts.destroy_toast(loader_id)

    if (res.status == lite.status_codes.ok) {
        lite.alerts.toast({
            toast_type: lite.status_codes.ok,
            title: "PAYROLL RESUBMISSION",
            message: "Payroll Resubmission Was Successfully"
        })
        form_controller.init_form ()
        return
    }else {
        lite.alerts.toast({
            toast_type: lite.status_codes.no_content,
            title: "PAYROLL RESUBMISSION",
            message: "Payroll Resubmission Failed"
        })
    }
    return
}


export const on_end_time_field_change = async (params) => {
    const controller = lite.page_controller.form_controller
    const emp = controller.get_form_data()?.values?.applicant
    const field_start_time = controller.get_form_data()?.values?.start_time
    const field_end_time = controller.get_form_data()?.values?.end_time
    const emp_info = await lite.connect.get_doc ("Employee", emp)
    // const overtime = await lite.connect.get_doc ("Overtime_Setup", emp_info.data.company)
    // const ss = overtime.status == lite.status_codes.ok ? overtime.data : undefined
    const employee_salary = emp_info.data.basic_pay
    const working_days = emp_info.data.working_days
    const get_overtime_setup_response = await lite.connect.x_post("get_overtime_setup", {name: lite.user.company.name})
    if (get_overtime_setup_response.status === lite.status_codes.ok) {
        if (get_overtime_setup_response.data.calculation_type === "Salary Based") {
            const number_of_hours = get_overtime_setup_response.data.number_of_hours
            if (field_start_time && field_end_time){
                if (employee_salary && working_days && number_of_hours > 0) {
                    const startTime = parseTime(field_start_time)
                    const endTime = parseTime(field_end_time)
                    const total_hours_worked = working_days * number_of_hours
                    const per_rate = employee_salary / total_hours_worked
                    const totalHours = calculateTotalHours(startTime, endTime)
                    const total_minutes_worked = totalHours.hours * 60 + totalHours.minutes
                    const total_earning = total_minutes_worked * per_rate / 60
                    controller.set_form_value(controller.get_form_field("total_earning"), parseFloat(total_earning).toFixed(2))
                }
            }
        } else {
            const fixed_rate = get_overtime_setup_response.data.fixed_rate
            if (field_start_time && field_end_time && fixed_rate > 0) {
                const startTime = parseTime(field_start_time)
                const endTime = parseTime(field_end_time)
                const totalHours = calculateTotalHours(startTime, endTime)
                const total_minutes_worked = totalHours.hours * 60 + totalHours.minutes
                const total_earning = total_minutes_worked * fixed_rate / 60
                controller.set_form_value(controller.get_form_field("total_earning"), parseFloat(total_earning).toFixed(2))

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
    const [hour, minute] = timeString.split(":").map(Number)
    return { hour, minute }
}

const calculateTotalHours = (startTime, endTime) => {
    let hourDiff = endTime.hour - startTime.hour
    let minDiff = endTime.minute - startTime.minute

    if (minDiff < 0) {
        hourDiff--
        minDiff += 60
    }

    return {
        hours: hourDiff,
        minutes: minDiff
    }
}





export const basic_pay_changed = async (params)=>{  }

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
async function calc_max_take_home_rate (max_take_home_rate, applied_amount, basic_pay, emp, max_advances) {
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
    const amount_difference = basic_pay - total_monthly_pending_payments
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
    const monthlyInterestRate = (interestRate / 100) / 12
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
        const success_id =lite.alerts.toast({ toast_type: lite.status_codes.ok, title: "SUCCESSFUL", message: "Fetch Was Successful" })
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
        const success_id =lite.alerts.toast({ toast_type: lite.status_codes.no_content, title: "COULDN't FETCH", message: `No Statutory Components Found` })
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
        const success_id =lite.alerts.toast({ toast_type: lite.status_codes.ok, title: "SUCCESSFUL", message: `Successfully allocated Component` })
        lite.alerts.destroy_toast(success_id)
    }else {
        lite.alerts.destroy_toast(loader_id)
        const error_id =lite.alerts.toast({ toast_type: lite.status_codes.no_content, title: "FAILED TO ALLOCATE", message: `Allocating Component Failed` })
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

export const validate_imprest = (params) =>{
    const values = params.values
    const req_amount = lite.utils.string_to_float(values.requested_amount)
    if(!req_amount){
        lite.alerts.toast({toast_type: lite.status_codes.not_found,title:"Requested Amount Required", message:"Please provide the amount you are requesting for requested."})
        return false
    }
} 

export const update_imprest_retirement_row =async(params)=>{
    const {controller, row_id} =params
    const table_name ="areas_of_expense"
    const row_data =controller?.get_table_row(table_name, row_id)   
    const obtained =controller?.get_form_data()?.values
    if(row_data?.usage_length && row_data?.unit_price_of_usage){
        controller?.set_form_table_value(table_name, row_id, "total_spent", ((parseFloat(row_data?.usage_length) || 0) *(parseFloat(row_data?.unit_price_of_usage) || 0)))  
    }

    const areas_of_expense =controller?.get_form_data()?.values?.areas_of_expense.map(row => row?.total_spent).reduce((total, num) => total +parseFloat(num), 0)
    let balance =parseFloat(obtained?.obtained_amount) - parseFloat(areas_of_expense)
    let owed_to =""
    if(balance !==0)
        {if(balance < 0){
            owed_to =`Officer ${obtained?.employee_no}`
            balance =balance *(-1) 
        } else if(balance >0){
            owed_to ="Examination Council of Zambia"
        }
    }
    
    controller.set_form_value(controller.get_form_field("retired_amount"), 0, null, false)
    controller.set_form_value(controller.get_form_field("retired_amount"), areas_of_expense, null, false)
    controller.set_form_value(controller.get_form_field("balance_left"), balance, null, false)
    controller.set_form_value(controller.get_form_field("owed_to"), owed_to, null, false)
    
    
}

export const recalculate_imprest_retirement_expenses =async(params)=>{
    const {controller, value} =params    
}


export const update_imprest_amount =(params)=>{
    const controller =params?.controller
    const retirement_item =controller?.get_form_data()?.values.retirement_item
    const expenses =retirement_item.map(item_cost => item_cost.amounts)
    const total_expenses =expenses.reduce((total, num) => total +parseFloat(num), 0)

    controller.set_form_value(controller.get_form_field("requested_amount"), total_expenses, null, false)
    
}

export const employee_annual_salary =async (params)=>{
    const {controller, value} =params
    
    const emp_info =await lite?.connect?.get_doc("Employee", value)
    
    if(emp_info.status ==lite.status_codes.ok){
        controller.set_form_value(controller.get_form_field("annual_salary"), (parseFloat(emp_info?.data?.basic_pay) || 0) * 12, null, false)
        
    }

}


export const populate_form =async (params)=>{
    const {controller, value} =params
    const form_data =controller?.get_form_data()?.values
    const retiring_doc_type =form_data?.retirement_type
    const model =retiring_doc_type.replace(" ", "_").replace("-","_").replace("-","_")    
    
    
    const ret_doc =await lite?.connect?.get_doc(model, value)
    
    if(ret_doc.status ==lite.status_codes.ok){   
        let total_retired =0
        let balance_from_retirement =0
        let owed_to =""
        const obtained_amount =parseFloat(ret_doc?.data?.balance)
        
        controller.set_form_value(controller.get_form_field("obtained_amount"), obtained_amount, null, false)  
        controller.set_form_value(controller.get_form_field("employee_no"), ret_doc?.data?.initiator, null, false)  
        controller.set_form_value(controller.get_form_field("surname"), ret_doc?.data?.initiator_last_name, null, false)  
        controller.set_form_value(controller.get_form_field("other_name"), ret_doc?.data?.initiator_first_name, null, false)  
        controller.set_form_value(controller.get_form_field("department"), ret_doc?.data?.department, null, false)  
        controller.set_form_value(controller.get_form_field("position"), model =="Petty_Cash" ? ret_doc?.data?.designation : ret_doc?.data?.job_title, null, false)  
        if(model !="Petty_Cash"){
            
            const areas_of_expense =[]
            let places_visited =[]
            if(!form_data?.areas_of_expense){
                $.each(ret_doc?.data?.retirement_item, (_, val) =>{
                    total_retired +=parseFloat(val.amounts)
                    areas_of_expense.push({subsistance_allowance: val.description, usage_length: 1, unit_price_of_usage: val.amounts, total_spent: val.amounts})
                }) 
                controller?.populate_child_table("areas_of_expense", areas_of_expense || [])
            }
            if(!form_data?.places_visited){
                if (ret_doc?.data?.visited_province_and_district){
                    $.each(ret_doc?.data?.visited_province_and_district, (_, val)=>{
                        places_visited.push({place :`${val.province}, ${val.district}`})
                    })
                    controller?.populate_child_table("places_visited", places_visited || [])        
                }
            }
            if (!form_data?.duration_of_tour_to){controller.set_form_value(controller.get_form_field("duration_of_tour_to"), ret_doc?.data?.duration_to_date || "", null, false)}  
            if (!form_data?.duration_of_tour_from){controller.set_form_value(controller.get_form_field("duration_of_tour_from"), ret_doc?.data?.duration_from_date || "", null, false)}  
            if (!form_data?.registration_vehicle){controller.set_form_value(controller.get_form_field("registration_vehicle"), ret_doc?.data?.registration_number_of_vechile || "", null, false)}  
            if (!form_data?.vehicle_model){controller.set_form_value(controller.get_form_field("vehicle_model"), ret_doc?.data?.vechile_make || "", null, false)}             
            if (!form_data?.retired_amount){controller.set_form_value(controller.get_form_field("retired_amount"), ret_doc?.data?.vechile_make || "", null, false)}  
        }
        balance_from_retirement =parseFloat(obtained_amount) - parseFloat(total_retired)
        owed_to =""
     

        if(balance_from_retirement !==0)
            {if(balance_from_retirement < 0){
                owed_to =`Officer ${employee_no}`
                balance_from_retirement =balance_from_retirement *(-1) 
            } else if(balance_from_retirement >0){
                owed_to ="Examination Council of Zambia"
            } else{
                owed_to =""
            }
        }

        
       if(!form_data?.obtained_amount) {controller.set_form_value(controller.get_form_field("obtained_amount"), obtained_amount, null, false)}  
       if(!form_data?.retired_amount) {controller.set_form_value(controller.get_form_field("retired_amount"), total_retired, null, false)}  
       if(!form_data?.balance_left) {controller.set_form_value(controller.get_form_field("balance_left"), balance_from_retirement, null, false)}     
       if(!form_data?.owed_to) {controller.set_form_value(controller.get_form_field("owed_to"), owed_to, null, false)}         
    }

}

export const update_retired_amount =(params)=>{
    const {controller, value} =params
    const form_data =controller?.get_form_data()?.values
    // controller.set_form_value(controller.get_form_field("imprest_obtained"), value, null, false)
    const balance =parseFloat(form_data?.imprest_obtained) ? ((parseFloat(form_data?.imprest_obtained) || 0) -(parseFloat(value) || 0)) : 0
    
    controller.set_form_value(controller.get_form_field("retired_amount"), value, null, false)
    controller.set_form_value(controller.get_form_field("balance_left"), balance, null, false)  
}

export const update_retired_and_bal_amount =(params)=>{
    const {controller, value} =params
    const form_value =controller?.get_form_data()?.values    
    
    if(form_value.imprest_obtained && form_value?.retired_amount){
        let balance =(parseFloat(form_value.imprest_obtained) || 0) -(parseFloat(form_value?.retired_amount) || 0)  
        const owed_to = ""
        if (parseFloat(balance) >0){
            owed_to ="Examination Council of Zambia"
        } else if(parseFloat(balance) <0){
            owed_to =`Officer ${employee_no}`
            balance =parseFloat(balance) *(-1)
        }
          
        controller.set_form_value(controller.get_form_field("balance_left"), balance, null, false)           
        controller.set_form_value(controller.get_form_field("owed_to"), owed_to, null, false)      
    }

}

export const provide_model =(params)=>{
    const {controller, value} =params
    let model =""
    if(value){
        if(value =="Medical Recovery"){
            model ="Recovery_Of_Medical_Bills"
        } else{
            model =value.replace(/ /g, "_")
        }    
        controller?.set_form_value(controller?.get_form_field("reference_model"), model)
    }
}

export const update_with_doc_data =async (params)=>{
    const {controller, value} =params
    const form_data =controller?.get_form_data ()?.values || {}
    
    let repayer ="",
        loan_obtained =0,
        repaid_amount =0,
        due_amount =0,
        repayer_full_name ="",
        repayment =0

    if (form_data.reference_model && value){
        
        const doc_data =await lite?.connect?.get_doc(form_data.reference_model, value)
        
        if(doc_data.status ==lite?.status_codes?.ok){

            repaid_amount =doc_data?.data?.total_amount_repaid || 0

            if(form_data.reference_model =="Advance_Application"){
                repayer =doc_data?.data?.employee_id
                loan_obtained =doc_data?.data?.amount || 0
                due_amount = doc_data?.data?.amount - repaid_amount || 0
            }else if(form_data.reference_model =="House_Loan_Application"){
                repayer =doc_data?.data?.employee
                loan_obtained =doc_data?.data?.requested_amount || 0
                due_amount =doc_data?.data?.requested_amount - repaid_amount || 0
            }else if(form_data.reference_model =="Personal_Loan_Application"){
                repayer =doc_data?.data?.employee_no
                loan_obtained =doc_data?.data?.requested_loan_amount || 0
                due_amount =doc_data?.data?.requested_loan_amount - repaid_amount || 0
            }else if(form_data.reference_model =="Long_Term_Sponsorship"){
                repayer =doc_data?.data?.employee
                loan_obtained =doc_data?.data?.tuition_fees || 0
                due_amount =doc_data?.data?.tuition_fees - repaid_amount || 0
            }else if(form_data.reference_model =="Professional_Membership_Subscription"){
                repayer =doc_data?.data?.employee
                loan_obtained =doc_data?.data?.requested_amount || 0
                
                due_amount =doc_data?.data?.requested_amount || 0
            }else if(form_data.reference_model =="Recovery_Of_Medical_Bills"){
                repayer =doc_data?.data?.employee
                loan_obtained =doc_data?.data?.staff_covered_expense || 0
                due_amount =doc_data?.data?.staff_covered_expense - repaid_amount || 0
            }else if(form_data.reference_model =="Tuition Advance"){
                repayer =doc_data?.data?.employee
                loan_obtained =doc_data?.data?.staff_covered_expense || 0
                due_amount =doc_data?.data?.staff_covered_expense - repaid_amount || 0
            }else if(form_data.reference_model =="Second_Salary_Advance_Application"){
                repayer =doc_data?.data?.employee
                loan_obtained =doc_data?.data?.amount || 0
                due_amount =doc_data?.data?.amount - repaid_amount || 0
            }
        }

        let repayer_name =""

        const fetch_emp =await lite?.connect?.get_doc("Employee", repayer)
        if (fetch_emp.status ==lite?.status_codes?.ok){
            repayer_name =fetch_emp?.data?.full_name
        }

        controller?.set_form_value(controller?.get_form_field("repayment_reference"), value)
        controller?.set_form_value(controller?.get_form_field("employee"), repayer)
        controller?.set_form_value(controller?.get_form_field("repayer"), repayer_name)
        controller?.set_form_value(controller?.get_form_field("loan_obtained"), loan_obtained)
        controller?.set_form_value(controller?.get_form_field("repaid_amount"), repaid_amount)
        controller?.set_form_value(controller?.get_form_field("due_amount"), due_amount)
        // controller?.set_form_value(controller?.get_form_field("repayment"), repayment)
    }
}

export const populate_personal_loan =async (params)=>{
    const {controller, value} =params  
    
    
    const emp_doc =await lite?.connect?.get_doc("Employee", value)
    
    if(emp_doc.status ==lite.status_codes.ok){      
        
        controller.set_form_value(controller.get_form_field("current_basic"), lite?.utils?.thousand_separator(emp_doc?.data?.basic_pay *12, lite?.currency_decimal), null, false)  
        controller.set_form_value(controller.get_form_field("employee_full_name"), emp_doc?.data?.full_name, null, false)  
        controller.set_form_value(controller.get_form_field("job_title"), emp_doc?.data?.designation, null, false)  
    }

}

function getTimeDifferenceInHours(startTime, endTime) {
    const [startHour, startMinute] = startTime.split(":").map(Number)
    const [endHour, endMinute] = endTime.split(":").map(Number)

    const startTotalMinutes = startHour * 60 + startMinute
    const endTotalMinutes = endHour * 60 + endMinute

    const diffMinutes = endTotalMinutes - startTotalMinutes
    return diffMinutes / 60
}


export const initiate_pre_payroll_payment =async (params)=> {
    const {controller, value} =params
    const item_content =null

    // const 7
    let sep =""
        
    const quick_modal = await lite.modals.quick_form("payroll", "pre_payroll", async (values, setup)=>{
        
        const loader_id = lite.alerts.loading_toast({
            title: `Initiating The Pre Payroll`,
            message:`Please wait while we organize the data.`
        })
        
        lite.modals.close_modal(quick_modal.modal_id)
        const save = await lite.connect.x_post("create_pre_payment_doc", values)
        lite.alerts.destroy_toast(loader_id)
        if(save.status === lite.status_codes.ok){
            lite.alerts.toast({
                toast_type:lite.status_codes.ok,
                title:"Initiation was Successfully",
                message:`Payroll initiation was successfully`
            })
            sep =save?.data?.emp
            const doc_name =save?.data?.pre_payroll_name
            
            lite?.utils.redirect("payroll", "payroll_processor", "new", "payroll processor", `sep=${sep}&pp=${doc_name}`, )
            
        }else {
            lite.alerts.toast({
                toast_type:lite.status_codes.no_content,
                title:"Initiation was Failed",
                message:`Failed to initiation payroll`
            })
        }
    },null)
}


export const load_temp_employees = async ({controller}) => {
    if (lite.utils.object_has_data (lite.form_data)) return
    const loader_id = lite.alerts.loading_toast({
            title: `FETCHING EMPLOYEES`,
            message:`Please wait while we fetch Seasonal and temporal employees.`
        })
        
    const r_data = await lite.connect.x_fetch ("load_temp_employees")
    const {status, data} = r_data
    lite.alerts.destroy_toast(loader_id)
    if (status == lite.status_codes.ok && data.length >= 0) {
        controller.populate_child_table ("employee", data)
        return
    }
    lite.alerts.toast({
        toast_type: lite.status_codes.no_content,
        title: `Temps Or Seasonal`,
        message: `no Temps or Seasonal Employees Found`,
    })
}

export const calc_rate_and_amount = (params) => {
    const {controller, value, row_id} = params
    const fd = controller.get_table_rows ("employee")
    $.each (fd, (_, el) => {
        if (row_id == el?.row_id) {
            const basic_pay = el?.basic_pay || 0
            const rate =  parseFloat (basic_pay / 26).toFixed (2)
            controller.set_form_table_value ("employee", row_id, "rate", rate)
            controller.set_form_table_value ("employee", row_id, "pay", parseFloat(rate * parseFloat (value).toFixed (2)).toFixed(2))
        }
    })
}