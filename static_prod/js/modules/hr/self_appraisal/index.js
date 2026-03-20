

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Self_Appraisal {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$self_appraisal = $ ("#self-appraisal")

        
    

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        // this.init_dashboard()
    }
    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("self_appraisal")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            // console.log(this.data )
            this.$self_appraisal.append (this.html_generator.self_appraisal(this.data?.submitted_appraisals))
            
            this.init_charts(this.data.self_appraisal_stats)
        }
        lite.utils.init_dashboard(true)
    }
    init_charts (stats_data) {
        this.form (stats_data)
    }

    form(stats_data) {
                const data = {
                    labels: ["Submitted", "Draft"],
                    values: [stats_data.submitted, stats_data.draft]
                }
                this.charts.pie_chart('self-appraisal-chart', data.labels, data.values, {
                })
            }


}

export default Self_Appraisal








