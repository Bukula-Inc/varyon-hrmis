
import Payroll_HTML_Generator from '../../../page/html/payroll_html_generator.js'

class Advance_Application {
    constructor(config) {   
        this.generator = new Payroll_HTML_Generator()
        this.$advance = $("#advance")
        this.$advance_stats = $("#advance_stats")

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connection
        this.init_dashboard()
    }

    async init_dashboard() {
        const dashboard_content = await lite.connect.dashboard("advance_side_view")
        if (dashboard_content.status == lite.status_codes.ok) {
            this.data = dashboard_content.data
            this.$advance.append(this.generator.advance(this.data.advance_info))
            this.$advance_stats.append(this.generator.advance_stats(this.data.advance_stats))
        }
        lite.utils.init_dashboard(true)
    }
}

export default Advance_Application
