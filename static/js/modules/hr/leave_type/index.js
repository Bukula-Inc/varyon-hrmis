

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Leave_Type {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.$side_view = $ ("#leave-type-stats")
        this.data = null
        this.init_dashboard()
    }
    async init_dashboard(){
        const dashboard_content = await lite.connect.dashboard("side_view_leave_type")
        this.data = dashboard_content.data.data
        lite.utils.init_dashboard(true)
        if (!this.data) {
            lite.utils.add_empty_component ({$wrapper: this.$side_view, text: "No Content Found", color: "gray"})
        }else if (this.data.length <= 0) {
            lite.utils.add_empty_component ({$wrapper: this.$side_view, text: "No Content Found", color: "gray"})
        
        }else{
            this.$side_view.append (this.html_generator.leave_type_side_view (this.data))
            
        }
    }
}

export default Leave_Type 

