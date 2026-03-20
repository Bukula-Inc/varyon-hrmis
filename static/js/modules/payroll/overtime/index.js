
import Payroll_HTML_Generator from '../../../page/html/payroll_html_generator.js'

class Overtime {
    constructor(config) {   
        this.generator = new Payroll_HTML_Generator()
        this.$overtime = $("#overtime")
        this.$overtime_stats = $("#overtime_stats")

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connectin
        this.init_dashboard()
    }

    async init_dashboard() {
        const dashboard_content = await lite.connect.dashboard("Overtime")
        if (dashboard_content.status == lite.status_codes.ok) {
            this.data = dashboard_content.data
            this.$overtime.append(this.generator.overtime(this.data.overtime_info))
            this.$overtime_stats.append(this.generator.overtime_stats(this.data.overtime_stats))
        }
        lite.utils.init_dashboard(true)
    }
}

export default Overtime
