import HR_HTML_GENERATOR from '../../../page/html/hr_html_generator.js';

class Employee_attendance {
    constructor(config) {
        this.html_generator = new HR_HTML_GENERATOR();
        this.$employee_attendance = $("#attendance");
        this.$present_employees = $("#present");
        this.$employees_on_leave = $("#emp-on-leave");
        this.$searchbar = $("[lite-field=Search-attendance]");
        this.utils = config.utils;
        this.page_controller = config.page_controller;
        this.nav_manager = config.nav_manager;
        this.charts = config.charts;
        this.sessions = config.sessions;
        this.connect = config.connect;

        this.emp_data = [];
        this.eventsBound = false;  // Prevent multiple event bindings

        this.init();
    }

    async init() {
        await this.fetch_data();
        this.bind_events();  // Attach events ONCE
    }

    async fetch_data() {
        const fetch_employee = await lite?.connect?.x_fetch("employees_for_attendance");
        if (fetch_employee.status === lite?.status_codes.ok) {
            this.emp_data = fetch_employee.data;
            this.render_attendance_list();
        }
    }

    render_attendance_list() {
        if (this.emp_data.length > 0) {
            $("#employee-attendant-info").html('');
            $("#employee-attendant-info").append(this.html_generator.attendance_list_cards(this.emp_data));

            if (!this.eventsBound) {
                this.bind_events();
            }
        }
    }

    bind_events() {
        if (this.eventsBound) return;  // Prevent re-binding events
        this.eventsBound = true;

        $("#employee-attendant-info").off("click", "[lite-attendance-card]");

        $("#employee-attendant-info").on("click", "[lite-attendance-card]", async (e) => {
            e.preventDefault();
            await this.handle_card_click(e);
        });
    }
    pt (emp_id) {
        let empID = ""
        let tries = 0
        while (tries < 3) {
            tries ++
            empID = prompt ("Provide Your Employee No: ")
            if (empID && empID == emp_id) {
                return empID
            }
        }
        return undefined
    }
    async handle_card_click(e) {
        const $card = $(e.currentTarget);
        const employee = $card.attr("lite-attendance-card");
        const employee_name = $card.attr("lite-name");
        const empID = this.pt (employee)
        if (empID && empID == empID) {
            await this.log_attendance({confirm_employee_id: employee, employee_name})
            setTimeout (()=> {
                this.init ()
            }, 500)
        }else
            lite.alerts.toast({
                toast_type: lite.status_codes.unauthorized,
                title: "Invalid",
                message: "Provide Your Correct Employee No",
            });

        // const model = await lite.modals.quick_form("hr", "attendance_confirm", async (values, setup) => {
        //     if (values) {
        //         await this.log_attendance(values, model);
        //     } else {
        //         lite.alerts.toast({
        //             toast_type: lite.status_codes.unprocessable_entity,
        //             title: "Attendance",
        //             message: "Something went wrong while processing your Attendance Log!",
        //         });
        //     }
        // }, null, { employee, employee_name });
        
    }

    async log_attendance(values, model="") {
        const loader_id = lite.alerts.loading_toast({
            title: "Attendance Logging",
            message: "Wait while we log your Attendance"
        });

        const res = await lite.connect.x_post("take_attendance", { ...values });

        if (res.status === lite.status_codes.ok) {
            lite.alerts.toast({
                toast_type: lite.status_codes.ok,
                title: "Attendance",
                message: "Attendance Logged Successfully",
            });
        }

        lite.alerts.destroy_toast(loader_id);
        // lite.modals.close_modal(model.modal_id);
    }
}

export default Employee_attendance;