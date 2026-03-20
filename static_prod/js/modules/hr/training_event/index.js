class Training_Event {
    constructor(config) {
        this.charts = config.charts
        this.page_controller = config.page_controller
        this.utils = config.utils
        this.Training_Event()
        
    }

   

    Training_Event() {
        const data = {
            labels: ["Finance", "Projects", "Human Resource", "Dev"],
            values: [80, 30, 25, 10, 5]
        }
        this.charts.pie_chart('training-event', data.labels, data.values, {
          
        })
    }

   

}

export default Training_Event