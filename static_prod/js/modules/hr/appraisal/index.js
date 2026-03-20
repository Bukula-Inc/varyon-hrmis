
import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Appraisal {
      constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$appraisal = $ ("#appraisal")
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()
    }

        async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("appraisal")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            console.log(this.data)
            this.$appraisal.append (this.html_generator.appraisal(this.data?.submitted_appraisals))

            
            this.init_charts(this.data.appraisal_setup_stats)
        }
        lite.utils.init_dashboard(true)
    }
    init_charts (stats_data) {
        this.Appraisal (stats_data)
    }

   Appraisal(stats_data) {
    console.log(stats_data)
    const data = {
        labels: ["Draft", "Submitted"],
        values: [stats_data.draft, stats_data.submitted]
    }
    this.charts.pie_chart('appraisal-chart', data.labels, data.values, {
        // legend_position: "right",
        // width: ,
        // height: 200
    })
}


}

export default Appraisal
