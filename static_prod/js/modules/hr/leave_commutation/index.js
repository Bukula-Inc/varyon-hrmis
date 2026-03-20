import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'
class Dashboard {
    constructor(config) {        
        this.utils = config.utils;
        this.page_controller = config.page_controller;
        this.nav_manager = config.nav_manager;
        this.charts = config.charts;
        this.sessions = config.sessions;
        this.connect = config.connect;
        this.$leave_com_stats = $("#leave_com_stats")
        this.html_generator = new HR_HTML_GENERATOR ()
        this.init_dashboard();
    }

    async init_dashboard() {
        try {
            const leave_commutation = await lite.connect.dashboard("leave_commutation");
            if (leave_commutation.status === lite.status_codes.ok) {
                this.leave  = leave_commutation.data;                
                this.init_charts();
            }
        } catch (error) {
            console.error("Error initializing dashboard:", error);
        } finally {
            await lite.utils.init_dashboard(true);
        }
    }

    init_charts() {
        this.leave_commutation();
    }

    leave_commutation() {
        const leave_Commut = this.leave.leave_commutation
        if (!leave_Commut || !lite.utils.object_has_data(leave_Commut)){
            lite.utils.add_empty_component({ $wrapper: this.$leave_com_stats, text: "No Commutations", color: "purple", classnames: "absolute" })  
        }
    const leave_data = Object.values(leave_Commut)
    this.$leave_com_stats.append(this.html_generator.leave_commutation(leave_data))
    } 
}
export default Dashboard;
