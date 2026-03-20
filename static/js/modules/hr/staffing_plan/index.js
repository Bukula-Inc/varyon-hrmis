import hr_html_generator from "../../../page/html/hr_html_generator.js";

export default class Staffing_Plan {
    constructor() {  
        this.$generator = new hr_html_generator();
        this.$staffing_plan_chart = $('.staffing-plan-chart')
        this.$staffing_plan_info = $('.staffing-plan-info')
        
        // this.init_page() 
    }

    async init_page(){
        const content_data = await lite.connect.x_fetch("get_staffing_plan")
        if(content_data?.status === lite.status_codes.ok){
            this.data = content_data.data
            
            this.populate_chart()
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
        if (this.data.metrics.total > 0) {
            Object.entries(this.data.metrics.department_metrics).forEach((dept, data) => {
                this.$staffing_plan_info.append(this.$generator.staffing_plan_by_department(dept, data));
            });
        }
        else {
            this.create_empty_component(this.$staffing_plan_info);
        }
    }

    populate_chart() {
        if (this.data.metrics.total > 0) {
            let labels = ["Draft", "Submitted", "Active"];
            let values = [this.data.metrics.Draft, this.data.metrics.Submitted, this.data.metrics.Active];

            if (values.some(val => val !== 0)) {
                lite.charts.donut_chart('staffing_plan_chart', labels, values, {
                    height: '100%',
                    plot_show: true,
                    show_legend: false,
                });
            } else {
                this.create_empty_component(this.$staffing_plan_chart);
            }
        } else {
            this.create_empty_component(this.$staffing_plan_chart);
        }
    }
}