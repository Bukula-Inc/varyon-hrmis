

import HTML_Builder from "../../../page/html/html_builder.js"
export default class Auth {
    constructor(config) {
        this.builder = new HTML_Builder ()
        this.alerts = config.alerts
        this.connect = config.connect
        this.session = config.session
        this.utils = config.utils
        this.email = ""
        this.pwd = ""
        this.$auth_logo = $(".auth-logo")
        this.$login_action_wrapper = $(".login-action-wrapper")
        this.$auth_company = $(".auth-company")
        this.$error_area = $('#auth-error')
        this.$field_wrapper = $("#login-fields-wrapper")
        this.$auth_btn = $('button[lite-id="auth-btn"]')
        this.$failed_btn = $('a[lite-id="failed-btn"]')
        this.$req_btn = $('a[lite-id="req-btn"]')
        this.$email = undefined
        this.$pwd = undefined
        this.$forgot_pwd = $('input[lite-id="forgot-pwd"]')
        this.auth_url = undefined
        this.init_auth()

    }
    init_auth() {
        lite.session.clear_cookies_for_domain()
        this.$auth_logo?.attr("src", `${lite.utils.get_protocal()}//${lite.utils.get_host()}${lite?.defaults?.company?.company_logo}` || lite?.default_logo)
        this.$auth_company.html(lite?.defaults?.company?.name)

        this.$field_wrapper.html (this.builder.build_form_field ({
            id: "email",
            fieldtype: "text",
            fieldname: "email",
            fieldlabel: "Email",
            placeholder: "Enter Your Email",
        }))

        this.$field_wrapper.append (this.builder.build_form_field ({
            id: "pwd",
            fieldtype: "password",
            fieldname: "pwd",
            fieldlabel: "Password",
            placeholder: "Enter Your Password",

        }))
        lite.utils.init_password_fields()
        this.init_authentication()
    }
    init_authentication () {
        lite.utils.show(this.$login_action_wrapper)
        this.$email = $('#email')
        this.$pwd = $('#pwd')

        this.$auth_btn?.on("click", async e => {
            e.preventDefault()
            this.$auth_btn.html (`Logging In &nbsp;
                ${lite.utils.generate_loader ({light_mode: true, loader_type: 'dots'})}
            `).prop ("disabled", true)
            const {status, data, error_message} = await lite.connect.authentication({ password: this.pwd?.trim (), email: this.email?.trim () })
            if(status === lite.status_codes.ok){
                location.replace(data.url)
            }
            else{
                $('button[lite-id="auth-btn"]').html ("Login").prop ("disabled", false)
                const error_area = $('.error-text')
                error_area.text (error_message)
                lite.utils.show(error_area.parents(".field-error-wrapper"))
                $ (`input[lite-id="email"]`).addClass("shake")
                $ (`input[lite-id="pwd"]`).addClass("shake")
            }
        })

        $(this.$email).keyup(e => {
            this.$error_area.fadeOut ()
            this.$email.removeClass("shrink")
            this.$pwd.removeClass("shrink")
            this.email = this.utils.get_field_value(this.$email)?.trim ()
            this.pwd = this.utils.get_field_value(this.$pwd)?.trim ()
            if (this.email?.trim() && this.pwd?.trim ()) {
                this.$req_btn.addClass("shrink")
            }
            else {
                this.$req_btn.removeClass("shrink")
            }
        })
        $(this.$pwd).keyup(e => {
            this.$error_area.fadeOut ()
            this.$email.removeClass("shrink")
            this.$pwd.removeClass("shrink")
            this.email = this.utils.get_field_value(this.$email)?.trim ()
            this.pwd = this.utils.get_field_value(this.$pwd)?.trim ()
            if (this.email?.trim() && this.pwd) {
                this.$req_btn.addClass("shrink")
                this.$email.removeClass("shake")
                this.$pwd.removeClass("shake")
            }
            else {
                this.$req_btn.removeClass("shrink")
            }
        })
    }
}

