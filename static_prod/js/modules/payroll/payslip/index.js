
import Payroll_HTML_Generator from '../../../page/html/payroll_html_generator.js'

class Payslip {
    constructor(config) {   
        this.generator = new Payroll_HTML_Generator()
        this.$payslip = $("#payslip")
        this.$payslip_stats = $("#payslip_stats")

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connection
        this.init_dashboard()
    }

    async init_dashboard() {
        const dashboard_content = await lite.connect.dashboard("payslip")
        if (dashboard_content.status == lite.status_codes.ok) {
            this.data = dashboard_content.data
            this.$payslip.append(this.generator.payslip(this.data.submitted_payslip))
            this.$payslip_stats.append(this.generator.payslip_stats(this.data.payslip_stats))
        }
        lite.utils.init_dashboard(true)
    }
}

export default Payslip