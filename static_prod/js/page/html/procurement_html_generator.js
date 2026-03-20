export default class Procurement_HTML_Generator{
    constructor(){

    }

    create_monthly_expenditure(expenditure){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(expenditure,(_,value)=>{
            if(_ < expenditure.length){
                cards += `
                    <div class="w-full flex justify-between mb-3">
                        <div class="p-2 bg-blue-100 rounded-full"><h2>${value.month}</h2></div>
                        <div class="rounded-full bg-slate-100 p-2"><strong>${value.expense}</strong></div>
                        <div class="text-xs rounded-full reporting_currency text-default p-2"><h5></h5></div>
                    </div>                    
                `
            }
        })
        return cards
    }

    create_department_expenditure(expenditure){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(expenditure,(_,value)=>{
            if(_ < expenditure.length){
                cards += `
                    <div class="w-full flex justify-between mb-3">
                        <div class="p-2 bg-green-100 rounded-full"><h2>${value.department}</h2></div>
                        <div class="rounded-full bg-slate-100 p-2"><strong>${value.expense}</strong></div>
                        <div class="text-xs rounded-full reporting_currency text-default p-2"><h5>k</h5></div>
                    </div>                  
                `
            }
        })
        return cards
    }

    create_savings_trackor(expenditure){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(expenditure,(_,value)=>{
            if(_ < expenditure.length){
                cards += `
                    <div class="w-full flex justify-between mb-3">
                        <div class="p-2 bg-green-100 rounded-full"><h2>${value.department}</h2></div>
                        <div class="rounded-full bg-slate-100 p-2"><strong>${value.expense}</strong></div>
                        <div class="text-xs rounded-full reporting_currency text-default p-2"><h5>k</h5></div>
                    </div>                  
                `
            }
        })
        return cards
    }

    requisition_side_views(req_status){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(req_status,(_,value)=>{
            if(_ < req_status.length){
                cards += `
                    <div class="w-full my-8 flex items-center justify-between">
                        <div class="flex flex-col">
                            <span class="font-semibold flex items-center justify-start">
                                <span class="material-symbols-outlined text-[14px] mr-1 text-orange-600">
                                    {draft_orders}
                                </span>
                                ${_}
                            </span>
                            <small class="text-slate-500 ml-5 w-[90%]">
                                ${Requisition}
                            </small>
                        </div>
                        <div class="total-drafted-req rounded-full bg-gray-200 px-2 h-[30px] flex items-center justify-center text-[12px]">
                            ${0}
                        </div>
                    </div>                
                `
            }
        })
        return cards
    }

    create_procurement_monthly_expenditure(expenditure){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(expenditure,(_,value)=>{
            if(_ < expenditure.length){
                cards += `
                    <div class="w-full flex justify-between mb-3">
                        <div class="p-2 bg-blue-100 rounded"><h2>${value.month}</h2></div>
                        <div class="rounded bg-slate-100 p-2"><strong>${value.spent}</strong></div>
                        <div class="text-xs rounded reporting_currency text-default p-2"><h5></h5></div>
                    </div>                
                `
            }
        })
        return cards
    }

    create_procurement_monthly_savings(expenditure){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(expenditure,(_,value)=>{
            if(_ < expenditure.length){
                cards += `
                    <div class="w-full flex justify-between mb-3">
                        <div class="p-2 bg-purple-100 rounded-full"><h2>${value.month}</h2></div>
                        <div class="rounded-full bg-slate-100 p-2"><strong>${value.savings}</strong></div>
                        <div class="text-xs rounded-full reporting_currency p-2"><h5>k</h5></div>
                    </div>             
                `
            }
        })
        return cards
    }

    create_supplier_performanace(expenditure){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(expenditure,(_,value)=>{
            if(_ < expenditure.length){
                cards += `
                    <tr class="" >
                        <td class="py-3 px-2">${value.supplier}</td>
                        <td class="py-3 px-2">${value.sup_transactions}</td>
                        <td class="py-3 px-2">${value.score}</td>
                        <td class="py-3 px-2">${value.percentage}</td>
                    </tr>           
                `
            }
        })
        return cards
    }

    create_bid_evalution_top_sv(expenditure){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(expenditure,(_,value)=>{
            if(_ < expenditure.length){
                cards += `
                <div class="w-full rounded-lg bg-teal-100 text-green-900 mt-2">
                    <h4 class="font-semibold w-full text-center">${value.supplier}</h4>
                    <div class="flex justify-between p-1">
                        <span>Score: <strong class="">${value.score}</strong></span>
                        <span>Supplyable items: <strong class="">${value.supplyable} %</strong></span>
                    </div>
                </div>        
                `
            }
        })
        return cards
    }

    create_bid_evalution_bottom_sv(expenditure){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(expenditure,(_,value)=>{
            if(_ < expenditure.length){
                cards += `
                 <div class="w-full rounded-lg bg-slate-300 text-stone-900 mt-2">
                    <h4 class="font-semibold w-full text-center">${value.bid}</h4>
                    <div class="flex justify-between p-1 flex-wrap py-1">
                            <span><strong class="">${value.supplier1}</strong>: ${value.supplier1_score}<small> score</small></span>
                            <span><strong class="">${value.supplier2}</strong>: ${value.supplier2_score}<small> score</small></span> 
                            <span><strong class="">${value.supplier3}</strong>: ${value.supplier3_score}<small> score</small></span>
                    </div>   
                </div>     
                `
            }
        })
        return cards
    }

    create_inventory_table(items){
        let cards = ''
        // const colors =['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(items,(_,value)=>{
            if(_ < 4){
                cards += `
                    <div class="h-[4rem] grid grid-cols-7 p-4 content-center">
                        <div class="col-span-1 text-center">${_}</div>
                        <div class="col-span-2 text-center">${value.name}</div>
                        <div class="col-span-2 text-center">${value.cost}</div>
                        <div class="col-span-2 text-center">${value.inventory_type}</div>  
                    </div> 
                `
            }
        })
        return cards
    }



    display_budget_distribution(items, freq,){
        let cards = ''
        let grid_col
        let grid_rows
        if (freq =="Quoterly"){
            grid_col =2
            grid_rows =2
        }
        $.each(items,(_,value)=>{
            console.log(value, freq);
            
            if(_ < 4){
                cards += `                  
                    <div class="row-span-1 col-span-1 rounded-lg content-center bg-theme_text_color text-default w-full h-full text-center">${value}<small id="till-1">${freq}_${_}</small></div>
                `
            }
        })
        return `
            <div class="w-full h-full grid grid-col-${grid_col} grid-rows-${grid_rows} gap-4 bg-theme_text_color">
                ${cards}
            </div>
        `
    }
}
