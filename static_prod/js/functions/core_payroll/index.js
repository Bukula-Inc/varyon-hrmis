// core Payrool js
import { count_week_days } from "../../overrides/form/hr/core.js"
import Payroll_HTML_Generator from "../../page/html/payroll_html_generator.js"
import { payroll_processor, calculate_payroll} from "../../overrides/form/payroll/shared.js"
export default class Core_Payroll{
    constructor(){
        this.has_initialized = false
        this.earnings = {}
        this.deductions = {}
        this.init()
        this.generator= new Payroll_HTML_Generator()
        this.$new_payroll_processor = $("#new-payroll-processor")
        this.total_income_tax = 0
        this.global_component_totals = {}
        this.global_employee_data = {}
        this.new_row = []
        this.global_freq = []
        this.counter = 0
        this.last_row = {}
    }

    #checkEmployeeEligibility (payrollFromDate, payrollToDate, joining_date, lastDayOfWork, separation_status, payment_state) {
        if (separation_status === 0 || typeof separation_status == 'object') {
            return (joining_date > payrollFromDate && joining_date <= payrollToDate) || (joining_date < payrollFromDate)
        } else if (separation_status === 1 && (payment_state === "Unsettled" || typeof payment_state == 'object')) {
            return (lastDayOfWork <= payrollToDate && lastDayOfWork >= payrollFromDate) || (payrollFromDate  < lastDayOfWork) 
        }
        return false
    }

    async #calculate_pro_rated_basic_pay (payrollFromDate, payrollToDate, employee, emp_basic_pay) {
        let prorated_salary = 0
        const joining_date = new Date(employee.date_of_joining)
        const basic_pay = lite.utils.string_to_float(emp_basic_pay) || 0.00
        const working_days = lite.utils.string_to_float(employee.working_days) || 22
        let dw = 0
        if (basic_pay === 0.00) {
            lite.alerts.toast({
                toast_type: 204,
                title: "Unprocessable Payroll",
                message: `${employee.name}'s basic pay is zero`
            })
            return
        }
        if (employee?.is_separated === 1 && (employee.is_separated_emp_paid === "Unsettled" || typeof employee.is_separated_emp_paid == 'object')) {
            const lastDayOfWork = new Date(employee.last_day_of_work)
            const isInPayrollPeriod = lastDayOfWork >= payrollFromDate && lastDayOfWork <= payrollToDate
            if (isInPayrollPeriod) {
                if (joining_date <= lastDayOfWork) {
                    dw = count_week_days(payrollFromDate, lastDayOfWork)
                    prorated_salary = (basic_pay / working_days) * count_week_days(payrollFromDate, lastDayOfWork)
                }
            }
        }
        else if (joining_date >= payrollFromDate && joining_date <= payrollToDate) {
            dw = count_week_days (joining_date, payrollToDate)
            prorated_salary = (basic_pay / working_days) * count_week_days (joining_date, payrollToDate)
        }else {
            prorated_salary = basic_pay
        }
        return lite.utils.fixed_decimals(prorated_salary, 2)
    }

    calculate_excluded_amount (earning, basic_pay, val=0.00) {
        if (val) return val
        let
            percentage = lite.utils.string_to_float(earning?.percentage) || 0.00,
            fixed_amount = lite.utils.string_to_float(earning?.fixed_amount) || 0.00
        let value = 0
        if(percentage)
            value = (basic_pay * percentage) / 100
        else if(fixed_amount)
            value = fixed_amount
        return value
    }

    addOrInit (obj, key, amountToAdd) {
        if (obj && typeof obj === "object") {
            const current = obj[key]
            obj[key] = (typeof current === "number" ? current : 0) + amountToAdd
        } else {
            throw new Error("Provided value is not a valid object")
        }
    }

    async update_payroll_content(controller, overalls){
        const currency = controller.get_form_value(controller.get_form_field("currency"))
        overalls.total_net = overalls.total_net
        controller.set_form_value(controller.get_form_field("total_employees"), overalls.total_employee, lite.utils.thousand_separator(overalls.total_employee,0))
        controller.set_form_value(controller.get_form_field("total_basic"),overalls.total_basic,lite.utils.currency(overalls.total_basic,lite.system_settings.currency_decimals,currency?.symbol), false)
        controller.set_form_value(controller.get_form_field("total_gross"),overalls.total_earnings,lite.utils.currency(overalls.total_earnings,lite.system_settings.currency_decimals,currency?.symbol), false)
        controller.set_form_value(controller.get_form_field("total_net"),overalls.total_net,lite.utils.currency(overalls.total_net,lite.system_settings.currency_decimals,currency?.symbol), false)
        controller.set_form_value(controller.get_form_field("total_earnings"),overalls.total_earnings,lite.utils.currency(overalls.total_earnings,lite.system_settings.currency_decimals,currency?.symbol), false)
        controller.set_form_value(controller.get_form_field("total__earnings_with_excluded"),overalls.total__earnings_with_excluded,lite.utils.currency(overalls.total__earnings_with_excluded,lite.system_settings.currency_decimals,currency?.symbol), false)
        controller.set_form_value(controller.get_form_field("total_deductions"),overalls.total_deductions,lite.utils.currency(overalls.total_deductions,lite.system_settings.currency_decimals,currency?.symbol), false)
    }

    // initialize payroll
    async init(){
        lite.payroll_content = lite.default_form_data
        this.earnings = lite.utils.array_to_object(lite.payroll_content.salary_components.Earning, "name")
        this.deductions = lite.utils.array_to_object(lite.payroll_content.salary_components.Deduction, "name")
        return lite.payroll_content
    }

    async addEventListeners (controller) {
        const pp = await payroll_processor ()
        const re_calc = await calculate_payroll ()
        $.each (lite.utils.get_object_keys (controller.get_table_rows ("employee_info")[0]), (_, idx) => {
            pp.on_field_change[idx] = [re_calc]
        })
    }

    async populate_employees ({ controller }) {
        const from_date = new Date(controller.get_form_value(controller.get_form_field("from_date")))
        const to_date = new Date(controller.get_form_value(controller.get_form_field("to_date")))
        await this.addEventListeners (controller)

        if (from_date >= to_date) {
            lite.alerts.toast({ toast_type: lite.status_codes.not_found, title: "Invalid Date Range", message: "Payroll from date is greater than payroll to date" })
            return false
        }

        if (lite.utils.get_url_parameters("page") !== "new-form") return
        const employeeData = lite.default_form_data.employees
        if (!lite.utils.object_has_data(employeeData)) return
        const ExcludedEarnings = {}
        const rows = []
        const freq = []
        let items = {}
        let overalls = {
            excluded_amount: 0,
            total_employee: 0,
            total_basic: 0,
            total_net: 0,
            total__earnings_with_excluded: 0,
            total_earnings: 0,
            total_deductions: 0,
            total_income_tax: 0,
            earnings_totals: {},
            deductions_totals: {}
        }
        await Promise.all (
            lite.utils.get_object_values(employeeData)?.map(async (emp) => {
                const lastDayOfWork = new Date(emp?.last_day_of_work)
                const joining_date = new Date(emp?.date_of_joining)
                const empIsEligible = this.#checkEmployeeEligibility(from_date, to_date, joining_date, lastDayOfWork, emp.is_separated, emp.is_separated_emp_paid)
                if (empIsEligible) {
                    let excludedVal = 0.00
                    const fullName = `${emp.first_name} ${emp.middle_name || ""} ${emp.last_name}`
                    overalls.total_employee += 1
                    let basic_pay = await this.#calculate_pro_rated_basic_pay(from_date, to_date, emp, lite.utils.string_to_float(emp.basic_pay))
                    basic_pay = lite.utils.string_to_float(basic_pay) || 0.00
                    overalls.total_basic += basic_pay
                    overalls.total_earnings += basic_pay
                    let employeeData = {
                        employee: emp.name,
                        full_names: fullName,
                        designation: emp.designation,
                        basic_pay: basic_pay,
                        gross: 0,
                        net: 0,
                        total_un_taxable_gross: 0,
                        total_earnings: basic_pay,
                        total_deductions: 0,
                        earnings_totals: {},
                        deductions_totals: {}
                    }
                    if (Array.isArray(emp.earnings) && emp.earnings.length > 0) {
                        await Promise.all (emp.earnings.map (async (earning) => {
                            if (earning !== null) {
                                const earningVal_obj = await this.calculate_earning(emp, basic_pay || 0.00, earning)
                                if (earningVal_obj.is_excluded) {
                                    const vl = earningVal_obj.earning_value
                                    this.addOrInit (ExcludedEarnings, earning, vl)
                                    excludedVal = vl
                                    employeeData[earning] = vl
                                }else {
                                    const vl = earningVal_obj.earning_value
                                    employeeData.total_earnings += vl
                                    overalls.total_earnings += vl
                                    overalls.earnings_totals[earning] = (overalls.earnings_totals[earning] || 0) + vl
                                    employeeData[earning] = vl
                                }
                            }
                        }))
                    }

                    employeeData.gross = employeeData.total_earnings

                    if (Array.isArray(emp?.deductions)) {
                        await Promise.all(emp.deductions.map(async (deduction) => {
                            const deductionValue = await this.calculate_deduction(emp, employeeData, deduction)
                            const parsedValue = lite.utils.string_to_float(deductionValue) || 0.00
                            employeeData[deduction] = parsedValue
                            employeeData.total_deductions += parsedValue
                            overalls.total_deductions += parsedValue
                            if (deduction !== null) {
                                overalls.deductions_totals[deduction] = (overalls.deductions_totals[deduction] || 0) + parsedValue
                            }
                        }))
                    }

                    const incomeTaxBand = await this.calculate_income_tax_band(emp, employeeData)
                    employeeData[lite.payroll_content?.tax_band?.name] = incomeTaxBand
                    employeeData.total_deductions += incomeTaxBand
                    overalls.total_deductions += incomeTaxBand
                    overalls.total_income_tax += incomeTaxBand
                    this.total_income_tax = overalls.total_income_tax
                    employeeData.net = (employeeData.gross - employeeData.total_deductions) + excludedVal
                    employeeData.total_un_taxable_gross = employeeData.gross + excludedVal
                    overalls.excluded_amount += excludedVal
                    this.global_employee_data = employeeData
                    rows.push(employeeData)
                } else {
                    console.log('====================================')
                    console.log({ emp: emp.name, empIsEligible })
                    console.log('====================================')
                }
            }
        ))


        const table_headers = lite.utils.get_object_keys(rows[0])
        table_headers.splice(0,3)
        freq.push(...table_headers)
        overalls.total_net = (overalls.total_earnings - overalls.total_deductions) + overalls.excluded_amount
        overalls.total__earnings_with_excluded = overalls.total_earnings + overalls.excluded_amount
        this.update_payroll_content(controller, overalls)
        items = {
            "details": {
                "employee": 0,
                "full_names": 0,
                "designation":0 ,
                "total_earnings": overalls.total_earnings,
                "total_deductions": parseFloat(overalls.total_deductions),
                "earnings_totals":overalls.total_earnings,
                "deductions_totals":overalls.total_deductions,
                "basic_pay":overalls.total_basic,
                "gross":overalls.total_earnings,
                "total_un_taxable_gross": overalls.excluded_amount + overalls.total_earnings,
                "net":  overalls.total_net,
                "PAYE": overalls.total_income_tax,
                ...ExcludedEarnings,
            }
        }
        for (let [earningName, totalValue] of Object.entries(overalls.earnings_totals)) {
            freq.push(earningName)

            items["details"][earningName] = totalValue
        }

        for (let [deductionName, totalValue] of Object.entries(overalls.deductions_totals)) {
            freq.push(deductionName)
            items["details"][deductionName] = totalValue  || 0.00
        }
        this.global_freq.push(...freq)
        this.global_component_totals = items["details"]
        items["details"]["employee"] = "TOTALS"
        items["details"]["full_names"] = "Totals"
        rows.push(items["details"])

        controller.populate_child_table("employee_info", rows)
    }


    async recalculate_payroll({controller, fieldname, row_id, value = 0}) {
        this.new_row = []
        this.counter += 1
        if (row_id && (lite.utils.is_number_variable(value) || value == null)) {
            const row = controller.get_table_row("employee_info", row_id);
            if (row.employee.value != "Totals" ) {
                let excludedEarning = undefined
                let excluded_amount = 0.00
                const rows = controller.get_table_rows("employee_info");
                this.last_row = rows[rows.length - 1]
                rows.pop (rows.length - 1)
                const basic_pay = lite.utils.string_to_float(row.basic_pay.value) || 0.00;
                let employee_data = {
                    employee: row.employee.value,
                    full_names: row.full_names.value,
                    designation: row.designation.value,
                    basic_pay: basic_pay,
                    gross: basic_pay,
                    net: basic_pay,
                    total_earnings: basic_pay,
                    total_deductions: 0,
                    total_un_taxable_gross: 0,
                };
                const employees = lite.utils.array_to_object(lite.payroll_content.employees, "name")
                const employee = employees[row.employee.value]
                const earnings = lite.utils.array_to_object(lite.payroll_content.salary_components.Earning, "name")
                const exclusive = ["employee", "full_names", "designation", "basic_pay", "gross", "net"];
                await Promise.all(lite.utils.get_object_values(row).map(async field => {
                    const earning = earnings[field.fieldname];
                    if (earning && !exclusive.includes(field.fieldname)) {
                        let component_value = 0
                        if (employee.earnings.includes (earning.name)) {
                            if (earning?.percentage || earning?.fixed_amount) {
                                const earningVal_obj = await this.calculate_earning(employee, employee_data.basic_pay, field.fieldname);
                                if (earningVal_obj.is_excluded) {
                                    excluded_amount = lite.utils.string_to_float (earningVal_obj.earning_value)
                                    excludedEarning = earning.name
                                }else {
                                    component_value = lite.utils.string_to_float(earningVal_obj.earning_value)
                                }
                            } else {
                                component_value = lite.utils.string_to_float(field.value) || 0.00;
                            }
                        }

                        employee_data[field.fieldname] = component_value;
                        employee_data.total_earnings += component_value;
                        employee_data.gross += component_value;
                    }
                }));
                await Promise.all(lite.utils.get_object_values(row).map(async field => {
                    if (!exclusive.includes(field.fieldname) && employee.deductions.includes (field.fieldname)) {
                        const deductions = lite.utils.array_to_object(lite.payroll_content.salary_components.Deduction, "name")
                        const deduction = deductions[field.fieldname];
                        let component_value = 0;
                        if (deduction?.component_type === "Deduction") {
                            if (deduction.percentage || deduction?.fixed_amount) {
                                component_value = await this.calculate_deduction(employee, employee_data, field.fieldname);
                            } else {
                                component_value = lite.utils.string_to_float(field.value) || 0.00;
                            }
                            console.table({fieldname, component_value, value});

                            employee_data[field.fieldname] = component_value || 0.00;
                            employee_data.total_deductions += component_value;
                        }
                    }
                }));
                const income_tax_band = await this.calculate_income_tax_band(employee, employee_data);
                employee_data[lite.payroll_content?.tax_band?.name] = income_tax_band;
                employee_data.total_deductions += income_tax_band;
                if (excluded_amount && employee.earnings.includes(excludedEarning)) employee_data[excludedEarning] = lite.utils.string_to_float(excluded_amount) || 0.00;
                employee_data.net = (employee_data.total_earnings - employee_data.total_deductions) + excluded_amount;
                employee_data.total_un_taxable_gross = employee_data.gross + excluded_amount
                let overalls = {
                    total_employee: rows.length,
                    total_basic: 0,
                    total_gross: 0,
                    total_net: 0,
                    total_earnings: 0,
                    total_deductions: 0
                };
                $.each(rows, (_, field) => {
                    if (field.employee.value != "Totals") {
                        const basic = lite.utils.string_to_float(field.basic_pay.value) || 0.00;
                        overalls.total_earnings += basic;
                        overalls.total_basic += basic;
                        $.each(lite.utils.get_object_values(field), (_, f) => {
                            if (f.row_id === row_id) {
                                controller.set_form_table_value("employee_info", row_id, f.field, employee_data[f.fieldname], null, false);
                            } else {
                                controller.set_form_table_value("employee_info", row_id, f.field, f.value, null, false);
                            }

                            if (!exclusive.includes(f.fieldname)) {
                                if (earnings[f.fieldname]) {
                                    overalls.total_earnings += lite.utils.string_to_float(f.value) || 0.00;
                                } else {
                                    overalls.total_deductions += lite.utils.string_to_float(f.value) || 0.00;
                                }
                            }
                        });
                    }
                });
                overalls.total_gross = overalls.total_earnings;
                overalls.total_net = overalls.total_earnings - overalls.total_deductions;
                this.new_row.push(employee_data);
                const excludedKeys = new Set(["employee", "full_names", "designation", "basic_pay", excludedEarning]);

                if (fieldname && !excludedKeys.has(fieldname)) {
                    const totals = controller.get_table_column_values("employee_info", [fieldname, "PAYE", "NAPSA", "gross", "net" ], false)
                    totals[fieldname].pop (totals[fieldname].length -1)
                    totals.NAPSA.pop (totals.NAPSA.length -1)
                    totals.PAYE.pop (totals.PAYE.length -1)
                    totals.gross.pop (totals.gross.length -1)
                    totals.net.pop (totals.net.length -1)
                    const vl = lite.utils.sum(totals[fieldname])
                    const napsa = lite.utils.sum(totals.NAPSA)
                    const paye = lite.utils.sum(totals.PAYE)
                    overalls.total_gross = lite.utils.sum(totals.gross)
                    overalls.total_net = lite.utils.sum(totals.net)
                    overalls.total_deductions = overalls.total_gross - overalls.total_net

                    controller.set_form_table_value("employee_info", this.last_row[fieldname].row_id, this.last_row[fieldname].field, vl, null, false);
                    controller.set_form_table_value("employee_info", this.last_row.NAPSA.row_id, this.last_row.NAPSA.field, napsa, null, false);
                    controller.set_form_table_value("employee_info", this.last_row.PAYE.row_id, this.last_row.PAYE.field, paye, null, false);
                    controller.set_form_table_value("employee_info", this.last_row.gross.row_id, this.last_row.gross.field, overalls.total_gross, null, false);
                    controller.set_form_table_value("employee_info", this.last_row.net.row_id, this.last_row.net.field, overalls.total_net, null, false);
                }

                this.update_payroll_content(controller, overalls);
            }
        }
    }

    async calculate_earning(employee, basic_pay, earning_name) {
        if (!earning_name) {
            console.warn(`⚠️ No earning found in employee_earnings for: ${earning_name}`)
            return 0.00
        }
        let earning_value = 0,
            is_excluded = false
        const earning = this.earnings[earning_name]
        if (!earning) {
            console.warn(`⚠️ No earning found in Salary components for: ${earning_name}`)
            return 0.00
        }
        let percentage = lite.utils.string_to_float(earning?.percentage) || 0.00,
            fixed_amount = lite.utils.string_to_float(earning?.fixed_amount) || 0.00

        if (earning?.exclude_on_statutory_deductions) {
            const excluded_earning = {
                emp: employee.name,
                earning: earning.name,
                value: this.calculate_excluded_amount(earning, basic_pay, earning_value)
            }
            earning_value = excluded_earning.value
            is_excluded = true
        } else {
            if (percentage) {
                earning_value = (basic_pay * percentage) / 100
            } else if (fixed_amount) {
                earning_value = fixed_amount
            }
        }
        return { is_excluded, earning_value }
    }

    async calculate_deduction(employee, employee_row, deduction_name) {
        if (!deduction_name) {
            console.warn(`⚠️ No earning found in employee_earnings for: ${deduction_name}`)
            return 0.00
        }
        if (!employee) {
            console.warn("⚠️ No employee provided.")
            return 0
        }
        let deduction_value = 0

        const deductions = lite.utils.array_to_object(lite.payroll_content.salary_components.Deduction, "name")
        const deduction = deductions[deduction_name]

        if (!deduction) {
            console.warn(`⚠️ Deduction "${deduction_name}" not found in salary components.`)
            return 0
        }
        const percentage = lite.utils.string_to_float(deduction?.percentage) || 0.00
        const fixed_amount = lite.utils.string_to_float(deduction?.fixed_amount) || 0.00
        if (deduction.has_ceiling === 1) {
            deduction_value = await this.calculate_ceiling_deduction(employee_row, deduction)
        } else if (deduction.shared_deduction_custom) {
            deduction_value = await this.calculate_shared_deduction(employee_row, deduction)
        } else {
            if (fixed_amount) {
                deduction_value = fixed_amount
            } else if (percentage) {
                const base_value = {
                    Basic: employee_row.basic_pay,
                    Gross: employee_row.gross,
                    Net: employee_row.net
                }[deduction?.apply_on] || 0

                deduction_value = (base_value * percentage) / 100
            }
        }
        return lite.utils.string_to_float(deduction_value)
    }

    async calculate_shared_deduction (emp_row, deduction) {
        let deductible_value = 0.00
        if (deduction?.shared_deduction_custom) {
            let employeePercentage = lite.utils.string_to_float(deduction?.shared_deduction_custom_emp) || 0.00
            if(deduction?.apply_on === "Basic") {
                deductible_value = (emp_row.basic_pay * employeePercentage) / 100
            }else if(deduction?.apply_on === "Gross") {
                deductible_value = (emp_row.gross * employeePercentage) / 100
            }else if(deduction?.apply_on === "Net") {
                deductible_value = (emp_row.net * employeePercentage) / 100
            }
        }
        return lite.utils.string_to_float (deductible_value)
    }

    async calculate_ceiling_deduction(employee_row, deduction){
        let deduction_value = 0
        if(deduction?.ceiling_amount > 0){
            let ceiling = 0
            if(deduction?.apply_on === "Basic"){
                ceiling = (employee_row.basic_pay * deduction?.percentage) / 100
            }
            else if(deduction?.apply_on === "Gross"){
                ceiling = (employee_row.gross * deduction?.percentage) / 100
            }
            else if(deduction?.apply_on === "Net"){
                ceiling = (employee_row.net * deduction?.percentage) / 100
            }
            if(ceiling > deduction?.ceiling_amount){
                deduction_value = deduction?.ceiling_amount
            }
            else{
                deduction_value = ceiling
            }
        }
        return deduction_value
    }
    async calculate_income_tax_band(employee, employee_row){
        const band = lite.payroll_content?.tax_band
        if(employee.tax_band && band){
            const tax_free_amount = band.tax_free_amount
            const salary_bands = band.salary_bands
            if (lite.utils.array_has_data(salary_bands)){
                const sorted_bands = salary_bands.slice().sort((a, b) => {
                    const fromA = parseFloat(a.amount_from)
                    const fromB = parseFloat(b.amount_from)
                    return fromA - fromB
                })
                let deductible_amount = employee_row[lite.utils.lower_case(band.deduct_on)]
                if (deductible_amount > tax_free_amount){
                    let deduction = 0,
                        cash_on_hand = deductible_amount - tax_free_amount,
                        taxable_amount = 0,
                        end_calculations=false,
                        total_bands = sorted_bands.length - 1
                    $.each(sorted_bands,(_, b)=>{
                        if(end_calculations) return
                        const perc = lite.utils.string_to_float(b.deduction_percentage) / 100
                        const amount_from = lite.utils.is_number_variable(b.amount_from) ? lite.utils.string_to_float(b.amount_from) : 0
                        const amount_to = lite.utils.is_number_variable(b.amount_to) && b.amount_to !== "Above" ? lite.utils.string_to_float(b.amount_to) : 0
                        const difference = lite.utils.fixed_decimals((Math.abs(amount_to - amount_from)),4)
                        let   tax_amount = 0
                        if (cash_on_hand >= difference){
                            if(_ < total_bands){
                                taxable_amount = difference
                                cash_on_hand -= difference
                            }
                            else{
                                taxable_amount = cash_on_hand
                                end_calculations = true
                            }
                        }
                        else{
                            taxable_amount = cash_on_hand
                            end_calculations = true
                        }
                        tax_amount = taxable_amount * perc
                        deduction += tax_amount
                    })
                    return deduction
                }
            }
        }
        return 0
    }
}