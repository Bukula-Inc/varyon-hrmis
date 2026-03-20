import { API_CONFIG } from "../connection/config.js"

export default class Lite_Commands {
    constructor(config) {
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.session = config.session
        this.nav = config.nav
        this.alerts = config.alerts
        this.init_key_events()
    }
    init_key_events() {
        const cls = this
        $(document).keydown(function (event) {
            // for menu dropdown
            if ((event.ctrlKey || event.metaKey) && (event.which === 77 || event.which === 109)) {
                cls.nav.toggle_nav_menu_dropdown()
            }
        });
    }

    init_form_commands(form_controller) {
        const cls = this
        const fc = form_controller
        $(document).off("keydown").keydown(function (event) {

            // to delete data
            if ((event.ctrlKey || event.metaKey) && event.keyCode === 8) {
                if (fc.setup?.allow_delete || fc.setup?.allow_delete === undefined) {
                    cls.copied = fc.get_form_data()
                    fc.delete_doc(fc.get_form_data())
                }
                else {
                    cls.alerts.toast({
                        toast_type: API_CONFIG.status_codes.forbidden,
                        title: `Forbiden`,
                        message: `You are not allowed to delete this doc!`,
                    })
                }

            }

            // to duplicate data
            if ((event.ctrlKey || event.metaKey) && (event.which === 68 || event.which === 100)) {
                event.preventDefault()
                cls.copied = fc.get_form_data()
                fc.duplicate_form(fc.get_form_data())
            }


            // to copy form data
            // if ((event.ctrlKey || event.metaKey) && (event.which === 67 || event.which === 99)) {
            //     cls.copied = fc.get_form_data()
            //     fc.copy_clipboard(fc.get_form_data())
            // }
            // // to paste data
            // if ((event.ctrlKey || event.metaKey) && (event.which === 86 || event.which === 118)) {
            //     if (cls.copied && !cls.utils.is_empty_object(cls.copied)) {
            //         fc.duplicate_form(cls.copied)
            //         cls.alerts.toast({
            //             toast_type: API_CONFIG.status_codes.ok,
            //             title: `Pasting`,
            //             message: `Form Data Pasted Successfully!`,
            //         })
            //     }

            // }

            // to save doc
            if ((event.ctrlKey || event.metaKey) && (event.which === 83 || event.which === 115)) {
                event.preventDefault()
                cls.copied = fc.get_form_data()
                fc.save_doc()
            }

            // new doc
            if ((event.ctrlKey || event.metaKey) && (event.which === 78 || event.which === 110)) {
                event.preventDefault()
                alert()
            }
        });
        this.init_key_events()
    }
}

