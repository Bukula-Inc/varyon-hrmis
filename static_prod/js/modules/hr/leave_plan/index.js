import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'
export default class Leave_Plan{
    constructor(config){
        this.charts =config.charts
        this.hr_html_gen =new HR_HTML_Generator()
        this.$leave_type_stats =$("#leave-type-stats")
        this.$leave_balance =$("#leave-balance")
        this.init_side_view()

    }

    async init_side_view(){
        const side_view_content =await lite.connect.dashboard("leave_plan_sv")
        console.log(side_view_content)
        if(side_view_content.status ==lite.status_codes.ok){
            this.sv_data =side_view_content.data
            if(this.sv_data){
                if (!this.sv_data?.leave_type_data || this.sv_data?.leave_type_data.length <= 0) {
                    lite.utils.add_empty_component({$wrapper :this.$leave_balance, text: "No Leave Stats"})
                }else {
                    this.$leave_type_stats.append(this.hr_html_gen.leave_plan_sv_stats(this.sv_data?.leave_type_data))
                }
                this.init_charts()
            }
        }else {
            lite.utils.add_empty_component({$wrapper :this.$leave_balance, text: "No Leave Stats"})
            lite.utils.add_empty_component({$wrapper :this.$leave_type_stats, text: "No Leave Type Found"})
        }
    }

    init_charts(){
        if (!this.sv_data?.leave_summary) {
            lite.utils.add_empty_component({$wrapper :this.$leave_balance, text: "No Leave Stats"})
        }
        else {
            const leave_balance_data ={
                labels :["Used Leave", "Unused Leave"],
                values :[this.sv_data.leave_summary.used_days, this.sv_data.leave_summary.remaining_days]
            }
            this.charts.donut_chart("leave-balance", leave_balance_data.labels, leave_balance_data.values,{
                show_legend: false,
                plot_show: true,
                width: "90%",
                height: "90%"
            })
        }
    }
}