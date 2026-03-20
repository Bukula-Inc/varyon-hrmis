class Dashboard {

    constructor(config) {
        this.$dashboard_content_wrapper = $(".dashboard-content");
        this.$average_resolutions_time = $("#average-resolutions-time");

        this.utils = config.utils;
        this.page_controller = config.page_controller;
        this.nav_manager = config.nav_manager;
        this.charts = config.charts;
        this.sessions = config.sessions;
        this.connect = config.connect;
        this.init_dashboard();
        this.init_charts()
    }

    async init_dashboard() {
        try {
            const dashboard_content = await lite.connect.dashboard("case_outcome");
            console.log(dashboard_content)
            if (dashboard_content.status == lite.status_codes.ok) {
                this.data = dashboard_content.data;

                console.log(this.data)

                if (this.data) {
                    const departmental_displinary =this.data.departmental_displinary
                    const pie_chart_data ={
                        labels :Object.keys(this.data.relution_distrubtion),
                        values :Object.values(this.data.relution_distrubtion) 
                    }
                    
                    lite.utils.count_figure(this.$average_resolutions_time, this.data.resolution_time);
                    this.init_charts(pie_chart_data, departmental_displinary);
                } else {
                    throw new Error("Data is undefined");
                }
            } else {
                throw new Error("Failed to fetch dashboard data");
            }
        } catch (error) {
            console.error("Error initializing dashboard:", error);
        }
    }

    init_charts(pie_chart_data, departmental_displinary) {
        try {
            this.case_outcome(pie_chart_data, departmental_displinary);
        } catch (error) {
            console.error("Error initializing charts:", error);
        }
    }

    case_outcome(pie_chart_data, departmental_displinary) {
        console.log(departmental_displinary);
        

        this.charts.pie_chart("actions-taken-chart", pie_chart_data.labels, pie_chart_data.values, {
            width: 300,
            show_legend: false,
            legend_position: "right",
        });

        this.charts.column_chart_with_negatives("employye-Retention-chart", departmental_displinary.labels, departmental_displinary.value,{
            height: 250,
            column_width: "10%",           
        })
    }
}

export default Dashboard;