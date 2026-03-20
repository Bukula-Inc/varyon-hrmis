import HTML_Builder from "../../../page/html/html_builder.js"
export default class Password_Reset {
    constructor() {
        this.fstage_vals = {}
        this.second_vals = {}
        this.$reset_btn = $('#reset-btn')
        this.$validate_btn = $('#validate-password-reset')
        this.$first_stage = $(".first-reset-stage")
        this.$second_stage = $(".second-reset-stage")
        this.$validation_fields = $("#validation-fields-wrapper")
        this.builder = new HTML_Builder ()
        this.init_reset()
    }
    init_reset() {
        this.$reset_btn?.off("click")?.on("click", async () => {
            this.$reset_btn.html (`Submitting Email &nbsp; ${lite.utils.generate_loader ({light_mode: true, loader_type: 'dots'})} `).prop ("disabled", true)
            try {
                $.each(this.$first_stage?.find("input"), (_,f)=>this.fstage_vals[$(f)?.attr("fieldname")] = $(f)?.val()?.trim() || "")
                const {status, data, error_message} = await lite.connect.request_password_reset (this.fstage_vals)
                this.$reset_btn.html("Reset").prop("disabled", false)
                if (status != lite.status_codes.ok){
                    $("#email-auth-error").removeClass("hidden").html(error_message || data)
                    $(".first-reset-stage")?.find("input")?.addClass("shake")
                    setTimeout(() => {
                        $(".first-reset-stage")?.find("input")?.removeClass("shake")
                        $("#email-auth-error").addClass("hidden shake")
                    }, 3000);
                }
                else{
                    lite.alerts.toast({
                        toast_type: status,
                        title: "Reset Email Sent",
                        message: "The password reset code has been sent to your email.",
                        timer: 6000
                    })
                    this.init_password_validation()
                }
            } catch (error) {
                console.error("An error occurred during Email Request:", error)
            }
        })
    }



    init_password_validation(){
        this.$first_stage?.addClass("hidden")
        this.$second_stage?.removeClass("hidden")
        this.populate_second_stage_fields()
        this.$validate_btn?.off("click").click(async ()=>{
            $.each(this.$second_stage?.find("input"),(_,f)=>this.second_vals[$(f)?.attr("fieldname")] = $(f)?.val()?.trim() || "")
            try {
                $.each(this.$first_stage?.find("input"),(_,f)=>this.fstage_vals[$(f)?.attr("fieldname")] = $(f)?.val()?.trim() || "")
                this.second_vals.email = this.fstage_vals.email
                this.$validate_btn.html(`Updating New Password &nbsp; ${lite.utils.generate_loader ({light_mode: true, loader_type: 'dots'})} `).prop ("disabled", true)
                const {status, data, error_message} = await lite.connect.validate_password_reset (this.second_vals)
                console.log(status, data, error_message)
                this.$validate_btn.html("Update").prop("disabled", false)
                if (status != lite.status_codes.ok){
                    $("#validation-auth-error").removeClass("hidden").html(error_message || data)
                    $(".first-reset-stage")?.find("input")?.addClass("shake")
                    setTimeout(() => {
                        $(".first-reset-stage")?.find("input")?.removeClass("shake")
                        $("#validation-auth-error").addClass("hidden shake")
                    }, 3000);
                }
                else{
                    lite.alerts.toast({
                        toast_type: status,
                        title: "Password Reset Successful",
                        message: "Your Password has been reset successfully, you are now required to login.",
                        timer: 6000
                    })
                    setTimeout(() => {
                        location.href = "/auth/login"
                    }, 4000);
                }
            } catch (error) {
                console.error("An error occurred during Email Request:", error)
            }
        })
    }





    populate_second_stage_fields(){
        this.$validation_fields.html (this.builder.build_form_field ({
            id: "reset_code",
            fieldtype: "text",
            fieldname: "reset_code",
            fieldlabel: "Reset Code",
            placeholder: "Enter Reset Code"

        }))
        this.$validation_fields.append (this.builder.build_form_field ({
            id: "pwd1",
            fieldtype: "password",
            fieldname: "pwd1",
            fieldlabel: "New Password",
            placeholder: "Enter New Password"
        }))
        this.$validation_fields.append (this.builder.build_form_field ({
            id: "pwd",
            fieldtype: "password",
            fieldname: "pwd",
            fieldlabel: "Confirm New Password",
            placeholder: "Enter Your Confirmation Password"
        }))
        lite.utils.init_password_fields ()
        // this.init_password_reset ()
    }
}