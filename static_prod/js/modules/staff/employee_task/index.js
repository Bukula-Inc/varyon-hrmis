
import Staff_HTML_Generator from '../../../page/html/staff_html_generator.js'

class staff_Project_Tasks {
    constructor(config) {   
        this.generator = new Staff_HTML_Generator()
        this.$staff_project_tasks = $("#stafff-project-task")
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
        const dashboard_content = await lite.connect.dashboard("staff_project_tasks")
       
        if (dashboard_content.status == lite.status_codes.ok) {
       
            this.data = dashboard_content.data
            console.log(this.data)
            if (!this.data?.tasks || this.data?.tasks.length == 0) {
                lite.utils.add_empty_component ({$wrapper: this.$staff_tasks, text: "No Content Found", color: "gray"})
            }else {
    
                this.$staff_project_tasks.append(this.generator.staff_project_task(this.data.tasks));          
            }

            if (!this.data?.status_counts || this.data?.status_counts.length == 0) {
                lite.utils.add_empty_component ({$wrapper: this.$staff_status_counts, text: "No Content Found", color: "gray"})
            }else {
                const data = this.data.status_counts;
                let labels = [];
                let values = [];
                
                data.forEach(item => {
                    const status = item?.status || "";
                 
                    const count = item?.count || 0;
                
                    labels.push(status);
                    values.push(count);
                });
                
                lite.charts.pie_chart('staff-task-status', labels, values, {
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

export default staff_Project_Tasks
