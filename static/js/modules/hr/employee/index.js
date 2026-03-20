import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Employee {
    constructor(config) {
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$employees_designation = $ ("#employee-by-designation")
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()

    }
    async init_dashboard(){
        const dashboard_content = await lite.connect.dashboard("employee")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            if (!this.data?.employees_designation || this.data?.employees_designation.length == 0) {
                lite.utils.add_empty_component ({$wrapper: this.$employees_designation, text: "No Content Found", color: "gray"})
            }else {
                this.$employees_designation.append (this.html_generator.employee_designation(this.data?.employees_designation))
            }
            if (!this.data?.gender || this.data?.gender.length == 0) {
                lite.utils.add_empty_component ({$wrapper: $ ("#donut"), text: "No Content Found", color: "gray"})
            }else {
                this.init_charts()
            }
        }
        lite.utils.init_dashboard(true)
    }
    init_charts () {
        this.donut ()
    }

    donut(){
        const data = {
            labels: ["Male", "Female"],
            values: this.data.gender
        }
        this.charts.donut_chart('donut', data?.labels, data?.values,{
            height: 300,
            show_legend: false,
            plot_show: true,
            legend_position:"bottom"
        })
    }


}

export default Employee