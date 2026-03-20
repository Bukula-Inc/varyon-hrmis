

// import Staff_Overtime from './sideview.js'

// import HTML_Builder from '../../../page/html/html_builder.js'
// import Staff_HTML_Generator from '../../../page/html/staff_html_generator.js'
// export default class Staff_Overtime_Statistics {
//     constructor() {
//         this.builder = new HTML_Builder()
//         this.generator = new Staff_HTML_Generator()
//         this.user = {}
//         this.$total_overtime_earning = $(".total-overtime-earning")
//         this.$total_applications = $('.overtime-applications')
//         this.$total_overtime_hours = $('.total-overtime-hours')
//         this.sideview = new Staff_Overtime()
    
       
    
//         this.init_dashboard()
//     }


//     async init_dashboard(){
//         const dashboard_content = await lite.connect.dashboard("staff_overtime_statistics")
//         lite.utils.init_dashboard(true)

//         if(dashboard_content.status === lite.status_codes.ok){
//             this.data = dashboard_content.data
            
//         }
//       this.populate_overtime_content()
    
//     }


//     populate_overtime_content(){
//         const overtime_stats = this.data;
//         if(overtime_stats){
//             lite.utils.count_figure(this.$total_overtime_earning,overtime_stats.total_earnings,true,lite.currency_decimals,this.currency)
//             lite.utils.count_figure(this.$total_applications,overtime_stats.total_applications,true)
//             lite.utils.count_figure(this.$total_overtime_hours, overtime_stats.total_overtime_hours,true)
            
//         }
//         else
//             lite.utils.add_empty_component ({$wrapper: this.$overtime_stats_wrapper, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
//     } 

// }


