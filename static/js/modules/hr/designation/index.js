

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Designation {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$employee_designation = $ ("#employee-designation")
        
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        
        this.init_dashboard()
    }
    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("designation")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            console.log(this.data)
            this.$employee_designation.append (this.html_generator.designation_card(this.data?.designation_employees))
          

            
            this.init_charts(this.data)
        }
        lite.utils.init_dashboard(true)
    }
    init_charts () {
        this.designations()
    
    }

    designations() {
        const data = {
            labels: this.data.designations.labels,
            values: this.data.designations.value
        }
        
        this.charts.pie_chart('emp-designations', data.labels, data.values, {
            legend_position: "right",
            height: 300
        })
    }


}

export default Designation

// const data = {
//     //     labels: [this.data.designations.designation_name],
//     //     values: [this.data.designations.number_of_employees]
//     // }
//     // // $.each (this.data.designation_employees, (_, val) => {
//     // //     data.labels.push (val?.designation_name)
//     // //     data.values.push (val?.number_of_employees)
//     // // })
//     // this.charts.pie_chart('designation', data.labels, data.values, {
//     //     title: "Designation Summary",
//     //     width: 250,
//     //     height: 140,
//     // })
//     // }