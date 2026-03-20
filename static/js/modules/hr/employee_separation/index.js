

import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'

export default class Employee {
    constructor(config) {   
        this.html_generator = new HR_HTML_Generator ()
        this.utils = config.utils
        this.$pending_exit_interview = $ ("#recent_seperation")
        this.$activities = $ ("#activities")
        this.$total_separation_interviews = $ ("#total_separation_interviews")
        this.$separated_employees = $ ("#separated_employees")
        this.$in_process_separation = $ ("#in_process_separation")
        this.page_controller = config.page_controller
        this.init_dashboard()
    }
    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("employee_separation")        
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data            
            const pending_exit = this.data?.pending_exit_interview
            
            if (pending_exit.length <= 0) {
                this.utils.add_empty_component ({
                    $wrapper: this.$pending_exit_interview,
                    text: "No Separation Content",
                    color: "slate",
                    classnames: "h-[80%] w-full absolute top-0 left-0"
                })
            }else {
                this.$pending_exit_interview.append (this.html_generator.separated_employees (pending_exit))
            }
        }
        lite.utils.init_dashboard(true)
    }
}