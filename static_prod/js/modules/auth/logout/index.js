

export default class Logout {
    constructor(config) {
        $ ("#logout-page").html (`Logging You Out &nbsp;
        ${lite.utils.generate_loader ({light_mode: false, loader_type: 'dots'})}
    `)

        this.clearCookiesForDomain ()
    }

    clearCookiesForDomain () {
        document.cookie.split(";").forEach(cookie => {
            const [name] = cookie.split("=").map(item => item.trim())
            lite.session.set_cookie (name, "", 'Thu, 01 Jan 1970 00:00:00 GMT')
        })
        document.location.replace ("/auth/login")
    }
}