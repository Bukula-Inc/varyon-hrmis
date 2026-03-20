import smart_invoice from "./json/smart_invoice.js"
export default class Integrations{
    constructor(){
        this.$request_headers = $("#request-headers")
        this.$request_body = $("#request-body")
        this.$response_body = $("#response-body")
        this.$request_url = $("#request-url")

        this.$integrations_menu_content_wrapper = $(".integration-menu-content-wrapper")
        this.$integration_menu_item = $(".integration-menu-item")
        this.$selected_integrations_guide_title = $(".selected-integration-guide")
        this.$close_integrations_menu = $(".close-integration-menus")


        this.skeleton = {
            status: 200,
            data: {
                "xxxxx": "xxxxxxxxxx xxxxxx xxxx",
                "xxx": "xxxxxxxxxx xxxxxx xxxx",
                "xxxxxxxx": "xxxxxxxxxx xxxxxx",
                "xxxx": "xxxxxxxxxx xxxx",
                "xxxxxxx":"xxxxxxxxxx xxxxxx xxxxx",
                "xxxxxxxx":"xxxxxxxxxx xxxxxx xxxxx",
                "xxxxxxxxx":"xxxxxxxxxx xxxxxx xxxxx",
            }
        }

        this.enable_integration_menu_items()
    }
    async init(){
        this.init_skeleton_json(smart_invoice.sales_invoice)
    }


    init_skeleton_json(json_data){
        this.$request_headers.text(JSON.stringify(json_data.headers, null, 2))
        this.$request_body.text(JSON.stringify(json_data.req, null, 2))
        this.$response_body.text(JSON.stringify(json_data.res, null, 2))
        this.$request_url.attr("href",json_data?.endpoint)?.find("small")?.text(json_data?.endpoint)
        hljs.highlightAll()
    }


    enable_integration_menu_items(){
        this.$integration_menu_item?.off("click")?.click(e=>{
            e.preventDefault()
            this.$integration_menu_item?.removeClass("bg-default text-theme_text_color")
            $(e.currentTarget)?.addClass("bg-default text-theme_text_color")
            const item = lite.utils.get_attribute(e.currentTarget,"href")
            this.$integrations_menu_content_wrapper?.removeClass("hidden")
        })

        this.$close_integrations_menu?.click(e=>{
            this.$integrations_menu_content_wrapper?.addClass("hidden")
        })
    }
}