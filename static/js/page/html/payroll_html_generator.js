
export default class Payroll_HTML_Generator{
    constructor(){

    }

    create_payroll_totals_titles(freq) {
        const total_cols = freq?.length;
        let cols = "";
        let row = "";
    
        // Build the header row with column names
        $.each(freq, (idx, col) => {
            let column_name = col.replace("_", " "); // Replace underscores with spaces for better readability
    
            cols += `
                <div class="w-full h-full font-semibold flex items-center justify-center h-[30px] text-12 ${idx < total_cols - 1 ? 'border-r' : ''}">
                    ${column_name}
                </div>`;
        });
    
        // Build the input fields row
        $.each(freq, (_, fr) => {
            const periodId = fr.replace(/\s+/g, '_'); // Replace spaces with underscores for the period ID
            
            const field = `
                <input 
                    autocomplete="off"
                    id="${periodId}" 
                    always-fetch="true"
                    is_required="false" 
                    type="text"
                    value="0.00"
                    class="text-13 h-full justify-center text-center w-full border border-t-0 border-l-0 border-dashed"
                    placeholder=""
                    readonly>
            `;
            row += `<div class="w-full h-full flex items-center justify-center">${field}</div>`;
        });
    
        // Return the full structure including the header and the row
        return `
            <div class="translate-y-8">
                <div class="w-full intro-x font-semibold col-span-4 border-t my-2 pt-1 text-12 transition duration-500 hover:scale-[1.2]">
                    Overall Totals
                </div>
                <div class="w-full h-[30px] bg-default text-theme_text_color rounded-t-md grid grid-cols-${total_cols} budget-titles-row">
                    ${cols}
                </div>
                <div class="w-full h-[40px] rounded-t-md grid grid-cols-${total_cols} border-b border-dashed budget-row">
                    ${row}
                </div>
            </div>
        `;
    }
    
    



    payroll_processor_totals(){
     return `
   
     `
    }

    create_payroll_total_row(sorted_items) {
        const numColumns = Object.keys(sorted_items).length;
    
        let totalRow = `<div class="w-full h-[40px] rounded-md grid grid-cols-${numColumns + 1} border-t border-b border-dashed total-row">`;
    
        let grandTotal = 0;
    
        for (const key in sorted_items) {
            if (sorted_items.hasOwnProperty(key)) {
                const value = parseFloat(sorted_items[key] || 0);
                grandTotal += value;
    
                const periodId = key.replace(/\s+/g, '_');
    
                totalRow += `
                    <div class="w-full h-full font-semibold flex flex-col items-center justify-center h-[40px] border-r text-12 total-cell" id="${periodId}">
                        <span class="font-medium">${key} Total</span>
                        <span>${lite.utils.thousand_separator(value, 2)}</span>
                    </div>`;
            }
        }
    
        totalRow += `
            <div class="w-full h-full font-semibold flex flex-col items-center justify-center h-[40px] text-12 main-total-cell">
                <span class="font-medium">Grand Total</span>
                <span>${lite.utils.thousand_separator(grandTotal, 2)}</span>
            </div>`;
    
        totalRow += `</div>`;
    
        return totalRow;
    }
    
    

    create_recent_payment_row(data){
        return `
            <div class="w-full grid grid-cols-7 border-b h-[40px] text-12 pl-2 intro-x">
                <a href="/app/payroll/payroll_processor/?app=payroll_processor&page=info&content_type=Payroll%20Processor&doc=${data.id}" class="w-full flex items-center justify-start h-full col-span-2">
                    <span class="material-symbols-outlined mr-1 text-orange-600">
                        event_available
                    </span>
                    ${lite.utils.convert_date(data.from_date)} - ${lite.utils.convert_date(data.to_date)}
                </a>
                <div class="w-full flex items-center justify-start h-full">
                    <span class="material-symbols-outlined mr-1">
                        badge
                    </span>
                    ${lite.utils.thousand_separator(data.total_employees,0)}
                </div>
                <div class="w-full flex items-center justify-start h-full">
                    <span class="material-symbols-outlined mr-1">
                        redeem
                    </span>
                    ${lite.utils.thousand_separator(data.total_gross,lite.system_settings?.currency_decimals,data.currency)}
                </div>
                <div class="w-full flex items-center justify-start h-full">
                    <span class="material-symbols-outlined text-green-700 mr-1">
                        trending_up
                    </span>
                    ${lite.utils.thousand_separator(data.total_earnings,lite.system_settings?.currency_decimals,data.currency)}
                </div>
                <div class="w-full flex items-center justify-start h-full">
                    <span class="material-symbols-outlined text-red-700 mr-1">
                        trending_down
                    </span>
                    ${lite.utils.thousand_separator(data.total_deductions,lite.system_settings?.currency_decimals,data.currency)}
                </div>
                <div class="w-full flex items-center justify-start h-full">
                    <span class="material-symbols-outlined mr-1 text-indigo-600">
                        credit_score
                    </span>
                    ${lite.utils.thousand_separator(data.total_net,lite.system_settings?.currency_decimals,data.currency)}
                </div>
            </div>
        `
    }

    create_cost_by_designation_row(data,color){
        return `
            <div class="w-full flex items-center justify-between h-[62px] intro-x">
                <div class="flex items-center justify-start w-[60%]">
                    <div class="flex text-10 items-center justify-start overflow-ellipsis truncate font-bold text-[${color.inner}] flex items-center justify-center bg-[${color.base}] rounded-full w-[40px] h-[30px] mr-2">
                        ${lite.utils.abbreviate(data.name)}
                    </div>
                    <div class="flex flex-col w-full">
                        <span class="text-11 overflow-ellipsis truncate w-[90%]">${data.name}</span>
                        <div class="w-full h-[10px] rounded-full bg-gray-200 relative overflow-hidden">
                            <div class="absolute left-0 h-full w-[${data.perc}%] rounded-full bg-[${color.inner}]"></div>
                        </div>
                    </div>
                </div>
                <span class="font-bold text-13 flex items-center justify-end overflow-ellipsis truncate">
                    <small class="mr-1 text-9">${data.currency}</small>
                    ${lite.utils.thousand_separator(data.value,2)}
                </span>
            </div>
        `
    }

    create_regulatory_summary_row(data){
        return `
            <div class="w-full flex items-center justify-between h-[65px] border rounded-md mb-2 px-2 intro-x">
                <div class="flex items-center justify-start">
                    <div class="flex text-10 items-center justify-start font-bold text-indigo-900 flex items-center justify-center bg-gray-100 rounded-full w-[40px] h-[40px] mr-2">
                        ${lite.utils.abbreviate(data.name)}
                    </div>
                    <div class="flex flex-col">
                        <span class="text-12 overflow-ellipsis truncate w-full">${data.name}</span>
                        <small class="text-gray-500 text-10"> ${lite.utils.currency(data.value,lite.defaults.currency_decimals,data.currency)}</small>
                    </div>
                </div>
            </div>
        `
    }


    // payroll processor history
    create_payroll_processor_history_side_row(data){
        return `
            <div class="w-full flex items-center justify-between h-[50px] border-b intro-x">
                <div class="flex items-center justify-start">
                    <span class="material-symbols-outlined text-default text-15"> history </span>
                    <div class="ml-2">
                        <h6 class="text-12 font-semibold M-0">PAYRL-2023-01-01</h6>
                        <small class="text-gray-600 text-10">GROSS of ${lite.utils.currency(data.total_gross,lite.system_settings.currency_decimals,data?.currency)}</small>
                    </div>
                </div>
                <div class="ml-2 flex items-end justify-center flex-col ">
                    <h6 class="text-12 font-semibold M-0">${data.total_employees}</h6>
                    <small class="text-gray-700 text-10 flex items-center justify-end">
                        <span class="material-symbols-outlined text-14">how_to_reg</span>
                        Total Employees
                    </small>
                </div>
            </div>
        `
    }

    overtime(data){
        let overtime = ''
        $.each(data,(index, value)=>{
            if (index <= 5) {
                overtime += `
                   <div class="w-full h-[45px] flex items-center justify-between border-b">
                   <div class="flex items-center justify-start">
                       <div class="flex items-ceenter justify-center mr-3">
                           <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                       </div>
                       <div class="text-gray-700">${value.applicant_name}</div>
                   </div>
                   <div class="flex flex-col items-end justify-center">
                       <span class="font-semibold text-12">
                           <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                           ${value.overtime_date}
                       </span>
                       <small class="text-orange-500 text-10">Applied</small>
                   </div>
              </div>   `
            }
        })
        return overtime
    }


overtime_stats(data){
    let overtime_stats= ''
    $.each(data,(index, value)=>{
        if (index <= 5) {
            overtime_stats += `
            <div class="w-full h-[45px] flex items-center justify-between">
            <div class="flex items-center justify-start">
                <div class="flex items-ceenter justify-center mr-3">
                   
                </div>
                <div class="text-gray-700">Approved Overtimes</div>
            </div>
            <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
                ${value.approved}
            </div>
       </div>
        <div class="w-full h-[45px] flex items-center justify-between">
            <div class="flex items-center justify-start">
                <div class="flex items-ceenter justify-center mr-3">
                    
                </div>
                <div class="text-gray-700">Rejected Overtimes</div>
            </div>
            <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
            ${value.rejected}
            </div>
       </div>
        <div class="w-full h-[45px] flex items-center justify-between">
            <div class="flex items-center justify-start">
                <div class="flex items-ceenter justify-center mr-3">
                    
                </div>
                <div class="text-gray-700">Pending Approval</div>
            </div>
            <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
            ${value.pending}
            </div>
       </div>
            `
        }
    })
    return overtime_stats
}

advance(data){
    let advance = ''
    $.each(data,(index, value)=>{
        if (index <= 5) {
            advance += `
               <div class="w-full h-[45px] flex items-center justify-between border-b">
               <div class="flex items-center justify-start">
                   <div class="flex items-ceenter justify-center mr-3">
                       <span class="material-symbols-outlined text-default text-17"> check_circle </span>
                   </div>
                   <div class="text-gray-700">${value.applicant_name}</div>
               </div>
               <div class="flex flex-col items-end justify-center">
                   <span class="font-semibold text-12">
                       <span class="material-symbols-outlined text-13 mr-1"> calendar_month </span>
                       ${value.advance_date}
                   </span>
                   <small class="text-orange-500 text-10">Applied</small>
               </div>
          </div>   `
        }
    })
    return advance
}


advance_stats(data){
    let advance_stats= ''
    $.each(data,(index, value)=>{
        if (index <= 5) {
            advance_stats += `
            <div class="w-full h-[45px] flex items-center justify-between">
            <div class="flex items-center justify-start">
                <div class="flex items-ceenter justify-center mr-3">
                   
                </div>
                <div class="text-gray-700">Approved Overtimes</div>
            </div>
            <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
                ${value.approved}
            </div>
       </div>
        <div class="w-full h-[45px] flex items-center justify-between">
            <div class="flex items-center justify-start">
                <div class="flex items-ceenter justify-center mr-3">
                    
                </div>
                <div class="text-gray-700">Rejected Overtimes</div>
            </div>
            <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
            ${value.rejected}
            </div>
       </div>
        <div class="w-full h-[45px] flex items-center justify-between">
            <div class="flex items-center justify-start">
                <div class="flex items-ceenter justify-center mr-3">
                    
                </div>
                <div class="text-gray-700">Pending Approval</div>
            </div>
            <div class="flex flex-col items-center justify-center w-[20px] h-[20px] rounded-full bg-gray-100 text-12">
            ${value.pending}
            </div>
       </div>
            `
        }
    })
    return advance_stats
}

payslip(data) {
    let slip = '';
    $.each(data, (index, value) => {
        if (index <= 5) {
            slip += `
            <div class="w-full flex items-center justify-between h-[40px]">
            <div class="flex items-center justify-start">
                <span class="material-symbols-outlined text-default text-17 mr-2"> credit_score </span>
                <span class="text-12">${value.employee_name}</span>
            </div>
            <a href=""><span class="material-symbols-outlined text-20">expand_circle_right</span>
            </a>
        </div>
            `;
        }
    });
    return slip;
}

payslip_stats(data) {
    let slip_stats = '';
    $.each(data, (index, value) => {
        if (index <= 5) {
            slip_stats += `
            <div class="my-5 bg-gray-300 w-full h-[3px] rounded-full"></div>
            <div class="w-full my-8 flex items-center justify-between">
                <div class="flex items-start justify-start">
                    <span class="material-symbols-outlined text-orange-500 text-17">
                        drafts
                    </span>
                    <div class="grid ml-2">
                        <span class="font-semibold">In Draft</span>
                        <small class="text-slate-500">
                            Total payslips in draft
                        </small>
                    </div>
                </div>
                <div class="rounded-full bg-gray-200 w-[30px] h-[30px] flex items-center justify-center text-[12px]">
                    ${value.draft}
                </div>
            </div>
            <div class="w-full my-8 flex items-center justify-between">
                <div class="flex items-start justify-start">
                    <span class="material-symbols-outlined text-indigo-500 text-15">
                        check_circle
                    </span>
                    <div class="grid ml-2">
                        <span class="font-semibold">Submitted</span>
                        <small class="text-slate-500">
                            Total payslips submitted
                        </small>
                    </div>
                </div>
                <div class="rounded-full bg-gray-200 w-[30px] h-[30px] flex items-center justify-center text-[12px]">
                    ${value.submitted}
                </div>
            </div>
            <div class="w-full my-8 flex items-center justify-between">
                <div class="flex items-start justify-start">
                    <span class="material-symbols-outlined text-orange-700 text-15">check_circle</span>
                    <div class="grid ml-2">
                        <span class="font-semibold">Total</span>
                        <small class="text-slate-500">
                            Total payslips
                        </small>
                    </div>
                </div>
                <div class="rounded-full bg-gray-200 w-[30px] h-[30px] flex items-center justify-center text-[12px]">
                    ${value.total}
                </div>
            </div>
            `;
        }
    });
    return slip_stats;
}


employee_grade(data){
    let employee_grade = ''

    $.each(data,(index,value)=>{
        if (index <=6){
            employee_grade += ` 
                <div class="flex items-center justify-between p-2">
                    <div class="flex items-center">
                        <div class="flex items-center justify-center relative w-[30px] h-[20px] mr-1">
                            <div class="absolute w-[15px] h-[15px] border-2 border-orange-600 rounded-md rotate-[50deg] mt-1"></div>
                            <div class="absolute w-[15px] h-[15px] border-2 border-indigo-600 rounded-md rotate-[40deg]"></div>
                        </div>
                        <span>${value.grade_name}</span>
                    </div>
                    <div class="rounded-full bg-gray-100 font-bold flex items-center justify-center w-[25px] h-[25px]">
                        ${value.total_grade_emp}
                    </div>
                </div>
      `
        }
    })
    return employee_grade
}

employee_grade_stats(data){
    let employee_grade_stats = ''

    $.each(data,(index,value)=>{
        if (index <=6){
            employee_grade_stats += ` 
             <div class="flex items-center justify-start p-2">
            <div class="flex ietms-center justify-center relative w-[30px] h-[20px] mr-1">
                <div class="absolute w-[15px] h-[15px] border-2 border-orange-600 rounded-md rotate-[50deg] mt-1"></div>
                <div class="absolute w-[15px] h-[15px] border-2 border-indigo-600 rounded-md rotate-[40deg]"></div>
            </div>
            <span>${value.grade_name}</span>
            <div class="rounded-full bg-gray-100 font-bold flex items-center justify-center w-[25px] h-[25px]">
            ${value.total_deductions}
            </div>
        </div>
      `
        }
    })
    return employee_grade_stats
}


component_grade(data){
    let component_grade = ''

    $.each(data,(index,value)=>{
        if (index <=6){
            component_grade += ` 
           <div class="flex items-center justify-between p-2">
            <div class="flex items-center">
        <div class="flex items-center justify-center relative w-[30px] h-[20px] mr-1">
            <div class="absolute w-[15px] h-[15px] border-2 border-orange-600 rounded-md rotate-[50deg] mt-1"></div>
            <div class="absolute w-[15px] h-[15px] border-2 border-indigo-600 rounded-md rotate-[40deg]"></div>
        </div>
        <span>${value.component_name}</span>
    </div>
    <div class="rounded-full bg-gray-100 font-bold flex items-center justify-center w-[25px] h-[25px]">
        ${value.total_grades}
    </div>
</div>

      `
        }
    })
    return component_grade
}

component_grade_stats(data){
    let component_grade_stats = ''

    $.each(data,(index,value)=>{
        if (index <=6){
            component_grade_stats += ` 
             <div class="flex items-center justify-start p-2">
            <div class="flex ietms-center justify-center relative w-[30px] h-[20px] mr-1">
                <div class="absolute w-[15px] h-[15px] border-2 border-orange-600 rounded-md rotate-[50deg] mt-1"></div>
                <div class="absolute w-[15px] h-[15px] border-2 border-indigo-600 rounded-md rotate-[40deg]"></div>
            </div>
            <span>${value.component_name}</span>
            <div class="rounded-full bg-gray-100 font-bold flex items-center justify-center w-[25px] h-[25px]">
            ${value.total_grades}
            </div>
        </div>
      `
        }
    })
    return component_grade_stats
}

recent_advance_applications(data){
    let component_grade_stats = ''

    $.each(data,(index,value)=>{
        if (index <=6){
            component_grade_stats += ` 
                <div class="h-[60px] flex items-center justify-between border-b border-slate-300/45 pb-3 pt-3 last:pb-0">
                    <div class="flex items-center gap-x-3">
                        <img
                            src=${value.image}
                            alt=${value.name}
                            class="relative inline-block h-8 w-8 rounded-full object-cover object-center"
                        />
                        <div>
                            <h6 class="text-slate-800 font-semibold text-[13px]">
                                ${value.name}
                            </h6>
                            <p class="text-slate-600 text-[11px]">
                                ${value.diesignaion}
                            </p>
                        </div>
                    </div>
                    <h6 class="text-[14px] text-indigo-600 font-medium">
                        ${lite?.user?.company?.reporting_currency} ${value.amount}
                    </h6>
                </div>
            `
        }
    })
    return component_grade_stats
}

defaulted_advances(data){
    let component_grade_stats = ''

    $.each(data,(index,value)=>{
        if (index <=6){
            component_grade_stats += ` 
                <div class="h-[50px] flex items-center justify-between border-b border-slate-300/55 pb-3 pt-3 last:pb-0">
                    <div class="flex items-center gap-x-3">
                        <span class="relative inline-block h-8 w-8 rounded-full object-cover object-center">
                            <span class="material-symbols-outlined text-[20px] text-rose-500">
                                contactless_off
                            </span>
                        </span>
                        <div>
                            <h6 class="text-slate-800 text-[11px] font-semibold">
                                ${value.name}
                            </h6>
                            <p class="text-slate-600 text-[10px]">
                                ${value.diesignaion}
                            </p>
                        </div>
                    </div>
                    <h6 class="text-[14px] text-indigo-600 font-medium">
                        ${lite?.user?.company?.reporting_currency} ${value.amount}
                    </h6>
                </div>
            `
        }
    })
    return component_grade_stats
}

}