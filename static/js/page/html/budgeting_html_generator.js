// import { validateSchema } from "webpack"
import HTML_Builder from "./html_builder.js"

export default class Budgeting_HTML_Generator{
    constructor(){
        this.builder = new HTML_Builder()
    }

    create_budget_wrapper(){
        return `
            <div class="income-wrapper border border-dashed rounded-md min-h-[40px] !important"></div>
            <div class="expense-wrapper border border-dashed rounded-md min-h-[40px] !important" style="margin-top: 25px;"></div>
        `
    }


    create_info_budget_wrapper(){
        return `
            <div class="info-income-wrapper border border-dashed rounded-md min-h-[40px] !important"></div>
            <div class="info-expense-wrapper border border-dashed rounded-md min-h-[40px] !important" style="margin-top: 25px;"></div>
        `
    }

    create_project_budget_wrapper(){
        return `
            <div class="project-budget-wrapper border border-dashed rounded-md whitespace-nowrap flex-nowrap min-h-[40px] !important"></div>
        `
    }

    create_budget_wrapper_digits(){
        return `
            <div class="income-wrapper-digits border border-dashed rounded-md min-h-[40px] !important style="margin-top: 25px;"></div>
            <div class="expense-wrapper-digits border border-dashed rounded-md min-h-[40px] !important" style="margin-top: 25px;"></div>
        `
    }

     
    create_budget_titles({ freq, title }) {
        const total_cols = freq?.length + 5 || 5; // added 1 for the checkbox and Total column
        let cols = "";
        $.each(freq, (idx, col) => cols += `<div class="w-full h-full font-semibold flex items-center justify-center h-[30px] text-12 ${idx < freq?.length - 1 ? "border-r" : ""} ">${col}</div>`);
        cols += `<div class="w-full h-full font-semibold flex items-center justify-center h-[30px] text-12 border-l ">Totals</div>`; // added Total title
        return `
            <div class="w-full h-[30px] bg-default text-theme_text_color rounded-t-md grid grid-cols-${total_cols} budget-titles-row">
                <div class=" head-check w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center col-span-1 max-w-[70px]">
                    <input autocomplete="off" id="" for="head-row" class="form-check-input  head-check" type="checkbox">
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center h-[30px] col-span-2 border-r text-12">${title}</div>
                <div class="w-full h-full font-semibold flex items-center justify-center h-[30px] col-span-1 border-r text-12">Unit Cost</div>
                ${cols}
            </div>
        `;
    }

    create_project_budget_titles() {
        return `
            <div class="w-full min-h-[30px] max-h-[60px] flex flex-row text-white rounded-t-md grid grid-cols-18 budget-titles-row">
                <div class="w-full h-[60px] bg-default flex flex-row text-white rounded-tl-md col-span-5 grid grid-cols-5">                    
                    <div class="w-full flex font-semibold col-span-3 border-r text-12">
                        <p class = "m-auto self-center text-center">Task/Activity</p>
                    </div>
                    <div class="w-full flex font-semibold col-span-1 border-r text-12">
                        <p class = "m-auto self-center text-center text-wrap">Start Date</p>
                    </div>
                    <div class="w-full flex font-semibold col-span-1 border-r text-12">
                        <p class = "m-auto self-center text-center text-wrap">End Date</p>
                    </div>                             
                </div>
                <div class="w-full h-[60px] bg-default flex flex-row border-r grid grid-cols-1 grid-rows-2 col-span-3"> 
                    <div class="w-full max-h-[30px] col-span-1 border-b row-span-1">
                        <div class="w-full h-full font-bold flex items-center justify-center col-span-1 text-14">Labor</div>                    
                    </div>   
                    <div class="w-full max-h-[30px] col-span-1 grid grid-cols-3 row-span-1 text-12">
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 border-r text-12">Day(s)</div>  
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 border-r text-12">ZMW/Day</div> 
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 text-12">Labor Total</div> 
                    </div>                                         
                </div>
                <div class="w-full h-[60px] bg-default flex flex-row border-r grid grid-cols-1 grid-rows-2 col-span-3"> 
                    <div class="w-full max-h-[30px] col-span-1 border-b row-span-1">
                        <div class="w-full h-full font-bold flex items-center justify-center col-span-1 text-14">Materials</div>                    
                    </div>   
                    <div class="w-full max-h-[30px] col-span-1 grid grid-cols-3 row-span-1 text-12">
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 border-r text-12">Items</div>  
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 border-r text-12">ZMW/Unit</div> 
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 text-12">Materials Total</div> 
                    </div>                                         
                </div>
                <div class="w-full h-[60px] bg-default flex flex-row border-r grid grid-cols-1 grid-rows-2 col-span-3"> 
                    <div class="w-full max-h-[30px] col-span-1 border-b row-span-1">
                        <div class="w-full h-full font-bold flex items-center justify-center col-span-1 text-14">Fixed</div>                    
                    </div>   
                    <div class="w-full max-h-[30px] col-span-1 grid grid-cols-3 row-span-1 text-12">
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 border-r text-12">Travel</div>  
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 border-r mb-0 text-12 text-wrap text-center leading-none">Equipment /Space</div> 
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 text-12">Misc.</div> 
                    </div>                                         
                </div>
                <div class="w-full h-[60px] bg-default flex flex-row border-r grid grid-cols-1 grid-rows-2 col-span-3"> 
                    <div class="w-full max-h-[30px] col-span-1 border-b row-span-1">
                        <div class="w-full h-full font-bold flex items-center justify-center col-span-1 text-14">Balance</div>                    
                    </div>   
                    <div class="w-full max-h-[30px] col-span-1 grid grid-cols-3 row-span-1 text-12">
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 border-r text-12">Budget</div>  
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 border-r text-12">Actual</div> 
                        <div class="w-full font-semibold flex items-center justify-center max-h-[30px] col-span-1 text-12">Variance</div> 
                    </div>                                         
                </div>
                <div class="w-full h-[60px] bg-default flex flex-row text-white rounded-tr-md col-span-1 grid grid-cols-1 click-attempt">
                    <div class="w-full flex font-semibold col-span-1 text-12">
                        <p class = "m-auto self-center text-center">Status</p>
                    </div>                          
                </div>
                
                
            </div>
        `;
    }

    create_project_budget_row(){
        const task_field = this.builder.build_form_field({
            id: "task-activity",
            fieldtype: "text",
            fieldlabel: "task_activity",
            omitlabels: true,
            istablefield: true,
            placeholder: "Select Task",
            classnames: "h-[98%] justify-center text-center budget-cell task-activity",
        });

        const description_field = this.builder.build_form_field({
            id: "description",
            fieldtype: "expandable",
            fieldlabel: "description",
            omitlabels: true,
            istablefield: true,
            placeholder: "Enter description",
            classnames: "justify-center text-center budget-cell",
        });

        const start_date = this.builder.build_form_field({
            id: "start-date",
            fieldtype: "date",
            fieldlabel: "start_date",
            omitlabels: true,
            istablefield: true,
            placeholder: "Start date",
            classnames: " justify-center text-center budget-cell",
        });

        const end_date = this.builder.build_form_field({
            id: "end-date",
            fieldtype: "date",
            fieldlabel: "end_date",
            omitlabels: true,
            istablefield: true,
            placeholder: "End date",
            classnames: "justify-center text-center budget-cell",
        });

        const days = this.builder.build_form_field({
            id: 'days',
            fieldtype: "int",
            fieldlabel: 'days',
            omitlabels: true,
            istablefield: true,
            placeholder: "Duration",
            classnames: "justify-center text-center budget-cell " 
        });

        const labor_unit_cost = this.builder.build_form_field({
            id: 'labor-unit-cost',
            fieldtype: "float",
            fieldlabel: 'labor_unit_cost',
            omitlabels: true,
            istablefield: true,
            placeholder: "Unit Cost",
            classnames: "justify-center text-center budget-cell " 
        });

        const labor_total = this.builder.build_form_field({
            id: 'labor-total',
            fieldtype: "float",
            fieldlabel: 'labor_total',
            omitlabels: true,
            istablefield: true,
            placeholder: "Total",
            classnames: "justify-center text-center budget-cell " 
        });


        const material_quantity = this.builder.build_form_field({
            id: 'material-quantity',
            fieldtype: "int",
            fieldlabel: 'material_quantity',
            omitlabels: true,
            istablefield: true,
            placeholder: "Qunatity",
            classnames: "justify-center text-center budget-cell" 
        });

        const material_unit_cost = this.builder.build_form_field({
            id: 'material-unit-cost',
            fieldtype: "float",
            fieldlabel: 'material_unit_cost',
            omitlabels: true,
            istablefield: true,
            placeholder: "Unit Cost",
            classnames: "justify-center text-center budget-cell " 
        });

        const material_total = this.builder.build_form_field({
            id: 'material-total',
            fieldtype: "float",
            fieldlabel: 'material_total',
            omitlabels: true,
            istablefield: true,
            placeholder: "Total",
            classnames: "justify-center text-center budget-cell " 
        });

        const fixed_travel = this.builder.build_form_field({
            id: 'fixed-travel',
            fieldtype: "float",
            fieldlabel: 'fixed_travel',
            omitlabels: true,
            istablefield: true,
            placeholder: "Travel Costs",
            classnames: "justify-center text-center budget-cell " 
        });

        const fixed_equip = this.builder.build_form_field({
            id: 'fixed-equip',
            fieldtype: "float",
            fieldlabel: 'fixed_equip',
            omitlabels: true,
            istablefield: true,
            placeholder: "Equipment Costs",
            classnames: "justify-center text-center  budget-cell" 
        });

        const fixed_misc = this.builder.build_form_field({
            id: 'fixed-misc',
            fieldtype: "float",
            fieldlabel: 'fixed_misc',
            omitlabels: true,
            istablefield: true,
            placeholder: "Misc. Costs",
            classnames: "justify-center text-center budget-cell " 
        });

        const balance_budget = this.builder.build_form_field({
            id: 'balance-budget',
            fieldtype: "float",
            fieldlabel: 'balance_budget',
            omitlabels: true,
            istablefield: true,
            placeholder: "Budget",
            classnames: "justify-center text-center budget-cell " 
        });

        const balance_actual = this.builder.build_form_field({
            id: 'balance-actual',
            fieldtype: "float",
            fieldlabel: 'balance_actual',
            omitlabels: true,
            istablefield: true,
            placeholder: "Actual",
            classnames: "justify-center text-center budget-cell " 
        });

        const variance = this.builder.build_form_field({
            id: 'variance',
            fieldtype: "float",
            fieldlabel: 'variance',
            omitlabels: true,
            istablefield: true,
            placeholder: "Variance",
            classnames: "justify-center text-center budget-cell " 
        });

        const task_status = this.builder.build_form_field({
            id: "task-status",
            fieldtype: "select",
            fieldlabel: "tast_status",
            options: [
                'Not Started',
                'In Progress',
                'Complete',
                'On Hold',
                'Overdue',

            ],
            omitlabels: true,
            istablefield: true,
            placeholder: "Select item",
            classnames: "justify-center text-center budget-cell",
        });


        let row = `
                <div class="w-full h-[40px] rounded-t-md flex grid grid-cols-18 border-b border-dashed budget-row ">                    
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-2 border-dashed border-r border-b text-12">
                        ${task_field}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${description_field}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${start_date}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${end_date}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${days}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${labor_unit_cost}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${labor_total}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${material_quantity}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${material_unit_cost}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${material_total}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${fixed_travel}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${fixed_equip}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${fixed_misc}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${balance_budget}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${balance_actual}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${variance}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12 ">
                        ${task_status}
                    </div>
                    
                </div>
            `;
        return row;
    }

    create_budget_titles_figures({ freq, title }) {

        const total_cols = freq?.length + 3 || 3; 
        let cols = "";
        $.each(freq, (idx, col) => cols += `<div class="w-full h-full font-semibold flex items-center justify-center h-[30px] text-12 ${idx < freq?.length - 1 ? "border-r" : ""} ">${col}</div>`);
        cols += `<div class="w-full h-full font-semibold flex items-center justify-center h-[30px] text-12 border-l ">Totals</div>`; // added Total title
        return `
            <div class="w-full h-[30px] bg-default text-theme_text_color rounded-t-md grid grid-cols-${total_cols} budget-titles-row">
                <div class="w-full h-full font-semibold flex items-center justify-center h-[30px] col-span-2 border-r text-12">${title}</div>
                ${cols}
            </div>
        `;
    }

    create_period_selector(options){
        const period_selector = this.builder.build_form_field({
            id: "period-selector",
            fieldtype: "select",
            fieldlabel: "period_selector",
            options: options,
            value: '',
            omitlabels: true,
            placeholder: "Select period",
            classnames: "justify-center text-center period-selector-field",
        });

        return period_selector

    }

    create_consolidated_project_budget_titles(){
        return `
            <div class="w-full h-[35px] bg-default text-theme_text_color rounded-t-md grid grid-cols-10 budget-titles-row">
                <div class="w-full h-full font-semibold flex col-span-2 items-center justify-center text-12 border-r">Department</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Labor</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Materials</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Travel</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Equipment/Space</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Miscellaneous</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Budget Total</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Actual Total</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12">Variance</div>
            </div>
        `;

    }


    create_consolidated_budget_analysis_titles(title){
        return `
            <div class="w-full h-[35px] bg-default text-theme_text_color rounded-t-md grid grid-cols-6 budget-titles-row">
                <div class="w-full h-full font-semibold flex col-span-2 items-center justify-center text-12 border-r">${title}</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Budget</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Actual</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12 border-r">Variance</div>
                <div class="w-full h-full font-semibold flex col-span-1 items-center justify-center text-12">Variance %</div>
            </div>
        `;

    }

    create_consolidated_budget_analysis_rows(data, month) {
        let rows = "";
    
        Object.keys(data).forEach(item => {
            const monthlyValue = data[item][month] || 0; 


            const budget = this.builder.build_form_field({
                id: 'budget',
                fieldtype: "float",
                fieldlabel: 'budget',
                omitlabels: true,
                istablefield: true,
                value: lite.utils.thousand_separator(monthlyValue, 2),
                placeholder: "budget",
                classnames: "justify-center text-center budget-cell " 
            });

            const actual = this.builder.build_form_field({
                id: 'actual',
                fieldtype: "float",
                fieldlabel: 'actual',
                omitlabels: true,
                istablefield: true,
                value: '0.00',
                placeholder: "Actual",
                classnames: "justify-center text-center budget-cell " 
                
            });

            const variance = this.builder.build_form_field({
                id: 'variance',
                fieldtype: "float",
                fieldlabel: 'variance',
                omitlabels: true,
                istablefield: true,
                value: '0.00',
                placeholder: "Variance",
                classnames: "justify-center text-center budget-cell " 
                
            });

            const variance_percent = this.builder.build_form_field({
                id: 'variance-percent',
                fieldtype: "float",
                fieldlabel: 'variance_percent',
                omitlabels: true,
                istablefield: true,
                value: '0.00',
                placeholder: "Variance",
                classnames: "justify-center text-center budget-cell " 
                
            });
            
    
            rows += `
                <div class="w-full h-[40px] rounded-t-md flex grid grid-cols-6 border-b border-dashed budget-row ">
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-2 border-dashed border-r text-12">
                        ${item}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${budget}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${actual}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${variance}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed text-12">
                        ${variance_percent}
                    </div>
                </div>
            `;
        });
    
        return rows;
    }
    

    

    create_consolidated_budget_items(item_list, freq, freqType) {
        const total_cols = freq?.length + 3 || 3;
        let cols = "";
    
        // Iterate over the item_list
        $.each(item_list, (category, item) => {
            let fields = "";
            let total = 0;
    
            // Iterate over each frequency period
            $.each(freq, (_, fr) => {
                let periodId = fr.replace(/\s+/g, '_'); // Replace spaces with underscores
                if (freqType == "Quarterly Budget"){
                    periodId = fr
                }

                const fieldValue = item[periodId] || "0.00"; 

                const field = this.builder.build_form_field({
                    id: periodId,
                    fieldtype: "float",
                    fieldlabel: fr,
                    omitlabels: true,
                    istablefield: true,
                    value: lite.utils.thousand_separator(fieldValue, 2),
                    classnames: "text-center budget-cell" 
                });
    
                fields += `<div class="border-dashed border-r">${field}</div>`;
                total += parseFloat(fieldValue) || 0; // Calculate total
            });
    
            const total_field = `<div class="w-full h-full font-semibold flex items-center justify-center h-[40px] border-r text-12 total-cell">${lite.utils.thousand_separator(total, 2)}</div>`; // Updated total field class
    
            cols += `
                <div class="w-full h-[40px] rounded-t-md grid grid-cols-${total_cols} border-b border-dashed budget-row ">
                    <input class="text-center w-full h-full font-semibold flex items-center justify-center h-[40px] col-span-2 border-r text-12 budget-item" type="text" id="item-name" value="${category}" readonly>
                    
                    ${fields}
                    ${total_field}
                </div>
            `;
        });
    
        return cols;
    } 
    
    create_budget_items(item_list, freq) {
        console.log(item_list);
        
        const total_cols = freq?.length + 3 || 3;
        let cols = "";
    
        // Iterate over the item_list
        $.each(item_list, (category, item) => {
            let fields = "";
            let total = 0;
    
            // Iterate over each frequency period
            $.each(freq, (_, fr) => {
                let budget_item = category.replace(/\s+/g, '-');
                let freq = fr.replace(/\s+/g, '-');
                let cell = budget_item + '-' + freq;  
                
                const periodId = fr.replace(/\s+/g, '_');
                const fieldValue = item[periodId] || "0.00";

                const field = this.builder.build_form_field({
                    id: periodId,
                    fieldtype: "float",
                    fieldlabel: fr,
                    omitlabels: true,
                    istablefield: true,
                    value: lite.utils.thousand_separator(fieldValue, 2),
                    read_only: true,
                    classnames: "justify-center mt-1 text-center budget-cell" 
                });
    
                fields += `<div id="${cell}" class="cell border-dashed border-r relative" data-column-name="${fr}">
                                ${field}
                                <span class="absolute top-1 right-1 flex justify-center items-center ping-effect hidden">
                                    <span class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-slate-500 opacity-75 duration-1000"></span>
                                    <span class="inline-flex rounded-full h-2 w-2 bg-[#151030]"></span>
                                </span>
                            </div>`;

                total += parseFloat(fieldValue) || 0; // Calculate total
            });
    
            const total_field = `<div class="w-full h-full font-semibold flex items-center justify-center h-[40px] border-r text-12 total-cell">${lite.utils.thousand_separator(total, 2)}</div>`; // Updated total field class
    
            cols += `
                <div class="w-full h-[40px] rounded-t-md grid grid-cols-${total_cols} border-b border-dashed budget-row ">
                    <input class="text-center w-full h-full font-semibold flex items-center justify-center h-[40px] col-span-2 border-b border-dashed text-12  budget-item-display" type="text" id=" " value="${category}" readonly>
                    
                    ${fields}
                    ${total_field}
                </div>
            `;
        });
    
        return cols;
    }

    create_budget_items_quantities(item_list, freq) {
        const total_cols = freq?.length + 5 || 5;
        let cols = "";
    
        // Iterate over the item_list
        $.each(item_list, (category, item) => {
            let fields = "";
            let total = 0;
    
            // Iterate over each frequency period
            $.each(freq, (_, fr) => {
                let budget_item = category.replace(/\s+/g, '-');
                let freq = fr.replace(/\s+/g, '-');
                let cell = budget_item + '-' + freq;  
                

                const periodId = fr.replace(/\s+/g, '_'); // Use the period name directly
                const fieldValue = item[periodId] || "0"; 
                
                // console.log(periodId)

                const field = `
                <input 
                    autocomplete="off"
                    id="${periodId}" 
                    always-fetch="true"
                    is_required="false" 
                    type="text"
                    value="${lite.utils.thousand_separator(fieldValue, 0)}"
                    class="text-13 h-full justify-center text-center budget-cell w-full border border-t-0 border-l-0 border-dashed"
                    placeholder=""
                >
                `;
    
                fields += `<div id="${cell}-quantity" class="cell relative" data-column-name="${fr}" data-row-name="${category}">
                                ${field}
                                <span class="absolute top-1 right-2 flex justify-center items-center ping-effect hidden">
                                    <span class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-slate-500 opacity-75 duration-1000"></span>
                                    <span class="inline-flex rounded-full h-2 w-2 bg-[#151030]"></span>
                                </span>
                            </div>`;
                total += parseInt(fieldValue) || 0; // Calculate total
            });
    
            const total_field = `<div class="w-full h-full font-semibold flex items-center justify-center h-[40px] border-r text-12 total-cell">${lite.utils.thousand_separator(total, 0)}</div>`; // Updated total field class
    
            cols += `
                <div class="w-full h-[40px] rounded-t-md grid grid-cols-${total_cols} border-b border-dashed budget-row ">
                    <div class="w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center col-span-1 max-w-[70px]">
                        <input autocomplete="off" for="body-row" class="row-check form-check-input" type="checkbox" value="">
                    </div>
                    <input class="text-center w-full h-full font-semibold flex items-center justify-center h-[40px] col-span-2 border-dashed border-l-0 border-t-0 text-12 budget-item" type="text" id="item-name" value="${category}" readonly>
                    <input class="text-center w-full h-full font-semibold flex items-center justify-center h-[40px] col-span-1 border-dashed border-l-0 border-t-0 text-12 unit-cost" type="text" value="0.00" readonly>
                    
                    ${fields}
                    ${total_field}
                </div>
            `;
        });
    
        return cols;
    }

    create_departmental_info(item_list, freq) {
        const total_cols = freq?.length + 3 || 3;
        let cols = "";
    
        // Iterate over the item_list
        $.each(item_list, (category, item) => {
            let fields = "";
            let total = 0;
    
            // Iterate over each frequency period
            $.each(freq, (_, fr) => {
                const periodId = fr.replace(/\s+/g, '_'); // Use the period name directly
                const fieldValue = item[periodId] || "0"; 
                
                // console.log(periodId)

                const field = `
                    <input 
                        autocomplete="off"
                        id="${periodId}" 
                        always-fetch="true"
                        is_required="false" 
                        type="text"
                        value="${lite.utils.thousand_separator(fieldValue, 0)}"
                        class="text-13 h-full justify-center text-center budget-cell w-full border-0 outline-0"
                        placeholder=""
                    >
                `;
    
                fields += `<div class="border border-dashed">${field}</div>`;
                total += parseInt(fieldValue) || 0; // Calculate total
            });
    
            const total_field = `<div class="w-full h-full font-semibold flex items-center justify-center h-[40px] border-r text-12 total-cell">${lite.utils.thousand_separator(total, 0)}</div>`; // Updated total field class
    
            cols += `
                <div class="w-full h-[40px] rounded-t-md grid grid-cols-${total_cols} border-b border-dashed budget-row ">
                    <input class="text-center w-full h-full font-semibold flex items-center justify-center h-[40px] col-span-2 border-r border-dashed text-12 budget-item" type="text" id="item-name" value="${category}" readonly>
                    
                    ${fields}
                    ${total_field}
                </div>
            `;
        });
    
        return cols;
    }
    


    create_budget_rows(item_list, freq) {
        const total_cols = freq?.length + 4 || 4;
        let cols = "";
    
        // Iterate over the item_list
        $.each(item_list, (category, item) => {
            let fields = "";
            let total = 0;
    
            // Iterate over each frequency period
            $.each(freq, (_, fr) => {
                const periodId = fr.replace(/\s+/g, '_');
                const fieldValue = item[periodId] || "0"; 

                const field = this.builder.build_form_field({
                    id: periodId,
                    fieldtype: "int",
                    fieldlabel: fr,
                    omitlabels: true,
                    istablefield: true,
                    value: lite.utils.thousand_separator(fieldValue, 0),
                    read_only: true,
                    classnames: "justify-center mt-1 text-center budget-cell" 
                });
    
                fields += `<div class="border-dashed border-r">${field}</div>`;
                total += parseFloat(fieldValue) || 0; // Calculate total
            });
    
            const total_field = `<div class="w-full h-full font-semibold flex items-center justify-center h-[40px] border-r text-12 total-cell">${lite.utils.thousand_separator(total, 0)}</div>`; // Updated total field class
    
            cols += `
                <div class="w-full h-[40px] rounded-t-md grid grid-cols-${total_cols} border-b border-dashed budget-row ">
                    <div class=" w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center col-span-1 max-w-[70px]">
                    <input autocomplete="off" for="body-row" class="row-check form-check-input" type="checkbox" value="">
                    </div>
                    <input class="text-center w-full h-full font-semibold flex items-center justify-center h-[40px] col-span-2 border-r border-dashed text-12 budget-item" type="text" id="item-name" value="${category}" readonly>
                    
                    ${fields}
                    ${total_field}
                </div>
            `;
        });
    
        return cols;
    }
       

    create_budget_total_row(items, freq) {
        let totalRow = `<div class="w-full h-[40px] rounded-md grid grid-cols-${freq.length + 3} border-t border-b border-dashed total-row">`;
        totalRow += `<div class="w-full h-full font-semibold flex items-center justify-center h-[40px] col-span-2 border-r text-12">Total Amount</div>`;
    
        let grandTotal = 0;

        $.each(freq, (_, fr) => {
            const periodId = fr.replace(/\s+/g, '_'); 
            let sum = 0;
            $.each(items, (_, item) => {
                sum += parseFloat(item[periodId] || 0);
            });

            grandTotal += sum;
    
            totalRow += `<div class="w-full h-full font-semibold flex items-center justify-center h-[40px] border-r text-12 total-cell" id="${periodId}">${lite.utils.thousand_separator(sum, 2)}</div>`;
        });

        totalRow += `<div class="w-full h-full font-semibold flex items-center justify-center h-[40px] text-12 main-total-cell">${lite.utils.thousand_separator(grandTotal, 2)}</div>`;

        totalRow += `</div>`;
    
        return totalRow;
    }


    create_add_remove_buttons_in(){
        let buttons = `
            <div class="bgt-btns w-full flex items-center justify-start h-[30px] rounded-b-md mt-4">
                <button type="button" class="btn w-[70px]  text-[18px] font-normal h-[25px] border-secondary_color text-orange-700 rounded-md" id="remove-btn-in">
                    <span class="material-symbols-outlined">remove</span>
                </button>
                <button type="button" class="btn w-[70px]  bg-default border-default/40 text-[18px] text-white ml-2 h-[25px] rounded-md" id="add-btn-in">
                    <span class="material-symbols-outlined">add_circle</span>
                </button>
            </div>
        `;
        return buttons
    }

    create_add_remove_buttons_ex(){
        let buttons = `
            <div class="bgt-btns w-full flex items-center justify-start h-[30px] rounded-b-md mt-4">
                <button type="button" class="btn w-[70px]  text-[18px] font-normal h-[25px] border-secondary_color text-orange-700 rounded-md" id="remove-btn-ex">
                    <span class="material-symbols-outlined">remove</span>
                </button>
                <button type="button" class="btn w-[70px]  bg-default border-default/40 text-[18px] text-white ml-2 h-[25px] rounded-md" id="add-btn-ex">
                    <span class="material-symbols-outlined">add_circle</span>
                </button>
            </div>
        `;
        return buttons
    }

    create_editable_budget_item(freq, options) {
        const total_cols = freq.length + 5 || 5;
        let row = "";
    
        const select_field = this.builder.build_form_field({
            id: "item-name",
            fieldtype: "select",
            fieldlabel: "item_name",
            options: options,
            omitlabels: true,
            istablefield: true,
            placeholder: "Select item",
            classnames: "justify-center text-center budget-item",
        });
    
        row += `
            <div class="relative w-full h-[40px] flex flex-row rounded-t-md grid grid-cols-${total_cols} border-b border-dashed budget-row editable-row">
                <div class=" w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center col-span-1 max-w-[70px]">
                    <input autocomplete="off" for="body-row" class="row-check form-check-input" type="checkbox" value="">
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-2 border-r text-12">
                    ${select_field}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    <input class="text-center w-full h-full font-semibold flex items-center justify-center h-[40px] col-span-1 border-dashed border-l-0 border-t-0 text-12 unit-cost" type="text" value="0.00" readonly>
                </div>
            `;
    
        $.each(freq, (_, fr) => {
            var x = "0";
            var periodId = fr.replace(/\s+/g, '_');
            const field = this.builder.build_form_field({
                id: periodId,
                fieldtype: "int",
                fieldlabel: fr,
                placeholder: "Enter figure",
                omitlabels: true,
                istablefield: true,
                value: x,
                // read_only: true,
                classnames: "justify-center text-center budget-cell",
            });
            row += 
                `
                <div class="flex cell items-center my-auto justify-center border-dashed ${freq.indexOf(fr) < freq.length - 1 ? "border-r" : ""} ">${field}</div>
                
                `;

        });
    
        const total_field = `<div class="w-full h-full font-semibold flex items-center justify-center border-l border-dashed text-12 total-cell">0</div>`; 
        row += total_field;
        row += `</div>`;
        
        return row;

    }

    quantities_toggle(){

        const toggle_field = `

            <div class="custom-switch w-full flex items-center ml-10 justify-between h-[30px] w-[130px]">
                <span class="text-12 font-semibold w-[90%]">Show Quantities</span>
                <div class="custom-switch-field" id="custom-switch-field" value="0">
                    <div class="custom-switch-wrapper bg-gray-200 flex items-center justify-center relative rounded-full h-[5px] w-[40px] transition duration-500">
                        <div class="custom-switch-toggler absolute w-[17px] h-[17px] rounded-full shadow-md transition duration-500 left-0 bg-gray-400 cursor-pointer" id="custom-switch-toggler"></div>
                    </div>
                </div>
            </div>
        
        `
        return toggle_field
    }


    figures_toggle(){

        const toggle_field = `

            <div class="custom-switch w-full flex items-center ml-10 justify-between h-[30px] w-[130px]">
                <span class="text-12 font-semibold w-[90%]">Show Figures</span>
                <div class="custom-switch-field" id="custom-switch-field" value="0">
                    <div class="custom-switch-wrapper bg-gray-200 flex items-center justify-center relative rounded-full h-[5px] w-[40px] transition duration-500">
                        <div class="custom-switch-toggler absolute w-[17px] h-[17px] rounded-full shadow-md transition duration-500 left-0 bg-gray-400 cursor-pointer" id="custom-switch-toggler"></div>
                    </div>
                </div>
            </div>
        
        `
        return toggle_field
    }


    department_info_popup(category){

        const popup = `
            <div class="popup-container fixed top-0 left-0 w-full h-full bg-gray-500/40 z-50 rounded-md flex items-center justify-center">
                <div class="w-[max-content] mx-auto">
                    <div class="bg-white rounded-md px-5 py-3 mt-10  h-[55vh] w-[80vw]">
                        <div class="relative text-gray-600 text-sm w-full border-b pb-2 flex items-center justify-between mb-5">
                            <span class="font-semibold">${category}</span>
                            <div class="custom-switch absolute right-16 w-full flex items-center ml-10  justify-between h-[30px] w-[130px]">
                                <span class="text-12 font-semibold w-[90%]">Show Figures</span>
                                <div class="custom-switch-field" id="custom-switch-field" value="0">
                                    <div class="custom-switch-wrapper bg-gray-200 flex items-center justify-center relative rounded-full h-[5px] w-[40px] transition duration-500">
                                        <div class="custom-switch-toggler absolute w-[17px] h-[17px] rounded-full shadow-md transition duration-500 left-0 bg-gray-400 cursor-pointer" id="custom-switch-toggler"></div>
                                    </div>
                                </div>
                            </div>

                            <button type = "button" class="close-info-popup text-orange-500">
                                <span class="material-symbols-outlined font-19 font-bold"> close </span>
                            </button>
                        </div>
                        <div class="departmental-budget-info left-4 h-[47vh] w-[78vw] overflow-y-auto">
                            
                        </div>
                        
                    </div>
                </div>
            </div>

        `
        return popup   

    }

    review_notes_field (){
        let field = `
            <div class="justify-center text-center budget-cell">
                <label for="review-notes-field" class="form-label text-12 text-slate-500 ">Review Notes</label>
                <textarea 
                    id="review-notes-field" 
                    name="review-notes-field" 
                    cols="9" 
                    rows="10" 
                    class="form-control border w-full px-3 py-2 text-13 focus:outline-none resize-none" 
                    style="height: 200px;">
                </textarea>
            </div>
        `
        return field
    }

    create_department_buttons(departments) {
        let buttons = `<button type="button" class="min-w-[10vw] h-[75%] font-semibold hover:-translate-y-1 text-sm m-1 flex justify-center items-center department-button">Consolidated</button>`;
        departments.forEach((department) => {
          buttons += `
            <button type="button" class="min-w-[10vw] h-[75%] font-semibold text-sm m-1 hover:-translate-y-1 flex justify-center items-center department-button">
              ${department}
            </button>
          `;
        });
        return buttons;
    }
      

    review_notes_popup(item, period, unit_cost, quantity, amount){
        let popup = `
            <div class="review-notes-popup fixed top-0 left-0 w-full h-full bg-gray-500/40 z-50 rounded-md flex items-center justify-center">
                <div class="w-[max-content] mx-auto">
                    <div class="bg-white rounded-md px-5 py-3 mt-10  h-[45vh] w-[55vw]">
                        <div class="text-gray-600 text-sm w-full border-b pb-2 flex items-center justify-between mb-5">
                            <span class="font-semibold">Cell Info</span>
                            <button type = "button" class="close-review-notes-popup text-orange-500">
                                <span class="material-symbols-outlined font-19 font-bold"> close </span>
                            </button>
                        </div>
                        <div class="h-[35vh] w-[52vw] -translate-y-4 grid grid-rows-3 gap-2 gap-y-0.5">
                            <div class = "h-[10vh] w-full row-span-1 grid grid-cols-5 gap-2">
                                <label for="cell-item-name" class="text-12 text-slate-500 ml-1">Item</label>
                                <label for="cell-period" class="text-12 text-slate-500 ml-1">Period</label>
                                <label for="unit-cost" class="text-12 text-slate-500 ml-1">Unit Cost</label>
                                <label for="item-quantity" class="text-12 text-slate-500 ml-1">Quantity</label>
                                <label for="cell-value" class="text-12 text-slate-500 ml-1">Total Cost</label>
                                <input id="cell-item-name" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11 " type="text" value="${item}" readonly>
                                <input id="cell-period" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${period}" readonly>
                                <input id="unit-cost" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${lite.utils.thousand_separator(unit_cost, 2)}" readonly>
                                <input id="item-quantity" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${lite.utils.thousand_separator(quantity, 0)}" readonly>
                                <input id="cell-value" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${amount}" readonly>
                            </div>
                            <div class="h-[25vh] w-full row-span-1 -translate-y-10">
                                <label for="review-notes-field" class="form-label tr text-12 text-slate-500 mt-1">Review Notes</label>
                                <textarea 
                                    id="review-notes-field" 
                                    name="review-notes-field" 
                                    cols="9" 
                                    rows="10" 
                                    class="form-control border w-full px-3 text-13 focus:outline-none resize-none" 
                                    style="height: 200px;">
                                </textarea>
                            </div>
                            <div class = "relative h-[5vh] w-full row-span-1 translate-y-20 mt-2">
                                <button class="absolute right-32 close-review-notes-popup text-black bg-gray-200 border w-[120px] h-[30px] btn rounded-md mt-2 ml-2">
                                    Cancel
                                    <span class="material-symbols-outlined">close</span>
                                </button>
                                <button  class="absolute right-0 save-review-notes text-white bg-default w-[120px] h-[30px] btn rounded-md mt-2 ml-2">
                                    Save
                                    <span class="material-symbols-outlined">save</span>
                                </button>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
        `
        return popup
    }
    review_notes_popup_in_department(item, period, unitCost, quantity, amount){
        let popup = `
            <div class="review-notes-popup fixed top-0 left-0 w-full h-full bg-gray-500/40 z-50 rounded-md flex items-center justify-center">
                <div class="w-[max-content] mx-auto">
                    <div class="bg-white rounded-md px-5 py-3 mt-10  h-[45vh] w-[55vw]">
                        <div class="text-gray-600 text-sm w-full border-b pb-2 flex items-center justify-between mb-5">
                            <span class="font-semibold">Cell Info</span>
                            <button type = "button" class="close-review-notes-popup text-orange-500">
                                <span class="material-symbols-outlined font-19 font-bold"> close </span>
                            </button>
                        </div>
                        <div class="h-[35vh] w-[52vw] -translate-y-4 grid grid-rows-3 gap-2 gap-y-0.5">
                            <div class = "h-[10vh] w-full row-span-1 grid grid-cols-5 gap-2">
                                <label for="cell-item-name" class="text-12 text-slate-500 ml-1">Item</label>
                                <label for="cell-period" class="text-12 text-slate-500 ml-1">Period</label>
                                <label for="unit-cost" class="text-12 text-slate-500 ml-1">Unit Cost</label>
                                <label for="cell-value" class="text-12 text-slate-500 ml-1">Quantity</label>
                                <label for="total-cost" class="text-12 text-slate-500 ml-1">Total Cost</label>
                                <input id="cell-item-name" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11 " type="text" value="${item}" readonly>
                                <input id="cell-period" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${period}" readonly>
                                <input id="unit-cost" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${unitCost}" readonly>
                                <input id="cell-value" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${quantity}">
                                <input id="total-cost" class="text-center min-w-[10vw] -translate-y-4 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${amount}" readonly>
                            </div>
                            <div class="h-[25vh] w-full row-span-1 -translate-y-10">
                                <label for="review-notes-field" class="form-label tr text-12 text-slate-500 mt-1">Review Notes</label>
                                <textarea 
                                    id="review-notes-field" 
                                    name="review-notes-field" 
                                    cols="9" 
                                    rows="10" 
                                    class="form-control border w-full px-3 text-13 focus:outline-none resize-none" 
                                    style="height: 200px;" readonly>
                                </textarea>
                            </div>
                            <div class = "relative h-[5vh] w-full row-span-1 translate-y-20 mt-2">
                                <button class="absolute right-44 close-review-notes-popup text-black bg-gray-200 border w-[160px] h-[30px] btn rounded-md mt-2 ml-2">
                                    Cancel
                                    <span class="material-symbols-outlined">close</span>
                                </button>
                                <button  class="absolute right-0 save-changes text-white bg-default w-[160px] h-[30px] btn rounded-md mt-2 ml-2">
                                    Save Changes
                                    <span class="material-symbols-outlined">check</span>
                                </button>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
        `
        return popup
    }

    create_project_budget_rows(data, price_list) {
        // console.log(data);
        
        let rows = ''
                
        // Iterate through the data (task list)
        data.forEach(task => {
            
            // Get the task name and details
            const taskName = Object.keys(task)[0];

            // // Skip the 'Total Amount' task
            if (taskName === 'Total Amount' || taskName === 'materials_data') {
                return; 
            }

            const taskDetails = task[taskName];   
                       
            // Use the `build_form_field` to create each field with values from taskDetails
            const task_field = this.builder.build_form_field({
                id: "task-activity",
                fieldtype: "text",
                fieldname: "task_field",
                value: taskName,
                omitlabels: true,
                istablefield: true,
                classnames: "h-[98%] budget-cell task-activity",
                read_only: true,
            });
        
            const start_date = this.builder.build_form_field({
                id: "start-date",
                fieldtype: "date",
                fieldname: "start_date",
                value: taskDetails?.start_date || '',
                omitlabels: true,
                istablefield: true,
                placeholder: "Start date",
                classnames: "h-[96%] justify-center text-center budget-cell",
            });
    
            const end_date = this.builder.build_form_field({
                id: "end-date",
                fieldtype: "date",
                fieldname: "end_date",
                value: taskDetails?.end_date || '',
                omitlabels: true,
                istablefield: true,
                placeholder: "End date",
                classnames: "h-[96%] justify-center text-center budget-cell",
            });
    
            const days = this.builder.build_form_field({
                id: "days",
                fieldtype: "int",
                fieldname: "days",
                value: taskDetails.task_duration || '0',
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell",
            });
    
            const labor_unit_cost = this.builder.build_form_field({
                id: "labor-unit-cost",
                fieldtype: "float",
                fieldname: "labor_unit_cost",
                value: lite.utils.thousand_separator(parseFloat(taskDetails.daily_labor_cost), 2) || '0.00',
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell",
                read_only: true,
            });
    
            const labor_total = this.builder.build_form_field({
                id: "labor-total",
                fieldtype: "float",
                fieldname: "labor_total",
                value: lite.utils.thousand_separator((taskDetails.daily_labor_cost * taskDetails.task_duration), 2) || '0.00',
                omitlabels: true,
                istablefield: true,
                classnames: "h-full justify-center text-center labor-total budget-cell bg-slate-100",
                read_only: true,
            });

            if(taskDetails?.material_quantity !== undefined){
                taskDetails.material_quantity = lite.utils.thousand_separator(taskDetails.material_quantity, 0)
                taskDetails.material_unit_cost = lite.utils.thousand_separator(taskDetails.material_unit_cost, 2)
                taskDetails.material_total = lite.utils.thousand_separator(taskDetails.material_total, 2)
                
            }
            
            const material_quantity = this.builder.build_form_field({
                id: "material-quantity",
                fieldtype: "int",
                fieldname: "material_quantity",
                value: taskDetails.material_quantity || '0',
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell material-quantity",
                read_only: true,
            });
    
            const material_unit_cost = this.builder.build_form_field({
                id: "material-unit-cost",
                fieldtype: "float",
                fieldname: 'material_unit_cost',
                value: taskDetails.material_unit_cost || '0.00',
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell material-unit-cost",
                read_only: true,
            });
    
            const material_total = this.builder.build_form_field({
                id: "material-total",
                fieldtype: "float",
                fieldname: 'material_total',
                value: taskDetails.material_total || '0.00',
                omitlabels: true,
                istablefield: true,
                classnames: "h-full justify-center text-center material-total budget-cell bg-slate-100",
                read_only: true, 
            });

            const fixed_travel = this.builder.build_form_field({
                id: 'fixed-travel',
                fieldtype: "float",
                fieldname: 'fixed_travel',
                value: taskDetails?.fixed_travel || '0.00',
                omitlabels: true,
                istablefield: true,
                placeholder: "Travel Costs",
                classnames: "justify-center text-center budget-cell travel-cost figures-cell" 
            });
    
            const fixed_equip = this.builder.build_form_field({
                id: 'fixed-equip',
                fieldtype: "float",
                fieldname: 'fixed_equip',
                value: taskDetails?.fixed_equip || '0.00',
                omitlabels: true,
                istablefield: true,
                placeholder: "Equipment Costs",
                classnames: "justify-center text-center  budget-cell equipment-cost figures-cell" 
            });
    
            const fixed_misc = this.builder.build_form_field({
                id: 'fixed-misc',
                fieldtype: "float",
                fieldname: 'fixed_misc',
                value: taskDetails?.fixed_misc || '0.00',
                omitlabels: true,
                istablefield: true,
                placeholder: "Misc. Costs",
                classnames: "justify-center text-center budget-cell misc-cost figures-cell" 
            });
    
            const balance_budget = this.builder.build_form_field({
                id: 'balance-budget',
                fieldtype: "float",
                fieldname: 'balance_budget',
                value: taskDetails?.balance_budget || '0.00',
                omitlabels: true,
                istablefield: true,
                placeholder: "Budget",
                classnames: "justify-center text-center budget-cell ",
                read_only: true, 
            });
    
            const balance_actual = this.builder.build_form_field({
                id: 'balance-actual',
                fieldtype: "float",
                fieldname: 'balance_actual',
                value: taskDetails?.balance_actual || '0.00',
                omitlabels: true,
                istablefield: true,
                placeholder: "Actual",
                classnames: "justify-center text-center budget-cell ",
                read_only: true, 
            });
    
            const variance = this.builder.build_form_field({
                id: 'variance',
                fieldtype: "float",
                fieldname: 'variance',
                value: taskDetails?.variance || '0.00',
                omitlabels: true,
                istablefield: true,
                placeholder: "Variance",
                classnames: "justify-center text-center budget-cell ",
                read_only: true, 
            });
    
            const task_status = this.builder.build_form_field({
                id: `task-status`,
                fieldtype: "select",
                fieldname: "tast_status",
                value: taskDetails?.task_status || 'Not Started',
                options: [
                    'Not Started',
                    'In Progress',
                    'Complete',
                    'On Hold',
                    'Overdue',    
                ],
                omitlabels: true,
                istablefield: true,
                placeholder: "Select item",
                classnames: "justify-center text-center task-status budget-cell ",
            });
    
    
            // Create a row for this taskcell_name
            rows += `
            <div class="w-full h-[40px] rounded-t-md flex grid grid-cols-18 border-b border-dashed budget-row ">
                <div class="relative w-full h-full font-semibold flex items-center justify-center col-span-3 border-dashed border-r border-b text-12 task-field">
                    ${task_field}
                    <span class="absolute top-1 right-1 flex justify-center items-center ping-effect hidden">
                        <span class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-slate-500 opacity-75 duration-1000"></span>
                        <span class="inline-flex rounded-full h-2 w-2 bg-[#151030]"></span>
                    </span>
                </div>
                <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${start_date}
                </div>
                <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${end_date}
                </div>
                <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${days}
                </div>
                <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${labor_unit_cost}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${labor_total}
                </div>
                <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${material_quantity}
                </div>
                <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${material_unit_cost}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${material_total}
                </div>
                <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${fixed_travel}
                </div>
                <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${fixed_equip}
                </div>
                <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${fixed_misc}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${balance_budget}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${balance_actual}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${variance}
                </div>
                <div class="task-status-cell w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                    ${task_status}
                </div>
            </div>
            `;
        });
        
        return rows;  // Return all rows



    }

    create_project_budget_totals_row(){
        let default_val = '0.00'

        const labor_sub_total = this.builder.build_form_field({
            id: "labor-sub-total",
            fieldtype: "float",
            fieldname: "labor_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const material_sub_total = this.builder.build_form_field({
            id: "material-sub-total",
            fieldtype: "float",
            fieldname: "material_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const travel_sub_total = this.builder.build_form_field({
            id: "travel-sub-total",
            fieldtype: "float",
            fieldname: "travel_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const equipment_sub_total = this.builder.build_form_field({
            id: "equipment-sub-total",
            fieldtype: "float",
            fieldname: "equipment_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const misc_sub_total = this.builder.build_form_field({
            id: "misc-sub-total",
            fieldtype: "float",
            fieldname: "misc_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const balance_budget_sub_total = this.builder.build_form_field({
            id: "balance-budget-sub-total",
            fieldtype: "float",
            fieldname: "balance_budget_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const balance_actual_sub_total = this.builder.build_form_field({
            id: "balance-actual-sub-total",
            fieldtype: "float",
            fieldname: "balance_actual_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const balance_variance_sub_total = this.builder.build_form_field({
            id: "balance-variance-sub-total",
            fieldtype: "float",
            fieldname: "balance_variance_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });


        let total_row = `
            <div id = "sub-totals-row" class="w-full h-[40px] rounded-md grid grid-cols-18 bg-slate-100 border-b border-dashed total-row" bis_skin_checked="1">
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-3 border-dashed border-r text-default text-12">
                    <p class = "m-auto self-center text-center">Total Amount</p>
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-4 text-default text-12">                    
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r border-l text-default text-12">
                    ${labor_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-2 text-default text-12">                    
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r border-l text-default text-12">
                    ${material_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${travel_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${equipment_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${misc_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${balance_budget_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${balance_actual_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${balance_variance_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">                    
                </div>
            </div>
        ` 
        return total_row
    }

    create_consolidated_project_budget_totals_row(){
        let default_val = '0.00'

        const labor_sub_total = this.builder.build_form_field({
            id: "labor-sub-total",
            fieldtype: "float",
            fieldname: "labor_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const material_sub_total = this.builder.build_form_field({
            id: "material-sub-total",
            fieldtype: "float",
            fieldname: "material_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const travel_sub_total = this.builder.build_form_field({
            id: "travel-sub-total",
            fieldtype: "float",
            fieldname: "travel_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const equipment_sub_total = this.builder.build_form_field({
            id: "equipment-sub-total",
            fieldtype: "float",
            fieldname: "equipment_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const misc_sub_total = this.builder.build_form_field({
            id: "misc-sub-total",
            fieldtype: "float",
            fieldname: "misc_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const balance_budget_sub_total = this.builder.build_form_field({
            id: "balance-budget-sub-total",
            fieldtype: "float",
            fieldname: "balance_budget_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const balance_actual_sub_total = this.builder.build_form_field({
            id: "balance-actual-sub-total",
            fieldtype: "float",
            fieldname: "balance_actual_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });

        const balance_variance_sub_total = this.builder.build_form_field({
            id: "balance-variance-sub-total",
            fieldtype: "float",
            fieldname: "balance_variance_sub_total",
            value: default_val,
            omitlabels: true,
            istablefield: true,
            classnames: "justify-center text-center total-budget-cell bg-slate-100",
            read_only: true,
        });


        let total_row = `
            <div id = "sub-totals-row" class="w-full h-[40px] rounded-md grid grid-cols-10 bg-slate-100 border-b border-dashed total-row" bis_skin_checked="1">
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-2 border-dashed border-r text-default text-12">
                    <p class = "m-auto self-center text-center">Total Amount</p>
                </div>   
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r border-l text-default text-12">
                    ${labor_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r border-l text-default text-12">
                    ${material_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${travel_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${equipment_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${misc_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${balance_budget_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${balance_actual_sub_total}
                </div>
                <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-dashed border-r text-default text-12">
                    ${balance_variance_sub_total}
                </div>
            </div>
        ` 
        return total_row
    }

    project_budget_task_info_popup(data){
        let materials = data.materials
        let rows = "";

        // Iterate over the materials object
        $.each(materials, (item, details) => {
            const { unit_cost, quantity } = details;
            const total = unit_cost * quantity;

            rows += `
            <div class="w-full h-[30px] col-span-2 grid grid-cols-4 border-b border-dashed budget-row material-related">
                <div class="w-full h-full flex items-center justify-center  text-sm border-r budget-item">
                    ${item}
                </div>
                <div class="w-full h-full flex items-center justify-center font-semibold text-sm border-r budget-unit-price">
                    ${lite.utils.thousand_separator(unit_cost, 2)}
                </div>
                <div class="w-full h-full flex items-center justify-center  text-sm border-r budget-quantity">
                    ${quantity}
                </div>
                <div class="w-full h-full flex items-center justify-center font-semibold font-semibold text-sm budget-total">
                    ${lite.utils.thousand_separator(total, 2)}
                </div>
            </div>
            `;
        });

        let popup = `
            <div class="task-info-popup fixed top-0 left-0 w-full h-full bg-gray-500/40 z-50 rounded-md flex items-center justify-center">
                <div class="w-[max-content] mx-auto">
                    <div class="bg-white rounded-md px-5 py-3 mt-10  h-[50vh] w-[70vw]">
                        <div class="text-gray-600 text-sm w-full border-b pb-2 flex items-center justify-between mb-5">
                            <span class="font-semibold">${data.task}</span>
                            <button type = "button" class="close-task-info-popup text-orange-500">
                                <span class="material-symbols-outlined font-19 font-bold"> close </span>
                            </button>
                        </div>
                        <div class="h-[43vh] w-[68vw] -translate-y-4 grid grid-rows-3 gap-2">
                            <div class = "min-h-[38vh] w-[66vw] flex grid grid-cols-2 row-span-2 gap-2 overflow-auto">
                                <div class = "h-[10vh] w-full col-span-2 grid grid-cols-4 gap-x-2">
                                    <label for="task-duration" class="text-12 text-slate-500 ml-1">Task Duration (Days)</label>
                                    <label for="daily-labor-cost" class="text-12 text-slate-500 ml-1">Daily Labor Cost</label>
                                    <label for="total-labor-cost" class="text-12 text-slate-500 ml-1">Total Labor Cost</label>
                                    <label for="task-status" class="text-12 text-slate-500 ml-1">Task Status</label>
                                    <input id="task-duration" class="text-center min-w-[10vw] -translate-y-2 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${lite.utils.thousand_separator(data.task_duration, 0)}" readonly>
                                    <input id="daily-labor-cost" class="text-center min-w-[10vw] -translate-y-2 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${lite.utils.thousand_separator(data.daily_labor_cost, 2)}" readonly>
                                    <input id="total-labor-cost" class="text-center min-w-[10vw] -translate-y-2 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${lite.utils.thousand_separator((data.task_duration * data.daily_labor_cost), 2)}" readonly>
                                    <input id="task-status" class="text-center min-w-[10vw] -translate-y-2 font-semibold flex items-center rounded-md justify-center h-[40px] col-span-1 text-11" type="text" value="${data.task_status}" readonly>
                                </div>
                                <div class = "w-full col-span-1">                                    
                                    <label for="description-field" class="form-label tr text-12 text-slate-500 mt-1">Task Description</label>
                                    <textarea 
                                        id="description-field" 
                                        name="description-field" 
                                        cols="1" 
                                        rows="10" 
                                        class="border rounded-md w-full px-3  text-sm  focus:outline-none resize-none" 
                                        style="height: 100px;" readonly>${data.description}</textarea>
                                </div>
                                <div class = "w-full col-span-1">
                                    <label for="objective-field" class="form-label tr text-12 text-slate-500 mt-1">Associated Objectives</label>
                                    <textarea
                                        id="objective-field" 
                                        name="objective-field" 
                                        cols="1" 
                                        rows="10" 
                                        class="border rounded-md w-full px-3 text-sm focus:outline-none resize-none"
                                        style="height: 100px;" >${data.objectives}</textarea>
                                </div>
                                
                                <div class="w-full col-span-2 font-semibold border-t text-12 mt-4 material-related">Material Details</div>

                                <div class = "h-full w-full col-span-2 material-related">
                                    <div class="task-materials-wrapper border border-dashed rounded-md  mb-4 rounded-t-md"></div>
                                </div>

                                <div class="w-full col-span-2 font-semibold border-t text-12 mt-8">Review Notes</div>
                                <div class="h-[20vh] w-full col-span-2 mt-1">
                                    <label for="review-notes-field" class="tr text-12 text-slate-500 mt-1">Review Notes</label>
                                    <textarea 
                                    id="review-notes-field" 
                                    name="review-notes-field" 
                                    cols="1" 
                                    rows="7" 
                                    class="border rounded-md w-full px-3 text-sm focus:outline-none resize-none"
                                    style="height: 100px;" readonly>${data.review_notes}</textarea>

                                    
                                    <div class = "w-full col-span-2 resolve-review-check hidden">
                                        <label for="resolve-review" class="tr text-12 text-slate-500 mt-1">Mark as Resolved</label>
                                        <input id = "resolve-review" name = "resolve-review" autocomplete="off" for="body-row" class="m-2 form-check-input" type="checkbox" value="">
                                    </div>
                                </div>
                            
                            </div>
                            <div class = "relative h-[5vh] w-full row-span-1 translate-y-20 mt-2 ">
                                <button class="absolute right-44 close-task-info-popup text-black bg-gray-200 border w-[160px] h-[30px] btn rounded-md mt-2 ml-2">
                                    Cancel
                                    <span class="material-symbols-outlined">close</span>
                                </button>
                                <button  class="absolute right-0 apply-changes text-white bg-default w-[160px] h-[30px] btn rounded-md mt-2 ml-2">
                                    Apply Changes
                                    <span class="material-symbols-outlined">check</span>
                                </button>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
        `
        return popup
    }

    create_consolidated_project_budget_rows(data) {
        // console.log(data);        
        let rows = "";
        
        // Iterate through the departments
        Object.keys(data).forEach(department => {
            const department_data = data[department];
            const total_amount = department_data.find(task => Object.keys(task)[0] === "Total Amount")['Total Amount'];

            // Initialize total values
            let total_labor = lite.utils.thousand_separator(parseFloat(total_amount.labor_sub_total), 2);
            let total_material = lite.utils.thousand_separator(parseFloat(total_amount.material_sub_total), 2);
            let total_travel = lite.utils.thousand_separator(parseFloat(total_amount.travel_sub_total), 2);
            let total_equip = lite.utils.thousand_separator(parseFloat(total_amount.equipment_sub_total), 2);
            let total_misc = lite.utils.thousand_separator(parseFloat(total_amount.misc_sub_total), 2);
            let total_budget = lite.utils.thousand_separator(parseFloat(total_amount.balance_budget_sub_total), 2);
            let total_actual = lite.utils.thousand_separator(parseFloat(total_amount.balance_actual_sub_total), 2);
            let total_variance = lite.utils.thousand_separator(parseFloat(total_amount.balance_variance_sub_total), 2);

            // Use the `build_form_field` to create consolidated fields
            const labor_total = this.builder.build_form_field({
                id: "labor-total",
                fieldtype: "float",
                fieldname: "labor_total",
                value: total_labor,
                omitlabels: true,
                istablefield: true,
                classnames: "h-full justify-center text-center labor-total budget-cell",
                read_only: true,
            });
    
            const material_total = this.builder.build_form_field({
                id: "material-total",
                fieldtype: "float",
                fieldname: "material_total",
                value: total_material,
                omitlabels: true,
                istablefield: true,
                classnames: "h-full justify-center text-center material-total budget-cell",
                read_only: true,
            });
    
            const fixed_travel = this.builder.build_form_field({
                id: 'fixed-travel',
                fieldtype: "float",
                fieldname: 'fixed_travel',
                value: total_travel,
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell travel-cost figures-cell",
                read_only: true,
            });
    
            const fixed_equip = this.builder.build_form_field({
                id: 'fixed-equip',
                fieldtype: "float",
                fieldname: 'fixed_equip',
                value: total_equip,
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell equipment-cost figures-cell",
                read_only: true,
            });
    
            const fixed_misc = this.builder.build_form_field({
                id: 'fixed-misc',
                fieldtype: "float",
                fieldname: 'fixed_misc',
                value: total_misc,
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell misc-cost figures-cell",
                read_only: true,
            });
    
            const balance_budget = this.builder.build_form_field({
                id: 'balance-budget',
                fieldtype: "float",
                fieldname: 'balance_budget',
                value: total_budget,
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell balance-budget",
                read_only: true,
            });
    
            const balance_actual = this.builder.build_form_field({
                id: 'balance-actual',
                fieldtype: "float",
                fieldname: 'balance_actual',
                value: total_actual,
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell balance-actual",
                read_only: true,
            });
    
            const variance = this.builder.build_form_field({
                id: 'variance',
                fieldtype: "float",
                fieldname: 'variance',
                value: total_variance,
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell variance",
                read_only: true,
            });
    
            // Create a row for the consolidated totals
            rows += `
                <div class="w-full h-[40px] rounded-t-md flex grid grid-cols-10 border-b border-dashed budget-row">
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-2 border-dashed border-r border-b text-12 department-name">
                        ${department}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${labor_total}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${material_total}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${fixed_travel}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${fixed_equip}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${fixed_misc}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${balance_budget}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${balance_actual}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${variance}
                    </div>
                </div>
            `;
        });
    
        return rows;  
    }

    create_consolidated_project_budget_rows_tasks(data) {
        // console.log(data);
        
        let rows = "";
        
        // Iterate through the tasks
        Object.keys(data).forEach(task => {
            const task_data = data[task];
    
            // Use the `build_form_field` to create consolidated fields
            const labor_total = this.builder.build_form_field({
                id: `labor-total`,
                fieldtype: "float",
                fieldname: "labor_total",
                value: lite.utils.thousand_separator(task_data.labor_total, 2),
                omitlabels: true,
                istablefield: true,
                classnames: "h-full justify-center text-center labor-total budget-cell",
                read_only: true,
            });
    
            const material_total = this.builder.build_form_field({
                id: `material-total`,
                fieldtype: "float",
                fieldname: "material_total",
                value: lite.utils.thousand_separator(task_data.material_total, 2),
                omitlabels: true,
                istablefield: true,
                classnames: "h-full justify-center text-center material-total budget-cell",
                read_only: true,
            });
    
            const fixed_travel = this.builder.build_form_field({
                id: `fixed-travel`,
                fieldtype: "float",
                fieldname: 'fixed_travel',
                value: lite.utils.thousand_separator(task_data.fixed_travel, 2),
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell travel-cost figures-cell",
                read_only: true,
            });
    
            const fixed_equip = this.builder.build_form_field({
                id: `fixed-equip`,
                fieldtype: "float",
                fieldname: 'fixed_equip',
                value: lite.utils.thousand_separator(task_data.fixed_equip, 2),
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell equipment-cost figures-cell",
                read_only: true,
            });
    
            const fixed_misc = this.builder.build_form_field({
                id: `fixed-misc`,
                fieldtype: "float",
                fieldname: 'fixed_misc',
                value: lite.utils.thousand_separator(task_data.fixed_misc, 2),
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell misc-cost figures-cell",
                read_only: true,
            });
    
            const balance_budget = this.builder.build_form_field({
                id: `balance-budget`,
                fieldtype: "float",
                fieldname: 'balance_budget',
                value: lite.utils.thousand_separator(task_data.balance_budget, 2),
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell balance-budget",
                read_only: true,
            });
    
            const balance_actual = this.builder.build_form_field({
                id: `balance-actual`,
                fieldtype: "float",
                fieldname: 'balance_actual',
                value: lite.utils.thousand_separator(task_data.balance_actual, 2),
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell balance-actual",
                read_only: true,
            });
    
            const variance = this.builder.build_form_field({
                id: `variance`,
                fieldtype: "float",
                fieldname: 'variance',
                value: lite.utils.thousand_separator(task_data.variance, 2),
                omitlabels: true,
                istablefield: true,
                classnames: "justify-center text-center budget-cell variance",
                read_only: true,
            });
    
            // Create a row for the consolidated totals
            rows += `
                <div class="w-full h-[40px] rounded-t-md flex grid grid-cols-10 border-b border-dashed budget-row">
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-2 border-dashed border-r border-b text-12 department-name">
                        ${task}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${labor_total}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${material_total}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${fixed_travel}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${fixed_equip}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${fixed_misc}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${balance_budget}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${balance_actual}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-dashed border-r text-12">
                        ${variance}
                    </div>
                </div>
            `;
        });
    
        return rows;  
    }

    create_project_materials_tittles(){
        return `
            <div class="w-full h-[30px] bg-default flex text-white rounded-t-md budget-titles-row">
                <div class=" head-check w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center max-w-[70px]">
                    <input autocomplete="off" id="" for="head-row" class="form-check-input  head-check" type="checkbox">
                </div>
                <div class = "w-full h-full grid grid-cols-4">
                    <div class="w-full h-full font-semibold flex items-center justify-center h-[30px] col-span-1 border-r text-12">Item</div>
                    <div class="w-full h-full font-semibold flex items-center justify-center h-[30px] col-span-1 border-r text-12">Unit Cost</div>
                    <div class="w-full h-full font-semibold flex items-center justify-center h-[30px] col-span-1 border-r text-12">Quantity</div>
                    <div class="w-full h-full font-semibold flex items-center justify-center h-[30px] col-span-1 border-r text-12">Total Cost</div>
                </div>
            </div>
        `;
    }

    create_project_materials_editable_rows(data, options){
        // console.log(data);
        let row = ''
        if (Object.keys(data).length !== 0) {
            this.create_project_material_rows()
            for (const [item_name, item_data] of Object.entries(data)) {
                row += this.create_project_material_rows(item_name, item_data);
            }            
        }        

        const select_field = this.builder.build_form_field({
            id: "material-item-name",
            fieldtype: "select",
            fieldlabel: "material_item_name",
            options: options,
            omitlabels: true,
            istablefield: true,
            placeholder: "Select item",
            classnames: "justify-center text-center material-item-name popup-budget-cell",
        });

        const unit_cost = this.builder.build_form_field({
            id: "material-unit-cost",
            fieldtype: "float",
            fieldname: "material_unit_cost",
            value: '0.00',
            omitlabels: true,
            istablefield: true,
            classnames: "h-full justify-center text-center material-unit-cost popup-budget-cell",
            read_only: true,
        });

        const quantity = this.builder.build_form_field({
            id: 'material-quantity',
            fieldtype: "int",
            fieldlabel: 'material_quantity',
            placeholder: "Enter figure",
            omitlabels: true,
            istablefield: true,
            value: '0',
            classnames: "justify-center text-center material-quantity popup-budget-cell",
        });

        const total_cost = this.builder.build_form_field({
            id: "material-total-cost",
            fieldtype: "float",
            fieldname: "material_total_cost",
            value: '0.00',
            omitlabels: true,
            istablefield: true,
            classnames: "h-full justify-center text-center material-total-cost popup-budget-cell",
            read_only: true,
        });

        if(options !== ''){

            row += `
                <div class="relative w-full h-[40px] flex flex-row border-b border-dashed materials-budget-row editable-row">
                    <div class=" w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center max-w-[70px]">
                        <input autocomplete="off" for="body-row" class="row-check form-check-input" type="checkbox" value="">
                    </div>
                    <div class = "w-full h-full grid grid-cols-4">
                        <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-r text-12">
                            ${select_field}
                        </div>
                        <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-r text-12">
                            ${unit_cost}
                        </div>
                        <div class="w-full h-full flex items-center justify-center col-span-1 border-r text-12">
                            ${quantity}
                        </div>
                        <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-r text-12 total-cost">
                            ${total_cost}
                        </div>                
                    </div>
                </div>
            `
        }

        return row
    }

    create_project_material_rows (item_name, item_data){
        let row = ''

        const item_field = this.builder.build_form_field({
            id: "material-item-name",
            fieldtype: "text",
            fieldlabel: "material_item_name",
            value: item_name,
            omitlabels: true,
            istablefield: true,
            placeholder: "Select item",
            classnames: "justify-center text-center material-item-name h-[96%] popup-budget-cell",
        });

        const unit_cost = this.builder.build_form_field({
            id: "material-unit-cost",
            fieldtype: "float",
            fieldname: "material_unit_cost",
            value: lite.utils.thousand_separator(item_data?.unit_cost, 2) || '0.00',
            omitlabels: true,
            istablefield: true,
            classnames: "h-full justify-center text-center material-unit-cost ",
            read_only: true
        });

        const quantity = this.builder.build_form_field({
            id: 'material-quantity',
            fieldtype: "int",
            fieldlabel: 'material_quantity',
            placeholder: "Enter figure",
            omitlabels: true,
            istablefield: true,
            value: lite.utils.thousand_separator(item_data?.quantity, 0) || '0',
            classnames: "justify-center text-center material-quantity popup-budget-cell",
        });

        const total_cost = this.builder.build_form_field({
            id: "material-total-cost",
            fieldtype: "float",
            fieldname: "material_total_cost",
            value: lite.utils.thousand_separator(item_data?.total_cost, 2) || '0.00',
            omitlabels: true,
            istablefield: true,
            classnames: "h-full justify-center text-center material-total-cost ",
            read_only: true,
        });

        row += `
            <div class="relative w-full h-[40px] flex flex-row border-b border-dashed materials-budget-row">
                <div class=" w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center max-w-[70px]">
                    <input autocomplete="off" for="body-row" class="row-check form-check-input" type="checkbox" value="">
                </div>
                <div class = "w-full h-full grid grid-cols-4">
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-r text-12">
                        ${item_field}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-r text-12">
                        ${unit_cost}
                    </div>
                    <div class="w-full h-full flex items-center justify-center col-span-1 border-r text-12">
                        ${quantity}
                    </div>
                    <div class="w-full h-full font-semibold flex items-center justify-center col-span-1 border-r text-12 total-cost">
                        ${total_cost}
                    </div>                
                </div>
            </div>
        `

        return row
        
    }
    



    

}



