

export default class Dynamic_Stock_Html {
    constructor(){
    }
    create_item_trends (trends_info) {
        let card = ''
        $.each (trends_info, (_, trend) => {
            if (_ < 5) {
                card += `
                    <div class="w-full">
                        <a href="/app/stock/items/?app=items&page=info&content_type=items&doc=${trend.item_name}" class="block w-full hover:bg-slate-400/5">
                            <div class="w-full h-full flex items-center justify-between border-b py-3">
                                <div class="flex items-center justify-start">
                                    <div class="ml-4">
                                        <h6 class="font-semibold text-gray-600">${trend.item_name}</h6>
                                        <small class="text-gray-600">Code: ${trend.item_code}</small>
                                    </div>
                                </div>
                                <div class="flex items-end justify-center flex-col">
                                    <h5 class="font-bold text-12 flex items-center justify-center">
                                        ${lite.defaults.company.reporting_currency} ${trend.total_sold}
                                    </h5>
                                    <div class="flex items-center justify-end text-10">
                                        <span class="material-symbols-outlined text-emerald-600 text-17 mr-1">
                                            trending_up
                                        </span>
                                        <span class="text-emerald-600 mr-1">+${trend.transactions_count}</span> : Past 10 Days
                                    </div>
                                </div>
                            </div>
                        </a>
                    </div>
                `
            }
        })
        return card
    }

    create_expiring_stock (expiring_stock) {
        let list = ''
        $.each (expiring_stock, (_, expiring) => {
            if (_ < 7) {
                list +=  `
                    <div class="w-full">
                        <div class="w-full h-full flex items-center justify-between border-b py-1">
                            <div class="flex items-center justify-start">
                                <div class="ml-4">
                                    <h6 class="font-semibold text-gray-600">${expiring.item_name}</h6>
                                    <small class="text-gray-600">Code: ${expiring.item_code}</small>
                                </div>
                            </div>
                            <div class="flex items-end justify-center flex-col">
                                <h5 class="font-bold text-12 flex items-center justify-center">
                                    ${lite.defaults.company.reporting_currency} ${expiring.current_value}
                                </h5>
                                <div class="flex items-center justify-end text-10">
                                    <span class="material-symbols-outlined text-emerald-600 text-17 mr-1">
                                        event
                                    </span>
                                    <span class="text-emerald-600 mr-1">${moment(expiring.item_expiry_date).format('Do MMM, YYYY')}</span> : ${expiring.days}
                                </div>
                            </div>
                        </div>
                    </div>
                `
            }
        })

        return list
    }

    create_dashboard_depleting_stock (stock_info) {
        let cards = ''
        $.each (stock_info, (_, depleting_stock) => {
            if (_ < 5) {
                cards += `
                    <div class="w-full flex items-end justify-between my-3">
                        <div class="w-[20px] text-orange-600 mr-2">
                            <span class="material-symbols-outlined text-13">
                                do_not_disturb_off
                            </span>
                        </div>
                        <div class="w-full flex items-center justify-center flex-col">
                            <div class="flex items-center justify-between  w-full">
                                <h5 class="font-semibold text-12">${depleting_stock.item}</h5>
                                <span class="text-default text-11 font-semibold">QTY: ${depleting_stock.quantity}</span>
                            </div>
                            <div class="w-full rounded-full h-[7px] bg-gray-300 mt-2 relative overflow-hidden">
                                <div class="w-[${depleting_stock.percentage}%] bg-orange-300 h-full rounded-full absolute left-0 top-0"></div>
                            </div>
                        </div>
                    </div>
                `
            }
        })
        return cards
    }

    side_view_items_list (items) {
        let list_row = ''
        $.each (items, (_, item) => {
            if (_ < 4) {
                list_row += `
                    <div class="border-b rounded-md">
                        <div class="h-full w-full grid grid-cols-7">
                            <div  class="col-span-5 flex justify-start items-center">
                                <h1 class="text-[13px] text-slate-700 truncate">${item.name}</h1>
                            </div>
                            <div  class="col-span-2 flex justify-end items-center">
                                <h1 class="text-[13px] text-slate-700 truncate">${item.sales}</h1>
                            </div>
                        </div>
                    </div>
                `
            }
        })

        return list_row
    }
    side_view_items_list2 (items) {
        let list_row = ''
        $.each (items, (_, item) => {
            if (_ < 4) {
                list_row += `
                    <div class="border-b rounded-md">
                        <div class="h-full w-full grid grid-cols-7">
                            <div  class="col-span-3 flex justify-start items-center">
                                <h1 class="text-[13px] text-slate-700 truncate">${item.name}</h1>
                            </div>
                            <div  class="col-span-2 flex justify-center items-center">
                                <h1 class="text-[13px] text-slate-700 font-semibold truncate">${item.qty}</h1>
                            </div>
                            <div  class="col-span-2 flex justify-end items-center">
                                <h1 class="text-[13px] text-slate-700 truncate">${item.value}</h1>
                            </div>
                        </div>
                    </div>
                `
            }
        })

        return list_row
    }

    create_dashboard_pending_stock_transfer (stock_info) {
        let cards = ''
        $.each (stock_info, (_, stock_transfer_info) => {
            console.log('====================================');
            console.log(stock_transfer_info);
            console.log('====================================');
            if (_ < 5) {
                cards += `
                    <div class="w-full flex items-center justify-between my-3">
                        <div class="w-[20px] text-orange-600 mr-2">
                            <span class="material-symbols-outlined text-18 text-default">
                                sync_alt
                            </span>
                        </div>
                        <div class="w-full flex items-center justify-center flex-col">
                            <div class="flex items-center justify-between text-13 w-full">
                                <div class="flex flex-col">
                                    <h5 class="font-semibold text-12">${stock_transfer_info.name}</h5>
                                    <small>Required By ${lite.utils.date_format_with_th_or_nd_and_rd (stock_transfer_info.by)}</small>
                                </div>
                                <span class="text-default text-11 font-semibold">QTY: ${stock_transfer_info.quantity}</span>
                            </div>
                        </div>
                        <button
                            class="flex items-center justify-center font-normal text-12 border w-[140px] rounded ml-5 btn h-[25px] shadow-none">
                            <span class="material-symbols-outlined text-15 mr-1 text-orange-700">
                                bottom_right_click
                            </span>
                            Open
                        </button>
                    </div>
                `
            }
        })
        return cards
    }

    transfers (data) {
        let list_item = ""
        $.each (data, (_, item) => {
            if (_ <= 17) {
                list_item += `
                    <div class="h-max-content py-2 text-[12px] border-t w-full grid grid-cols-11">
                        <span class="col-span-3 text-indigo-900 flex justify-start font-semibold items-center">${item.source_warehouse}</span>
                        <span class="col-span-3 flex justify-center items-center capitalize">${item.target_warehouse}</span>
                        <span class="col-span-3 flex justify-center items-center">${item.item_code}</span>
                        <span class="col-span-2 flex justify-end items-center font-semibold text-orange-600">${item.quantity_to_transfer}</span>
                    </div>
                `
            }
        })

        return list_item
    }

    stock_checks (data) {
        let list_item = ""
        $.each (data, (_, item) => {
            if (_ <= 17) {
                list_item += `
                    <div class="h-max-content py-2 text-[12px] border-t w-full grid grid-cols-11">
                        <span class="col-span-3 text-indigo-900 flex justify-start font-semibold items-center">${item.warehouse}</span>
                        <span class="col-span-3 flex justify-center items-center capitalize">${item.item}</span>
                        <span class="col-span-2 flex justify-center items-center">${item.quantity}</span>
                        <span class="col-span-2 flex justify-end items-center font-semibold text-orange-600">${item.physical_count_qyt}</span>
                    </div>
                `
            }
        })

        return list_item
    }

    inspection (data) {
        let list_item = ""
        $.each (data, (_, item) => {
            if (_ <= 17) {
                list_item += `
                    <div class="h-max-content py-2 text-[12px] border-t w-full grid grid-cols-11">
                        <span class="col-span-4 text-indigo-900 flex justify-start font-semibold items-center">${item.reference_name}</span>
                        <span class="col-span-3 flex justify-center items-center capitalize">${item.inspection_type}</span>
                        <span class="col-span-2 flex justify-center items-center">${item.item_code}</span>
                        <span class="col-span-2 flex justify-end items-center">
                            <span class="p-1 px-2 rounded-md text-[10px] bg-[${item.status_info.status_color}] text-[${item.status_info.inner_color}]">${item.status}</span>
                        </span>
                    </div>
                `
            }
        })

        return list_item
    }
}