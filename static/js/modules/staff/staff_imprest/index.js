
import Staff_HTML_Generator from '../../../page/html/staff_html_generator.js'

class Staff_Imprest {
    constructor(config) {   
        this.generator = new Staff_HTML_Generator()
        this.$staff_imprest = $("#stafff-imprest")
        // this.$staff_overtime_stats = $("#staff-overtime-stats")

        // this.utils = config.utils
        // this.page_controller = config.page_controller
        // this.nav_manager = config.nav_manager
        // this.charts = config.charts
        // this.sessions = config.sessions
        // this.connect = config.connectin
        this.init_dashboard()
    }

    async init_dashboard() {
        //{name: emp_name, employee:lite.employee_info.name}
        const emp_name = lite.employee_info.name
        const dashboard_content = await lite.connect.dashboard("staff_imprest_side_view")
       
        if (dashboard_content.status == lite.status_codes.ok) {
       
            this.data = dashboard_content.data
            if (!this.data?.imprest_info || this.data?.imprest_info.length == 0) {
                lite.utils.add_empty_component ({$wrapper: this.$staff_imprest, text: "No Content Found", color: "gray"})
            }else {
    
                this.$staff_imprest.append(this.generator.imprest(this.data.imprest_info));          
            }

            if (!this.data?.imprest_stats || this.data?.imprest_stats.length == 0) {
                lite.utils.add_empty_component ({$wrapper: this.$staff_imprest_stats, text: "No Content Found", color: "gray"})
            }else {
                const data = this.data.imprest_stats;
                let labels = [];
                let values = [];
                
                data.forEach(item => {
                    const status = item?.status || "";
                 
                    const count = item?.count || 0;
                
                    labels.push(status);
                    values.push(count);
                });
                
                lite.charts.pie_chart('staff-imprest-stats', labels, values, {
                    show_legend: false,
                    height: 300,
                    colors: [
                        lite.charts.colors[1],
                        lite.charts.colors[0],
                        lite.charts.negative_colors[1],
                        lite.charts.colors[5]
                    ]
                });
                
            }
           
           
        }
        lite.utils.init_dashboard(true)
    }
}

export default Staff_Imprest
