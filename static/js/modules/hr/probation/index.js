export default class Employee_Promotion{
    constructor(config){
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connect
        this.init_dashboard()        
    }

    async init_dashboard(){
        const fetch_probation_emp =await lite?.connect?.dashboard("probation_sv")
        console.log(fetch_probation_emp);
        if(fetch_probation_emp.status ==lite?.status_code?.ok){
            console.log("LETS GET IT ON....");
            
        }
        
    }

}