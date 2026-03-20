export default class Job_application {
    constructor() {  
        this.$job_applications_chart = $('.job-applications-chart')
        this.$job_applications_info = $('.job-applications-info')
        this.$total_applicants = $ ("#total_applicants")
        this.$successful_applications = $("#successful_applications")
        this.$rejected_applications = $("#rejected_applications")
        this.init_page() 
    }

    async init_page(){
        const content_data = await lite.connect.dashboard("Job_Application")
        if(content_data?.status === lite.status_codes.ok){
            this.data = content_data.data
            console.log(this.data);
            
            lite.utils.count_figure(this.$total_applicants, this.data?.job_application_stats?.total_applications)
            lite.utils.count_figure(this.$successful_applications, this.data?.job_application_stats.successful_applications)
            lite.utils.count_figure(this.$rejected_applications, this.data?.job_application_stats.rejected_applications)            
            this.job_application_by_designation()
            this.populate_summary()
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

    populate_summary() {
        this.$job_applications_info.find('.total-applications').text(this.data?.applications || 0)
        this.$job_applications_info.find('.total-applicants').text(this.data?.applicants || 0)
        this.$job_applications_info.find('.active').text(this.data?.active || 0)
        this.$job_applications_info.find('.rejected').text(this.data?.rejected || 0)
    }

    job_application_by_designation() {
        const job_applic_by_desig = this.data.applications_by_designation;    
        const labels = Object.keys(job_applic_by_desig); 
        const values = Object.values(job_applic_by_desig); 
    
        lite.charts.donut_chart('job_applic_by_desig-chart-info', labels, values, {
            height: "80%",
            width: "100%",
            legend_position: 'bottom',
        });
    }
    
}