class Dashboard {
    constructor(config) {        
        this.utils = config.utils;
        this.page_controller = config.page_controller;
        this.nav_manager = config.nav_manager;
        this.charts = config.charts;
        this.sessions = config.sessions;
        this.connect = config.connect;

        this.$total_openins =$("#total_openins")
        this.$total_vacancies =$("#total_vacancies")
        this.init_dashboard();
    }

    async init_dashboard() {
        try {
            const job_dashboard_content = await lite.connect.dashboard("job_opening");
            if (job_dashboard_content.status === lite.status_codes.ok) {
                this.jb_opeing = job_dashboard_content.data;
                console.log(this.crmData);
                lite.utils.count_figure(this.$total_openins, this.jb_opeing.total_openings)
                lite.utils.count_figure(this.$total_vacancies, this.jb_opeing.total_vacancies)
                this.init_charts();
            }
        } catch (error) {
            console.error("Error initializing dashboard:", error);
        } finally {
            await lite.utils.init_dashboard(true);
        }
    }

    init_charts() {
        this.job_opening_by_department();
    }

    job_opening_by_department() {
        const departments = this.jb_opeing?.departments;    
        if (departments) {
            const departmentNames = departments.map(department => department.department_name);
            const numberOfVacancies = departments.map(department => department.number_of_vacancies);    
            const data = {
                values: numberOfVacancies,
                labels: departmentNames
            };    
            lite.charts.pie_chart('job-openings-data', data.labels, data.values, {
                height: "80%",
                width: "100%",
                legend_position: 'bottom',
            });
        } else {
            console.error("No department data found.");
        }
    }
    
}
export default Dashboard;
