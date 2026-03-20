

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'
class Leave_Application {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$application = $ ("#application")
        this.$department_stats = $ ("#dep-stats")
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()
    }
    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("leave_application")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            this.$application.append (this.html_generator.application(this.data.applied_employees))
            this.$department_stats.append (this.html_generator.leave_departments_stats(this.data?.department_employees))
        }
        lite.utils.init_dashboard(true)
    }
}
export default Leave_Application








