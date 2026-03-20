import HTML_Builder from '../../../page/html/html_builder.js'
import Staff_HTML_Generator from '../../../page/html/staff_html_generator.js'
export default class Staff_Statistics {
    constructor() {
        this.builder = new HTML_Builder()
        this.generator = new Staff_HTML_Generator()
        this.user = {}
        this.$total_earning = $(".total-earning")
        this.$total_deduction = $('.total-deduction')
        this.$total_tax = $('.total-tax')
        this.$total_net = $('.total-net')
        this.$total_gross = $('.total-gross')
        this.$total_basic = $('.total-basic')
        this.$payslip_stats_wrapper = $('#payslip-stats-wrapper')
    
        this.init_dashboard()
    }


    async init_dashboard(){
        const dashboard_content = await lite.connect.dashboard("staff_payslip_statistics")
        lite.utils.init_dashboard(true)

        if(dashboard_content.status === lite.status_codes.ok){
            this.data = dashboard_content.data
        }
      this.populate_payslip_content()
    
    }


    populate_payslip_content(){
        const payslip_stats = this.data;
        if(payslip_stats){
            lite.utils.count_figure(this.$total_earning,payslip_stats.overall_earnings,true,lite.currency_decimals,this.currency)
            lite.utils.count_figure(this.$total_deduction,payslip_stats.overall_deductions,true,lite.currency_decimals,this.currency)
            lite.utils.count_figure(this.$total_tax,payslip_stats.overall_tax,true,lite.currency_decimals,this.currency)
            lite.utils.count_figure(this.$total_basic,payslip_stats.overall_basic_pay,true,lite.currency_decimals,this.currency)
            lite.utils.count_figure(this.$total_gross,payslip_stats.overall_gross,true,lite.currency_decimals,this.currency)
            lite.utils.count_figure(this.$total_net,payslip_stats.overall_net,true,lite.currency_decimals,this.currency)

        
        }
        else
            lite.utils.add_empty_component ({$wrapper: this.$payslip_stats_wrapper, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
    } 

}

