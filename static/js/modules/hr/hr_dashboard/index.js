

import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'

export default class Dashboard {
    constructor() {   
        this.data = undefined
        this.generator = new HR_HTML_Generator ()
        this.$total_employees = $(".total-employees")
        this.$employees_by_gender_wrapper = $(".employees-by-gender")
        this.$employee_by_department = $(".employee-by-department")
        this.$employee_by_designation = $(".employees-by-designation")
        this.$employee_files = $(".employee-files")
        this.$active_employees = $(".active-employees")
        this.$employees_on_leave = $(".employees-on-leave")
        this.$resigned_employees = $(".resigned-employees")
        this.$total_leave_days = $(".total-leave-days")
        this.$pending_leave_applications = $(".pending-leave-applications")
        this.$approved_leave_applications = $(".approved-leave-applications")
        this.$total_leave_available_days = $(".total-available-days")
        this.$open_disciplinary_cases = $(".open-disciplinary-cases")
        this.$closed_disciplinary_cases = $(".closed-disciplinary-cases")
        this.$open_grievance_cases = $(".open-grievance-cases")
        this.$closed_grievance_cases = $(".closed-grievance-cases")
        this.$attendance_summary = $ ("#attendance-summary-chart")
        this.init_dashboard()
    }

    async init_dashboard(){
        const dashboard_content = await lite.connect.dashboard("hr")
        lite.utils.init_dashboard(true)

        if(dashboard_content.status === lite.status_codes.ok){
            this.data = dashboard_content.data
            console.log(this.data)
        }
        this.populate_total_employees()
        this.populate_employees_by_designation()
        this.populate_employees_by_gender()
        this.populate_employees_by_department()
        this.populate_leave_summary()
        this.populate_employees_disciplinary()
        this.populate_employees_by_status()
        this.populate_attendance_summary ()
    }

    populate_total_employees(){
        if(this.data.total_employees){
            lite.utils.count_figure(this.$total_employees,this.data.total_employees)
        }
    }

    populate_employees_by_designation(){
        const by_designation = this.data?.employees_by_designation
        if(by_designation && lite.utils.object_has_data(by_designation)){
            $.each(lite.utils.get_object_keys(by_designation).reverse(),(_,k)=>{
                if(_ < 9)
                    this.$employee_by_designation.append(this.generator.create_employee_designation_card(k,by_designation[k]))
            })
        }
        else
            lite.utils.add_empty_component ({$wrapper: this.$employee_by_designation, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
    }

    populate_attendance_summary () {
        const attendance_data = {}
        if (!lite.utils.object_has_data (attendance_data)) {
            lite.utils.add_empty_component ({$wrapper: this.$attendance_summary, text: "No Content Found", color: "gray"})
        }else {
            lite.charts.pie_chart('employees-by-gender', data.labels, data.values, {
                title: "Employees By Gender",
                width: 250,
                height: 150,
                colors: [lite.charts.colors[4], lite.charts.colors[2]]
            })
        }
    }
    populate_employees_by_gender(){
        const by_gender = this.data?.employees_by_gender
        if(by_gender){
            let data = {labels:[],values:[]}
            $.each(lite.utils.get_object_keys(by_gender),(_,k)=>{
                data.labels.push(k)
                data.values.push(by_gender[k])
            })
            lite.charts.donut_chart('employees-by-gender', data.labels, data.values, {
                title: "Employees By Gender",
                // width: 250,
                height: 225,
                show_legend: false,
                plot_show: true,
                colors: [lite.charts.colors[4], lite.charts.colors[2]]
            })
        }
        else
            lite.utils.add_empty_component ({$wrapper: this.$employees_by_gender_wrapper, text: "No Content Found", color: "gray"})
    }


    populate_employees_by_department(){
        const by_department = this.data?.employees_by_department
        if(by_department && lite.utils.object_has_data(by_department)){
            $.each(lite.utils.get_object_keys(by_department).reverse(),(_,k)=>{
                if(_ < 5)
                    this.$employee_by_department.append(this.generator.create_employee_by_department_card(k,by_department[k]))
            })
        }
        else
            lite.utils.add_empty_component ({$wrapper: this.$employee_by_department, text: "No Content Found", color: "gray", classnames:"col-span-3 row-span-2"})
    }
    

    populate_leave_summary(){
        const leave_summary = this.data?.leave_summary
        if(leave_summary && lite.utils.object_has_data(leave_summary)){
            lite.utils.count_figure(this.$total_leave_days, leave_summary?.overall_totals || 0)
            lite.utils.count_figure(this.$total_leave_available_days, leave_summary?.remaining_days || 0)
            lite.utils.count_figure(this.$pending_leave_applications, leave_summary?.pending_applications || 0)
            lite.utils.count_figure(this.$approved_leave_applications, leave_summary?.approved_applications || 0)
        }
    }

    populate_employees_disciplinary(){
        const employees_disciplinary = this.data?.employees_disciplinary
        lite.utils.count_figure(this.$open_disciplinary_cases,employees_disciplinary?.open_disciplinary_cases || 0)
        lite.utils.count_figure(this.$closed_disciplinary_cases,employees_disciplinary?.closed_disciplinary_cases || 0)
        lite.utils.count_figure(this.$open_grievance_cases,employees_disciplinary?.open_grievance_cases || 0)
        lite.utils.count_figure(this.$closed_grievance_cases,employees_disciplinary?.closed_grievance_cases || 0)
    }
    
    populate_employees_by_status(){
        const by_status = this.data.employees_by_status
        if(by_status && lite.utils.object_has_data(by_status)){
            lite.utils.count_figure(this.$active_employees,by_status?.active || 0)
            lite.utils.count_figure(this.$employees_on_leave,by_status?.on_leave || 0)
            lite.utils.count_figure(this.$resigned_employees,by_status?.left || 0)
        }
    }

}