import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'

export default class Recruitment_Dashboard {
    constructor() {   
        this.$generator = new HR_HTML_Generator ()
        this.$overview = $('.overview')
        this.$overview_stats = $('.overview-stats')
        this.$total_job_applications = $('#total_job_applications')
        this.$new_interviews = $('#new_interviews')
        this.$job_offers = $("#job_offers")
        this.$total_employees = $("#total_employees")
        this.$total_full_time  = $("#total_full_time")
        this.$total_interns = $("#total_interns")
        this.$published_job_openings = $("#published_job_openings")
        this.$resigned_employees = $("resigned_employees")
        this.$hires = $("#hires")
        this.$a_year = $("#a_year")
        this.$two_year = $("#two_year")
        this.$three_year_plus = $("#three_year_plus")
        this.$resigned = $("#resigned")
        this.$retired = $("#retired")
        this.$vacancies = $("#vacancies")
        this.$termination = $("#termination")
        this.$total_applicants_selected = $("#total_applicants_selected")
        this.init_dashboard()
    }

    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("recruitment_dashboard")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            console.log(this.data);
            lite.utils.count_figure(this.$total_job_applications, this.data?.job_application?.total_job_application)
            lite.utils.count_figure(this.$new_interviews, this.data?.get_interviews.new_interviews)
            lite.utils.count_figure(this.$job_offers, this.data?.job_offers.total_job_offers)
            lite.utils.count_figure(this.$total_employees, this.data?.retention?.total_employees)
            lite.utils.count_figure(this.$total_full_time, this.data?.retention?.employee_on_full_time)
            lite.utils.count_figure(this.$total_interns, this.data?.retention?.on_probation)
            lite.utils.count_figure(this.$published_job_openings, this.data?.overview?.published)
            lite.utils.count_figure(this.$resigned_employees, this.data?.retention.resigned)
            lite.utils.count_figure(this.$hires, this.data?.retention?.hires)
            lite.utils.count_figure(this.$a_year, this.data?.retention?.a_year)
            lite.utils.count_figure(this.$two_year, this.data?.retention?.two_year)
            lite.utils.count_figure(this.$three_year_plus , this.data?.retention?.three_year_plus )
            lite.utils.count_figure(this.$termination, this.data?.retention?.termination)
            lite.utils.count_figure(this.$resigned, this.data?.retention.resigned)
            lite.utils.count_figure(this.$retired, this.data?.retention?.retired)
            lite.utils.count_figure(this.$vacancies, this.data.retention?.vacancies)
            lite.utils.count_figure(this.$total_applicants_selected, this.data?.total_applicants_selected?.total_applicants_selected)
            this.init_charts(this.data)
        }
        lite.utils.init_dashboard(true)
    }
    init_charts () {
        this.job_application_by_dept ()
        this.outstanding_interviews()
    }


    create_empty_component($wrapper) {
        lite.utils.add_empty_component({
            $wrapper: $wrapper,
            text: "No Data",
            color: "gray",
            classnames: "absolute"
        });
    }

    populate_overview() {
        this.$overview.find('#total_employees').text(this.data.employees_metrics?.total || 0)
        this.$overview.find('#total_interns').text(this.data.employees_metrics.type_metrics?.intern || 0)
        this.$overview.find('#total_temps').text(this.data.employees_metrics.type_metrics?.temps || 0)
        this.$overview.find('#total_full_time').text(this.data.employees_metrics.type_metrics?.full_time || 0)
    }

    populate_overview_stats() {
        this.$overview_stats.find('.total-vacancies').text(this.data.job_openings?.vacancies || 0)
        this.$overview_stats.find('.total-applicants').text(this.data.job_applications?.applicants || 0)
        this.$overview_stats.find('.total-selected-applicants').text(this.data.applointment_leters?.applicants || 0)
        this.$overview_stats.find('.total-applicant-offers').text(this.data.job_offers?.applicants || 0)
    }

    populate_overview_stats_chart() {
        let labels = []
        let series_1 = []
        let series_2 = []

        if (labels != null && (series_1.length > 0 || series_2.length > 0)) {
            let series = [
                {
                    name: 'Total',
                    data: series_1.map(value => parseFloat(value).toFixed(2))
                },
            ]

            let data = {
                labels: labels,
                series: series
            }
            
            lite.charts.grouped_bar_chart('overview-stats-chart', data.labels, data.series, {
                height: '100%',
                column_width: '30%',
                show_legend: false,
            })
        }
        else {
            this.create_empty_component(this.$overview_stats.find('#overview-stats-chart'))
        }
    }

    populate_employee_retention() {
        this.$employee_retention.find('.one-year').text(this.data.employees_metrics?.one_year || 0)
        this.$employee_retention.find('.terminated').text(this.data.employees_metrics?.terminated || 0)
        this.$employee_retention.find('.two-years').text(this.data.employees_metrics?.two_years || 0)
        this.$employee_retention.find('.three-years-plus').text(this.data.employees_metrics?.three_years_plus || 0)
        this.$employee_retention.find('.retired').text(this.data.employees_metrics?.retired || 0)
        this.$employee_retention.find('.resigned').text(this.data.employees_metrics?.resigned || 0)
        this.$employee_retention.find('.vacancies').text(this.data.job_openings?.vacancies || 0)
    }

    populate_employee_retention_chart() {
        let labels = [];
        let series_data = [];

        if (sorted_income_items.length > 0) {
            let series = [
                {
                    name: 'Total',
                    data: series_data
                },
            ];

            let data = {
                labels: labels,
                series: series
            };

            lite.charts.column_chart('employee-retention-chart', data.labels, data.series, {
                height: '100%',
                column_width: '30%',
                show_legend: false,
            });
        } else {
            this.create_empty_component(this.$employee_retention.find('#employee-retention-chart'))
        }
    }
    outstanding_interviews() {
        const data = {
            labels: ["0-7 Days", "7-14 Days", "14-21 Days", "21-30 Days"], 
            values: [2, 3, 8, 9] 
        };
    
        lite.charts.line_chart('outstanding-Interviews', data.labels, data.values, {
            enable_markers: true,                
            series_title: 'Outstanding Interview', 
            curve: 'straight',                   
            markers_color: lite.charts.negative_colors[5], 
            line_color: lite.charts.negative_colors[5],    
            stroke_size: 2,                      
            height: 400,                         
            formatter: value => `${value} Interview`, 
            x_axis_style: {                      
                fontSize: "10px",
                colors: ["purple","blue", "green", "orange","red","#3fd321","#d3a521","#9f21d3","#216fd3","#6f21d3","#0ec1b0","#620ec1"]
            }
        });
    }
    job_application_by_dept() {
        const job_opening = this.data?.job_opening
            const labels = Object.keys(job_opening)
            const values = Object.values(job_opening)
        lite.charts.pie_chart ('top-grieved-person', labels, values, {
            legend_position: 'bottom',
            height: "90%",
            width: "100%"
        })
    }
}