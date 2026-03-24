import Utils from "./utils/utils.js"
import Reports from "./page/report_controller/index.js";
import Nav_Manager from "./nav/nav.js";
import Session_Controller from "./session/session_controller.js";
import Page_Controller from "./page/page_controller.js"
import NetworkMonitorService from "./utils/network.js";
import Charts from "./charts/index.js";
import Animations from "./page/Animations.js";
import Connection from "./connection/index.js";
import Alerts from "./alerts/alert.js";
import Lite_Commands from "./utils/commands.js";
import Lite_File_Picker from "./components/lite_file_picker/index.js";
import Lite_Selector from "./components/lite_selector/index.js"
import Expandable_Field from "./components/expandable_field/index.js";
import Time_Picker from "./components/time_picker/index.js";
import Year_Picker from "./components/year_picker/index.js";
import Date_Picker from "./components/date_picker/index.js";
import Code_Editor from "./components/code_editor/index.js";
import Rich_Editor from "./components/rich_editor/index.js";
import { API_CONFIG } from "./connection/config.js";
import Currency from "./functions/core/currency.js";
import HTML_Builder from "./page/html/html_builder.js";
import Lite_Switch from "./components/lite_switch/index.js";
import User from "./functions/core/user.js";
import Permission_Controller from "./functions/core/permission_controller.js";
import Modals from "./modals/index.js";
import Web from "./web/index.js";
import { color_codes } from "./constants/colors.js";
import { Global_Action_Inits } from "./init/index.js";
import Scanners from './components/scanners/index.js';
export default class Main {
    constructor() {
        this.currency = new Currency()
        this.utils = new Utils()
        this.networkMonitor = new NetworkMonitorService()
        this.session_controller = new Session_Controller(this.utils)
        this.nav_manager = new Nav_Manager()
        this.alerts = new Alerts({ utils: this.utils })
        this.lite_switch = new Lite_Switch()
        this.lite_date_picker = new Date_Picker()
        this.lite_time_picker = new Time_Picker()
        this.year_picker = new Year_Picker()
        this.connect = new Connection({ utils: this.utils, network: this.networkMonitor, alerts: this.alerts })
        this.lite_commands = new Lite_Commands({ utils: this.utils, session: this.session, nav: this.nav_manager, alerts: this.alerts })
        this.lite_file_picker = new Lite_File_Picker()
        this.lite_selector = new Lite_Selector({ utils: this.utils, connect: this.connect, alerts: this.alerts })
        this.animations = new Animations(this.utils)
        this.charts = new Charts()
        this.html_generator = new HTML_Builder()
        this.user_controller = new User()
        this.code_editor = new Code_Editor()
        this.rich_editor = new Rich_Editor()
        this.scanners = new Scanners()
        this.utils.hide_display_icons(true)
        this.expandable_field = new Expandable_Field()
        lite.default_logo="/static/images/logo/logo.svg"
        lite.default_solid_logo = "/static/images/logo/solid.png"
        lite.user_avatar="/media/defaults/avatas/dp.jpeg"
        lite.default_fields=[ "id","created_on","doctype","owner","modified_by","last_modified", "status","idx","disabled","status_info","docstatus","creation_time"]
        lite.colors = ["#1f1847", "#4941ED", "#306DF9", "#EDB141", "#A030F9", "#C8A11C", "#C85B1C","#eb73bb","#b91c1b","#0c9488","#05b6d3","#0ba5e9","#4337c9","#6d27d9"]
        lite.color_codes = color_codes
        lite.main= this
        lite.status_codes= API_CONFIG.status_codes
        lite.nav= this.nav_manager
        lite.utils= this.utils
        lite.alerts= this.alerts
        lite.modals= null
        lite.charts= this.charts
        lite.animations= this.animations
        lite.lite_commands= this.lite_commands
        lite.lite_selector=this.lite_selector
        lite.lite_date_picker= this.lite_date_picker
        lite.lite_time_picker= this.lite_time_picker
        lite.lite_year_picker= this.year_picker
        lite.lite_file_picker= this.lite_file_picker
        lite.lite_switch= this.lite_switch
        lite.expandable_field = this.expandable_field
        lite.network= this.networkMonitor
        lite.connect= this.connect
        lite.session= this.session_controller
        lite.currency= this.currency
        lite.currency_decimals = 2
        lite.scanners = this.scanners
        lite.system_settings= {}
        lite.code_editor= this.code_editor
        lite.rich_editor= this.rich_editor
        lite.preloaded_code={}
        lite.rich_editor_values= {}
        lite.temp_exchange_rates= {}
        lite.form_state= "new"
        lite.html_generator= this.html_generator
        lite.user_controller= this.user_controller
        lite.pp = this.pp
        // after lite has been initialized
        lite.modals = new Modals()
        lite.global_action_inits = new Global_Action_Inits()

        this.fetch_system_defaults().then(resolve=>{
            if(resolve){
                this.page_controller = new Page_Controller({
                    utils: this.utils,
                    session: this.session_controller,
                    nav: this.nav_manager,
                    connect: this.connect,
                    alerts: this.alerts,
                    lite_commands: this.lite_commands,
                    lite_selector: this.lite_selector,
                    lite_date_picker: this.lite_date_picker
                })
                lite.page_controller = this.page_controller
                lite.permission_controller = new Permission_Controller()
                this.page_controller.on_page_loaded(this.init)
            }
            else{
                this.page_controller = new Page_Controller({
                    utils: this.utils,
                    session: this.session_controller,
                    nav: this.nav_manager,
                    connect: this.connect,
                    alerts: this.alerts,
                    lite_commands: this.lite_commands,
                    lite_selector: this.lite_selector,
                    lite_date_picker: this.lite_date_picker
                })
                lite.page_controller = this.page_controller
                lite.alerts.toast({
                    toast_type: lite.status_codes.internal_server_error,
                    title: "System Initialization Failed",
                    message: "Failed to fetch system settings!"
                })
            }
        })
    }
    async fetch_system_defaults(){
        const {status, data, error_message} = await this.connect.get_system_settings()
        if(status === lite.status_codes.ok){
            lite.user = data.user
            lite.system_settings = data
            lite.currency_decimals = data.currency_decimals
            const company = data?.linked_fields?.default_company,
                    currency = data?.linked_fields?.default_currency ,
                    country = data?.linked_fields?.default_country,
                    cost_center = data?.linked_fields?.default_cost_center,
                    currency_decimals = data.currency_decimals,
                    accounting_defaults = data?.accounting_defaults || {}
            lite.defaults = {
                company: company,
                currency: currency,
                country: country,
                cost_center: cost_center,
                currency_decimals: currency_decimals,
                accounting_defaults: accounting_defaults,
            }
            lite.roles = data?.roles
            lite.allowed_content = data?.allowed_content
            // lite.allowed_modules = data?.allowed_modules
            lite.employee_info = data?.employee_info
            lite.permission_controller = new Permission_Controller()
            if(lite.user){
                lite.user.company = lite?.defaults?.company || {}
            }
            return data
        }
        else{
            lite.alerts.toast({
                toast_type: lite.status_codes.internal_server_error,
                title: "Initialization Failed",
                message: `Failed to fetch system defaults: ${error_message}`
            })
            new Error("Failed to fetch system defaults!")
        }
    }



    async init() {
        // when the page is loaded. initialize the main controller class for the current module
        const config = {
            utils: lite.utils,
            networkService: lite.networkMonitor,
            session: lite.session_controller,
            nav_manager: lite.nav_manager,
            page_controller: lite.page_controller,
            charts: lite.charts,
            animations: lite.animations,
            connect: lite.connect,
            alerts: lite.alerts,
            lite_commands: lite.lite_commands
        }

        const current_module = lite.utils.get_current_module()
        
        if(current_module){
            const module_initializer = await lite.utils.import_module_content()
            if(module_initializer){
                if (lite.utils.is_report_page()) {
                    config.reports = new Reports(config)
                }
                new module_initializer(config)
            }
            if(lite.utils.lower_case(current_module) === "" || lite.utils.lower_case(current_module) === "web" ){
                new Web()
            }
        }
        else{
            if(lite.utils.lower_case(current_module) === "" ){
                new Web()
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => new Main())
