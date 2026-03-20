
export default class ASSET_HTML_GENERATOR{
    constructor(){

    }



    // DASHBOARD CONTENT
    create_maintenance_team_dashboard(asset_maintenance){
        let cards = ''
        const colors = ['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(asset_maintenance,(_,value)=>{
            if(_ < 5)
                cards += `
                    <div class="h-[50px] w-full value-1">
                        <div class="h-full w-full grid grid-cols-12 p-3 gap-6">
                            <div class="h-full w-full flex items-center text-slate-700 col-span-4">
                                <div>
                                    <span class="material-symbols-outlined text-[20px] mr-2">
                                        reset_wrench
                                    </span>
                                </div>
                                <h1 class="truncate w-[100%]">
                                    ${value.category}
                                </h1>
                            </div>
                            <div class="h-full w-full items-center text-slate-600 col-span-4">
                                <span class="text-[13px] ${colors[_]} px-3 py-2 rounded-md flex justify-between">
                                    <div class="currency-asset"></div>
                                    ${value.avg_expense}
                                </span>
                            </div>
                            <div class="h-full w-full flex items-center text-slate-600 col-span-4 justify-between">
                                <div class="currency-asset">K </div>
                                ${value.total_expense}
                            </div>
                        </div>
                    </div>
                `
        })
        return cards
    }

    // DASHBOARD CONTENT
    create_insurance_dashboard(insurance_data){
        let cards = ''
        const colors = ['bg-indigo-100', 'bg-rose-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-current']
        $.each(insurance_data,(_,value)=>{
            if(_ < 5)
                cards += `
                    <div class="h-[50px] w-full value-1">
                        <div class="h-full w-full grid grid-cols-12 p-3 gap-6">
                            <div class="h-full w-full flex items-center text-slate-700 col-span-8">
                                <div>
                                    <span class="material-symbols-outlined text-[20px] mr-2">
                                        health_and_safety
                                    </span>
                                </div>
                                <h1 class="truncate w-[100%]">
                                    ${value.category}
                                </h1>
                            </div>
                            <div class="h-full w-full flex items-center text-slate-600 col-span-4 justify-between">
                                <div class="currency-asset">K </div>
                                ${value.total_expense}
                            </div>
                        </div>
                    </div>
                `
        })
        return cards
    }

    create_category_side_view_upper(data){
        let cards = ''
        const colors = ['bg-indigo-100', 'bg-emerald-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-[#f683ae]']
        $.each(data,(_,value)=>{
            if(_ < 3)
                cards += `
                    <div class="max-h-full flex flex-col justify-even text-3">
                        <div class="bg-white">
                            <div class="h-full grid grid-cols-3 p-2">
                                <div class="h-full col-span-2 flex items-center gap-2">
                                    <span class="item-img w-10 h-8 ${colors[_]} rounded-full material-symbols-outlined text-5 flex items-center justify-center text-black-800">
                                        real_estate_agent
                                    </span>
                                    <div class="details font-normal w-[80%] truncate overflow-ellipsis">${value.name}</div>
                                </div>
                                <div class="h-full col-span-1 flex justify-end items-center">
                                    <strong class="flex text-2 ">${value.data.asset_category_qty}</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                `
        })
        return cards
    }

    create_category_side_view_lower(data){
        let cards = ''
        const colors = ['bg-indigo-100', 'bg-emerald-100', 'bg-orange-100', 'bg-emerald-100', 'bg-purple-100', 'bg-[#f683ae]']
        $.each(data,(_,value)=>{
            if(_ < 3)
                cards += `
                    <div class="max-h-full flex flex-col  justify-even text-3">
                        <div class="bg-white">
                            <div class="h-full grid grid-cols-4 p-2">
                                <div class="h-full col-span-2 flex items-center gap-2">
                                    <span class="item-img w-10 h-8 ${colors[_]} rounded-full material-symbols-outlined text-5 flex items-center justify-center text-black-800">
                                        real_estate_agent
                                    </span>
                                    <div class="details w-[50%] truncate overflow-ellipsis">${value.name}</div>
                                </div>
                                <div class="h-full w-full col-span-2 flex justify-center items-center">
                                    <span class="flex justify-end text-1">${value.currency}</span>
                                    <strong class="flex text-1 mt-1 justify-end w-[100%] font-semi-bold">${value.data.asset_category_cost}</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                `
        })
        return cards
    }

    // ASSET INFO UPPER
    create_asset_info_upper_side_view_maintenance(cate){
        let cards = ''
        $.each(cate,(_,cate)=>{
            if(_ < 4)
                cards += `
                <div class="col-span-2 text-6 font-medium p-2 place-content-center truncate w[50%]">
                    Task
                </div>
                <div class="grid col-span-2 text-6 font-medium p-2 place-content-center truncate w[50%] rounded-lg bg-green-100">Status</div>
                <div class="grid col-span-2 text-6 font-medium p-2 place-content-center  place-content-end truncate w[50%]">ZMW 30,000</div>
                `
        })
        return cards
    }
    create_asset_info_upper_side_view_insurance(cate){
        let cards = ''
        $.each(cate,(_,cate)=>{
            if(_ < 4)
                cards += `
                
                    <div class="col-span-2 text-6 font-medium p-2 place-content-center truncate w[50%]">
                    insurance company
                    </div>
                    <div class="grid col-span-2 text-6 font-medium p-2 place-content-center truncate w[50%] rounded-lg bg-blue-100">Status</div>
                    <div class="grid col-span-2 text-6 font-medium p-2 place-content-center  place-content-end truncate w[50%]">ZMW 30,000</div>
                `
        })
        return cards
    }

    create_asset_entry(data){
        let assets = ''
        $.each(data,(index,value)=>{
            if(index <=6){
                assets += `
                <div class="col-span-2 text-6 font-medium p-2 place-content-center truncate w[50%]">
                    ${value.task}
                </div>
                <div class="grid col-span-2 text-6 font-medium p-2 place-content-center truncate w[50%] rounded-lg bg-green-100">
                    ${value.status}
                </div>
                <div class="grid col-span-2 text-6 font-medium p-2 place-content-center  place-content-end truncate w[50%]">
                    ${value.cost}
                </div>
`
            }
        })
        return assets
    }

    // ASSET INFO LOWER
    create_asset_info_lower_side_view(cate){
        let cards = ''
        $.each(cate,(_,cate)=>{
            if(_ < 4)
                cards += `
                <div class="rounded-lg grid row-span-1 grid-cols-6 gap-1 place-content-center h-min">
                    <span class="material-symbols-outlined rounded-lg grid col-span-1 place-content-center text-12 text-blue-700 font-thin">
                        real_estate_agent
                    </span>
                    <div class="grid col-span-2 truncate text-clip"><p class="text-ellipsis overflow-hidden ...">${cate.category}</p></div>
                    <div class="grid col-span-3 w-full rounded-lg place-content-end">${cate.currency} ${lite.utils.thousand_separator(cate.amount)}</div>
                </div>
                `
        })
        return cards
    }
}



