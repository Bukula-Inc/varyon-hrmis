
import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'

class Gratuity {
    constructor(config) {   
        this.generator = new HR_HTML_Generator()
        this.$gratuity = $("#gratuity")
        this.$gratuity_stats = $("#gratuity_stats")

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connectin
        this.init_dashboard()
    }

    async init_dashboard() {
        const dashboard_content = await lite.connect.dashboard("gratuity_side_view")
        if (dashboard_content.status == lite.status_codes.ok) {
            this.data = dashboard_content.data
            console.log(this.data)
            this.$gratuity.append(this.generator.gratuity(this.data.gratuity_info))
            this.$gratuity_stats.append(this.generator.gratuity_stats(this.data.gratuity_stats))
        }
        lite.utils.init_dashboard(true)
    }
}

export default Gratuity
