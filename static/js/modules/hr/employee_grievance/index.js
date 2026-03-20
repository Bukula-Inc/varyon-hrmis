

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Employee_Grievance {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$grievance = $ ("#grievance")

        
    

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()
    }
    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            this.$grievance.append (this.html_generator.employee_grievance(this.data?.grieved_employees))
            this.init_charts(this.data)
        }
        lite.utils.init_dashboard(true)
    }
    init_charts () {
        this.form ()
    }

    form() {
                const data = {
                    labels: ["Submitted", "Draft"],
                    values: [30, 1]
                }
                this.charts.pie_chart('appraisal-form-chart', data.labels, data.values, {
                    // legend_position: "right",
                    // width: ,
                    // height: 200
                })
            }


}

export default Employee_Grievance








