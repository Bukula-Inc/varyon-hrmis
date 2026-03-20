
import HTML_Builder from '../../../page/html/html_builder.js'
import Staff_HTML_Generator from '../../../page/html/staff_html_generator.js'
export default class Staff_Advance {
    constructor() {
        this.builder = new HTML_Builder()
        this.generator = new Staff_HTML_Generator()
        this.user = {}
        this.$total_advance = $(".total-advance")
        this.$total_applications = $('.advance-applications')
        this.$overall_principal = $('.overall-principal')
        this.$overall_balance = $('.overall-balance')
        this.$overall_payment = $('.overall-payment')
        this.$overall_interest = $('.overall-interest')
        this.$unsettled_amount =$('.unsettled-amount')
        this.$settled_amount = $ ('.settled-amount')
        this.$current_month_payment = $('.current-month-payment')
      
    
       
    
        this.init_dashboard()
    }


    async init_dashboard(){
        const dashboard_content = await lite.connect.dashboard("staff_advance")
        lite.utils.init_dashboard(true)

        if(dashboard_content.status === lite.status_codes.ok){
            this.data = dashboard_content.data
         

            
        }
      this.populate_advance_content()
    
    }


    populate_advance_content(){
        const advance_stats = this.data;
        console.log(advance_stats)
        if(advance_stats){
            lite.utils.count_figure(this.$total_advance,advance_stats.overall_advance_amount,true,lite.currency_decimals,this.currency)
            lite.utils.count_figure(this.$total_applications,advance_stats.total_applications,true)
            lite.utils.count_figure(this.$overall_principal,advance_stats.overall_principal,true)
            lite.utils.count_figure(this.$overall_balance,advance_stats.overall_balance,true)
            lite.utils.count_figure(this.$overall_interest,advance_stats.overall_interest,true)
            lite.utils.count_figure(this.$overall_payment,advance_stats.overall_payment,true)
            lite.utils.count_figure(this.$unsettled_amount,advance_stats.unsettled_amount,true)
            lite.utils.count_figure(this.$settled_amount,advance_stats.settled_amount,true)
            lite.utils.count_figure(this.$current_month_payment,advance_stats.current_month_payment,true)
           
            
        }
        else
            lite.utils.add_empty_component ({$wrapper: this.$advance_stats_wrapper, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
    } 

}


