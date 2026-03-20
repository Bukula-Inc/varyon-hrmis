;
import Nav_HTML_Generator from "../page/html/nav_html_generator.js";
export default class Searcher{
    constructor(config){
        this.generator = new Nav_HTML_Generator()
        this.$search_trigger = $(".search__input")
        this.$search_module_filters = $('.search-module-filters')
        this.$search_results = $('.search-results')
        this.$search_field = $('#quick-search-input')
        this.utils = config.utils
        this.nav = config.nav
        this.routes = []
        this.init_searcher()
    }
  

    async init_searcher(){
        const allowed_content = await this.utils.delay_until(()=> {
            if(!this.utils.array_has_data(lite))
                return lite.allowed_content
        },9000)
        this.$search_trigger?.attr("placeholder", `Search ${lite?.user?.company?.name} (Ctrl + K)`)
        const current_module = lite.utils.get_current_module()
        const content = allowed_content[current_module]
        if(lite.utils.object_has_data(content)){
            this.$search_module_filters.empty()
            this.$search_results.empty()
            const cards = lite.utils.get_object_keys(content?.menu_cards)
            Promise.all(cards?.map(async mc=>{
                const mc_cards = content?.menu_cards[mc]
                if(mc_cards?.card_items){
                    $.each(mc_cards.card_items, (_, card)=>{
                        card.parent_card = mc
                        card.module = current_module
                        this.$search_results.append(this.generator.create_search_Result_card(card))
                    })
                }
                // this.$search_module_filters.prepend(this.generator.create_search_module_filter(m_title,m?.name))
            }))
            // this.$search_module_filters.prepend(this.generator.create_search_module_filter("All","all"))
        }
        this.init_search_field()
    }
    init_search_field(){
        this.$search_field.off("keyup").keyup(e=>{
            const value = $(e.currentTarget).val()?.toLowerCase()?.trim()
            const search_wrappers = $(".search-module-content-wrapper")
            $('.search-item').addClass("hidden")
            if(!value){
                $('.search-item').removeClass("hidden")
                $(".search-module-content-wrapper")?.removeClass("hidden")
            }
            else{
                $(`.search-item[content-type*="${value}"], .search-item[module*="${value}"]`).removeClass("hidden")
                $(".search-module-content-wrapper:not(:has(.search-item:not(.hidden)))")?.addClass("hidden")
                $(".search-module-content-wrapper:has(.search-item:not(.hidden))")?.removeClass("hidden")
            }
        })
    }

}

