

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Appraisal_360 {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$setup = $ ("#setup")

        
    

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()
    }
    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("appraisal_setup")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            this.$setup.append (this.html_generator.appraisal_setup(this.data?.appraisal_setup_stats))
            
            this.init_charts(this.data.appraisal_type)
        }
        lite.utils.init_dashboard(true)
    }
    init_charts (appraisal_type) {
        this.appraisal (appraisal_type)
    }

    appraisal(appraisal_type) {
                const data = {
                    labels: ["360 Degree Apprisal", "Self Appraisal"],
                    values: [appraisal_type.three_degree_apprisal, appraisal_type.self_appraisal]
                }
                this.charts.pie_chart('appraisal360', data.labels, data.values, {
                    width: 300,
                    height: 250,
                })
            }


}

export default Appraisal_360























// class Checkin {
//     constructor(config) {
//         this.charts = config.charts
//         this.page_controller = config.page_controller
//         this.utils = config.utils
//         this.checkins()
        
//     }

   

//    

   

// }

// export default Checkin








// class Appraisal_360 {
//     constructor(config) {
//         this.charts = config.charts
//         this.page_controller = config.page_controller
//         this.utils = config.utils
//         this.Appraisal_360()
        
//     }

   

//     Appraisal_360() {
//         const data = {
//             labels: ["Appraised Employees", "Employees Not Appraised"],
//             values: [80, 30]
//         }
//         this.charts.pie_chart('appraisal360', data.labels, data.values, {
//             // legend_position: "right",
//             // width: ,
//             // height: 200
//         })
//     }

   

// }

// export default Appraisal_360