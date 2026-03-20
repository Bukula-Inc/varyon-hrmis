import HR_HTML_Generator from "../../../page/html/hr_html_generator.js"
export default class Staff_Profile {
    constructor(config) {
        
        this.charts = config.charts
        this.page_controller = config.page_controller
        this.utils = config.utils
        // this.data =null
        this.hr_gene =new HR_HTML_Generator()
        
        this.fetch_data()
    }

   

    async fetch_data() {
        let emp_data =null
        if(lite?.employee_info){
            emp_data =lite?.employee_info?.name           
        }    
        else{
            return emp_data
        }
        const fetch_dashboard_data =await lite?.connect?.x_post("fetch_employee_profile_data", {"employee": emp_data})
        console.log(fetch_dashboard_data);
        
        if(fetch_dashboard_data.status ==lite.status_codes.ok){
            this.data =fetch_dashboard_data.data
            this.upper_cards()
            this.job_and_personal_info()
            this.brief_descriptions()
            this.appraisal()
            this.work_plan()
            this.leave_info()
            
        }
    }

    upper_cards(){
        let years_served =0
        let period_qty =""
        if(this.data?.top_cards?.years_of_service){
            years_served =this.data?.top_cards?.years_of_service
            if(years_served ==1){
                period_qty =" Year"
            } else if(years_served >1){

                period_qty =" Years"
            }
        }
        // if(this.data.top_cards !={}){
            $('#avaliable_leave_days').html(this.data?.top_cards?.leave_balance || 0)
            $('.years_served').html(this.data?.top_cards?.years_of_service || 0)
            $('.period-qty').html(period_qty)
            $('#income').html(this.data?.top_cards?.total_income || 0)
            $('#amount').html(this.data?.top_cards?.total_expanse || 0)
        // }
    }

    async job_and_personal_info(){
        
        $('.full_name').append(this.data.job_personal_info.full_name || "")
        $('.contact').html(this.data.job_personal_info.contact || "")
        $('.email').html(this.data.job_personal_info.email || "")
        $('.emergency_contact').html(this.data.job_personal_info.emergancy_contact || "")
        $('.company').html(this.data.job_personal_info.company || "")
        $('.department').html(this.data.job_personal_info.department || "")
        $('.job_title').html(this.data.job_personal_info.job_title || "")
        $('.supervisor').html(this.data.job_personal_info.supervisor || "")
    }

    brief_descriptions(){

        $('.salary').html(this.data.brief_descriptions.salary || "")
        $('.main_status').html(this.data.brief_descriptions.status || "")
        $('.main_joining_date').html(this.data.brief_descriptions.joined_on || "")
        $('.department').html(this.data.brief_descriptions.qualification || "")
        $('.main_dob').html(this.data.brief_descriptions.date_of_birth || "")
    }

    leave_info(){
        if(this.data?.leave_type?.staff_leave_days){
            $('#leave_type_data').append(this.hr_gene.emp_profile(this.data?.leave_types?.staff_leave_days))
        }
        // $('#leave_type_data').append(this.hr_gene.emp_profile(this.data?.leave_types?.staff_leave_days))

        this.charts.pie_chart('leave_summary', this.data?.leave_types?.distribution?.labels, this.data?.leave_types?.distribution?.value, {
            legend_position: 'top', 
            height:300,
            width: 300,
        })
    }

    appraisal(){
        this.charts.column_chart_with_negatives('appraisal_360_a', this.data?.appraisal?.distribution?.labels, this.data?.appraisal?.distribution?.values, {
            title: 'Work Plan',
            stroke_size: 1,
            height: "100%",
            width: "100%",   
            column_width: '10%',   
        })
    }

    work_plan(){
        this.charts.column_chart_with_negatives('work_plan_tasks', this.data?.work_plan?.distribution?.labels, this.data?.work_plan?.distribution?.value, {
            title: 'Income Distribution',
            stroke_size: 1,
            height: "100%",
            width: "100%",   
            column_width: '10%',   
        })
    }
}

