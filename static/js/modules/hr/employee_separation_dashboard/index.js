import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'
export default class Dashboard {
    constructor(config) {
        this.utils = config.utils
        this.hr = new HR_HTML_Generator()
        this.$separation_trends = $("#separation_trends")
        this.$employee_under_discipline = $("#employee_under_discipline")
        this.$separation_by_gender = $("#separation_by_gender")
        this.$separation_by_dept = $("#separation_by_dept")
        this.$new_separation = $("#new_separation")
        this.$separation_trends = $("#separation_trends")
        this.$employees_under_discipline =$("#employees_under_discipline")
        this.$star_rates =$("#star-rating")
        
        $(".currency").html(lite?.user?.company?.reporting_currency)
        this.data
        this.init_dashboard()
    }

    async init_dashboard() {
        const dashboard_content = await lite.connect.dashboard("employee_separation_dashboard")  
        if (dashboard_content.status ==lite?.status_codes.ok){
            this.data =dashboard_content.data


            if (this.data.separation_trends.monthly){
                this.#separation_trends ()
            }else{
                lite.utils.add_empty_component ({$wrapper: $("#separation_trends"), text: "No Content Found", color: "gray"})         
            }
            if (this.data.separation_trends.gender){
                this.#separation_by_gender ()
            }else{
                lite.utils.add_empty_component ({$wrapper: $("#separation_by_gender"), text: "No Content Found", color: "gray"})                  
            }
            if (this.data.separation_trends.departmental){
                this.#separation_by_dept ()
            }else{
                lite.utils.add_empty_component ({$wrapper: $("#separation_by_dept"), text: "No Content Found", color: "gray"})
            }
            if (this.data.emp_under_disciplinary){
                this.$employees_under_discipline.append(this.hr.emp_under_disciplinary(this.data.emp_under_disciplinary))
            }else{
                lite.utils.add_empty_component ({$wrapper: this.$employees_under_discipline, text: "No Content Found", color: "gray"})                    
            }
            if (this.data.recent_separations){
                this.$new_separation.append(this.hr.recent_separations(this.data.recent_separations))
            }else{
                lite.utils.add_empty_component ({$wrapper: this.$new_separation, text: "No Content Found", color: "gray"})                    
            }
            if (this.data.emp_settlement){
                $("#settlement_rate").html(lite?.utils.thousand_separator(this.data.emp_settlement?.rate*100 || 0.00, lite?.defaults?.currency_decimals))
                $("#pending_amt").html(lite?.utils.thousand_separator(this.data.emp_settlement?.amount_pending || 0.00, lite?.defaults?.currency_decimals))
                $("#concluded").html(lite?.utils.thousand_separator(this.data.emp_settlement?.amount_con || 0.00, lite?.defaults?.currency_decimals))
                $("#overall_rate").html(lite?.utils.thousand_separator(this.data.emp_settlement?.overall_rate || 0.00, lite?.defaults?.currency_decimals))
                $("#leave_value_paid").html(lite?.utils?.thousand_separator(this.data.emp_settlement?.leave_value_paid || 0.00, lite?.defaults?.currency_decimals))
                $("#gratuity_value_paid").html(lite?.utils?.thousand_separator(this.data.emp_settlement?.gratuity_value_paid || 0.00, lite?.defaults?.currency_decimals))

                this.$star_rates.append(this.hr.separation_settlements(this.data.emp_settlement?.overall_rate))
                console.log(this.data.emp_settlement?.overall_rate);                
            }
            console.log(dashboard_content)
        } 
    }


    #separation_by_gender () {
        lite.charts.donut_chart ('separation_by_gender', this.data.separation_trends.gender.labels, this.data.separation_trends.gender.value, {
            show_legend: false,
            plot_show: true,
            width: "90%",
            height: "90%"
        })
    }

    #separation_trends () {
        lite.charts.multi_line_chart ('separation_trends', this.data?.separation_trends?.monthly?.labels, this.data?.separation_trends?.monthly.values, {
            enable_markers: true,
            stroke_size: 2,
            height: "90%"
        })
    }
    #separation_by_dept () {
        lite.charts.multi_line_chart ('separation_by_dept', this.data?.separation_trends?.departmental?.labels, this.data?.separation_trends?.departmental.values, {
            enable_markers: true,
            stroke_size: 2,
            height: "90%"
        })
    }
}