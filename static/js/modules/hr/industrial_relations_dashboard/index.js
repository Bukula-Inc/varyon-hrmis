

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

export default class Employee_Grievance {
    constructor(config) {
        this.html_generator = new HR_HTML_GENERATOR ()
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect

        this.$total_grievances_rate = $("#total_grievances_rate")
        this.$resolved_percentage = $("#resolved_percentage")
        this.$resolution_rate = $("#resolution_rate")
        this.$recent_grievance_submissions = $("#recent_submissions")
        this.$recent_actions = $("#recent_actions")
        this.init_dashboard()
    }
    async init_dashboard(){
        const ind_rel_dash = await lite.connect.dashboard("industrial_relations_dashboard")
        if (ind_rel_dash.status === lite.status_codes.ok) {
            this.ind_rel_data = ind_rel_dash.data; 
            console.log(this.ind_rel_data);
            lite.utils.count_figure(this.$total_grievances_rate, this.ind_rel_data?.get_grievance_stats?.total_grievances_percentage)
            lite.utils.count_figure(this.$resolved_percentage, this.ind_rel_data?.get_grievance_stats?.total_resolved_grievances_percentage)
            lite.utils.count_figure(this.$resolution_rate, this.ind_rel_data?.get_grievance_stats?.resolution_rate)
            this.init_charts ()
        }
        lite.utils.init_dashboard(true)
    }
    init_charts () {
        this.#escalated_cases_quartery()
        this.#discipline_by_department ()
        this.#grievance_by_type ()
        this.#employee_attendance_punctuality ()
        this.#employee_turn_over_and_retention ()
        this.#recent_grievances()
        this.#recent_actions()
    }

    #escalated_cases_quartery() {
        const escalated_issues = this.ind_rel_data.escalated_cases
        if (!escalated_issues) {
            lite.utils.add_empty_component({
                $wrapper: $('#performance_rate_after_discipline'),
                text: "No Data",
                color: "gray",
                classnames: "absolute w-full h-full"
            });
        }else {
            const data = {
                labels: ["First Quarter", "Second Quarter", "Third Quarter", "Fourth Quarter"], 
                values: [
                    escalated_issues.Q1?.["Escalate To Disciplinary"] || 0,
                    escalated_issues.Q2?.["Escalate To Disciplinary"] || 0,
                    escalated_issues.Q3?.["Escalate To Disciplinary"] || 0,
                    escalated_issues.Q4?.["Escalate To Disciplinary"] || 0
                ] 
            };
        
            lite.charts.line_chart('performance_rate_after_discipline', data.labels, data.values, {
                enable_markers: true,                
                series_title: 'Escalated Grievance', 
                curve: 'straight',                   
                markers_color: lite.charts.negative_colors[5], 
                line_color: lite.charts.negative_colors[5],    
                stroke_size: 2,                      
                height: 250,                         
                formatter: value => `${value} Grievances`, 
                x_axis_style: {                      
                    fontSize: "10px",
                    colors: ["purple","blue", "green", "orange","red","#3fd321","#d3a521","#9f21d3","#216fd3","#6f21d3","#0ec1b0","#620ec1"]
                }
            });
        }
    }
    #discipline_by_department() {
        const action_by_depart = this.ind_rel_data?.descipline_by_department;
        if (!action_by_depart) {
            lite.utils.add_empty_component({
                $wrapper: $('#discipline_by_department'),
                text: "No Data",
                color: "gray",
                classnames: "absolute w-full h-full"
            });
        }else {
            const labels = Object.keys(action_by_depart); 
            const values = [];    
            Object.keys(action_by_depart).forEach(department => {
                Object.keys(action_by_depart[department]).forEach(grievance => {
                    const existingGrievance = values.find(g => g.name === grievance);
                    if (existingGrievance) {
                        existingGrievance.data[labels.indexOf(department)] = action_by_depart[department][grievance];
                    } else {
                        values.push({
                            name: grievance,
                            data: new Array(labels.length).fill(0)
                        });
                        values[values.length - 1].data[labels.indexOf(department)] = action_by_depart[department][grievance];
                    }
                });
            });
                const data = {
                values,
                labels
            };    
            lite.charts.stacked_column_chart('discipline_by_department', data.labels, data.values, {
                enable_markers: true,
                stroke_size: 2,
                height: "90%"
            });
        }
    }
    #grievance_by_type() {
        const data = this.ind_rel_data?.grievance_types_per_month || [];
        if (!data) {
            lite.utils.add_empty_component({
                $wrapper: $('#grievance_by_type'),
                text: "No Data",
                color: "gray",
                classnames: "absolute w-full h-full"
            });
        }else {
            if (!Array.isArray(data)) {
                console.error("Invalid data");
                return;
            }
        
            const labels = data.map(item => item.month);
            const values = [
                {
                    name: "Grievances",
                    data: data.map(item => item.count)
                }
            ];
        
            lite.charts.multi_line_chart('grievance_by_type', labels, values, {
                enable_markers: true,
                stroke_size: 2,
                height: "90%"
            });
        }
    }

    #employee_attendance_punctuality () {
        const grievance_by_status = this.ind_rel_data?.grievances_by_status || undefined
        if (!grievance_by_status || !lite.utils.object_has_data(grievance_by_status)) {
            lite.utils.add_empty_component({
                $wrapper: $('#employee_attendance_punctuality'),
                text: "No Data",
                color: "gray",
                classnames: "absolute w-full h-full"
            });
        }else {
            const values = Object.values(grievance_by_status)
            const labels = Object.keys(grievance_by_status)
            lite.charts.donut_chart ('employee_attendance_punctuality', labels, values, {
                show_legend: false,
                plot_show: true,
                width: "90%",
                height: "90%"
            })
        }
    }
    #employee_turn_over_and_retention () {
        const emp_retention = this.ind_rel_data ?.employee_retentions || {}
        if (!emp_retention) {
            lite.utils.add_empty_component({
                $wrapper: $('#employee_turn_over_and_retention'),
                text: "No Data",
                color: "gray",
                classnames: "absolute w-full h-full"
            });
        }else {
            const values = Object.values(emp_retention) 
            const labels = Object.keys(emp_retention)
            lite.charts.pie_chart ('employee_turn_over_and_retention', labels, values, {
                show_legend: false,
                plot_show: true,
                width: "90%",
                height: "90%"
            })
        }
    }
    #recent_grievances(){
        const recent_submisions = this.ind_rel_data?.recent_grievances
        
        if (!recent_submisions || !lite.utils.object_has_data(recent_submisions)){
            lite.utils.add_empty_component({ $wrapper: $('#recent_submissions'), text: "No Recent Grievance", color: "default", classnames: "absolute w-full h-full" })
        }else {
            $('#recent_submissions').append(this.html_generator.recent_grieves(recent_submisions))        
        }
    }
    #recent_actions(){
        const recent_actions = this.ind_rel_data?.recent_actions 
        if (!recent_actions || !lite.utils.object_has_data(recent_actions)){
            lite.utils.add_empty_component({ $wrapper: $("#recent_actions"), text: "No Recent Actions", color: "default", classnames: "absolute w-full h-full" })     
        }else {
            $("#recent_actions").append(this.html_generator.recent_actions(recent_actions))
        }
    }
}

