import HTML_Builder from '../../../page/html/html_builder.js'
import Staff_HTML_Generator from '../../../page/html/staff_html_generator.js'
export default class Staff_Dashboard {
    constructor() {
        this.builder = new HTML_Builder()
        this.generator = new Staff_HTML_Generator()
        this.$edit_basic_info = $('#edit_basic_info')
        this.$employee_basic_infor = $('#employee_basic_infor')
        this.$grievances = $('#grievances')

        this.$total_leave_days = $('#total_leave_dasy')
        this.$taken_days = $('#taken_days')
        this.$remaining_leave_days = $('#remaining_leave_days')

        this.$total_net_pay = $('#net_pay')
        this.$total_gross = $('#total_gross')
        this.$total_pension = $('#total_pension')
        this.$total_paye = $('#total_paye')
        this.$total_napsa = $('#total_napsa')

        this.$recent_leave_applications = $('#recents_leaves')
        this.$employee_payslips = $('#employee_payslips')
        this.$add_employee_file = $('#add_employee_file')
        this.init_dashboard()
    }

    async init_dashboard(){
        const dashboard = await lite.connect.dashboard("staff", {emp: lite.employee_info.name})
        
        
        if(dashboard.status == lite.status_codes.ok){
            this.data = dashboard.data
            console.log(this.data);
            lite.utils.count_figure( this.$total_leave_days, this.data?.staff_infor?.total_leave_days)
            lite.utils.count_figure( this.$taken_days, this.data?.staff_infor?.used_leave_days)
            lite.utils.count_figure( this.$remaining_leave_days, this.data?.staff_infor?.remaining_leave_days)

            lite.utils.count_figure( this.$total_gross, this.data?.staff_infor?.total_gross)
            lite.utils.count_figure( this.$total_pension, this.data?.staff_infor?.total_pension)
            lite.utils.count_figure( this.$total_net_pay, this.data?.staff_infor?.total_net)
            lite.utils.count_figure( this.$total_gross, this.data?.staff_infor?.total_gross)
            lite.utils.count_figure( this.$total_pension, this.data?.staff_infor?.total_pension)
            lite.utils.count_figure( this.$total_paye, this.data?.staff_infor?.total_paye)
            lite.utils.count_figure( this.$total_napsa, this.data?.staff_infor?.total_napsa)
            this.init_charts ()
        }
        lite.utils.init_dashboard(true)
    }

    init_charts () {
        this.leave_allocations ()
        this.#target_metrics ()
        // this.leave_utilization ()
        this.task_stats ()
        this.#staff_dash_infro()
        this.#recent_payslips()
        this.#staff_grievance()
        // this.leave_summary_chart()
        this.workplan()
        this.earnings_and_deductions()
        this.recent_leaves()
    }
    #staff_dash_infro(){
        const get_emp = this.data?.staff_infor
        if (!get_emp || !lite.utils.object_has_data(get_emp)) {
            lite.utils.add_empty_component({ $wrapper: this.$employee_basic_infor, text: "No Employee Infor", color: "default", classnames: "absolute" })
        } else {
            this.$employee_basic_infor.append(this.generator.staff_stats_infor(get_emp))
        }
    }
    #recent_payslips(){
        const emp_payslips = this.data?.payslips
        console.log(emp_payslips);
        
        if (!emp_payslips || !lite.utils.object_has_data(emp_payslips)) {
            lite.utils.add_empty_component({ $wrapper: this.$employee_payslips, text: "No Employee Infor", color: "default", classnames: "absolute" })
        } else {
            this.$employee_payslips.append(this.generator.payslips_infor(emp_payslips))
        }
    }
    #staff_grievance(){
        const employee_grievance = this.data?.grievance || []
        if (!employee_grievance || !lite.utils.object_has_data(employee_grievance)) {
            lite.utils.add_empty_component({ $wrapper: this.$grievances, text: "No Employee Infor", color: "default", classnames: "absolute" })
        } else {
            this.$grievances.append(this.generator.recent_grievance(employee_grievance))
        }
    }
    recent_leaves(){
        const get_recent_leave_application  = this.data?.leave_application || []
        if (!get_recent_leave_application || lite.utils.object_has_data(get_recent_leave_application)){
            lite.utils.add_empty_component({ $wrapper: this.$recent_leave_applications, text: "No Recent applications", color: "default", classnames: "absolute" })
        }else{
            this.$recent_leave_applications.append(this.generator.recent_leave_applications(get_recent_leave_application))
        }
    }
    leave_allocations() {
        const leaveAllocations = this.data?.leave_allocations || [];
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const leaveTypes = {};
        leaveAllocations.forEach(allocation => {
            Object.keys(allocation).forEach(key => {
                if (key !== "month" && !leaveTypes[key]) {
                    leaveTypes[key] = {
                        name: key,
                        data: Array(months.length).fill(NaN)
                    };
                }
            });
        });
        leaveAllocations.forEach(allocation => {
            const monthIndex = months.indexOf(allocation.month);
            if (monthIndex !== -1) {
                Object.keys(allocation).forEach(key => {
                    if (key !== "month" && leaveTypes[key]) {
                        leaveTypes[key].data[monthIndex] = allocation[key];
                    }
                });
            }
        });
        const data = {
            values: Object.values(leaveTypes),
            labels: months
        };
        lite.charts.multi_line_chart('leave_allocations', data.labels, data.values, {
            enable_markers: true,
            stroke_size: 2,
            height: "90%"
        });
    }
    workplan() {
        const earnings_deductions = this.data?.payroll_infor;
        const allMonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const labels = allMonths;
        const values = allMonths.map(month => {
            const monthData = earnings_deductions.find(item => item.month === month);
            return monthData ? monthData.earning : 0;
        });

        const data = {
            labels,
            values
        };

        lite.charts.line_chart('workplan', data.labels, data.values, {
            enable_markers: true,
            series_title: 'Earnings',
            curve: 'straight',
            markers_color: lite.charts.negative_colors[5],
            line_color: lite.charts.negative_colors[5],
            stroke_size: 2,
            height: 200,
            formatter: value => `K ${value}`,
            x_axis_style: {
                fontSize: "10px",
                colors: ["purple", "blue", "green", "orange", "red", "#3fd321", "#d3a521", "#9f21d3", "#216fd3", "#6f21d3", "#0ec1b0", "#620ec1"]
            }
        });
    }
    task_stats() {
        const raw_stats = this.data?.work_plan_stats || [];

        const allQuarters = ["2025Q1", "2025Q2", "2025Q3", "2025Q4"];

        const statsMap = {};
        raw_stats.forEach(stat => {
            statsMap[stat.quarter] = stat;
        });

        const pendingData = [];
        const completedData = [];
        const delayedData = [];

        allQuarters.forEach(q => {
            const stat = statsMap[q] || {};
            pendingData.push(stat.Pending || 0);
            completedData.push(stat.Completed || 0);
            delayedData.push(stat.Delayed || 0);
        });

        const datasets = [
            {
                name: 'Pending',
                data: pendingData,
                borderColor: lite.charts.negative_colors[5],
                backgroundColor: lite.charts.negative_colors[5],
            },
            {
                name: 'Completed',
                data: completedData,
                borderColor: 'green',
                backgroundColor: 'green',
            },
            {
                name: 'Delayed',
                data: delayedData,
                borderColor: 'blue',
                backgroundColor: 'blue',
            }
        ];

        lite.charts.multi_line_chart('work-task-stats', allQuarters, datasets, {
            enable_markers: true,
            curve: 'straight',
            height: 300,
            width: 200,
            formatter: value => `${value}`,
            tooltip: {
                formatter: (seriesName, value) => `${seriesName}: ${value}`
            },
            x_axis_style: {
                fontSize: "10px"
            }
        });
    }

    #target_metrics () {
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const data = {
            values: [
                {
                    name: "Completed On Time",
                    data: Array(months.length).fill(0)
                },
                {
                    name: "Complete After Due Date",
                    data: Array(months.length).fill(0)
                },
                {
                    name: "Pending",
                    data: Array(months.length).fill(0)
                },
                {
                    name: "In Progress",
                    data: Array(months.length).fill(0)
                },
                {
                    name: "Over Due",
                    data: Array(months.length).fill(0)
                },
            ],
            labels: months
        }
        lite.charts.line_chart('target_metrics', data.values, data.labels, {
            enable_markers: true,
            stroke_size: 2,
            height: "90%",
            colors: ["#008FFB", "#00E396", "#FEB019", "#FF4560", "#775DD0"]
        })
    }
    earnings_and_deductions() {
        const earnings_deductions = this.data?.payroll_infor;
        const allMonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const earnings = allMonths.map(month => {
            const monthData = earnings_deductions.find(item => item.month === month);
            return monthData ? monthData.earning : 0;
        });
        const deductions = allMonths.map(month => {
            const monthData = earnings_deductions.find(item => item.month === month);
            return monthData ? monthData.deduction : 0;
        });

        const data = {
            values: [
                {
                    name: "Earnings",
                    data: earnings
                },
                {
                    name: "Deductions",
                    data: deductions
                }
            ],
            labels: allMonths
        };

        lite.charts.column_chart('earnings_deductions_chart', data.labels, data.values, {
            bar_grouped: true,
            width: "45%",
            height: "95%",
            colors: ["#3b82f6", "#22c55e"],
            title: "Monthly Earnings and Deductions",
            enable_tooltips: true,
            xaxis_title: "Month",
            yaxis_title: "Amount",
        });
    }
}

