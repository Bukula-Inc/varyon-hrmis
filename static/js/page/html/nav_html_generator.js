
export default class Nav_HTML_Generator{
    constructor(){
        this.color_codes = lite.color_codes
    }

    create_search_module_filter(title, id){
        return `
            <div class="flex items-center justify-start">
                <input id="${id}" type="checkbox" class="shadow-none  module-filter form-check-input w-[20px] h-[20px] accent-default mr-2"/> 
                <label for="${id}">${title}</label>
            </div>
        `
    }

    create_search_Result_card(card){
        const colour = lite.color_codes[Math.floor(Math.random() * (lite.color_codes.length-1))]
        return `
            <a href="/app/${card?.module}/${card?.app}?app=${card?.app}&module=accounting&page=${card?.page_type}&content_type=${card?.content_type}" 
                module="${lite.utils.lower_case(card.module)}" content-type="${lite.utils.lower_case(card.title)}" 
                class="search-item rounded-md intro-x flex items-center text-13 bg-[${colour.base}] hover:bg-[${colour.base}] transition duration-300 py-1 h-max-content max-h-[40px]">
                <div class="ml-3 truncate flex items-start justify-start truncate overflow-ellipsis">
                    <div class="w-[30px] h-[30px] rounded-full bg-[${colour.base}] flex items-center justify-center mr-1">
                        <span class="material-symbols-outlined text-20 text-[${colour.inner}]"> ${card.icon} </span>
                    </div>
                    <div class="flex flex-col">
                        <span>${card.title}</span>
                        <small class="text-10">${card?.parent_card}</small>
                    </div>
                </div>
            </a>
        `
        
    }
}