

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Checkin {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$department_checkin = $ ("#department-checkin")

        
    

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()
    }
    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("employee_checkin")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            this.$department_checkin.append (this.html_generator.department_checkin(this.data?.department_employees))
            console.log(this.data)
            console.log(this.data.department_employees)
            
          

            
            this.init_charts(this.data)
        }
        lite.utils.init_dashboard(true)
    }
    init_charts () {
        this.checkins ()
    }

    checkins() {
                const data = {
                    labels: ["Logged In", "Logged Out"],
                    values: [this.data?.checkins.in, this.data?.checkins.out]
                }
                this.charts.pie_chart('checkin', data.labels, data.values, {
                    // legend_position: "right",
                    // width: ,
                    // height: 200
                })
            }


}

export default Checkin























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