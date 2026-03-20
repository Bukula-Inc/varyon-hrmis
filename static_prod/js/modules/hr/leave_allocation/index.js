

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Allocation {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$allocated_department = $ ("#allocated-department")
        this.$leave = $ ("#leave")
        this.$available_days = $("#available-days")
        this.$pending_applications = $("#pending-applications")
        this.$approved_applications = $("#approved-applications")
        this.$overall_totals = $("#total-days")
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()
    }

    async init_dashboard(){
        const dashboard_content = await lite.connect.dashboard("leave_allocation")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            // console.log(this.data)
            const leave = this.data.leave_usage
            if (this.data.allocated_employees.length <= 0) {
                this.utils.add_empty_component ({
                    $wrapper: this.$leave,
                    text: "No Content",
                    color: "slate",
                    classnames: "h-[80%] w-full absolute top-0 left-0"
                })
            }else {
                this.$leave.append (this.html_generator.allocation_view(this.data.allocated_employees)) 
            }
            this.$available_days.html (leave.available_days)
            this.$approved_applications.html (leave.approved_applications)
            this.$pending_applications.html (leave.pending_applications)
            this.$overall_totals.html (leave.total_days)
            this.init_charts()
        }
        
        lite.utils.init_dashboard(true)
    }
    init_charts(){
        this.leave_allocation_leave_type()
    }
    leave_allocation_leave_type(){
        const data = {
            values: [1900, 509, 549, 120],
            labels: ["Annual Leave", "Casual Leave", "Sick Leave", "Maternity Leave"]
        }
        lite.charts.semi_donut_chart ('leave-allocation-by-leave-type', data.labels, data.values, {
            height: "100%",
            width: "100%",
            legend_position: 'bottom',
        })
    }
}

export default Allocation 






















