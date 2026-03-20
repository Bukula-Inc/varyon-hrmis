

import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'

export default class Performance_Dashboard {
    constructor() {   
        this.generator = new HR_HTML_Generator ()
        this.$work_plan_task_progress = $("#top-performing-employees")
        this.$self_appraisal = $(".self_appraisal-score ")
        this.$appraisal = $ (".score-appraisal-360")
        this.$overall_apprisal = $ (".total-overall-appraisals")
        this.$performance_by_department = $(".performance-by-department")
        this.$employee_attendance = $("#employee-performance")
        this.$employee_by_status_wrapper = $("#employee-by-status")
        this.$employee_by_status = $(".employee-by-status")
        this.$employees_by_status_wrapper = $("#employee-by-status")
        this.$performance_by_gender_wrapper = $("#peformance-by-gender")
        this.$appraisals_by_departs_wrapper = $("#appraisals-by-departs-wrapper")
        this.$performance_by_gender = $(".peformance-by-gender")
        this.$pending_tasks = $(".pending-tasks")
        this.$completed_tasks = $(".completed-tasks")
        this.$total_tasks = $(".total-tasks")
        this.$task_in_progress = $(".task-in-progress")
        this.init_dashboard()
    }

    async init_dashboard(){
        const dashboard_content = await lite.connect.dashboard("performance_dashboard")
        lite.utils.init_dashboard(true)

        if(dashboard_content.status === lite.status_codes.ok){
            this.data = dashboard_content.data
        }
        this.populate_performance_by_department()
        this.work_plan_task_progress()
        this.populate_appraisal_by_type()
        this.populate_performance_by_gender()
        this.populate_employees_by_status()
        this.Performance_by_depts()
        this.task_progress_summary()
        this.employee_attendance()
    
    }



    task_progress_summary(){
        lite.utils.count_figure(this.$task_in_progress, this.data?.get_work_plan_stats_by_depts.in_progress)
        lite.utils.count_figure(this.$pending_tasks, this.data?.get_work_plan_stats_by_depts.pending)
        lite.utils.count_figure(this.$completed_tasks, this.data?.get_work_plan_stats_by_depts.completed)
        lite.utils.count_figure(this.$total_tasks, this.data?.get_work_plan_stats_by_depts.total_tasks)
        
        
    }
    


    work_plan_task_progress() {
        const work_plan_task_progress = this.data?.work_plan_task_progress
        
        if(work_plan_task_progress && lite.utils.object_has_data(work_plan_task_progress)){

            this.$work_plan_task_progress.append(this.generator.employee_performance(work_plan_task_progress))
        
        }
        else
            lite.utils.add_empty_component ({$wrapper: this.$work_plan_task_progress, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
    } 

    employee_attendance() {
        const attendance =  this.data?.employee_attendance
        console.log(attendance)
        
        if(attendance && lite.utils.object_has_data(attendance)){

            this.$employee_attendance.append(this.generator.employee_attendance(attendance))
        
        }
        else
            lite.utils.add_empty_component ({$wrapper: this.$employee_attendance, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
    } 

    populate_appraisal_by_type() {
        const appraisals_by_type = this.data?.appraisals_by_type
        if (!this.data?.appraisals_by_type || this.data?.appraisals_by_type.length == 0) {
            lite.utils.add_empty_component ({$wrapper: $ ("#employee-info-wrapper"), text: "No Content Found", color: "gray",classnames:"relative h-5 "})
        }else {
            this.$overall_apprisal.html(this.data?.appraisals_by_type?.overall_total)
            this.$self_appraisal.html(this.data?.appraisals_by_type?.self_appraisals)
            this.$appraisal.html(this.data?.appraisals_by_type?.appraisals)
         
        
        }

    }

    Performance_by_depts () {
       const appraisals_by_dept = this.data.appraisals_by_dept
        if (appraisals_by_dept) {
            lite.charts.multi_line_chart ('appraisals-by-depts', this.data.appraisals_by_dept.labels, this.data.appraisals_by_dept.values, {
                legend_position: 'bottom',
                height: "90%",
                width: "100%"
            })
        }
        else{
            
            lite.utils.add_empty_component ({$wrapper: this.$appraisals_by_departs_wrapper, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
        }
        
    }


    populate_performance_by_department(){
        const by_department = this.data?.appraisal_performance_summary_department
        if(by_department && lite.utils.object_has_data(by_department)){
            $.each(lite.utils.get_object_keys(by_department).reverse(),(_,k)=>{
                if(_ < 5)
                    this.$performance_by_department.append(this.generator.create_performance_by_department_card(k,by_department[k]))
            })
        }
        else
            lite.utils.add_empty_component ({$wrapper: this.$performance_by_department, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
    }

    populate_performance_by_gender(){
        const by_gender = this.data?.peformance_by_gender
        if(by_gender){
            let data = {labels:[],values:[]}
            $.each(lite.utils.get_object_keys(by_gender),(_,k)=>{
                data.labels.push(k)
                data.values.push(by_gender[k])
            })
            lite.charts.donut_chart('peformance-by-gender', data.labels, data.values, {
                show_legend: false,
                plot_show: true,
                title: "Performance By Gender",
                width: 300,
                height: 250,
                colors: [
                    lite.charts.colors[1],
                    lite.charts.colors[0],
                    lite.charts.negative_colors[1],
                    lite.charts.colors[5]
                ]
            })
        }
        else
            lite.utils.add_empty_component ({$wrapper: this.$performance_by_gender_wrapper, text: "No Content Found", color: "gray"})
    }

   


    populate_employees_by_status(){
        const by_status = this.data?.employees_by_status
        if(by_status){
            let data = {labels:[],values:[]}
            $.each(lite.utils.get_object_keys(by_status),(_,k)=>{
                data.labels.push(k)
                data.values.push(by_status[k])
            })
            lite.charts.pie_chart('employee-by-status', data.labels, data.values, {
                title: "Employee by Status",
                width: 400,
                height: 250,
                colors: [
                    lite.charts.colors[1],
                    lite.charts.colors[0],
                    lite.charts.negative_colors[1],
                    lite.charts.colors[5]
                ]
            })
        }else {
           
            
            lite.utils.add_empty_component ({$wrapper: this.$employees_by_status_wrapper, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
        }

    }


    
}