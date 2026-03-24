export default class Smart_Invoice_HTML_Generator{
    constructor(){

    }

    create_unsubmitted_invoice_row(sn, data){
        return `
            <a href="/app/smart_invoice/si_receivable?loc=si_receivable&type=info&document=Tax Invoice&doc=${data?.id}">
                <div class="w-full h-[30px] rounded-t-md grid grid grid-cols-15 gap-x text-11 border-b intro-y">
                    <div class="w-full h-full flex items-center justify-center">${sn}</div>
                    <div class="w-full h-full flex items-center ml-5 justify-start col-span-3 truncate overflow-ellipsis">
                        ${data?.custNm}
                    </div>
                    <div class="w-full h-full flex items-center ml-5 justify-start col-span-2 truncate overflow-ellipsis">
                        ${data?.name}
                    </div>
                    <div class="w-full h-full flex items-center ml-5 justify-start col-span-2 truncate overflow-ellipsis">
                        ${lite.utils.thousand_separator(data?.totItemCnt)}
                    </div>
                    <div class="w-full h-full flex items-center ml-5 justify-start col-span-2 truncate overflow-ellipsis">
                        ${lite.utils.thousand_separator(data?.totTaxAmt)}
                    </div>
                    <div class="w-full h-full flex items-center ml-5 justify-start col-span-2 truncate overflow-ellipsis">
                        ${lite.utils.thousand_separator(data?.totItemCnt)}
                    </div>
                    
                    <div class="w-full h-full flex items-center ml-5 col-span-3 justify-start">
                        ${data?.status}
                    </div>
                </div>
            </a>
        `
    }

    create_unregistered_customer_list(data){
        let cards =''
        $.each(data,(_,value)=>{
            if (_ < 3){
                cards +=`
                    <div class="w-full flex items-center justify-between border-b border-dotted min-h-[30px]">
                        <div class="flex items-center justify-start py-2">
                            <a href="/app/smart_invoice/si_receivable?loc=si_receivable&type=info&document=Customer&doc=${value?.id}" class="flex items-center justify-start">
                                <div class="w-[27px] h-[27px] rounded-md bg-indigo-200  flex items-center justify-center mr-2">
                                    <span class="material-symbols-outlined text-20"> assignment_ind </span>
                                </div>
                                <div class="flex flex-col">
                                    <span class="text-13">${value?.name}</span>
                                    <small class="text-gray-400 text-10">Contact eamil ${value?.email}</small>
                                </div>
                            </a>
                        </div>
                        <button data-id="${value.name}" data-doctype="${value.doctype}" class="text-6 text-default register-btn font-semibold text-[10px] border-1 rounded-md"> Register Customer </button>
                    </div>
                `
            }
        })
        return cards
    }

    create_unregistered_items_list(item_data){
        let cards =''
        $.each(item_data,(_,value)=>{
            if (_ < 3){
                cards +=`
                    <div class="w-full flex items-center justify-between border-b border-dotted min-h-[30px]">
                        <div class="flex items-center justify-start py-2">
                            <a href="/app/smart_invoice/si_item?loc=si_item&type=info&document=Items&doc=${value?.id}" class="flex items-center justify-start">
                                <div class="w-[27px] h-[27px] rounded-md bg-purple-200 flex items-center justify-center mr-2">
                                    <span class="material-symbols-outlined text-20"> shopping_bag </span>
                                </div>
                                <div class="flex flex-col">
                                    <span class="text-13">${value?.name} </span>
                                    <small class="text-gray-400 text-10">Created on ${value.created_on}</small>
                                </div>
                            </a>
                        </div>
                        <button data-id="${value.name}" data-doctype="${value.doctype}" class="text-2 text-purple-800 register-btn font-semibold text-[10px] border-1 rounded-md">Register Item </button>
                    </div>
                `
            }
        })
        return cards
    }
}