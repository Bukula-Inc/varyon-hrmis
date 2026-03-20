import { color_codes } from "../../constants/colors.js"

export default class Core_HTML_Generator{
    constructor(){
        this.color_codes = color_codes
    }

    // core dashboard
    create_sector_row(data){
        return `
            <div class="w-full flex items-start justify-start mb-4 intro-y hover:translate-x-[-3%] hover:text-purple-700">
                <span class="material-symbols-outlined mr-2 text-purple-800 text-16"> work </span>
                <a href="/app/core/sector/?app=sector&page=info&content_type=Sector&doc=${data?.id}" class="overflow-ellipsis truncate">${data.name}</a>
            </div>
        `
    }
    create_industry_row(data){
        return `
            <div class="w-full flex items-start justify-start mb-4 intro-y hover:translate-x-[-3%] hover:text-purple-700">
                <span class="material-symbols-outlined mr-2 text-emerald-800 text-16"> business_center </span>
                <a href="/app/core/industry/?app=industry&page=info&content_type=Industry&doc=${data?.id}" class="overflow-ellipsis truncate">${data.name}</a>
            </div>
        `
    }

    create_user_role_row(data){
        return `
            <div class="flex items-start justify-start intro-y">
                <span class="material-symbols-outlined text-17 mr-2 text-default"> admin_panel_settings </span>
                <a href="/app/core/role/?app=core&page=info&content_type=Role&doc=${data?.id}" class="hover:text-default">${data.name}</a>
            </div>
        `
    }
    create_workflow_row(data){
        return `
            <div class="flex items-start justify-start intro-y">
                <span class="material-symbols-outlined text-17 mr-2 text-orange-500"> hub </span>
                <a href="/app/core/workflow/?app=core&page=info&content_type=Workflow&doc=${data?.id}" class="hover:text-orange-500">${lite.utils.replace_chars(data.name,"_"," ")}</a>
            </div>
        `
    }

    create_data_import_row(data){
        return `
            <div class="flex items-start justify-start intro-y">
                <span class="material-symbols-outlined text-17 mr-2 text-default"> publish </span>
                <a href="/app/core/data_importation/?app=data_importation&page=info&content_type=data%20importation&doc=${data?.id}" class="hover:text-default">${data.name}</a>
            </div>
        `
    }

    create_series_row(data){
        return `
            <div class="flex items-start justify-start overflow-hidden intro-y">
                <span class="material-symbols-outlined text-17 mr-2 text-default"> signature </span>
                <a href="/app/core/series/?app=series&page=info&content_type=Series&doc=${data?.id}" class="hover:text-default overflow-ellipsis truncate">${data.name_format}</a>
            </div>
        `
    }


    // CURRENCY
    create_top_xrate_row(x){
        return `
            <div class="w-full intro-x flex items-center justify-between border-b py-2">
                <div class="flex items-start justify-start">
                    <div class="flex items-center justify-center mr-2 rounded-full bg-default text-theme_text_color w-[20px] h-[20px]">
                        <span class="material-symbols-outlined text-13">sync_alt</span>
                    </div>
                    <div class="flex items-start justify-center flex-col">
                        <div class="font-semibold text-10 flex items-center justify-between"> 
                            <span class="from-currency">${x.from} </span>
                            <span class="material-symbols-outlined mx-3">trending_flat</span> 
                            <span class="to-currency">${x.to}</span>
                        </div>
                        <small class="text-10 text-slate-600">${x.history.date}</small>
                    </div>
                </div>
                <div class="font-bold text-red flex flex-col items-end justify-center text-12">
                    <span class="">${x.rate}</span>
                    <small class="text-10">
                        <span class="material-symbols-outlined ${x.history.diff < 0 ? "text-red-900" : "text-indigo-900"}">
                            ${x.history.diff < 0 ? "trending_down" : "trending_up"}
                        </span>
                        <span class="gain-or-loss-value">${x.history.diff} ${x.history.diff < 0 ? "Loss" : "Gain"}</span>
                    </small>
                </div>
            </div>
        `
    }

    create_xchange_rate_history_row(xh){
        return `
            <div class="w-full  flex items-center justify-between border-b py-2 intro-y">
                <div class="flex items-start justify-start">
                    <div class="flex items-center justify-center mr-2 rounded-full border border-orange-700 text-orange-800 w-[20px] h-[20px]">
                        <span class="material-symbols-outlined text-13">sync_alt</span>
                    </div>
                    <div class="flex items-start justify-center flex-col">
                        <div class="font-semibold text-10 flex items-center justify-between"> 
                            <span class="from-currency">${xh.from} </span>
                            <span class="material-symbols-outlined mx-3">trending_flat</span> 
                            <span class="to-currency">${xh.to}</span>
                        </div>
                        <small class="text-10 text-slate-600">${xh.date}</small>
                    </div>
                </div>
                <div class="font-bold text-red flex flex-col items-end justify-center text-12">
                    <span class="text-red-500">${xh.rate}</span>
                    <small class="text-10">
                        <span class="material-symbols-outlined text-red-900">
                            trending_down 
                        </span>
                        <!--Inverse: ${xh.inverse}-->
                    </small>
                </div>
            </div>
        `
    }

    generate_forex_table(reporting_currency, trade_currencies){
        const loader = lite.utils.generate_loader({size:7,loader_type:"dots"})
        const cols = trade_currencies?.length + 2
        console.log(reporting_currency)
        let header_wrapper = `
            <div class="forex-wrapper-header w-full min-h-[40px] grid grid-cols-${cols} border-b">
                <div class="w-full border-r h-full flex items-center bg-slate-50 flex items-center justify-center flex-col text-10">
                    <span class="material-symbols-outlined">
                        sync_alt
                    </span>
                    Cross Rates
                </div>
        `
        const reporting_cell = `
            <div index="1" currency="${reporting_currency?.name}" class="tr-cell  truncate overflow-ellipsis w-full border-r h-full flex items-center justify-center flex-col bg-slate-50 text-13">
                <div class="flex items-center justify-center">
                    <img src="/static/images/country/${lite.utils.lower_case(reporting_currency?.country_code)}.svg" class="w-[13px] h-[13px] rounded-full object-cover mr-2" alt="">
                    ${reporting_currency?.symbol}
                </div>
            </div>
        `
        header_wrapper += reporting_cell

        $.each(trade_currencies,(_,c)=>{
            header_wrapper += `
                <div index="1" currency="${c?.name}" class="tr-cell w-full truncate overflow-ellipsis border-r h-full flex items-center justify-center flex-col bg-slate-50 text-13  intro-x">
                    <div class="flex items-center justify-center">
                        <img src="/static/images/country/${lite.utils.lower_case(c?.country_code)}.svg" class="w-[13px] h-[13px] rounded-full object-cover mr-2" alt="">
                        ${c?.symbol}
                    </div>
                    <div class="px-3 text-orange-500 text-9">${c.country?.substring(0,22)}</div>
                </div>
            `
        })
        header_wrapper += '</div>'
        let rows = ""
        let row = `
            <div class="w-full h-full grid grid-cols-${cols} border-b">
                <div class="w-full border-r h-full flex items-center justify-center flex-col bg-slate-50 text-11 border-b  intro-x">
                    <div class="flex items-center justify-center">
                        <img src="/static/images/country/${lite.utils.lower_case(reporting_currency?.country_code)}.svg" class="w-[13px] h-[13px] rounded-full object-cover mr-2" alt="">
                        ${reporting_currency?.symbol}
                    </div>
                </div>
        `
        trade_currencies.unshift(0)
        trade_currencies[0] = reporting_currency
        $.each(trade_currencies,(_,c)=>{
            const is_own = reporting_currency.name === c.name
            row += `
                <div from-currency="${reporting_currency.name}" to-currency="${c.name}" class="forex-cell ${is_own ? "is-own bg-default text-theme_text_color" : ""} w-full border-r h-full flex items-center justify-center flex-col text-11  intro-x">
                    <div class="forex-fields-wrapper flex items-center justify-center flex-col intro-x ${!is_own ? "hidden" : ""}">
                        ${
                            !is_own ? '<input from-currency="'+reporting_currency.name+'" to-currency="'+c.name+'" class="forex-rate font-semibold w-full outline-none text-center mt-2" value="1.00" />' :
                            '<span class="font-bold">1.00</span>'
                        }
                        ${
                            !is_own? '<!--<small class="inverse text-gray-400">Invr: <span class="inverse-value font-semibold">1.00</span></small>-->':
                            '<small class="inverse text-white text-center">Reporting Currency</small>'
                        }
                    </div>
                    ${!is_own ? loader : ""}
                </div>
            `
        })
        row += "</div>"
        rows += row

        $.each(trade_currencies,(_,c)=>{
            if(c.name != reporting_currency.name){
                let row = `
                <div class="w-full h-full grid grid-cols-${cols} border-b  intro-y">
                    <div class="w-full border-r h-full flex items-center justify-center flex-col bg-slate-50 text-11 border-b">
                        <div class="flex items-center justify-center">
                            <img src="/static/images/country/${lite.utils.lower_case(c?.country_code)}.svg" class="w-[13px] h-[13px] rounded-full object-cover mr-2" alt="">
                            ${c?.symbol}
                        </div>
                        <div class="px-3 text-orange-500 text-9 text-center">${c.country?.substring(0,18)}</div>
                    </div>
            `
            $.each(trade_currencies,(_,cc)=>{
                const is_own = c.name === cc.name
                row += `
                    <div from-currency="${c.name}" to-currency="${cc.name}" class="forex-cell ${is_own ? "is-own bg-slate-100" : ""} w-full border-r h-full flex items-center justify-center flex-col text-11 intro-x">
                        <div class="forex-fields-wrapper flex items-center justify-center flex-col intro-x ${ !is_own? "hidden" : ""}">
                            ${
                                !is_own ? '<input from-currency="'+c.name+'" to-currency="'+cc.name+'" class="forex-rate font-semibold w-full outline-none text-center mt-2" value="1.00" />' :
                                '<span class="font-bold">1.00</span>'
                            }
                            <!--<small class="inverse text-gray-400 mb-2">Invr: <span class="inverse-value font-semibold">1.00</span></small>-->
                        </div>
                        ${!is_own? loader : ""}
                    </div>
                `
                })
                row += "</div>"
                rows += row
            }
        })

        return  `${header_wrapper}${rows}</div> `
    }



    // user
    create_user_role_checkbox(data){
        return `
            <label for="backdating" class="w-full intro-x flex items-center justify-start cursor-pointer">
                <input id="${data?.id}" name="${data?.name}" ${data?.checked?"checked":""} type="checkbox" class="lite-field role-check text-13 shadow-none form-check-input w-[15px] h-[15px] accent-default mr-1">
                <span class="text-12">${data?.name}</span>
            </label>
        `
    }

    create_recent_user(u){
        return `
            <div class="w-full grid gap-y-2 mb-4 intro-x">
                <div class="flex items-center justify-between">
                    <div class="flex items-center justify-start">
                        <div class="flex items-center justify-center border border-default w-[40px] h-[40px] rounded-full overflow-hidden">
                            <img src="${u.dp || "/media/defaults/avatas/dp.jpeg"}" alt="" class="w-full h-full object-cover object-top rounded-full">
                        </div>
                        <div class="grid ml-2">
                            <span class="font-semibold text-12">${u.first_name || ""} ${u.middle_name || ""} ${u.last_name || ""}</span>
                            <small class="text-gray-400">${u.main_role || ""}</small>
                        </div>
                    </div>
                    <button class="flex items-center justify-center h-[25px] w-[70px] rounded-md btn">
                        <span class="material-symbols-outlined mr-2 text-purple-700"> open_in_new </span>
                        <a href="/app/core/user/?app=core&page=info&content_type=User&doc=${u.id}" class="text-11">View</a>
                    </button>
                </div>
            </div>
        
        `
    }

    create_disabled_user(u){
        return `
            <div class="flex items-center justify-between">
                <div class="flex items-center justify-start">
                    <div class="flex items-center justify-center border border-default w-[40px] h-[40px] rounded-full overflow-hidden">
                        <img src="${u.dp || "/media/defaults/avatas/dp.jpeg"}" alt="" class="w-full h-full object-cover object-top rounded-full">
                    </div>
                    <div class="grid ml-2">
                        <span class="font-semibold text-12">${u.first_name || ""} ${u.middle_name || ""} ${u.last_name || ""}</span>
                        <small class="text-gray-400">${u.main_role || ""}</small>
                    </div>
                </div>
                <button class="flex items-center justify-center h-[25px] w-[70px] rounded-md btn">
                    <span class="material-symbols-outlined mr-2 text-purple-700"> task_alt </span>
                    <span class="text-11 w-[70px]">Enable</span>
                </button>
            </div>
        `
    }




    create_module_permission_wrapper(data){
        // console.log(data)
        // const existing_role_module_permissions = $(`.role-module-permission-list`).find(`.module-permission-card-wrapper[permission-id="${data?.name}"]`)
        // if(!lite.utils.array_has_data(existing_role_module_permissions)){
            
        // }
        return this.create_permission_card(data)
    }

    create_permission_card(data){
        // const {apps, name} = config
        // const role_module = values ? values?.role_module : {}
        // const role_permission = values ? values?.role_permission : []
        // const top_config = role_module[name] || {}
        
        const color = this.color_codes[Math.floor(Math.random() * this.color_codes.length)]
        let cards = this.create_permission_switch(data, color, data?.permit_all_components || 0)
        let basic_field_config = { id:"select-all", fieldtype: "switch", fieldlabel: "Allow All", default: 0, omitlabels: true }
        
        let default_dashboard = { 
            id:"default-dashboard", 
            fieldtype: "link", 
            fieldname:"default_dashboard",
            model:"Default_Dashboard", 
            placeholder: "Select Default Dashboard", 
            omitlabels: true, 
            classnames:`mr-2 w-[195px] border-white`,
            value: data?.default_dashboard || "",
            filters:{ module:data?.name}
        }
        return `
            <div permission-id="${data?.name}" module="${data?.name}" class="module-permission-card-wrapper w-full rounded-md border transition duration-500 border-[${color.inner}]">
                <div class="w-full bg-[${color.base}] text-[${color.inner}] border-b border-b-[${color.inner}]  p-2 mb-2 flex items-center justify-between h-[50px] rounded-t-md">
                    <h4 class="font-bold">
                        <span class="material-symbols-outlined mr-1 text-15 text-[${color.inner}]"> ${data?.icon || ''} </span>
                        ${lite.utils.capitalize(lite.utils.replace_chars(data?.name,"_", " "))}
                    </h4>
                    <span class="flex items-center justify-end w-[400px]"> 
                        ${lite.html_generator.build_form_field(default_dashboard)}
                        <div class="w-[100px]" >
                            ${lite.html_generator.build_form_field({...basic_field_config, classnames:"allow-all", id:"allow-all", value:data?.permit_all_components || 0})}
                        </div>
                    </span>
                </div>
                <div class="w-full h-[40vh] overflow-y-auto">
                    <div class="w-[97%] h-[max-content] mx-auto grid grid-cols-2 gap-3 gap-5">${cards}</div>
                </div>
            </div>
        `
    }

    create_permission_switch(data,  color, allow_all=0){
        let module_cards = ""
        let basic_field_config = { id:"select-all", fieldtype: "switch", fieldlabel: "Select All", default: allow_all, omitlabels: true }
        $.each(data.menu_cards, (_, card)=>{
            let ext = {}
            console.log(card)
            const values = {
                "Select All": allow_all == 1 ? allow_all : ext["Allow All"] || 0,
                "Create": allow_all == 1 ? allow_all : ext["Create"] || 0,
                "Read": allow_all == 1 ? allow_all : ext["Read"] || 0,
                "Update": allow_all == 1 ? allow_all : ext["Update"] || 0,
                "Submit": allow_all == 1 ? allow_all : ext["Submit"] || 0,
                "Cancel": allow_all == 1 ? allow_all : ext["Cancel"] || 0,
                "Delete": allow_all == 1 ? allow_all : ext["Delete"] || 0,
                "Print": allow_all == 1 ? allow_all : ext["Print"] || 0,
                "Download": allow_all == 1 ? allow_all : ext["Download"] || 0,
                "Export": allow_all == 1 ? allow_all : ext["Export"] || 0,
            }

            module_cards += `
                <div module="${data?.name}" app="" model="" class="permission-card intro-y w-full h-max-content bg-gray-50 rounded-md overflow-hidden h-max-content">
                    <div class="w-full bg-[${color.base}] text-[${color.inner}] text-12 flex items-center justify-between px-2 h-[30px]">
                        <div class="flex items-center justify-start">
                            <span class="material-symbols-outlined mr-1 text-14 text-gray-500"> ${data?.icon || ''} </span>
                            <span class="font-bold">${lite.utils.capitalize(card.name)}</span>
                        </div>
                        <button class="border-none flex items-center justify-center">
                            <span class="material-symbols-outlined"> expand_more </span>
                        </button>
                    </div>
                    <div class="permission-action-list w-full grid grid-cols-2 gap-2 p-1">
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">All</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,classnames:"select-all",id:card.name, value: values["Select All"]  })}
                        </div>
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">Create</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,fieldlabel:"Create",id:"Create", value: values["Create"] })}
                        </div>
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">Read</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,fieldlabel:"Read",id:"Read", value: values["Read"] })}
                        </div>
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">Update</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,fieldlabel:"Update",id:"Update", value: values["Update"] })}
                        </div>
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">Submit</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,fieldlabel:"Submit",id:"Submit", value: values["Submit"] })}
                        </div>
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">Cancel</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,fieldlabel:"Cancel",id:"Cancel", value: values["Cancel"] })}
                        </div>
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">Delete</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,fieldlabel:"Delete",id:"Delete", value: values["Delete"] })}
                        </div>
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">Print</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,fieldlabel:"Print",id:"Print", value: values["Print"] })}
                        </div>
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">Download</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,fieldlabel:"Download",id:"Download", value: values["Download"] })}
                        </div>
                        <div class="w-[80%] flex items-center justify-between h-[30px]">
                            <span class="text-11 w-[70px]">Export</span>
                            ${lite.html_generator.build_form_field({...basic_field_config,fieldlabel:"Export",id:"Export", value: values["Export"] })}
                        </div>
                    </div>
                </div>
            `
        })
        return module_cards
    }




    // data importation
    create_recent_data_importation_row(i){
        return `
            <a href="/app/core/data_importation/?app=data_importation&page=info&content_type=data%20importation&doc=${i.id}" class="w-full flex items-center justify-between h-[50px] border-b intro-x hover:text-default">
                <div class="flex items-center justify-start">
                    <div class="flex items-center justify-start truncate overflow-ellipsis">
                        <span class="material-symbols-outlined text-17 flex items-center justify-center rounded-md bg-indigo-100 mr-2 p-1 rounded-full"> publish </span>
                        <span class="text-12">${i.name}</span>
                    </div>
                </div>
                <div class="flex items-center justify-between">
                    <span class="material-symbols-outlined text-18 ${i.status == "Importation Successful" ? "text-default" : "text-orange-700"} "> ${i.status == "Importation Successful" ? "check_circle" : "cancel"} </span>
                </div>
            </a>
        `
    }
}