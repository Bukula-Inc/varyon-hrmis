
export default class Accounting_HTML_Generator{
    constructor(){
        
    }



    // DASHBOARD CONTENT
    create_dashboard_bank_summary_cards(banking_info){
        let cards = ''
        $.each(banking_info,(_,bi)=>{
            if(_ < 3)
                cards += `
                    <div class="flex items-center justify-between mb-1  intro-x">
                        <div class="flex items-start justify-start mt-2">
                            <div class="flex items-center justify-center bg-default/30 rounded-full p-1 mr-1">
                                <span class="material-symbols-outlined text-13 text-default"> credit_card </span>
                            </div>
                            <span class="flex flex-col text-12 truncate overflow-ellipsis">${bi.account_name}<small class="text-gray-600 text-10"> (${bi.parent})</small></span>
                        </div>
                        <span class="font-semibold text-12">${lite.utils.currency(bi.balance, lite.system_settings.currency_decimals,bi.currency)}</span>
                    </div>
                `
        })
        return cards
    }
    

    create_dashboard_bank_summary_empty_content_card($wrapper){
        lite.utils.add_empty_component({$wrapper: $wrapper, text:"No Banks Found.",classnames:"h-full mt-5"})
        $wrapper.append(`
            <div class="flex items-center justify-center flex-col mt-5">
                <a href="/app/accounting/banking/?loc=banking&type=new&document=Bank%20Account" class="border border-indigo-300 px-2 py-1 rounded-md text-12 flex items-center justify-center btn">
                    New Bank Account 
                    <span class="material-symbols-outlined ml-2"> east </span>
                </a>
            </div>
        `)
    }

    generate_bank_accounts_list(bank_accounts){
        const $wrapper =  $('.bank-account-selector')
        if(!lite.utils.is_empty_array(bank_accounts)){
           $wrapper.empty()
            $.each(bank_accounts,(_,ba)=>{
                if(!lite.utils.is_empty_array(ba.bank_account)){
                    $.each(ba.bank_account,(__,acc)=>{
                        acc.logo = ba.logo
                        $wrapper.append(this.#create_bank_account_row(acc))
                    })
                }
            })
        }
    }
    
    #create_bank_account_row(bank_account){
        let selected_accounts = []
        let is_selected = false
        const form_accounts = lite.form_data?.bank_accounts
        if(form_accounts && !lite.utils.is_empty_array(form_accounts)){
            $.each(form_accounts,(_,fa)=>{
                selected_accounts.push(fa.account_no)
            })
            is_selected = selected_accounts.includes(bank_account?.account_no)
        }
        return `
            <div class="w-full my-8 flex items-start justify-between intro-y">
                <div class="flex items-start justify-center">
                    <div class="flex items-center justify-center mr-1 grayscale">
                        <img src="${bank_account.logo || '/static/images/others/default-bank.png'}" class="w-[30px] h-[30px] rounded-full object-cover" alt="">
                    </div>
                    <div class="flex flex-col">
                        <span class="font-semibold">${bank_account.account_name}</span>
                        <small class="text-slate-500 text-12">
                            ${bank_account?.parent || '-'} <small class="font-semibold">(${bank_account.currency})</small>
                        </small>
                        <small class="text-slate-500 text-12">
                            ${bank_account?.account_no || '-'}
                        </small>
                    </div>
                </div>
                <button 
                    account-id="${bank_account.id}"
                    account-name="${bank_account.account_name}" 
                    bank="${bank_account.parent}" 
                    added="${is_selected}"
                    class="bank-account-selector-btn ${is_selected ? 'border-default border-3 bg-orange-500 text-white' : ''} w-[70px] h-[30px] border border-secondary_color/50 shadow-none flex items-center justify-center text-[12px] btn">
                        Select <span class="added-el ${is_selected ? '' : 'hidden'} material-symbols-outlined text-17"> done_all </span>
                </button>
            </div>
        `
    }
    create_invoice_bank_account_content(accounts, accs){
        let account_content = ''
        $('.bank-accounts-wrapper')?.empty()
        if(!lite.utils.is_empty_array(accounts)){
            let added_banks = []
            $.each(accounts,(_,acc)=>{
                added_banks.push(acc.bank?.value)
                let account_nos = `
                    <div class="w-full flex items-center justify-between mb-2 intro-x">
                        <span class="font-semibold">Account No</span>
                        <span class="font-semibold">${acc.account_no?.value || "-"}</span>
                    </div>
                `
                $.each(accounts,(__,_acc)=>{
                    if(_acc?.bank?.value === acc.bank?.value && _acc?.account_no?.value !== acc?.account_no?.value){
                        account_nos += `
                            <div class="w-full flex items-center justify-between mb-2 intro-x">
                                <span class="font-semibold">Account No</span>
                                <span class="font-semibold">${acc.account_no?.value || "-"}</span>
                            </div>
                        `
                    }
                })
                account_content += `
                    <div class="w-full flex items-center justify-between mb-2 intro-x">
                        <span class="font-semibold">Bank</span>
                        <span class="font-semibold">${acc.bank?.value || "-"}</span>
                    </div>
                    <div class="w-full flex items-center justify-between mb-2 intro-x">
                        <span class="font-semibold">Account Name</span>
                        <span class="font-semibold">${acc.bank_account?.value || "-"}</span>
                    </div>
                    <div class="w-full flex items-center justify-between mb-2 intro-x">
                        <span class="font-semibold">Branch Code</span>
                        <span class="font-semibold">${acc.branch_code?.value || "-"}</span>
                    </div>
                    ${account_nos}
                    <div class="w-full flex items-center justify-between mb-2 intro-x">
                        <span class="font-semibold">Swift</span>
                        <span class="font-semibold">${acc.swift?.value || "-"}</span>
                    </div>
                    <div class="w-full flex items-center justify-between mb-2 intro-x">
                        <span class="font-semibold">Currency</span>
                        <span class="font-semibold">${acc?.currency?.value || "-"}</span>
                    </div>
                    `
                })
        }
        $('.bank-accounts-wrapper').html(account_content)
    }






    // banking
    generate_bank_details(bank){
        return `
            <div class="w-full flex items-center justify-between border rounded-md border-gray-150 p-2 my-1 intro-x hover:bg-gray-100 transition duration-1000">
                <a href="/app/accounting/banking/?loc=banking&type=info&document=Bank%20Account&doc=${bank.id}" bank-id="${bank.id}" class="flex w-full cursor-pointer items-center justify-start">
                    <div class="rounded-full border border-secondary_color/50 border w-[30px] h-[30px] flex items-center justify-center">
                    ${
                        bank.logo ? `<img src="${bank.logo}" class="w-full h-full rounded-full object-cover" alt="">` :
                        '<span class="material-symbols-outlined text-14 text-indigo-900">account_balance</span>'
                    }
                    </div>
                    <div class="ml-3 flex flex-col">
                        <span class="font-semibold text-gray-600 text-13">${bank.name}</span>
                        <small class="text-gray-500">${bank.bank_account?.length} Account${bank.bank_account?.length > 1 ? "s" :""}</small>
                    </div>
                </a>
                <div class="flex items-center justify-end">
                    <div class="dropdown w-[300px] sm:w-auto" style="position: relative;">
                        <div class="h-full border-l">
                            <button class="bank-drop-down-toggler dropdown-toggle border-none ml-4 btn  shadow-none btn-outline-secondary w-full sm:w-auto" aria-expanded="false" data-tw-toggle="dropdown">
                                <span class="material-symbols-outlined text-25">more_vert</span>
                            </button>
                        </div>
                        <div class="dropdown-menu w-[200px]" id="_hjlc5luf1" data-popper-placement="bottom-end"
                            style="position: absolute; inset: 0px 0px auto auto; margin: 0px; transform: translate3d(-0.5px, 38px, 0px);">
                            <ul  class="dropdown-content w-[300px]">
                                <!--<li>
                                    <a action="download_statement" bank-id="${bank.id}" class="dropdown-item bank-drop-down-item">
                                        <span class="material-symbols-outlined text-16 mr-1 text-indigo-600"> download </span>
                                        Download Statement
                                    </a>
                                </li>-->
                                <li>
                                    <a action="edit_bank" bank-id="${bank.id}" class="dropdown-item bank-drop-down-item">
                                        <span class="material-symbols-outlined text-16 mr-1 text-blue-600"> edit_square </span>
                                        Edit Bank
                                    </a>
                                </li>
                                <li>
                                    <a action="delete_bank" bank-id="${bank.id}" class="dropdown-item bank-drop-down-item">
                                        <span class="material-symbols-outlined text-16 mr-1 text-orange-600"> delete </span>
                                        Delete Bank
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `
    }

    generate_bank_account(bank_account){
        return `
            <div id="${bank_account.id}" class="w-full flex items-center justify-between border border-gray-150 rounded-md p-2 my-1 intro-y">
                <div class="flex items-start justify-start">
                    <div class="text-gray-600">
                        <span class="material-symbols-outlined text-[14px] tex-orange-600">credit_score</span>
                    </div>
                    <div class="ml-2 flex flex-col">
                        <span class="font-normal text-gray-600 text-13">${bank_account.account_name}</span>
                        <small class="text-gray-500 text-10">${bank_account.parent}</small>
                        <small class="text-gray-500 text-10">${bank_account.account_no} (${bank_account.currency})</small>
                    </div>
                </div>
                <div class="flex items-center justify-end">
                    <div class="font-bold text-[12px] mr-5 pr-5 border-r h-full flex items-end justify-end flex-col">
                        <h5 class="${bank_account.balance <= 0 ? "text-orange-700":"text-default"}">${lite.utils.thousand_separator(bank_account.balance)}</h5>
                        <small class="text-gray-500 font-normal">Balance</small>
                    </div>
                </div>
            </div>
        `
    }

    generate_bank_transaction_filters(){
        return `
            <select id="transaction-current-account" value="" type="link" for="Bank_Account" linkfield="name" fieldname="transaction_account" class="lite-selector font-semibold border border-orange-400 border-[1px] border-dotted bg-orange-50 rounded-md px-3 w-[230px] mr-2" placeholder="Select Account"></select>
            <select id="bank-transaction-branch" value="" type="link" for="Branch" linkfield="name" fieldname="transaction_branch" class="lite-selector font-semibold border border-indigo-400 border-[1px] border-dotted bg-indigo-100 rounded-md px-3 w-[230px] mr-2" placeholder="Select Branch"></select>
            <select type="select"  fieldname="document_status" class="lite-selector border border-default/600 border-[1px] border-dotted bg-orange-100 rounded-md px-3 w-[230px] mr-2" placeholder="Filter By Status">
                <option value="Draft/Unsubmitted">Draft/Unsubmitted</option>
                <option value="Approved/Submitted">Approved/Submitted</option>
                <option value="Rejected/Reversed">Rejected/Reversed</option>
            </select>
        `
    }

    add_transaction_loader($wrapper,text){
        $wrapper.html(`
        <div class="h-[40vh] flex items-center justify-center flex-col w-full font-semibold text-gray-600">
            ${lite.utils.generate_loader({loader_type:"dots",size:20})}
            ${text}
        </div>
        `)
    }
    add_transaction_empty_content($wrapper,text){
        lite.utils.add_empty_component({$wrapper:$wrapper,text:text,classnames:"text-gray-400 empty-transactions"})
    }









    // ===========================================================TRADING HTMLS =========================================
    create_top_customer_card(data, currency, classnames){
        return `
                <a href="/app/accounting/trading/?loc=trading&type=info&document=customer&doc=${data.customer}" class="w-full transition duration-1000 hover:scale-[1.1] mb-1 flex items-start justify-start ${classnames || "bg-gray-100"}  p-1 rounded-md">
                <div class="flex items-center justify-center rounded-full bg-gray-200 border border-default w-[30px] h-[30px]">
                    <img src="/media/defaults/avatas/dp.jpeg" class="w-full h-full rounded-full object-cover object-top" alt="">
                </div>
                <div class="flex items-start flex-col ml-3 overflow-ellipsis truncate">
                    <span class="font-bold text-11">${data.customer}</span>
                    <span class="text-10 text-gray-600">${lite.utils.currency(data.total_sales,lite.currency_decimals, currency)} Total Sales</span>
                </div>
            </a>
        `
    }
    create_new_customer_card(data){
        return `
            <a href="/app/accounting/trading/?loc=trading&type=info&document=Customer&doc=${data?.id}" class="w-[40px] h-[40px] rounded-full border p-[0.5px] new-trader shadow-darker cursor-pointer">
                <img src="${data?.customer_logo || "/media/defaults/avatas/dp.jpeg"}" alt="" class="w-full h-full object-cover rounded-full">
            </a>
        `
    }
    create_new_customer_plus_card(total_new){
        return `
            <div class="w-[40px] h-[40px] flex items-center justify-center rounded-full border p-[0.5px] new-trader shadow-darker cursor-pointer bg-indigo-800 text-white text-12 font-bold">
                ${total_new}+
            </div>
        `
    }


    create_top_supplier_card(data,currency, classnames){
        return `
                <a href="/app/accounting/trading/?loc=trading&type=info&document=supplier&doc=${data.supplier}" class="w-full transition duration-1000 hover:scale-[1.1] mb-1 flex items-start justify-start ${classnames || "bg-gray-100"}  p-1 rounded-md">
                <div class="flex items-center justify-center rounded-full bg-gray-200 border border-default w-[30px] h-[30px]">
                    <img src="/media/defaults/avatas/dp.jpeg" class="w-full h-full rounded-full object-cover object-top" alt="">
                </div>
                <div class="flex items-start flex-col ml-3 overflow-ellipsis truncate">
                    <span class="font-bold text-11">${data.supplier}</span>
                    <span class="text-10 text-gray-600">${lite.utils.currency(data.total_sales,lite.currency_decimals, currency)} Total Purchases</span>
                </div>
            </a>
        `
    }
    create_new_supplier_card(data){
        return `
            <a href="/app/accounting/trading/?loc=trading&type=info&document=supplier&doc=${data?.id}" class="w-[40px] h-[40px] rounded-full border p-[0.5px] new-trader shadow-darker cursor-pointer">
                <img src="${data?.supplier_logo || "/media/defaults/avatas/dp.jpeg"}" alt="" class="w-full h-full object-cover rounded-full">
            </a>
        `
    }
    create_new_supplier_plus_card(total_new){
        return `
            <div class="w-[40px] h-[40px] flex items-center justify-center rounded-full border p-[0.5px] new-trader shadow-darker cursor-pointer bg-indigo-800 text-white text-12 font-bold">
                ${total_new}+
            </div>
        `
    }



    // RECEIVABLES AND PAYABLES DASHBOARD
    create_receivable_top_customer_card(data,currency){
        return `
            <a href="/app/accounting/trading/?loc=trading&type=info&document=customer&doc=${data.customer}" class="intro-y w-full flex items-center justify-start bg-gray-100 border border-dotted border-gray-300 p-1 rounded-md transition duration-1000 hover:bg-gray-300">
                <div class="flex items-center justify-center rounded-full bg-gray-200 border border-default w-[30px] h-[30px]">
                    <img src="/media/defaults/avatas/dp.jpeg" class="w-full h-full rounded-full object-cover object-top" alt="">
                </div>
                <div class="flex items-start flex-col ml-3">
                    <span class="font-bold text-11">${data.customer}</span>
                    <span class="text-10 text-gray-600">${lite.utils.currency(data.total_sales,lite.currency_decimals, currency)} Sales</span>
                </div>
            </a>
        `
    }
    
    create_receivable_top_supplier_card(data,currency){
        return `
            <a href="/app/accounting/trading/?loc=trading&type=info&document=supplier&doc=${data.supplier}" class="intro-y w-full flex items-center justify-start bg-gray-100 border border-dotted border-gray-300 p-1 rounded-md transition duration-1000 hover:bg-gray-300">
                <div class="flex items-center justify-center rounded-full bg-gray-200 border border-default w-[30px] h-[30px]">
                    <img src="/media/defaults/avatas/dp.jpeg" class="w-full h-full rounded-full object-cover object-top" alt="">
                </div>
                <div class="flex items-start flex-col ml-3">
                    <span class="font-bold text-11">${data.supplier}</span>
                    <span class="text-10 text-gray-600">${lite.utils.currency(data.total_sales,lite.currency_decimals, currency)} Purchases</span>
                </div>
            </a>
        `
    }

    create_invoice_due_in_7_days_card(invoice){
        return `
            <a href="/app/accounting/receivables/?loc=receivables&type=info&document=tax%20invoice&doc=${invoice.name}" class="intro-y w-full flex items-center justify-between">
                <div class="flex items-center justify-start">
                    <div class="flex items-center justify-center bg-orange-100 border border-orange-600 rounded-full w-[30px] h-[30px]">
                        <span class="material-symbols-outlined text-18 text-orange-600"> receipt_long </span>
                    </div>
                    <div class="flex-col ml-2">
                        <h4 class="font-bold text-11">${invoice.name}</h4>
                        <small class="text-orange-700 text-11">Due On ${lite.utils.convert_date(invoice.due_date)}</small>
                    </div>
                </div>
                <div>
                    <small class="text-10 font-bold">${lite.utils.currency(invoice.base_total_outstanding_amount,lite.utils.currency_decimals,invoice.currency)}</small>
                </div>
            </a>
        `
    }



    // ACCOUNTING IMPORTATION SCRIPTS
    create_importation_column_header(cols){
        const total_cols = (cols.length * 2) + 1
        let col_header = `
            <div class="grid grid-cols-${total_cols} w-full min-h-[30px] text-12 bg-default text-theme_text_color rounded-t-md" >
                <div class="text-center flex items-center justify-center border-r-theme_text_color border-r border-r-default border-dotted">S/N</div>
        `
        $.each(cols,(_,rw)=>{
            col_header += `<div class="text-center flex items-center justify-center col-span-2 px-2 border-r-theme_text_color border-r border-dotted">${lite.utils.capitalize(lite.utils.replace_chars(rw,"_"," "))}</div>`
        })

        return col_header + "</div>"
    }

    create_importation_body(rows, cols){
        const total_cols = (cols.length * 2) + 1
        let row_data = ``
        $.each(rows,(_,rw)=>{
            row_data += `
                <div class="grid grid-cols-${total_cols} w-full min-h-[30px] text-13  rounded-t-md border-b border-dotted border-b-dotted" >
                <div class="flex items-center justify-center border-r border-dotted border-r-default font-bold bg-default/10">${lite.utils.thousand_separator(_+1,0)}</div>
            `
            $.each(cols,(_,cl)=>{
                const has_error = rw?.errors[cl]
                row_data += `<div class="flex items-start justify-start flex-col col-span-2 border-r border-dotted px-2 ${has_error ? 'border border-red-700 bg-red-100' : 'bg-default/10 border-r-default'}">
                <span> ${rw[cl] || "-"} </span>
                <small class="text-red-700">${rw?.errors[cl] || ""}</small>
                </div>`
            })
            row_data += "</div>"
        })

        return `<div class="w-full h-[55vh] overflow-hidden overflow-y-auto rounded-md">${row_data}</div>`
    }
    
   
}