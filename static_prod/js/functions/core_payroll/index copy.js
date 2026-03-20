
import { payroll_processor } from "../../overrides/form/payroll/index.js"
import { calculate_payroll } from "../../overrides/form/payroll/core.js"
import Payroll_HTML_Generator from "../../page/html/payroll_html_generator.js"

let EXCLUDED_EARNING = []
const EARNINGS = []

export default class Core_Payroll{
    constructor(){
        this.has_initialized = false
        this.init()
        this.generator= new Payroll_HTML_Generator()
        this.$new_payroll_processor = $("#new-payroll-processor");
        this.total_income_tax = 0
        this.global_component_totals = {}
        this.global_employee_data = {}
        this.new_row = []
        this.global_freq = []
        this.counter = 0;
    }

    // initialize payroll
    async init(){
        // const {status, data, error_message} = await lite.connect.x_fetch("get_payroll_processor_content")
        // this.has_initialized = true
        // if(status !== lite.status_codes.ok){
        //     lite.alerts.toast({toast_type: status, title: "Something went wrong", message: error_message})``
        //     return false
        // }
        // else{
        //     lite.payroll_content = data
        //     return lite.payroll_content
        // }
    }

  // to extend payroll fields
    async extend_payroll_fields(fields){
        let component_fields = []
        const  earnings = lite.payroll_content?.earnings || [], deductions = lite.payroll_content?.deductions || []
        $.each([...lite.utils.get_object_values(earnings),...lite.utils.get_object_values(deductions)],(_,comp)=>{
            component_fields.push({
                id: comp.name,
                fieldlabel: comp.name,
                fieldname: comp.name,
                fieldtype: (comp?.is_standard_component === 1 || ["Fixed Amount", "Percentage"].includes(comp.value_type) || comp.fixed_amount != 0) ? "read-only" : "currency",
                columns: 4,
                required: false,
                hidden: false,
                placeholder: `Enter ${comp.name}`,
                default:"0.00",
                is_figure:true
            })
            payroll_processor.on_field_change[comp.name] = [calculate_payroll]
        })
        $.each(fields,(_, f)=>{
            if(f.fieldname === "employee_info"){
                if(lite.payroll_content?.income_tax_band){
                    component_fields.push({
                        id: lite.payroll_content?.income_tax_band?.name,
                        fieldlabel: lite.payroll_content?.income_tax_band?.name,
                        fieldname: lite.payroll_content?.income_tax_band?.name,
                        fieldtype: "read-only",
                        columns: 4,
                        required: false,
                        hidden: false,
                        placeholder: "",
                        default:"0.00",
                        is_figure:true
                    })
                }
                component_fields.push(...[
                    {
                        id: "gross",
                        fieldlabel: "Gross",
                        fieldname: "gross",
                        fieldtype: "read-only",
                        columns: 4,
                        required: true,
                        hidden: false,
                        placeholder: "",
                        default:"0.00",
                        is_figure:true
                    },
                    {
                        id: "net",
                        fieldlabel: "Net",
                        fieldname: "net",
                        fieldtype: "read-only",
                        columns: 4,
                        required: true,
                        hidden: false,
                        placeholder: "",
                        default:"0.00",
                        is_figure:true
                    }
                ])
                f.fields.push(...component_fields)
            }
        })
    
        return fields
    }

    async extend_total_fields(fields) {
        let total_fields = [];
        const earnings = lite.payroll_content?.earnings || [], 
            deductions = lite.payroll_content?.deductions || [];

        // Create fields for total earnings
        $.each(earnings, (_, earning) => {
            total_fields.push({
                id: `${earning.name}_total`,
                fieldlabel: `${earning.name} Total`,
                fieldname: `${earning.name}_total`,
                fieldtype: "read-only",
                columns: 4,
                required: false,
                hidden: false,
                placeholder: "",
                default: "0.00",
                is_figure: true
            });
        });

        // Create fields for total deductions
        $.each(deductions, (_, deduction) => {
            total_fields.push({
                id: `${deduction.name}_total`,
                fieldlabel: `${deduction.name} Total`,
                fieldname: `${deduction.name}_total`,
                fieldtype: "read-only",
                columns: 4,
                required: false,
                hidden: false,
                placeholder: "",
                default: "0.00",
                is_figure: true
            });
        });

        // Push total fields to the existing form fields
        $.each(fields, (_, f) => {
            if (f.fieldname === "employee_info") {
                f.fields.push(...total_fields);
            }
        });

        return fields;
    }


    // to populate employee data for the first time
    async populate_employees({ controller }) {
        const payrollToDateStr = controller.get_form_value(controller.get_form_field("to_date"));
        const payrollToDate = new Date(payrollToDateStr);
        const payrollFromDateStr = controller.get_form_value(controller.get_form_field("from_date"));
        const payrollFromDate = new Date(payrollFromDateStr);
    
        if (payrollFromDate >= payrollToDate) {
            lite.alerts.toast({ toast_type: lite.status_codes.not_found, title: "Invalid Date Range", message: "Payroll from date is greater than payroll to date" });
            return false;
        } 
        else {
        
            if (lite.utils.get_url_parameters("page") !== "new-form") return;
    
            const employeeData = lite.payroll_content?.employee;
            if (!lite.utils.object_has_data(employeeData)) return;
    
            controller.clear_table("employee_info");

            let freq = [];
            let items = {};
            let rows = [];
            let overalls = {
                // total_employee: lite.utils.get_object_values(employeeData)?.length,
                total_employee: 0,
                total_basic: 0,
                total_gross: 0,
                total_net: 0,
                total_earnings: 0,
                total_deductions: 0, 
                total_income_tax: 0,
                earnings_totals: {},  
                deductions_totals: {} 
            };
    
            await Promise.all(
       
                lite.utils.get_object_values(employeeData)?.map(async (emp) => {
                    const lastDayOfWorkStr = emp?.separation?.last_day_of_work;
                    const lastDayOfWork = new Date(lastDayOfWorkStr) 
                    const separation_status = emp?.is_separated;
                   
                    const joiningDate = new Date(emp?.date_of_joining);


                    function isEligibleForPayroll(joiningDate, lastDayOfWork, payrollToDate, payrollFromDate, separation_status) {
                        if (separation_status === 0) { 
                            // Employee is not separated
                            return (joiningDate <= payrollToDate && joiningDate >= payrollFromDate) || (joiningDate < payrollFromDate);
                        } else if (separation_status === 1) { 
                            // Employee is separated
                            return (lastDayOfWork <= payrollToDate && lastDayOfWork >= payrollFromDate) || (payrollFromDate  < lastDayOfWork) ;
                        }
                        return false;
                    }


               
                const isEligible = isEligibleForPayroll(joiningDate, lastDayOfWork, payrollToDate, payrollFromDate, separation_status);

                if (isEligible) {

                    overalls.total_employee +=1
                    let basic = await this.calculate_pro_rata(emp, controller, emp.basic_pay);
                    overalls.total_basic += lite.utils.string_to_float(basic) || 0.00;
                    overalls.total_earnings += lite.utils.string_to_float(basic) || 0.00;
    
                        const fullName = `${emp.first_name} ${emp.middle_name || ""} ${emp.last_name}`;
                        let employeeData = {
                            employee: emp.name,
                            full_names: fullName,
                            designation: emp.designation,
                            basic_pay: basic,
                            gross: basic,
                            net: basic,
                            total_earnings: basic,
                            total_deductions: 0,
                            earnings_totals: {},  
                            deductions_totals: {} 
                        };
    
                   // Calculate employee earnings
                        await Promise.all(emp.earnings.map(async (earning) => {

                            const earningValue = await this.calculate_earning(emp, basic, earning.earning);
                            employeeData[earning.earning] = lite.utils.string_to_float(earningValue) || 0.00;
                            employeeData.gross += lite.utils.string_to_float(earningValue) || 0.00;
                            employeeData.total_earnings += lite.utils.string_to_float(earningValue) || 0.00;
                            overalls.total_earnings += lite.utils.string_to_float(earningValue) || 0.00;
                            if (earning.earning !== null) {
                                overalls.earnings_totals[earning.earning] = (overalls.earnings_totals[earning.earning] || 0) + earningValue;
                            }
                        }));
                        // Calculate deductions
                        await Promise.all(
                            emp?.deductions?.map(async (deduction) => {
                                const deductionValue = await this.calculate_deduction(emp, employeeData, deduction.deduction, controller);
                                employeeData[deduction.deduction] = lite.utils.string_to_float(deductionValue) || 0.00;
                                employeeData.total_deductions +=  lite.utils.string_to_float(deductionValue) || 0.00;
                                overalls.total_deductions +=  lite.utils.string_to_float(deductionValue) || 0.00;
                                if (deduction.deduction !== null) {
                                overalls.deductions_totals[deduction.deduction] = (overalls.deductions_totals[deduction.deduction] || 0) + deductionValue || 0.0;
                                }
                            })
                        );
                        // Calculate income tax band
                        const incomeTaxBand = await this.calculate_income_tax_band(emp, employeeData);
                        employeeData[lite.payroll_content?.income_tax_band?.name] = incomeTaxBand;
                        employeeData.total_deductions += incomeTaxBand;
                        overalls.total_deductions += incomeTaxBand;
                        overalls.total_income_tax += incomeTaxBand;
                        this.total_income_tax = overalls.total_income_tax
                        employeeData.net = employeeData.total_earnings - employeeData.total_deductions;
                        this.global_employee_data = employeeData
                       
                        rows.push(employeeData);
                             
                    }
                
                  
                }));



           
         
            const table_headers = lite.utils.get_object_keys(rows[0]);
            table_headers.splice(0,3);

         
            freq.push(...table_headers);
          
            
         
            overalls.total_gross = overalls.total_earnings;
            overalls.total_net = overalls.total_gross - overalls.total_deductions;
            this.update_payroll_content(controller, overalls);
             items = {
                "details": {
                    "employee": 0,
                    "full_names": 0,
                    "designation":0 ,
                    "total_earnings": overalls.total_gross,
                    "total_deductions": parseFloat(overalls.total_deductions),
                    "earnings_totals":overalls.total_earnings,
                    "deductions_totals":overalls.total_deductions,
                    "basic_pay":overalls.total_basic,
                    "gross":overalls.total_gross,
                    "net":  overalls.total_net,
                    "PAYE": overalls.total_income_tax
                }
            }


            for (let [earningName, totalValue] of Object.entries(overalls.earnings_totals)) {
                freq.push(earningName)
                items["details"][earningName] = totalValue || 0.00;
              

            }
        
            for (let [deductionName, totalValue] of Object.entries(overalls.deductions_totals)) {
                freq.push(deductionName)
                items["details"][deductionName] = totalValue  || 0.00;
                
                
            }
            this.global_freq.push(...freq)
            this.global_component_totals = items["details"]
            items["details"]["employee"] = "Totals"
            items["details"]["full_names"] = "Totals"
            rows.push(items["details"])
            controller.populate_child_table("employee_info", rows); 
            // this.$new_payroll_processor.html('').prop ("disabled", true); 
            // $('.payroll-processor-totals ').empty()?.html( this.generator.create_payroll_totals_titles(freq))
            // freq.forEach((col) => {
            //    let column = col.replace(/\s+/g, '_');
               
            //    $('#' + column ).val( lite.utils.thousand_separator(items["details"][col], 2))
            // })

           


           
        }
    }


async populate_employee({ controller, employeeId }) {
    if (lite.utils.get_url_parameters("page") !== "new-form") {
        return;
    }
    
    const employee = lite.payroll_content?.employee?.[employeeId];
    
    if (!employee) {
        console.error("Employee not found");
        return;
    }
    
    let overalls = { 
        total_employee: 1, 
        total_basic: 0, 
        total_gross: 0, 
        total_net: 0, 
        total_earnings: 0, 
        total_deductions: 0 
    };



    
    const basic = await this.calculate_pro_rata(employee, controller, employee.basic_pay )
    overalls.total_basic = basic;
    overalls.total_earnings = basic;
    const full_name = employee.full_name
    // const full_name = `${employee.first_name} ${employee.middle_name || ""} ${employee.last_name}`;
    
    let employee_data = {
        employee: employee.name,
        full_names: full_name,
        designation: employee.designation,
        basic_pay: basic,
        gross: basic,
        net: basic,
        total_earnings: basic,
        total_deductions: 0
    };
    
    // calculate employee earnings
    await Promise.all(employee?.earnings?.map(async earning => {
        const earning_value = await this.calculate_earning(employee, basic, earning?.earning);
        employee_data[earning.earning] =  lite.utils.string_to_float(earning_value) || 0.00;
        employee_data.gross += lite.utils.string_to_float(earning_value) || 0.00;
        employee_data.total_earnings += lite.utils.string_to_float(earning_value) || 0.00;
        overalls.total_earnings +=  lite.utils.string_to_float(earning_value) || 0.00;
    }));
  
    
    // calculate deductions
    await Promise.all(employee?.deductions?.map(async deduction => {
        const deduction_value = await this.calculate_deduction(employee, employee_data, deduction.deduction);
        employee_data[deduction.deduction] =  lite.utils.string_to_float(deduction_value) || 0.00;
        employee_data.total_deductions +=  lite.utils.string_to_float(deduction_value) || 0.00;
        overalls.total_deductions += lite.utils.string_to_float(deduction_value) || 0.00;
    }));
    
    // calculate income tax band
    const income_tax_band = await this.calculate_income_tax_band(employee, employee_data);
    employee_data[lite.payroll_content?.income_tax_band?.name] = income_tax_band;
    employee_data.total_deductions += income_tax_band;
    overalls.total_deductions += income_tax_band;
    employee_data.net = employee_data.total_earnings - employee_data.total_deductions;

    // controller.set_form_table_value("employee_info", [employee_data]);
    
    overalls.total_gross = overalls.total_earnings;
    overalls.total_net = overalls.total_gross - overalls.total_deductions;
    // this.update_payroll_content(controller, overalls);
    return employee_data
   
}

 

async recalculate_payroll({controller, row_id, value = 0}) {
    this.new_row = []
    this.counter += 1
    if (row_id && (lite.utils.is_number_variable(value) || value == null)) {
        const row = controller.get_table_row("employee_info", row_id);
        if (row.employee.value != "Totals" ) {
            const rows = controller.get_table_rows("employee_info");
            const basic_pay = lite.utils.string_to_float(row.basic_pay.value) || 0.00;
    
            let employee_data = {
                employee: row.employee.value,
                full_names: row.full_names.value,
                designation: row.designation.value,
                basic_pay: basic_pay,
                gross: basic_pay,
                net: basic_pay,
                total_earnings: basic_pay,
                total_deductions: 0
            };
    
            const employee = lite.payroll_content.employee[row.employee.value];
            const exclusive = ["employee", "full_names", "designation", "basic_pay", "gross", "net"];
    
            // Calculate earnings
            await Promise.all(lite.utils.get_object_values(row).map(async field => {
                const earning = lite.payroll_content.earnings[field.fieldname];
                if (earning && !exclusive.includes(field.fieldname)) {
                    let component_value = 0;
                    if (earning?.percentage || earning?.fixed_amount) {
                        component_value = await this.calculate_earning(employee, employee_data.basic_pay, field.fieldname);
                    } else {
                        component_value = lite.utils.string_to_float(field.value) || 0.00;
                    }
                    employee_data[field.fieldname] = component_value;
                    employee_data.total_earnings += component_value;
                    employee_data.gross += component_value;
                }
            }));
    
            // Calculate deductions
            await Promise.all(lite.utils.get_object_values(row).map(async field => {
                if (!exclusive.includes(field.fieldname)) {
                    const deduction = lite.payroll_content.deductions[field.fieldname];
                    
                    let component_value = 0;
                    if (deduction?.component_type === "Deduction") {
                        if (deduction.percentage || deduction?.fixed_amount) {
                            component_value = await this.calculate_deduction(employee, employee_data, field.fieldname);
                        
                        } else {
                            component_value = lite.utils.string_to_float(field.value) || 0.00;
                           
                        }
                        employee_data[field.fieldname] = component_value || 0.00;
                        employee_data.total_deductions += component_value;
                        
                    }
                }
            }));

    
            const income_tax_band = await this.calculate_income_tax_band(employee, employee_data);
            employee_data[lite.payroll_content?.income_tax_band?.name] = income_tax_band;
            employee_data.total_deductions += income_tax_band;
            employee_data.net = employee_data.total_earnings - employee_data.total_deductions;

    
            // Recalculate overall totals
            let overalls = {
                total_employee: rows.length -1,
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
                        if (lite.payroll_content.earnings[f.fieldname]) {
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
            this.update_payroll_content(controller, overalls);
            this.new_row.push(employee_data);
           
    
            const totals = {};
            
    
            if ( this.new_row.length == rows.length - 1) {
                  // Loop through each employee object
                  this.new_row.forEach(employee => {
                // Loop through each key in the employee object
                Object.keys(employee).forEach(key => {
                    // Check if the value is a number and should be totaled
                    if (typeof employee[key] === 'number') {
                        if (!totals[key]) {
                            totals[key] = 0;
                        }
                        totals[key] += employee[key];
                    }
                });
            });
    
    
            totals["earnings_totals"] = overalls.total_earnings,
            totals["deductions_totals"] = overalls.total_deductions,
            totals["employee"] = "Totals"
            totals["full_names"] = "Totals"
           this.new_row.push(totals)
           controller.populate_child_table("employee_info",   this.new_row);
         
            }
            
          
            // // Populate payroll totals
            // $('.payroll-processor-totals').empty()?.html(this.generator.create_payroll_totals_titles(this.global_freq));
            // this.global_freq.forEach((col) => {
            //     let column = col.replace(/\s+/g, '_');
            //     $('#' + column).val(lite.utils.thousand_separator(totals[col] || 0.00, 2));
            // });
            
           
        }
    
    }
    
  
  
}

    

    async update_payroll_content(controller, overalls){
        const currency = controller.get_form_value(controller.get_form_field("currency"))
            overalls.total_net = overalls.total_earnings - overalls.total_deductions
            controller.set_form_value(controller.get_form_field("total_employees"), overalls.total_employee, lite.utils.thousand_separator(overalls.total_employee,0))
            controller.set_form_value(controller.get_form_field("total_basic"),overalls.total_basic,lite.utils.currency(overalls.total_basic,lite.system_settings.currency_decimals,currency?.symbol), false)
            controller.set_form_value(controller.get_form_field("total_gross"),overalls.total_gross,lite.utils.currency(overalls.total_gross,lite.system_settings.currency_decimals,currency?.symbol), false)
            controller.set_form_value(controller.get_form_field("total_net"),overalls.total_net,lite.utils.currency(overalls.total_net,lite.system_settings.currency_decimals,currency?.symbol), false)
            controller.set_form_value(controller.get_form_field("total_earnings"),overalls.total_earnings,lite.utils.currency(overalls.total_earnings,lite.system_settings.currency_decimals,currency?.symbol), false)
            controller.set_form_value(controller.get_form_field("total_deductions"),overalls.total_deductions,lite.utils.currency(overalls.total_deductions,lite.system_settings.currency_decimals,currency?.symbol), false)
    }

    // function to calculate earnings
    async calculate_earning(employee, basic_pay, earning_name){
        const employee_earnings = lite.utils.array_to_object(employee.earnings, "earning")
        let earning_value = 0
        if(employee_earnings[earning_name]){
            const earning = lite.payroll_content.earnings[earning_name]
            let 
                percentage = lite.utils.string_to_float(earning?.percentage) || 0.00, 
                fixed_amount = lite.utils.string_to_float(earning?.fixed_amount) || 0.00
            if(earning?.is_overtime)
                earning_value = this.calculate_overtime(employee,basic_pay)
            if(earning?.is_commission)
                earning_value = this.calculate_commission(employee,basic_pay)
            else if (earning?.exclude_on_statutory_deductions) {
                const excluded_earning = {
                    emp: employee.name,
                    earning: earning.name,
                    value: this.calculate_excluded_amount (earning, basic_pay)
                }
                this.addToExcludedEarning (EXCLUDED_EARNING, excluded_earning)
                EARNINGS.push (earning.name)
                earning_value = excluded_earning.value
            }else{
                if(percentage)
                    earning_value = (basic_pay * percentage) / 100
                else if(fixed_amount)
                    earning_value = fixed_amount
            }

        }
        return earning_value
       
    }

    // function to calculate earnings
    async calculate_deduction(employee, employee_row, deduction_name){
      if (employee != null) {

        const employee_deductions = lite.utils.array_to_object(employee.deductions, "deduction")
    
        let deduction_value = 0
        if(employee_deductions[deduction_name] ){
            const deduction = lite.payroll_content.deductions[deduction_name]
            if (deduction){
            // if deduction component is advance checked
            if(deduction?.is_advance)
                deduction_value = this.calculate_advance(employee, employee_row)

            else{
                if(deduction?.has_ceiling === 1){
                    deduction_value = await this.calculate_ceiling_deduction(employee, employee_row, deduction)
                }
                else{
                    if (!deduction?.percentage || deduction?.percentage == 0){
                        if(deduction?.fixed_amount === 0){
                            deduction_value = lite.utils.string_to_float(employee_deductions[deduction.name]) || 0.00
                           
                        }
                        else{
                            deduction_value =  lite.utils.string_to_float(deduction?.fixed_amount) || 0.00
                          
                        }
                    }
                    else{
                        if(deduction?.apply_on === "Basic"){
                          
                            deduction_value = (employee_row.basic_pay * deduction.percentage) / 100
                        }
                        else if(deduction?.apply_on === "Gross"){
                            deduction_value = (employee_row.gross * deduction.percentage) / 100
                        }
                    }
                }
            }

        }
       
        }
        return deduction_value
        }
    }

    // calculate deduction with ceiling amount
    async calculate_ceiling_deduction(employee, employee_row, deduction){
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


    // calculate income tax band
    async calculate_income_tax_band(employee, employee_row){
        const band = lite.payroll_content?.income_tax_band
        if(employee.tax_band && band){
            const tax_free_amount = band.tax_free_amount
            const salary_bands = band.salary_bands
            if(lite.utils.array_has_data(salary_bands)){
                const sorted_bands = salary_bands.slice().sort((a, b) => a.id - b.id);
                let deductable_amount = employee_row[lite.utils.lower_case(band.deduct_on)]
                if (deductable_amount > tax_free_amount){
                    let deduction = 0, cash_on_hand = deductable_amount - tax_free_amount, taxable_amount = 0, end_calculations=false, total_bands = sorted_bands.length - 1
                    $.each(sorted_bands,(_, b)=>{
                        if(end_calculations)
                            return
                        const perc = lite.utils.string_to_float(b.deduction_percentage) / 100
                        const amount_from = lite.utils.is_number_variable(b.amount_from) ? lite.utils.string_to_float(b.amount_from) : 0
                        const amount_to = lite.utils.is_number_variable(b.amount_to) ? lite.utils.string_to_float(b.amount_to) : 0
                        const difference = lite.utils.fixed_decimals((Math.abs(amount_to - amount_from)),0)
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
                        tax_amount = lite.utils.fixed_decimals(taxable_amount * perc, 0)
                        deduction += tax_amount
                    })
                    return deduction
                }
            }
        }
        return 0
    }
    
    async calculate_pro_rata(employee, controller, emp_basic_pay) {
        let proRataSalary = 0;
    
        const payrollToDateStr = controller.get_form_value(controller.get_form_field("to_date"));
        const payrollToDate = new Date(payrollToDateStr);
        const joiningDate = new Date(employee.date_of_joining);
        const promotion_date = new Date(employee.promotion.promotion_date);
        const old_basic_pay = lite.utils.string_to_float(employee.promotion.current_basic) || 0.00;
        const revised_basic = lite.utils.string_to_float(employee.promotion.revised_basic) || 0.00;
        const basic_pay = lite.utils.string_to_float(emp_basic_pay) || 0.00;
        const working_days = lite.utils.string_to_float(employee.working_days) || 22;
        const payrollFromDateStr = controller.get_form_value(controller.get_form_field("from_date"));
        const payrollFromDate = new Date(payrollFromDateStr);
    
        if (basic_pay === 0.00) {
            lite.alerts.toast({
                toast_type: 204,
                title: "Unprocessable Payroll",
                message: `${employee.name}'s basic pay is zero`
            });
            return;
        }
    
        const countWorkingDays = (startDate, endDate, workingDaysPerMonth) => {
            let count = 0;
            let currentDate = new Date(startDate);
    
            const workingDaysPerWeek = () => {
                if (workingDaysPerMonth <= 5) return 1;
                if (workingDaysPerMonth <= 9) return 2;
                if (workingDaysPerMonth <= 14) return 3;
                if (workingDaysPerMonth <= 18) return 4;
                if (workingDaysPerMonth <= 22) return 5;
                if (workingDaysPerMonth <= 27) return 6;
                return 5;
            };
    
            const daysPerWeek = workingDaysPerWeek();
    
            const isWorkingDay = (dayOfWeek, daysPerWeek) => {
                switch (daysPerWeek) {
                    case 1:
                        return dayOfWeek === 1;
                    case 2:
                        return dayOfWeek === 1 || dayOfWeek === 3;
                    case 3:
                        return dayOfWeek === 1 || dayOfWeek === 3 || dayOfWeek === 5;
                    case 4:
                        return dayOfWeek >= 1 && dayOfWeek <= 4;
                    case 5:
                        return dayOfWeek >= 1 && dayOfWeek <= 5;
                    case 6:
                        return dayOfWeek >= 1 && dayOfWeek <= 6;
                    default:
                        return false;
                }
            };
    
            while (currentDate <= endDate) {
                const dayOfWeek = currentDate.getDay();
                if (isWorkingDay(dayOfWeek, daysPerWeek)) {
                    count++;
                }
                currentDate.setDate(currentDate.getDate() + 1);
            }
            return count;
        };
    
        // Handle separated employees
        if (employee?.is_separated === 1) {
            const lastDayOfWorkStr = employee.separation.last_day_of_work;
            const lastDayOfWork = new Date(lastDayOfWorkStr);
    
            if (
                (payrollFromDate.getFullYear() === lastDayOfWork.getFullYear() &&
                    payrollFromDate.getMonth() === lastDayOfWork.getMonth()) ||
                payrollToDate.getMonth() === lastDayOfWork.getMonth()
            ) {
                let daysWorked = 0;
                if (joiningDate <= lastDayOfWork) {
                    daysWorked = countWorkingDays(payrollFromDate, lastDayOfWork, working_days);
                    if (daysWorked > 0) {
                        const daily_pay = basic_pay / working_days;
                        proRataSalary = daily_pay * daysWorked;
                    } else {
                        proRataSalary = basic_pay;
                    }
                }
                return lite.utils.fixed_decimals(proRataSalary, 2);
            }
        }
    
        // Handle employees who joined during the payroll period
        if (joiningDate >= payrollFromDate && joiningDate <= payrollToDate) {
            const daysWorked = countWorkingDays(joiningDate, payrollToDate, working_days);
    
            if (daysWorked > 0) {
                const daily_pay = basic_pay / working_days;
                proRataSalary = daily_pay * daysWorked;
            } else {
                proRataSalary = basic_pay;
            }
        }
        // Handle promotions during the payroll period
        else if (promotion_date >= payrollFromDate && promotion_date <= payrollToDate) {
            const daysWorked_after_prom = countWorkingDays(promotion_date, payrollToDate, working_days);
            const daysWorked_before_promotion = countWorkingDays(payrollFromDate, promotion_date, working_days);
    
            if (daysWorked_after_prom > 0 && daysWorked_before_promotion > 0) {
                const daily_pay = basic_pay / working_days;
                const postpromotion_basic_pay = revised_basic / working_days * daysWorked_after_prom;
                const prepromotion_basic_pay = old_basic_pay / working_days * daysWorked_before_promotion;
                proRataSalary = postpromotion_basic_pay + prepromotion_basic_pay;
            } else {
                proRataSalary = basic_pay;
            }
    
        } else {
            proRataSalary = basic_pay;
        }
    
        return lite.utils.fixed_decimals(proRataSalary, 2);
    }
    

    // async calculate overtime earning
    async calculate_overtime(employee, basic_pay){
        return employee?.overtime?.overtime  || 0.00
    }

    // async calculate commission earning
    async calculate_commission(employee, basic_pay){
        return 0
    }

    
    // async calculate advace deduction earning
    async calculate_advance(employee, basic_pay){
        return employee?.advance?.repayment_amount  || 0.00
        
    }
    calculate_excluded_amount (earning, basic_pay) {
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

    addToExcludedEarning (array, newObject)  {
        const exists = array.some (item =>
            item.emp === newObject.emp &&
            item.earning === newObject.earning &&
            item.value === newObject.value
        )
        if (!exists) {
            array.push (newObject)
        }
    }
}
