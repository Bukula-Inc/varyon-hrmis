

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Work_Plan {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$work_plan = $ ("#work-plan")

        
    

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        // this.init_dashboard()
    }
    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("work_plan")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            this.$work_plan.append (this.html_generator.work_plan_data(this.data?.work_plan_activities))
            console.log(this.data)
            console.log(this.data.work_plan_activities)
            
          

            
            // this.init_charts(this.data)
        }
        lite.utils.init_dashboard(true)
    }
    // init_charts () {
    //     this.form ()
    // }

    // form() {
    //             const data = {
    //                 labels: ["Submitted", "Draft"],
    //                 values: [30, 1]
    //             }
    //             this.charts.pie_chart('appraisal-form-chart', data.labels, data.values, {
    //                 // legend_position: "right",
    //                 // width: ,
    //                 // height: 200
    //             })
    //         }


}

export default Work_Plan








