class Employee_Feedback {
    constructor(config) {
        this.charts = config.charts
        this.page_controller = config.page_controller
        this.utils = config.utils
        this.feedback()
        
    }

   

    feedback() {
        const data = {
            labels: ["Comments", "Question"],
            values: [80, 30]
        }
        this.charts.pie_chart('feedback', data.labels, data.values, {
            // legend_position: "right",
            // width: ,
            // height: 200
        })
    }

   

}

export default Employee_Feedback