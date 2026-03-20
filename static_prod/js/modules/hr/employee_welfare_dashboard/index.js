import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'
export default class Employee_Welfare {
    constructor(config) {
        this.generator = new HR_HTML_Generator ()
        this.$finance_by_welfare = $("#finance_by_welfare")
        this.$trending_welfare = $("#trending_welfare")
        this.$approved_amount = $ ("#total_approved_amount") 
        this.$rejected_amount = $ ("#rejected_amount")
        this.$participated_emps = $ ("#total_participants")
        this.$non_participants = $ ("#non_participants")
        this.$recent_welfare = $ ("#recent_welfare")
        this.$total_welfare = $ ("#total_welfares")
        this.$total_welfare_rejceted = $ ("#total_welfare_rejceted")
        this.$approved_welfares = $ ("#approved_welfares")
        this.$participation_rate = $ ("#participation_rate")
        $(".currency").html(lite?.user?.company?.reporting_currency)
        this.init_dashboard()
    }

    async init_dashboard() {
        const fetch_dashboard_data =await lite?.connect?.dashboard("welfare_dashboard")
        
        if (fetch_dashboard_data.status ==lite?.status_codes?.ok){
            this.data =fetch_dashboard_data.data
            console.log(this.data);
            
            lite.utils.count_figure(this.$approved_amount, this.data?.total_approved_rejceted?.total_approved || 0)
            lite.utils.count_figure(this.$rejected_amount, this.data?.total_approved_rejceted?.rejected_amount || 0)
            lite.utils.count_figure(this.$participated_emps, this.data?.participants?.ytd_total_participants || 0)
            lite.utils.count_figure(this.$non_participants, this.data?.participants?.ytd_num_never_participated || 0)

            lite.utils.count_figure(this.$total_welfare, this.data?.welfare_stats?.total_welfare || 0)
            lite.utils.count_figure(this.$approved_welfares, this.data?.welfare_stats?.approved_programs || 0)
            lite.utils.count_figure(this.$total_welfare_rejceted, this.data?.welfare_stats?.rejected_programs || 0)
            lite.utils.count_figure(this.$participation_rate, this.data?.welfare_stats?.participation_rate || 0)

            this.init_charts ()

        }

        lite.utils.init_dashboard(true)
    }
    init_charts(){
        this.on_going_training_programs()
        this.total_expense_monthly()
        this.top_participation_welfare()
        this.recent_welfares()
    }
    recent_welfares(){
        const get_recent_expenses = this.data?.get_welfare_applications || []
        if (get_recent_expenses.length > 0){
            this.$recent_welfare.append(this.generator.recent_welfare(get_recent_expenses))
        }else{
            lite.utils.add_empty_component ({
                $wrapper: $("#recent_welfare"), 
                text: "No Content Found", 
                color: "gray"
            })         
        }
    }

    on_going_training_programs() {
        const trainingPrograms = this.data?.on_going_training_program;
        if (trainingPrograms) {
            const { labels, values } = Object.entries(trainingPrograms).reduce((acc, [key, value]) => {
            acc.labels.push(key);
            acc.values.push(value);
            return acc;
            }, { labels: [], values: [] });

            if (labels.length && values.length) {
            lite.charts.pie_chart('training_program_participation', labels, values, {
                legend_position: 'bottom',
                height: "90%",
                width: "100%"
            });
            } else {
            console.log('No data for chart');
            }
        } else {
            console.log('No training programs data');
        }
        }
    top_participation_welfare (){
        const data = {
            values: [1900, 509, 549, 120],
            labels: ["Resolved", "Pending", "Inprogress", "Overdue"]
        }
        lite.charts.donut_chart ('top_participation_welfare', data.labels, data.values, {
            height: "50%",
            width: "50%",
            legend_position: 'bottom',
        })
    } 
    total_expense_monthly() {
        const get_quartery_data = this.data?.get_training_program_expenses?.quarterly_expenses

        const data = {
            labels: ["Q1", "Q2", "Q3", "Q4"],
            values: [get_quartery_data?.first_quarter || 0, get_quartery_data?.second_quarter || 0, get_quartery_data?.third_quarter || 0, get_quartery_data?.fourth_quarter || 0]
        };

        lite.charts.line_chart('total-expense-monthly', data.labels, data.values, {
            enable_markers: true,
            series_title: 'Amount Spent Quarterly',
            curve: 'straight',
            markers_color: lite.charts.negative_colors[5],
            line_color: lite.charts.negative_colors[5],
            stroke_size: 2,
            height: 200,
            formatter: value => `${value}`,
            x_axis_style: {
                fontSize: "10px",
            }
        });
    }
}


