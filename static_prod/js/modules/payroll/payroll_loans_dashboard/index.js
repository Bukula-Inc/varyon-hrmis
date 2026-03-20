import Payroll_HTML_Generator from '../../../page/html/payroll_html_generator.js'

export default class Advance_And_Loan_Balances {
    constructor(config) {
        this.generator = new Payroll_HTML_Generator()
        this.$disbursement_repayment_defaults = $("#disbursement-repayment-default")
        this.$loan_by_dept = $("#loan_by_dept")
        this.$collection_vs_disbursement = $("#collection_vs_disbursement")
        this.$recent_advance_applications =$("#recent_advance_applications")
        this.$defaulted_advances =$("#defaulted_advances")
        $(".currency").html(lite?.user?.company?.reporting_currency)
        

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connection
        console.log("dashboard_content");
        this.init_dashboard()
    }

    async init_dashboard() {
        const dashboard_content = await lite.connect.dashboard("payroll_loans_dashboard")        
        if (dashboard_content.status == lite.status_codes.ok) {
            this.data = dashboard_content.data
            console.log(this.data);
            
            if (this.data.recent_applications){
                this.$recent_advance_applications.append(this.generator.recent_advance_applications(this.data.recent_applications))

            } else{               
                lite.utils.add_empty_component ({$wrapper: this.$recent_advance_applications, text: "No Content Found", color: "gray"}) 
            }

            if (this.data.disbursements_repayments_and_defaults){
                if (this.data.disbursements_repayments_and_defaults){
                    this.$defaulted_advances.append(this.generator.defaulted_advances(this.data.disbursements_repayments_and_defaults.default_data))
                }else{
                    lite.utils.add_empty_component ({$wrapper: this.$defaulted_advances, text: "No Content Found", color: "gray"})                
                }

                if (this.data.disbursements_repayments_and_defaults.trio_distribution){
                    this.#disbursement_repayment_defaults ()
                } else{
                    lite.utils.add_empty_component ({$wrapper: $("#disbursement-repayment-default"), text: "No Content Found", color: "gray"})                
                }
    
                if (!this.data.disbursements_repayments_and_defaults.default_data){
                    this.#collection_vs_disbursement ()
                } else{
                    lite.utils.add_empty_component ({$wrapper: $("#disbursement-repayment-default"), text: "No Content Found", color: "gray"})                
                }
            } else{
                lite.utils.add_empty_component ({$wrapper: this.$defaulted_advances, text: "No Content Found", color: "gray"})      
                lite.utils.add_empty_component ({$wrapper: $("#disbursement-repayment-default"), text: "No Content Found", color: "gray"})       
                lite.utils.add_empty_component ({$wrapper: $("#collection_vs_disbursement"), text: "No Content Found", color: "gray"})       
                lite.utils.add_empty_component ({$wrapper: $("#loan_by_dept"), text: "No Content Found", color: "gray"})      
            }

            if (this.data.advances_and_loans){

                $("#total_collected_amt_advance").html(this.data.advances_and_loans.Advance.collected_amount || 0.00)
                $("#total_disbursement_amt_advance").html(this.data.advances_and_loans.Advance.disbursed_amount || 0.00)

                $("#total_collected_amt_loan").html(this.data.advances_and_loans.Loan.collected_amount || 0.00)
                $("#total_disbursement_amt_loan").html(this.data.advances_and_loans.Loan.disbursed_amount || 0.00)
            } 

        }
        this.#loan_by_dept ()
        this.#collection_vs_disbursement ()
        lite.utils.init_dashboard(true)
    }

    #disbursement_repayment_defaults () {
        const data = {
            values: [1900, 509, 230],
            labels: ["Disbursement", "Repayment", "Default"]
        }
        lite.charts.donut_chart ('disbursement-repayment-default', this.data.disbursements_repayments_and_defaults.trio_distribution.labels, this.data.disbursements_repayments_and_defaults.trio_distribution.value, {
            show_legend: false,
            plot_show: true,
            width: "90%",
            height: "90%"
        })
    }
    #collection_vs_disbursement () {
        const data = {
            values: [
                {
                    name: "Advance Disbursement ZMW",
                    data: [39000, 23488, 1050,1440, 49900,3000 ]
                },
                {
                    name: "Loan Disbursement ZMW",
                    data: [90005, 25688, 10000, 440, 102, 5688 ]
                },
                {
                    name: "Advance Repayment ZMW",
                    data: [3900, 1200, 1050,4335, 90044,120 ]
                },
                {
                    name: "Loan Repayment ZMW",
                    data: [5849, 49883, 100, 120, 5660, 98827 ]
                },
            ],
            labels: ["Jan", "Fed", "Apr", "May", "Jun"]
        }
        lite.charts.multi_line_chart ('collection_vs_disbursement', data.labels, data.values, {
            enable_markers: true,
            stroke_size: 2,
            height: "90%"
        })
    }
    #loan_by_dept () {
        const data = {
            values: [
                {
                    name: "Advance",
                    data: [39000, 23488, 1050,1440 ]
                },
                {
                    name: "Loan",
                    data: [90005, 25688, 10000, 440 ]
                },
            ],
            labels: ["HR", "Customer Relations", "Operation", "Technical"]
        }
        lite.charts.multi_line_chart ('loan_by_dept', data.labels, data.values, {
            enable_markers: true,
            stroke_size: 2,
            height: "90%"
        })
    }
}


