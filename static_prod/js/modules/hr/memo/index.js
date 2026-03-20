

import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js'

class Memo {
    constructor(config) {   
        this.html_generator = new HR_HTML_GENERATOR ()
        this.$memo_stats = $ ("#memo-stats")
        
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()
    }
    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("memo")
        
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            console.log(this.data)
            console.log(this.data.memo_list)
            this.$memo_stats.append(this.html_generator.memo_card(this.data?.memo_list))        

        }
        lite.utils.init_dashboard(true)
    }
 




}

export default Memo
