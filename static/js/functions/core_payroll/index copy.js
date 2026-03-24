import { count_week_days } from "../../overrides/form/hr/core.js"
import Payroll_HTML_Generator from "../../page/html/payroll_html_generator.js"
import { payroll_processor, calculate_payroll} from "../../overrides/form/payroll/shared.js"
export default class Core_Payroll{
    constructor(){
        this.excludeKeys = ["current_page_index", "row_id", "employee", "full_names", "designation", "basic_pay", "gross", "net", "total_un_taxable_gross",]
        this.has_initialized = false
        this.earnings_ = new Set ()
        this.noneTaxableEarnings = new Set ()
        this.noneTaxableDeductions = new Set ()
        this.noneTaxables = new Set ()
        this.listen_to = []
        this.deductions = {}
        this.employees = {}
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

    async init_pp () {
        const employeeData = lite.default_form_data.employees
        this.employees = lite.utils.array_to_object (employeeData, "name")
    }

    async init(){
        const taxable_earnings = []
        const none_taxable_earnings = []
        lite.payroll_content = lite.default_form_data
        for (const earning of lite.payroll_content.salary_components.Earning) {
            if (earning?.exclude_on_statutory_deductions && !earning?.grossable) none_taxable_earnings.push(earning)
            else taxable_earnings.push(earning)
        }

        this.paye = lite.payroll_content?.tax_band || {}
        this._deducs =  lite.utils.array_to_object(lite.payroll_content.salary_components.Deduction, "name")
        this._earnings =  lite.utils.array_to_object(lite.payroll_content.salary_components.Earning, "name")
        this.deductions = lite.utils.group (lite.payroll_content.salary_components.Deduction, "exclude_on_statutory_deductions")
        this.earnings = lite.utils.group (lite.payroll_content.salary_components.Earning, "exclude_on_statutory_deductions")
        this.taxable_earnings = lite.utils.array_to_object(taxable_earnings, "name")
        this.none_taxable_earnings = lite.utils.array_to_object(none_taxable_earnings, "name")
        this.taxable_deductions = lite.utils.array_to_object(this.deductions[0], "name")
        this.none_taxable_deductions = lite.utils.array_to_object(this.deductions[1], "name")
        this.listen_to = [...lite.payroll_content.salary_components.Deduction, ...lite.payroll_content.salary_components.Earning]
        return lite.payroll_content
    }

    #safeEval(expr) {
        const tokens = expr.match(/(\d+(\.\d+)?|\+|\-|\*|\/|\(|\))/g);
        if (!tokens) throw new Error('Invalid expression');

        let index = 0;

        function parseExpression() {
            let value = parseTerm();
            while (tokens[index] === '+' || tokens[index] === '-') {
                const op = tokens[index++];
                const nextValue = parseTerm();
                value = op === '+' ? value + nextValue : value - nextValue;
            }
            return value;
        }

        function parseTerm() {
            let value = parseFactor();
            while (tokens[index] === '*' || tokens[index] === '/') {
                const op = tokens[index++];
                const nextValue = parseFactor();
                value = op === '*' ? value * nextValue : value / nextValue;
            }
            return value;
        }

        function parseFactor() {
            const token = tokens[index++];

            if (token === '(') {
                const value = parseExpression();
                if (tokens[index++] !== ')') {
                    throw new Error('Missing closing parenthesis');
                }
                return value;
            }

            const num = parseFloat(token);
            if (isNaN(num)) {
                throw new Error(`Unexpected token: ${token}`);
            }
            return num;
        }

        const result = parseExpression();
        if (index < tokens.length) {
            throw new Error('Unexpected token at end of expression');
        }

        return result;
    }

    #evaluateExpression(template, values) {
        let expression = template.replace(/%/g, '/').replace(/x/g, '*');
        const placeholders = [...expression.matchAll(/{(.*?)}/g)].map(match => match[1]);

        for (const key of placeholders) {
            if (!(key in values)) {
                throw new Error(`Missing value for placeholder: ${key}`);
            }
            const regex = new RegExp(`{${key}}`, 'g');
            expression = expression.replace(regex, values[key]);
        }

        if (!/^[\d+\-*/().\s]+$/.test(expression)) {
            throw new Error('Invalid characters in expression');
        }

        return this.#safeEval (expression)
    }

    #checkEmployeeEligibility (payrollFromDate, payrollToDate, joining_date, lastDayOfWork, separation_status, payment_state, employee) {
        let return_bool = false
        if (separation_status === 0 || typeof separation_status === 'object') {
            return_bool = joining_date <= payrollToDate
        } else if (separation_status === 1 && (payment_state === "Unsettled" || typeof payment_state === 'object') || payment_state == 0) {
            if (lastDayOfWork >= payrollToDate) return_bool = true
            else return_bool = lastDayOfWork >= payrollFromDate && lastDayOfWork <= payrollToDate
        }
        return return_bool
    }

    normalize_date(date) {
        return new Date(date.getFullYear(), date.getMonth(), date.getDate())
    }

    removeKeysFromObjects(list, keysToRemove) {
        const removeSet = new Set(keysToRemove)

        return list.map(obj => {
            const newObj = {}
            for (const [key, value] of Object.entries(obj)) {
                if (!removeSet.has(key)) {
                    newObj[key] = value
                }
            }
            return newObj
        })
    }

    sumObjectKeys(list) {
        return list.reduce((acc, obj) => {
            for (const [key, value] of Object.entries(obj)) {
                const floatVal = lite.utils.fixed_decimals(value, 2) || 0.00
                acc[key] = (acc[key] || 0.00) + floatVal
            }
            return acc
        }, {})
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
        else if (joining_date > payrollFromDate && joining_date <= payrollToDate) {
            
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

    async update_payroll_content(controller){
        const payroll_rows = controller.get_table_rows ("employee_info") || []
        const currency = controller.get_form_value(controller.get_form_field("currency"))
        const last_row = payroll_rows.find (r => r.employee === "TOTALS" ) || {}
        
        if (lite.utils.object_has_data (last_row)) {

            for (let key of ["total_earnings", "total_deductions", "basic_pay", "net", "gross"]) {
                const val = last_row[key] 
                if (key == "gross")
                    key = "total_gross"
                else if (key == "net")
                    key = "total_net"
                else if (key == "basic_pay")
                    key = "total_basic"
                controller.set_form_value(
                    controller.get_form_field(key),
                    val,
                    lite.utils.currency(val,lite.system_settings.currency_decimals,currency?.symbol),
                    false
                )
            }
        }
    }

    async addEventListeners (controller) {
        const pp = await payroll_processor ()
        const re_calc = await calculate_payroll ()
        this.listen_to.map (field => {
            pp.on_field_change[field.name] = [re_calc]
        })
    }

    async populate_employees ({ controller }) {
        const from_date = new Date(controller.get_form_value(controller.get_form_field("from_date")))
        const to_date = new Date(controller.get_form_value(controller.get_form_field("to_date")))

        if (from_date >= to_date) {
            lite.alerts.toast({ toast_type: lite.status_codes.not_found, title: "Invalid Date Range", message: "Payroll from date is greater than payroll to date" })
            return false
        }

        if (lite.utils.get_url_parameters("page") !== "new-form" || lite.utils.get_url_parameters("page") !== "new") return
        const employeeData = lite.default_form_data.employees
        this.employees = lite.utils.array_to_object (employeeData, "name")
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
                if (emp) {
                    const allowance_temps = ["Temporal", "Seasonal Employment"]
                    const lastDayOfWork = new Date(emp?.last_day_of_work)
                    const joining_date = new Date(emp?.date_of_joining)
                    const empIsEligible = this.#checkEmployeeEligibility(from_date, to_date, joining_date, lastDayOfWork, emp?.is_separated, emp.is_separated_emp_paid, emp.full_name)
                    if (empIsEligible) {
                        const fullName = `${emp.first_name} ${emp.middle_name || ""} ${emp.last_name}`
                        overalls.total_employee += 1
                        let basic_pay = allowance_temps.includes (emp?.employment_type) ? emp.basic_pay : await this.#calculate_pro_rated_basic_pay(from_date, to_date, emp, lite.utils.string_to_float(emp.basic_pay))
                        basic_pay = lite.utils.string_to_float(basic_pay) || 0.00
                        overalls.total_basic += basic_pay
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
                            await Promise.all (emp.earnings.map (async (earning_name) => {
                                employeeData.basic_pay = basic_pay
                                if (earning_name != null) {
                                    let vl = 0.00
                                    const earning = this.taxable_earnings[earning_name]
                                    if (!earning) {
                                        this.noneTaxableEarnings.add (earning_name)
                                        this.noneTaxables.add (earning_name)
                                        this.earnings_.add (earning_name)

                                    }else {
                                        vl = await this.calc_earning (emp, employeeData, earning)
                                    }
                                    employeeData[earning_name] = vl
                                    employeeData.total_earnings += vl || 0.00
                                    overalls.earnings_totals[earning_name] = (overalls.earnings_totals[earning_name] || 0) + vl
                                }
                            }))
                        }

                        employeeData.gross = employeeData.total_earnings
                        overalls.total_earnings += employeeData.gross
                        
                        if (Array.isArray(emp?.deductions)  && emp.deductions.length > 0) {
                            await Promise.all(emp.deductions.map(async (deduction_name) => {
                                employeeData.basic_pay = basic_pay
                                if (deduction_name != null) {
                                    let ded_vl = emp[deduction_name] || 0.00
                                    const deduction = this._deducs[deduction_name]
                                    if (!deduction) {
                                        this.noneTaxables.add (deduction_name)
                                    }else if (!deduction.is_statutory_component) {
                                        this.noneTaxableDeductions.add (deduction_name)
                                    }else {
                                        ded_vl = await this.calc_deduction (emp, employeeData, deduction)
                                    }
                                    const parsedValue = lite.utils.string_to_float(ded_vl) || 0.00
                                    employeeData[deduction_name] = parsedValue
                                    employeeData.total_deductions += parsedValue
                                    overalls.total_deductions += parsedValue
                                    if (deduction != null) {
                                        overalls.deductions_totals[deduction_name] = (overalls.deductions_totals[deduction_name] || 0) + parsedValue
                                    }
                                }
                            }))
                        }

                        const incomeTaxBand = await this.calculate_income_tax_band(emp, employeeData)
                        employeeData[lite.payroll_content?.tax_band?.name] = incomeTaxBand
                        employeeData.total_deductions += incomeTaxBand
                        overalls.total_deductions += incomeTaxBand
                        overalls.total_income_tax += incomeTaxBand
                        this.total_income_tax = overalls.total_income_tax
                        employeeData.net = (employeeData.gross - employeeData.total_deductions)
                        employeeData.total_un_taxable_gross = employeeData.gross

                        if (Array.isArray(emp.earnings)  && emp.earnings.length > 0) {
                            if (this.noneTaxableEarnings instanceof Set && this.noneTaxableEarnings.size > 0) {
                                await Promise.all ([...this.noneTaxableEarnings].map (async (earning_name) => {
                                    employeeData.basic_pay = basic_pay
                                    if (earning_name != null) {
                                        const earning = this.none_taxable_earnings[earning_name]
                                        this.earnings_.add (earning_name)
                                        let vl = 0.00
                                        if (earning) {
                                            vl = await this.calc_earning (emp, employeeData, earning)
                                        }
                                        employeeData[earning_name] = vl
                                        employeeData.total_earnings += vl || 0.00
                                        employeeData.net += vl
                                        this.addOrInit (ExcludedEarnings, earning_name, vl)
                                        employeeData.total_un_taxable_gross += vl
                                        overalls.excluded_amount += vl
                                        overalls.earnings_totals[earning_name] = (overalls.earnings_totals[earning_name] || 0) + vl
                                    }
                                }))
                            }
                        }

                        if (Array.isArray(emp?.deductions) && emp.deductions.length > 0) {
                            if (this.noneTaxableDeductions instanceof Set && this.noneTaxableDeductions.size > 0) {
                                await Promise.all([...this.noneTaxableDeductions].map(async (deduction_name) => {
                                    employeeData.basic_pay = basic_pay
                                    if (deduction_name != null && emp?.deductions.includes (deduction_name)) {
                                        let ded_vl = 0.00
                                        const deduction = this._deducs[deduction_name]
                                        if (deduction) {
                                            ded_vl = await this.calc_deduction (emp, employeeData, deduction)
                                        }
                                        const parsedValue = lite.utils.string_to_float(ded_vl) || 0.00
                                        employeeData[deduction_name] = parsedValue
                                        employeeData.total_deductions += parsedValue
                                        overalls.total_deductions += parsedValue
                                        employeeData.net -= parsedValue
                                        if (deduction != null) {
                                            overalls.deductions_totals[deduction_name] = (overalls.deductions_totals[deduction_name] || 0) + parsedValue
                                        }
                                    }
                                }))
                            }
                        }
                        
                        this.global_employee_data = employeeData
                        rows.push(employeeData)
                    }
                }
            }
        ))
        const table_headers = lite.utils.get_object_keys(rows[0])
        table_headers.splice(0,3)
        freq.push(...table_headers)
        overalls.total_net = (overalls.total_earnings - overalls.total_deductions) + overalls.excluded_amount
        overalls.total__earnings_with_excluded = overalls.total_earnings + overalls.excluded_amount
        this.update_payroll_content(controller)
        items = {
            details: {
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

            items.details[earningName] = totalValue
        }

        for (let [deductionName, totalValue] of Object.entries(overalls.deductions_totals)) {
            freq.push(deductionName)
            items.details[deductionName] = totalValue  || 0.00
        }
        this.global_freq.push(...freq)
        this.global_component_totals = items.details
        items.details["employee"] = "TOTALS"
        items.details["full_names"] = "Totals"
        
        controller.set_form_value(
            controller.get_form_field("total_employees"),
            rows.length,
        )

        rows.push(items.details)
        
        controller.populate_child_table("employee_info", rows)
    }

    return_its_last_row (controller, row_id, fieldname) {
        controller.set_form_table_value("employee_info", row_id, fieldname, 0, null, false)
        return
    }

    async recalculate_payroll ({controller, fieldname, row_id, value = 0}) {
        let overalls = {
            total_employee: 0,
            total_basic: 0,
            total_gross: 0,
            total_net: 0,
            total_earnings: 0,
            total_deductions: 0
        }

        if (row_id && (lite.utils.is_number_variable(value) || value == null)) {
            const updated_row = controller.get_table_row("employee_info", row_id)
            const payroll_rows = controller.get_table_rows ("employee_info")

            if (updated_row?.employee == "TOTALS") this.return_its_last_row (controller, row_id, fieldname)
            if (lite.utils.array_has_data (payroll_rows)) {
                this.last_row = payroll_rows.find (r => r.employee === "TOTALS" ) || {}
                if (this.last_row.row_id == row_id) this.return_its_last_row (controller, row_id, fieldname)
            }

            if  (!lite.utils.array_has_data (payroll_rows)) return
            
            const basic_pay = updated_row?.basic_pay || 0.00

            let employee_data = {
                employee: updated_row.employee,
                full_names: updated_row.full_names,
                designation: updated_row.designation,
                basic_pay: basic_pay,
                gross: basic_pay,
                net: basic_pay,
                total_earnings: 0,
                total_deductions: 0,
                total_un_taxable_gross: 0,
            }

            const employees = lite.utils.array_to_object(lite.payroll_content.employees, "name")
            const employee = employees[updated_row.employee]

            if (!employee) return

            const keys = lite.utils.get_object_keys (this.removeKeysFromObjects ([updated_row], this.excludeKeys)[0])
            const all_keys = [...keys, "basic_pay", "gross", "net", "total_un_taxable_gross"]

            await Promise.all(keys.map (async column => {
                employee_data.basic_pay = basic_pay
                if (!this.noneTaxables.has (column)) {
                    const earning = this.taxable_earnings[column]
                    if (earning) {
                        if (employee.earnings.includes (column)) {
                            let component_value = 0
                            if (earning?.percentage || earning?.fixed_amount) {
                                component_value = await this.calc_earning(employee, employee_data, earning)
                            } else {
                                component_value = updated_row[column] || 0.00
                            }
                            employee_data[column] = component_value
                            employee_data.total_earnings += employee_data[column]
                            employee_data.gross += employee_data[column]
                            employee_data.total_un_taxable_gross = employee_data.gross
                        }else {   
                            employee_data[column] += 0     
                        } 
                    }
                }      
            }))

            employee_data.total_earnings += employee_data.basic_pay
            overalls.total_gross += employee_data.gross

            await Promise.all(keys.map(async column => {
                employee_data.basic_pay = basic_pay
                const deduction = this.taxable_deductions[column]
                if (deduction) {
                    if (employee.deductions.includes (column)) {
                        let component_value = 0
                        if (deduction.percentage || deduction?.fixed_amount) {
                            component_value = await this.calc_deduction(employee, employee_data, deduction)
                        } else {
                            component_value = updated_row[column] || 0.00
                        }
                        employee_data[column] = component_value
                        employee_data.total_deductions += employee_data[column]
                    }
                }else {
                    employee_data[column] += 0
                }
            }))

            const income_tax_band = await this.calculate_income_tax_band(employee, employee_data)
            employee_data[lite.payroll_content?.tax_band?.name] = income_tax_band
            employee_data.total_deductions += income_tax_band
            employee_data.net = (employee_data.total_earnings - employee_data.total_deductions)
            
            await Promise.all(keys.map(async column => {
                employee_data.basic_pay = basic_pay
                const earning = this.none_taxable_earnings[column]
                if (earning) {
                    if (employee.earnings.includes (column)) {
                        let component_value = 0
                        if (earning?.percentage || earning?.fixed_amount) {
                            component_value = await this.calc_earning(employee, employee_data, earning)
                        } else {
                            component_value = updated_row[column] || 0.00
                        }
                        employee_data[column] = component_value
                        employee_data.total_earnings += employee_data[column]
                        employee_data.net += employee_data[column]
                        employee_data.total_un_taxable_gross += employee_data[column]
                    }else {
                        employee_data[column] = 0
                    }
                }
            }))

            await Promise.all(keys.map(async column => {
                employee_data.basic_pay = basic_pay
                const deduction = this.none_taxable_deductions[column]
                if (deduction) {
                    if (employee.deductions.includes (column)) {
                        let component_value = 0
                        if (deduction.percentage || deduction?.fixed_amount) {
                            component_value = await this.calc_deduction(employee, employee_data, deduction)
                        } else {
                            component_value = updated_row[column] || 0.00
                        }
                        employee_data[column] = component_value
                        employee_data.total_deductions += employee_data[column]
                        employee_data.net -= employee_data[column]
                    }else {
                        employee_data[column] = 0
                    }
                }
            }))

            overalls.total_net += employee_data.net
            
            payroll_rows.forEach(row => {
                if (row.employee != "TOTALS" && row.full_names != "Totals") {
                    const basic = lite.utils.string_to_float(row.basic_pay) || 0.00
                    overalls.total_earnings += basic
                    overalls.total_basic += basic
                    if (row.row_id == row_id) {
                        for (const key of all_keys) {
                            const val = isNaN (employee_data[key]) ? 0 : employee_data[key]
                            controller.set_form_table_value("employee_info", row_id, key, val, null, false)
                        }
                    }
                }
            })

            const rows = []
            payroll_rows.map (itm => {
                if (itm?.employee != "TOTALS" && itm.full_names != "Totals") rows.push (itm)
            })

            const TOTALS = this.sumObjectKeys (rows)

            overalls.total_gross = TOTALS.gross
            overalls.total_net = TOTALS.net
            overalls.total_deductions = overalls.total_gross - overalls.total_net
            
            for (const key of all_keys) {
                if (!["current_page_index", "row_id", "employee", "full_names", "designation"].includes (key)) {
                    controller.set_form_table_value("employee_info", this.last_row.row_id, key, TOTALS[key], null, false)
                }
            }

            controller.set_form_value(
                controller.get_form_field("total_employees"),
                rows.length,
            )

        }

        this.update_payroll_content(controller)
        
    }

    async calc_payroll_totals ({controller, rows} ) {

        const rows_to_skip = []
        
        const payroll_rows = controller.get_table_rows ("employee_info")
        
        const keys = lite.utils.get_object_keys (this.removeKeysFromObjects ([payroll_rows[0]], this.excludeKeys)[0])
        const all_keys = [...keys, "basic_pay", "gross", "net", "total_un_taxable_gross", "row_id"]

        if (lite.utils.array_has_data (payroll_rows)) {
            const L_R = payroll_rows.find (r => r.employee === "TOTALS" ) || {}
            if (lite.utils.object_has_data (L_R)) {
                this.last_row = L_R
            }else {
                const Earn = []
                const Deduc = ["PAYE"]
                const columns = ["basic_pay", "net", "gross", "PAYE", "total_un_taxable_gross"]
                for (const col of this.listen_to) {
                    columns.push (col.name)
                    if (col.component_type === "Earning") {
                        Earn.push (col.name)
                    }else{
                        Deduc.push (col.name)
                    }
                }

                const TOTALS = this.sumObjectKeys (this.removeKeysFromObjects ((payroll_rows), ["row_id"]))
                
                let last_row = {
                    "employee": "TOTALS",
                    "full_names": "Totals",
                    "designation": '',
                    "total_un_taxable_gross": 0,
                    "total_earnings": 0, 
                    "total_deductions:": 0,
                }
                for (const key of columns) {
                    if (!["current_page_index", "row_id", "employee", "full_names", "designation"].includes (key)) {
                        last_row[key] = TOTALS[key] || 0.00
                        if (Deduc.includes (key)) {
                            last_row['total_deductions'] += TOTALS[key] || 0.00
                        }else if (Earn.includes (key)) {
                            last_row['total_earnings'] += TOTALS[key] || 0.00
                        }
                    }
                }

                payroll_rows.push (last_row)
                
                controller.populate_child_table("employee_info", payroll_rows, true,)
            }
        }

        if (rows && lite.utils.array_has_data (rows)) {
            for (const row of rows) {
                if (this.last_row.row_id != row.row_id) {
                    rows_to_skip.push (row.row_id)
                }else {
                    payroll_rows.push (row)
                    controller.populate_child_table("employee_info", payroll_rows, true,)
                }
            }
            const new_rows = []
            payroll_rows.map (itm => {
                if (itm?.employee != "TOTALS" && !rows_to_skip.includes (itm.row_id)) new_rows.push (itm)
            })

            const TOTALS = this.sumObjectKeys (new_rows)

            for (const key of all_keys) {
                if (!["current_page_index", "row_id", "employee", "full_names", "designation"].includes (key)) {
                    controller.set_form_table_value("employee_info", this.last_row.row_id, key, TOTALS[key], null, false)
                }
            }
            
            controller.set_form_value(
                controller.get_form_field("total_employees"),
                new_rows.length,
            )
        }

        this.update_payroll_content(controller)
    }

    safeJsonParse (str, fallback = []) {
        try {
            return str ? JSON.parse(str) : fallback;
        } catch {
            return fallback;
        }
    }

    async calc_earning (emp, employee_row, earning) {
        let percentage = lite.utils.string_to_float(earning?.percentage) || 0.00,
            fixed_amount = lite.utils.string_to_float(earning?.fixed_amount) || 0.00,
            earning_value = lite.utils.string_to_float(emp[earning?.name]) || 0.00
            const basic_pay = employee_row.basic_pay
        
        const vals = {
            Basic: basic_pay,
            Gross: employee_row.gross,
            Net: employee_row.net
        }
        
        if (earning?.unstandardized) {
            if (earning?.value_type == "Percentage") percentage = earning_value
            else if (earning?.value_type == "Fixed Amount") fixed_amount = earning_value
            earning_value = 0.00
        }
        
        if (!earning_value) {
            const custom_formula = earning?.custom_formula || 0,
                formula = earning?.formula || null
            if (custom_formula) {
                if (!formula) return 0.00
                let template_calc = {}
                const custom_formula_section = this.safeJsonParse (earning?.custom_formula_section)
                for (const custom_f of custom_formula_section) {

                    const wrk_days = emp?.working_days || 22
                    const wrk_hrs = emp?.working_hours || 8

                    switch (custom_f?.component) {
                        case "Basic":
                        case "Net":
                        case "Gross":
                            template_calc[custom_f?.representation] = vals[custom_f?.component] || 0
                            break;
                        case "Daily Rate":
                            template_calc[custom_f?.representation] = basic_pay/wrk_days
                            break;
                        case "Hourly Rate":
                            template_calc[custom_f?.representation] = basic_pay/wrk_days/wrk_hrs
                            break;
                        default:
                            template_calc[custom_f?.representation] = 0.00
                            break;
                    }
                }

                earning_value = this.#evaluateExpression (formula, template_calc)

            }else if (percentage) earning_value = (basic_pay * percentage) / 100

            else if (fixed_amount) earning_value = fixed_amount
        }
        
        if (earning?.exclude_on_statutory_deductions && earning?.grossable) {
            earning_value = earning_value/(this.paye?.take_home_percentage/100)
        }

        return !isNaN (earning_value) ? earning_value : 0.00
    }

    async calc_deduction (employee, employee_row, deduction) {
        let percentage = lite.utils.string_to_float(deduction?.percentage) || 0.00,
            deduction_value = lite.utils.string_to_float(employee[deduction?.name]) || 0.00,
            fixed_amount = lite.utils.string_to_float(deduction?.fixed_amount) || 0.00
        
        const basic_pay = employee_row.basic_pay
        
        let vals = {
            Basic: basic_pay,
            Gross: employee_row.gross,
            Net: employee_row.net
        }

        if (deduction?.unstandardized) {
            const main_value = employee[`main_value_${deduction?.name}`] || 0
            if (main_value) {
                vals.Basic = main_value
                employee_row['basic_pay'] = main_value
            }
            if (deduction?.value_type == "Percentage") percentage = deduction_value
            else if (deduction?.value_type == "Fixed Amount") fixed_amount = deduction_value
            deduction_value = 0.00
        }
        
        if (!deduction_value) {
            const custom_formula = deduction?.custom_formula || 0,
                formula = deduction?.formula || null
            if (custom_formula) {
                if (!formula) return 0.00
                let template_calc = {}
                const custom_formula_section = this.safeJsonParse (deduction?.custom_formula_section)
                for (const custom_f of custom_formula_section) {
                    const wrk_days = employee?.working_days || 22
                    const wrk_hrs = employee?.working_hours || 8

                    switch (custom_f?.component) {
                        case "Basic":
                        case "Net":
                        case "Gross":
                            template_calc[custom_f?.representation] = vals[custom_f?.component] || 0
                            break;
                        case "Daily Rate":
                            template_calc[custom_f?.representation] = basic_pay/wrk_days
                            break;
                        case "Hourly Rate":
                            template_calc[custom_f?.representation] = basic_pay/wrk_days/wrk_hrs
                            break;
                        default:
                            template_calc[custom_f?.representation] = 0.00
                            break;
                    }
                }
                deduction_value = this.#evaluateExpression (formula, template_calc)
            }else if (deduction.shared_deduction_custom) {
                const percentage_offset = percentage ? percentage : fixed_amount
                percentage = (percentage_offset / 100) * lite.utils.string_to_float(deduction?.shared_deduction_custom_emp) || 0.00
            }
            if (deduction.has_ceiling === 1) {
                deduction_value = await this.calculate_ceiling_deduction(employee_row, percentage, deduction?.apply_on, deduction?.ceiling_amount)
            }else if (deduction.shared_deduction_custom && !fixed_amount) {
                deduction_value = await this.calculate_shared_deduction(employee_row, percentage, deduction?.shared_deduction_custom, deduction?.apply_on)
            }else {
                if (fixed_amount) {
                    if (percentage) deduction_value = percentage
                    else deduction_value = fixed_amount
                } else if (percentage) {
                    const base_value = vals[deduction?.apply_on] || 0

                    deduction_value = (base_value * percentage) / 100
                }
            }
        }

        return lite.utils.string_to_float(deduction_value)
    }

    async calculate_shared_deduction (emp_row, deduction_percentage, shared_deduction_custom, apply_on) {
        let deductible_value = 0.00
        if (shared_deduction_custom) {
            if(apply_on === "Basic") {
                deductible_value = (emp_row.basic_pay * deduction_percentage) / 100
            }else if(apply_on === "Gross") {
                deductible_value = (emp_row.gross * deduction_percentage) / 100
            }else if(apply_on === "Net") {
                deductible_value = (emp_row.net * deduction_percentage) / 100
            }
        }
        return lite.utils.string_to_float (deductible_value)
    }

    async calculate_ceiling_deduction(employee_row, deduction_percentage, apply_on, ceiling_amount){
        let deduction_value = 0
        if(ceiling_amount > 0){
            let ceiling = 0
            if(apply_on === "Basic"){
                ceiling = (employee_row.basic_pay * deduction_percentage) / 100
            }
            else if(apply_on === "Gross"){
                ceiling = (employee_row.gross * deduction_percentage) / 100
            }
            else if(apply_on === "Net"){
                ceiling = (employee_row.net * deduction_percentage) / 100
            }
            if(ceiling > ceiling_amount){
                deduction_value = ceiling_amount
            }
            else{
                deduction_value = ceiling
            }
        }
        return deduction_value
    }
    async calculate_income_tax_band(employee, employee_row){
        const band = lite.payroll_content?.tax_band
        if(employee?.tax_band && band){
            const tax_free_amount = band.tax_free_amount
            const salary_bands = band.salary_bands
            if (lite.utils.array_has_data(salary_bands)){
                const sorted_bands = salary_bands.slice().sort((a, b) => {
                    const fromA = parseFloat(a.amount_from)
                    const fromB = parseFloat(b.amount_from)
                    return fromA - fromB
                })
                let deductible_amount = employee_row[lite.utils.lower_case(band.deduct_on)]

                if (deductible_amount > tax_free_amount) {
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