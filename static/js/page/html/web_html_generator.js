
export default class Web_HTML_Generator{
    constructor(){
        this.icons = [
            ["monitoring","donut_small","add_chart"],
            ["settings","business_center","public"],
            ["spoke","tune","trending_up"],
            ["account_tree","insert_chart","finance_mode"],
            ["qr_code_scanner","planner_review","package_2"],
        ]
    }

    create_module_group(data, config,idx, freq){
        let modules = ""
        if(lite.utils.array_has_data(data?.modules)){
            $.each(lite.utils.ascend(data.modules, "id"),(_,mdl)=>{
                modules += `
                    <div class="w-full mb-4 grid grid-cols-7 border-b border-b-gray-400 border-dotted pb-3">
                        <div class="col-span-5 w-full">
                            <div class="flex flex-col">
                                <h5 class="">${mdl?.name}</h5>
                                <div>
                                <small module="${mdl?.name}" class="module-cost text-10 font-bold">${lite.utils.currency(mdl?.total_cost,2,config?.billing_currency || "ZMW")}</small> /
                                <small class="text-10 group-frequency">${freq}</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-span-2">
                            <button module="${mdl?.name}" class="add-remove-module-btn w-full h-[30px] text-[10px] flex items-center justify-center btn bg-default border-none shadow-none text-white">
                                <span class="material-symbols-outlined mr-1 text-10 group-add-icon"> add_task </span> 
                                <span class="add-remove-text">Add</span>
                            </button>
                        </div>
                    </div>
                `
            })
        }
        
        let group_wrapper = `
            <div group-name="${data?.name}" class="module-group w-full h-max-content min-h-[400px] bg-gray-300 rounded-md p-4 intro-y">
                <div class="w-[95%] h-full m-auto">
                    <div class="w-full h-[150px] flex items-center justify-center flex-col">
                        <h5 class="text-[18px] w-full font-bold">${data?.name}</h5>
                        <div class="flex items-center justify-center flex-col my-10">
                            <div class="flex items-start justify-center">
                                <small class="mt-1 mr-1 text-gray-800 font-bold">${config?.billing_currency || "ZMW"}</small>
                                <h1 class="text-[50px] my-3 font-black group-total">0.00</h1>
                            </div>
                            <span class="text-12 ml-5 group-frequency">${freq}</span>
                        </div>
                    </div>
                    <div class="text-12 mb-3">Select your suitable packages below</div>
                    <div class="grid grid-cols-3 w-[50%] mb-2">
                        <span class="material-symbols-outlined text-orange-600 text-20 w-[30px] h-[30px] rounded-md bg-white flex items-center justify-center"> ${this.icons[idx][0]} </span>
                        <span class="material-symbols-outlined text-indigo-600 text-20 w-[30px] h-[30px] rounded-md bg-white flex items-center justify-center"> ${this.icons[idx][1]} </span>
                        <span class="material-symbols-outlined text-teal-600 text-20 w-[30px] h-[30px] rounded-md bg-white flex items-center justify-center">   ${this.icons[idx][2]} </span>
                    </div>
                    <div class="w-full package-group-modules w-[80%] mx-auto mt-5">${modules}</div>
                </div>
            </div>
        `
        return group_wrapper
    }


    create_selected_module_card(data, config, freq){
        const color = lite.colors[Math.floor(Math.random() * lite.colors.length)]
        return `
            <div class="w-full flex items-start justify-between  text-[12px] lg:xl:text-[14px] py-3 border-b border-dotted transition duration-1000 hover:bg-gray-300 selected-module-card lg:xl:px-7 px-2 rounded-md cursor-pointer intro-x">
                <div class="flex items-start justify-start">
                    <div class="w-[30px] h-[30px] rounded-md bg-gray-200 border border-[${color}] text-white flex items-center justify-center mr-3">
                        
                    <span class="material-symbols-outlined text-[${color}]"> ${data.linked_fields.module?.icon} </span>
                    <!--<span class="material-symbols-outlined text-20"> check </span>-->
                    </div>
                    <div class="">
                        <h4 class="lg:xl:font-semibold  text-[12px] lg:xl:text-[14px]">${data?.name} Module</h4>
                        <span class="text-12 text-gray-500">${data?.module_group}</span>
                    </div>
                </div>
                <div class="flex items-center justify-end">
                    <div class="selected-module-price lg:xl:font-semibold  text-[12px] lg:xl:text-[14px]">
                        ${lite.utils.currency(data?.total_cost * freq,2, config?.billing_currency || "ZMW")}
                    </div>
                    <button module="${data?.name}" class="add-remove-module-btn remove-module flex items-center justify-center border-none bg-orange-600 text-white rounded-full w-[15px] h-[15px] ml-2">
                        <span class="material-symbols-outlined"> close </span>
                    </button>
                </div>
            </div>
        `
    }

}