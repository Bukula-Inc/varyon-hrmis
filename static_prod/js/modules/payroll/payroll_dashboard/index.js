
import Payroll_HTML_Generator from "../../../page/html/payroll_html_generator.js"
export default class Dashboard {
    constructor() {
        this.generator = new Payroll_HTML_Generator()
        this.$total_employees = $(".total-employees")
        this.$number_of_employes_on_payroll = $(".number-of-employes-on-payroll")
        this.$overtime_accrued = $(".overtime-accrued")
        this.$overtime_accrued_amount = $ (".overtime-accrued-amount")
        this.$recent_payments_list = $(".recent-payments-list")
        this.$cost_by_designation = $(".cost-by-designation")
        this.$regulatory_summary = $(".regulatory-summary")
        this.$next_payroll_date = $(".next-payroll-date")
        this.colors = [
            {base:"#dfe7ff", inner:"#3730a3"},
            {base:"#ffedd5", inner:"#993413"},
            {base:"#f3e7ff", inner:"#6b21a8"},
            {base:"#d1fae4", inner:"#065f46"},
            {base:"#dbe9fe", inner:"#1d40af"}
        ]
        this.init_dashboard()
        
    }
    async init_dashboard() {
        
        const dashboard_content = await lite.connect.dashboard("payroll")

        lite.utils.init_dashboard(true)
        if(dashboard_content.status === lite.status_codes.ok){
            this.data = dashboard_content.data
            this.populate_employee_info()
            this.populate_payroll_cost_summary()
            this.next_payroll_date()
            this.populate_recent_payments()
            this.populate_salary_advance_summary()
            this.populate_regulatory_summary()
            this.populate_payroll_cost_by_designation()
           
       
        }
    }

    populate_employee_info(){

        if (!this.data?.employee_info || this.data?.employee_info.length == 0) {
            lite.utils.add_empty_component ({$wrapper: $ ("#employee-info-wrapper"), text: "No Content Found", color: "gray",classnames:"relative h-5 "})
        }else {

            this.$total_employees.html(this.data?.employee_info?.total_employees)
            // this.$total_working_hours.html(this.data?.employee_info?.working_hours)
            this.$number_of_employes_on_payroll.html(this.data?.employee_info?.number_of_employes_on_payroll)
            this.$overtime_accrued.html(this.data?.overall_accrued_overtime.total_accrued_hours)
            this.$overtime_accrued_amount.html(this.data?.overall_accrued_overtime.total_accrued_overtime)
        
        }
       
    }

    next_payroll_date(){
      
        if (!this.data?.next_payroll_date || this.data?.next_payroll_date.length == 0) {
            lite.utils.add_empty_component ({$wrapper: $ ("#next-date-wrapper"), text: "No Content Found", color: "gray",classnames:"relative h-5 "})
        }else {

            this.$next_payroll_date.html(this.data.next_payroll_date)
        
        }
     
    }
    populate_payroll_cost_summary(){
        if (!this.data?.payroll_cost_summary || this.data?.payroll_cost_summary.length == 0) {
            lite.utils.add_empty_component ({$wrapper: $ ("#payroll-cost-summary-wrapper"), text: "No Content Found", color: "gray",classnames:"relative h-5 "})
        }else {

            if(lite.utils.array_has_data(this.data?.payroll_cost_summary)){
                let data = { labels: [], values: [] }
                $.each(this.data?.payroll_cost_summary,(_,cs)=>{
                    data.labels.push(cs.name)
                    data.values.push(cs.value)
                })
                lite.charts.donut_chart('payroll-cost-summary', data.labels, data.values, {
                    width: 300,
                    height: 240,
                    legend_position: 'bottom'
                })
            }
        
        }

    }

    populate_recent_payments(){
        if (!this.data?.recent_payments || this.data?.recent_payments.length == 0) {
            lite.utils.add_empty_component ({$wrapper: $ ("#recent-payments-wrapper"), text: "No Content Found", color: "gray",classnames:"relative h-5 "})
        }else {

            if(lite.utils.array_has_data(this.data?.recent_payments)){
                this.$recent_payments_list.empty()
                $.each(this.data.recent_payments,(_,rp)=>{
                    this.$recent_payments_list.append(this.generator.create_recent_payment_row(rp))
                })
            }
        
        }
   
    }

    populate_salary_advance_summary() {
        if (!this.data?.advance_info || this.data?.advance_info.length == 0) {
            lite.utils.add_empty_component ({$wrapper: $ ("#salary-advance-summary-wrapper"), text: "No Content Found", color: "gray",classnames:"relative h-5 "})
        }else {

            if(lite.utils.array_has_data(this.data?.advance_info)){
                let data = { labels: [], values: [] }
                $.each(this.data?.advance_info,(_,ai)=>{
                    data.labels.push(ai.name)
                    data.values.push(ai.value)
                })
                lite.charts.pie_chart('salary-advance-summary', data.labels, data.values, {
                    width: 300,
                    height: 240,
                    legend_position: 'bottom',
                    colors: [
                        lite.charts.colors[1],
                        lite.charts.colors[0],
                        lite.charts.negative_colors[1],
                        lite.charts.colors[5]
                    ]
                })
            }
        
        }


    }

    populate_regulatory_summary(){
      
        if (!this.data?.regulatory_summary || this.data?.regulatory_summary.length == 0) {
            lite.utils.add_empty_component ({$wrapper: $ ("#regulatory-summary-wrapper"), text: "No Content Found", color: "gray",classnames:"relative h-5 "})
        }else {
            console.log(this.data?.regulatory_summary)

            if(lite.utils.array_has_data(this.data?.regulatory_summary)){
                $.each(this.data?.regulatory_summary,(_,rs)=>{
                    this.$regulatory_summary.append(this.generator.create_regulatory_summary_row(rs))
                })
            }
        
        }

    }
    populate_payroll_cost_by_designation(){
     
        if (!this.data?.payroll_cost_by_designation || this.data?.payroll_cost_by_designation.length == 0) {
            lite.utils.add_empty_component ({$wrapper: $ ("#cost-by-designation-wrapper"), text: "No Content Found", color: "gray",classnames:"relative h-5 "})
        }else {

            if(lite.utils.array_has_data(this.data?.payroll_cost_by_designation)){
                $.each(this.data?.payroll_cost_by_designation,(_,c)=>{
                    this.$cost_by_designation.append(this.generator.create_cost_by_designation_row(c, this.colors[_]))
                })
            }
        
        }
    }

}