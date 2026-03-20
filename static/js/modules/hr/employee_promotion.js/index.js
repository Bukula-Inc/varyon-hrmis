
import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Promotion {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$recent_promotions = $ ("#recent-promotions")

        
    

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()
    }
    async init_dashboard(){
        lite.utils.init_dashboard()
        const dashboard_content = await lite.connect.dashboard("employee_promotion")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            console.log(this.data)
            console.log(this.data.promoted_employees)
            this.$recent_promotions.append (this.html_generator.promoted_employees(this.data?.promoted_employees))

            
            
          

            
            
        }
        lite.utils.init_dashboard(true)
    }



}

export default Promotion























