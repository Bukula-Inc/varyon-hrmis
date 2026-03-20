
import Core_HTML_Generator from '../../../page/html/core_html_generator.js'
export default class Currency{
    constructor(){
        this.generator = new Core_HTML_Generator()
        this.$recent_importations = $(".recent-data-importations")
        this.init_dashboard()
    }
    async init_dashboard(){
        
        const recent  = await lite.connect.dashboard("data_importation")
        lite.utils.init_dashboard(true)
        if(recent.status == lite.status_codes.ok){
            $.each(recent.data,(_,r)=>{
                this.$recent_importations?.append(this.generator.create_recent_data_importation_row(r))
            })
        }
    }
}