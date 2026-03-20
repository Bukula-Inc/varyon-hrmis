import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'
export default class Intervew{
    constructor() {  
        // this.$job_applications_chart = $('.job-applications-chart')
        // this.$job_applications_info = $('.job-applications-info')
        // this.$total_applicants = $ ("#total_applicants")
        // this.$successful_applications = $("#successful_applications")
        this.$interivews_week = $("#interivews_week")
        this.generator = new HR_HTML_Generator()
        
        this.init_page() 
    }

    async init_page(){
        const content_data = await lite.connect.dashboard("Interview")
        console.log(content_data);
        if(content_data?.status === lite.status_codes.ok){
            this.data = content_data.data
            
            // lite.utils.count_figure(this.$total_applicants, this.data?.job_application_stats?.total_applications)
            // lite.utils.count_figure(this.$successful_applications, this.data?.job_application_stats.successful_applications)
            // lite.utils.count_figure(this.$rejected_applications, this.data?.job_application_stats.rejected_applicat
            // ions)
            if(this.data?.interview_info.length >0 ){
                this.interviews_this_week()
            }else{
                lite.utils.add_empty_component ({$wrapper: $("#job-applicatio"), text: "No Content Found", color: "gray"})
            }            
            if(this.data?.interview_stats){
                this.interview_stats()
            }else{
                lite.utils.add_empty_component ({$wrapper: $("#job_applic_by_desig-chart-info"), text: "No Content Found", color: "gray"})
            }
        }
    }

    create_empty_component($wrapper) {
        lite.utils.add_empty_component({
            $wrapper: $wrapper,
            text: "No Data",
            color: "gray",
            classnames: "absolute"
        });
    }

    interviews_this_week() {
        const interview_week = this.data?.interview_info
        if (!interview_week || lite.utils.object_has_data(interview_week))
        {
            this.create_empty_component()
        }
        const interview_data = Object.values(interview_week)
        this.$interivews_week.append(this.generator.interviews_this_week(interview_data))

    }

    interview_stats() {
        const interview_stats = this.data?.interview_stats?.[0];    
        if (interview_stats) {
            const labels = ["Pending", "Accepted", "Conducted"];
            const values = [
                interview_stats.pending,
                interview_stats.accepted,
                interview_stats.rejected
            ];
    
            lite.charts.pie_chart('interview_stats_chart', labels, values, {
                legend_position: 'bottom',
                height: "100%",
                width: "100%"
            });
        } 
    }    
}