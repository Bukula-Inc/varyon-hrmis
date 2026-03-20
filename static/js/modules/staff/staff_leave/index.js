import HTML_Builder from '../../../page/html/html_builder.js'
import Staff_HTML_Generator from '../../../page/html/staff_html_generator.js'
export default class Staff_Leave_Summary {
    constructor() {

        this.builder = new HTML_Builder()
        this.generator = new Staff_HTML_Generator()
        this.user = {}
        this.$apply_for_leave_btn = $(".apply-for-leave")
        this.$total_leave_days = $('.total-leave-days')
        this.$available_leave_days = $('#available-days')
        this.$used_leave_days = $('#used-days')
        this.$leave_summary_by_type = $('.leave-summary-by-type')
        this.$leave_breakdown = $ ("#leave-breakdown")
        this.init_dashboard()
    }

    async init_dashboard(){
        lite.utils.add_empty_component ({
            $wrapper: this.$available_leave_days,
            text:"No Leave Days",
            color:"gray"
        })
        lite.utils.add_empty_component ({
            $wrapper: this.$used_leave_days,
            text:"No Used Leave Days",
            color:"gray"
        })
        const dashboard = await lite.connect.x_post("staff_leave_summary", {name: lite.employee_info?.name})
        lite.utils.init_dashboard(true)
        if(dashboard.status == lite.status_codes.ok){
            this.data = dashboard.data
            this.populate_leave_type ()
            this.populate_leave_content()
        }
        else{
            this.$apply_for_leave_btn.remove()
            lite.utils.add_empty_component({$wrapper:this.$leave_summary_by_type,text:"No Content", color:"gray"})
        }

    }

    populate_leave_type () {
        const leave_types =  this.data.leave_breakdown
        if (leave_types.length <= 0) {
            lite.utils.add_empty_component({$wrapper: $("#leave-breakdown-h"),text:"No Content", color:"gray"})
        }else {
            this.$leave_breakdown.append (this.generator.leave_breakdown (leave_types))
            let used = {
                labels: [],
                values: []
            }
            let available = {
                labels: [],
                values: []
            }
            leave_types.forEach (lt => {
                available.labels.push (lt?.leave_type || "")
                available.values.push (lt?.remaining_days || 0)
                used.labels.push (lt?.leave_type || "")
                used.values.push (lt?.used_days || 0)
            })
            this.$available_leave_days.html ('')
            this.$used_leave_days.html ('')
            console.log('====================================');
            console.log(used);
            console.log('====================================');

            lite.charts.donut_chart ("available-days", available.labels, available.values, {
                height: '100%',
                show_legend: false,
                // plot_show: true,
                legend_position:"bottom",
                // colors: [lite.charts.colors[3], lite.charts.colors[2], lite.charts.colors[1], lite.charts.colors[0]]
            })

            lite.charts.donut_chart ("used-days", used.labels, used.values, {
                height: '100%',
                show_legend: false,
                // plot_show: true,
                legend_position:"bottom",
                // colors: [lite.charts.colors[1], lite.charts.colors[3], lite.charts.colors[1], lite.charts.colors[0]]
            })
        }
    }
}
