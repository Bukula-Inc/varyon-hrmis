class Dashboard {
    constructor(config) {
        this.$customers = $("#customers");
        
        this.utils = config.utils;
        this.page_controller = config.page_controller;
        this.nav_manager = config.nav_manager;
        this.charts = config.charts;
        this.sessions = config.sessions;
        this.connect = config.connect;
        this.init_dashboard();
    }

    async init_dashboard() {
        try {
            const crm_dashboard_content = await lite.connect.dashboard("side_views");
            if (crm_dashboard_content.status === lite.status_codes.ok) {
                this.crmData = crm_dashboard_content.data;
                console.log(this.crmData);

                lite.utils.count_figure(this.$total_leads, this.crmData?.customers)
                this.init_charts();
            }
        } catch (error) {
            console.error("Error initializing dashboard:", error);
        } finally {
            await lite.utils.init_dashboard(true);
        }
    }

    init_charts() {
        this.sales_pipeline();
    }

    sales_pipeline (){
        const data = {
            values: [30, 40, 50, 100],
            labels: ["Overall Performance", "Rating", "performance Goals Achieved"]
        }
        lite.charts.semi_donut_chart ('staff_performance_agreement', data.labels, data.values, {
            height: "50%",
            width: "70%",
            legend_position: 'bottom',
        })
    } 
}
export default Dashboard;
