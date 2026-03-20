
export default class Portal_HTML_Generator{
    constructor(){
        this.app = lite.utils.get_current_app()
    }

    create_client_menu(config){
        return `
            <a href="/portal/${config.app}?module=portal&app=${config.app}&page=${config.page}&content_type=${config.content_type}" class="client-menu ${this.app === config.app ? "bg-default text-theme_text_color" : ""} w-full flex items-center justify-start h-[50px] intro-x  transition duration-1000 hover:bg-default/30 hover:text-black hover:translate-x-[4%] rounded-md px-2">
                <span class="material-symbols-outlined text-15"> ${config.icon} </span>
                <span class="ml-2 text-13">${config.title}</span>
            </a>
        `
    }

    create_client_listview_content(config){
        let total_cols = 3
        let cols = `
            <div class="w-full h-full intro-x flex items-center justify-center">S/N</div>
            <div class="w-full h-full intro-x flex items-center justify-start col-span-1">
                <span class="material-symbols-outlined mr-1 text-teal-600"> schedule </span>
                Creation Date
            </div>
        `

        $.each(config.columns,(_,c)=> {
            c.columns ? total_cols += lite.utils.string_to_float(c.columns) : 2
            cols += `
                <div class="w-full h-full intro-x flex items-center justify-start col-span-${c.columns || 2}">
                    <span class="material-symbols-outlined mr-1 text-${c.icon_color}-600"> ${c.icon} </span>
                    ${c.column_title}
                </div>
            `
        })

        return `
            <div class="w-full grid grid-cols-${total_cols} bg-default text-theme_text_color h-[40px] text-12">
                ${cols}
                <div class="w-full h-full intro-x flex items-center justify-center col-span-1">
                    <span class="material-symbols-outlined mr-1 text-teal-600"> tune </span>
                    Actions
                </div>
            </div>
        `
    }

    create_listview_content_row(idx, data, config){
        
        // console.log(data, config)
        let total_cols = 3
        let cols = `
            <div class="w-full h-full intro-x flex items-center justify-center col-span-1">${idx}</div>
            <div class="w-full h-full intro-x flex items-center justify-start col-span-1 font-semibold">
                ${lite.utils.convert_date(data?.created_on)}
            </div>
        `

        $.each(config.columns,(_,c)=> {
            c.columns ? total_cols += lite.utils.string_to_float(c.columns) : 2
            let v = data[c.column_name]

            if(c.column_name === "status"){
                v = `
                    <div class="px-3 bg-[${data?.status_info?.status_color}] rounded-md w-[90%] text-center flex items-center justify-center">
                        <div class="w-[4px] h-[4px] rounded-full bg-[${data?.status_info?.inner_color}] mr-1"></div>
                        ${data[c.column_name]}
                    </div>
                `
            }
            cols += `
                <div class="w-full truncate overflow-ellipsis h-full pl-2 intro-x flex items-center justify-start col-span-${c.columns || 2}">
                    ${v || "-"}
                </div>
            `
        })

        return `
            <div lite-id="${lite.utils.unique()}" id="${data?.id}" class="list-row cursor-pointer w-full grid border-b border-dashed grid-cols-${total_cols} h-[40px] text-12 hover:translate-x-[-1%] transition duration-500 hover:bg-default/30">
                ${cols}

                <div class="w-full h-full intro-x flex items-center justify-center col-span-1">
                    <button class="w-[90%] flex items-center justify-center h-[30px] btn border shadow-none bg-white">
                        <small class="text-10 mr-1 font-normal">Open</small>
                        <span class="material-symbols-outlined"> keyboard_arrow_right </span>
                    </button>
                </div>
            </div>
        `
    }




    // dashboard
    create_dashboard_ticket_history_card(history){
        return `
            <a href="/portal/client_ticket?module=portal&app=client_ticket&page=new-form&content_type=Ticket" class="flex items-start justify-between border-b h-[50px] w-full py-3 intro-y">
                <div class="flex items-start justify-start">
                    <span class="material-symbols-outlined text-12 mr-1 mt-1"> local_activity </span>
                    <div class="flex flex-col">
                        <span class="text-12">System failure</span>
                        <small class="text-11 text-[${history?.status_info?.inner_color}]">${history?.status}</small>
                    </div>
                </div>
                <div class="flex items-center justify-end mt-1">
                    <span class="material-symbols-outlined text-[${history?.status_info?.inner_color}]"> 
                    ${["open","draft"].includes(lite.utils.lower_case(history?.status)) ? "pending" : "task_alt"}
                     
                    </span>
                </div>
            </a>
        `
    }
    news_letter(history) {        
        let card = ``
        $.each(history, (index, Values) => {
            
            if (index < 9) {
                card += `
                    <div class="flex items-start justify-between border-b h-[50px] w-full py-3 intro-y">
                    <div class="flex items-start justify-start">
                        <span class="material-symbols-outlined text-12 mr-1 mt-1"> local_activity </span>
                        <div class="flex flex-col">
                            <span class="text-12">News Letter: ${Values.subject}</span>
                            <small class="text-gray-500 text-11">Rolling On: ${Values.created}</small>
                        </div>
                    </div>
                    <div class="flex items-center justify-end mt-1">
                        <span class="material-symbols-outlined text-indigo-600"> task_alt </span>
                    </div>
                </div>
                `
            }
        })
        return card
    }
}