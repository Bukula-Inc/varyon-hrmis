from controllers.utils import Utils
utils = Utils()

class Crm_Templates:
    def __init__(self):
        pass

    @classmethod
    def appointment_schedule_template(cls, content, subject="Appointment Confirmation", company=None):
        background_color = "#151030"
        btn_color = "#151030"
        text_color = "white"
        logo_url = "/static/images/logo.png"
    
        if company:
            background_color = company.default_theme_color or background_color
            btn_color = company.default_secondary_color or btn_color
            text_color = company.default_theme_text_color or text_color
            if company.logo:
                logo_url = company.logo
    
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100%  !important; } .title{font-size: 20px !important;}}"
    
        # Conditionally add view link if recipient is a customer
        view_link = ""
        if content.get("appointment_with") == "Customer":
            view_link = f"""
            <div style="margin-top: 30px; text-align:center;">
                <a href="{content.get('redirect_url', '#')}" style="padding: 12px 25px; background: linear-gradient(135deg, {btn_color}, #3f3d56); color: white; border-radius: 6px; text-decoration: none; font-weight: 500;">View Appointment</a>
            </div>
            """
    
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{subject}</title>
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
                <style>{wrapper}</style>
            </head>
            <body style="margin:0; padding:0; background-color:#e3e3e3; font-family: 'Poppins', sans-serif;">
    
                <div class="wrapper" style="width:60%; margin: 40px auto; background: {background_color}; color: {text_color}; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.2); overflow:hidden;">
                    
                    <div style="padding: 30px; text-align:center;">
                        <img src="{logo_url}" alt="Company Logo" style="width: 120px;">
                        <h2 style="margin-top: 20px; font-size: 28px; color: {text_color};">Appointment Confirmed 🎉</h2>
                    </div>
    
                    <div style="background: #ffffff; padding: 30px; color: #151030;">
                        <h3 style="margin-top: 0;">Hello {content['recipient_name']},</h3>
                        <p style="font-size: 14px;">We're excited to let you know that your appointment has been successfully scheduled.</p>
    
                        <div style="margin-top: 25px;">
                            <h4 style="margin-bottom: 15px; color: {btn_color};">📅 Appointment Details</h4>
                            <div style="margin-bottom: 10px;"><strong>Date:</strong> {content['date']}</div>
                            <div style="margin-bottom: 10px;"><strong>Time:</strong> {content['time']}</div>
                            <div style="margin-bottom: 10px;"><strong>Location:</strong> {content['location']}</div>
                            <div style="margin-bottom: 10px;"><strong>Purpose:</strong> {content['purpose']}</div>
                        </div>
    
                        {view_link}
                    </div>
    
                    <div style="padding: 20px 30px; background: #fff; border-top: 1px solid #ddd; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                        <div style="display: flex; align-items: center; font-size: 12px;">
                            <span>Powered by&nbsp;</span>
                            <a href="https://www.startappsolutions.com/auth/login">
                                <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="Varyon" style="width: 70px; margin-top: 5px;">
                            </a>
                        </div>
                        <div style="font-size: 12px;">&copy; 2024 | All Rights Reserved</div>
                    </div>
    
                </div>
    
            </body>
            </html>
        """
    

@classmethod
def ticket_escalation_template(cls, data, subject="Ticket Escalation Notification", company=None):
    background_color = "#151030"
    btn_color = "#151030"
    text_color = "white"
    logo_url = "/static/images/logo.png"

    if company:
        background_color = company.default_theme_color or background_color
        btn_color = company.default_secondary_color or btn_color
        text_color = company.default_theme_text_color or text_color
        if company.logo:
            logo_url = company.logo

    wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100%  !important; } .title{font-size: 20px !important;}}"

    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                {wrapper}
            </style>
        </head>
        <body style="width:100%; min-height: 100dvh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
            <div class="wrapper" style="width: 60%;min-height:170px; height: max-content; background-color: {background_color}; color: {text_color}; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                    <img src="{logo_url}" alt="" style="width: 120px;">
                </div>
                <h3 style="font-size: 26px; margin: auto; text-align: center;margin-top: 30px;">Ticket Escalation Alert</h3>
                <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #151030;">
                    <h3 style="width: 80%; margin: 0 auto; margin-top: 30px;">Hello {data['recipient_name']},</h3>
                    <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 30px;">
                        A ticket from <strong>{data['customer']}</strong> has been escalated and needs urgent attention for resolution.
                    </p>
                    <div style="width: 80%; margin: 30px auto; font-size: 14px; color: #151030;">
                        <h4 style="margin-bottom: 20px;">Ticket Details</h4>
                        
                        <div style="margin-bottom: 10px;">
                            <strong>Ticket ID:</strong> {data['ticket_id']}
                        </div>
                        <div style="margin-bottom: 10px;">
                            <strong>Subject:</strong> {data['subject']}
                        </div>
                        <div style="margin-bottom: 10px;">
                            <strong>Priority:</strong> {data['priority']}
                        </div>
                        <div style="margin-bottom: 10px;">
                            <strong>Status:</strong> {data['status']}
                        </div>
                        <div style="margin-bottom: 10px;">
                            <strong>Created On:</strong> {data['created_on']}
                        </div>
                        <div style="margin-bottom: 10px;">
                            <strong>Ticket Age:</strong> {data['time_since_created']}
                        </div>
                        <div style="margin-bottom: 10px;">
                            <strong>Description:</strong><br>
                            <span style="display: block; margin-top: 5px;">{data['description']}</span>
                        </div>
                    </div>                        

                    <div style="width:80%; text-align: center; margin: 0 auto; margin-top: 40px;">
                        <a href="https://www.startappsolutions.com/auth/login" style="margin: 0 auto; background-color: {btn_color}; color: {text_color}; padding: 10px 20px; text-align: center;text-decoration: none; border-radius: 5px; font-size: 13px;">View Ticket</a>
                    </div>

                </div>
                <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #151030;">
                    <div style="width: 80%; margin: 0 auto; border-top: 1px gray solid; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                        <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                            <div style="margin: auto 0;"> Powered by</div>
                            <a href="https://www.startappsolutions.com/auth/login" style="margin: auto 0;"><img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;"></a>
                        </div>
                        <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
    """
    

    @classmethod
    def issue_template (cls, customer):
        return """
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en" style="font-family:arial, 'helvetica neue', helvetica, sans-serif">
                <head>
                <meta charset="UTF-8">
                <meta content="width=device-width, initial-scale=1" name="viewport">
                <meta name="x-apple-disable-message-reformatting">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta content="telephone=no" name="format-detection">
                <title>THANKS FOR SUBMITTING THE ISSUE</title><!--[if (mso 16)]>
                    <style type="text/css">
                    a {text-decoration: none;}
                    </style>
                    <![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]>
                <xml>
                    <o:OfficeDocumentSettings>
                    <o:AllowPNG></o:AllowPNG>
                    <o:PixelsPerInch>96</o:PixelsPerInch>
                    </o:OfficeDocumentSettings>
                </xml>
                <![endif]--><!--[if !mso]><!-- -->
                <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
                <link href="https://fonts.googleapis.com/css2?family=Righteous&display=swap" rel="stylesheet"><!--<![endif]-->
                <style type="text/css">
                #outlook a {
                    padding:0;
                }
                .es-button {
                    mso-style-priority:100!important;
                    text-decoration:none!important;
                }
                a[x-apple-data-detectors] {
                    color:inherit!important;
                    text-decoration:none!important;
                    font-size:inherit!important;
                    font-family:inherit!important;
                    font-weight:inherit!important;
                    line-height:inherit!important;
                }
                .es-desk-hidden {
                    display:none;
                    float:left;
                    overflow:hidden;
                    width:0;
                    max-height:0;
                    line-height:0;
                    mso-hide:all;
                }
                @media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:50px!important; text-align:center!important } h2 { font-size:26px!important; text-align:left } h3 { font-size:20px!important; text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:50px!important; text-align:center!important } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:26px!important; text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important; text-align:left } .es-menu td a { font-size:12px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:16px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:12px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:inline-block!important } a.es-button, button.es-button { font-size:20px!important; display:inline-block!important } .es-adaptive table, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0!important } .es-m-p0r { padding-right:0!important } .es-m-p0l { padding-left:0!important } .es-m-p0t { padding-top:0!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; max-height:inherit!important } .es-m-p5 { padding:5px!important } .es-m-p5t { padding-top:5px!important } .es-m-p5b { padding-bottom:5px!important } .es-m-p5r { padding-right:5px!important } .es-m-p5l { padding-left:5px!important } .es-m-p10 { padding:10px!important } .es-m-p10t { padding-top:10px!important } .es-m-p10b { padding-bottom:10px!important } .es-m-p10r { padding-right:10px!important } .es-m-p10l { padding-left:10px!important } .es-m-p15 { padding:15px!important } .es-m-p15t { padding-top:15px!important } .es-m-p15b { padding-bottom:15px!important } .es-m-p15r { padding-right:15px!important } .es-m-p15l { padding-left:15px!important } .es-m-p20 { padding:20px!important } .es-m-p20t { padding-top:20px!important } .es-m-p20r { padding-right:20px!important } .es-m-p20l { padding-left:20px!important } .es-m-p25 { padding:25px!important } .es-m-p25t { padding-top:25px!important } .es-m-p25b { padding-bottom:25px!important } .es-m-p25r { padding-right:25px!important } .es-m-p25l { padding-left:25px!important } .es-m-p30 { padding:30px!important } .es-m-p30t { padding-top:30px!important } .es-m-p30b { padding-bottom:30px!important } .es-m-p30r { padding-right:30px!important } .es-m-p30l { padding-left:30px!important } .es-m-p35 { padding:35px!important } .es-m-p35t { padding-top:35px!important } .es-m-p35b { padding-bottom:35px!important } .es-m-p35r { padding-right:35px!important } .es-m-p35l { padding-left:35px!important } .es-m-p40 { padding:40px!important } .es-m-p40t { padding-top:40px!important } .es-m-p40b { padding-bottom:40px!important } .es-m-p40r { padding-right:40px!important } .es-m-p40l { padding-left:40px!important } }
                @media screen and (max-width:384px) {.mail-message-content { width:414px!important } }
                </style>
                </head>
                <body style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
                <div dir="ltr" class="es-wrapper-color" lang="en" style="background-color:#314B70"><!--[if gte mso 9]>
                            <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                                <v:fill type="tile" color="#314B70"></v:fill>
                            </v:background>
                        <![endif]-->
                <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#314B70">
                    <tr>
                    <td valign="top" style="padding:0;Margin:0">
                    <table cellpadding="0" cellspacing="0" class="es-content" align="center" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                        <tr>
                        <td align="center" style="padding:0;Margin:0">
                        <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" background="https://eewwwlv.stripocdn.email/content/guids/CABINET_dd9759b09de82ede623cff0b42f718ca19c0a4f85f6337f81c705fd693708d47/images/simonleezftw1kvehgunsplash_1_1.png" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#07021F;background-repeat:no-repeat;width:600px;background-image:url(https://eewwwlv.stripocdn.email/content/guids/CABINET_dd9759b09de82ede623cff0b42f718ca19c0a4f85f6337f81c705fd693708d47/images/simonleezftw1kvehgunsplash_1_1.png);background-position:center bottom" role="none">
                            <tr>
                            <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px">
                            <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                <tr>
                                <td align="center" valign="top" style="padding:0;Margin:0;width:560px">
                                <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                    <tr>
                                    <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#FFFFFF;font-size:18px"><img src="https://startapperp.africa/img/logo/white.svg" alt="Logo" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" height="50" title="ECZ HRMIS"></a></td>
                                    </tr>
                                </table></td>
                                </tr>
                            </table></td>
                            </tr>
                            <tr>
                            <td class="es-m-p40t" align="left" style="Margin:0;padding-top:20px;padding-left:20px;padding-right:20px;padding-bottom:40px">
                            <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                <tr>
                                <td align="center" valign="top" style="padding:0;Margin:0;width:560px">
                                <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                    <tr class="es-mobile-hidden">
                                    <td align="center" height="85" style="padding:0;Margin:0"></td>
                                    </tr>
                                    <tr>
                                    <td align="center" style="padding:0;Margin:0;padding-bottom:15px;font-size:0px"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#FFFFFF;font-size:18px"><img src="https://eewwwlv.stripocdn.email/content/guids/CABINET_dd9759b09de82ede623cff0b42f718ca19c0a4f85f6337f81c705fd693708d47/images/bluebubblelikebuttoniconthumbsuplikesignfeedbackconceptwhitebackground3drendering.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="60"></a></td>
                                    </tr>
                                    <tr>
                                    <td align="center" style="padding:0;Margin:0;padding-bottom:25px;letter-spacing:5px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Manrope, sans-serif;line-height:18px;color:#efefef;font-size:12px">YOUR EXPERIENCE IS VERY IMPORTANT</p></td>
                                    </tr>
                                    <tr>
                                    <td align="center" style="padding:0;Margin:0;padding-bottom:40px"><h1 style="Margin:0;line-height:72px;mso-line-height-rule:exactly;font-family:Righteous, sans-serif;font-size:60px;font-style:normal;font-weight:bold;color:#FFFFFF">We take all your Issues seriously</h1></td>
                                    </tr>
                                    <tr>
                                    <td align="center" class="es-m-p0r es-m-p0l" style="padding:0;Margin:0;padding-bottom:40px;padding-left:40px;padding-right:40px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Manrope, sans-serif;line-height:27px;color:#FFFFFF;font-size:18px">Big thanks for flagging the issue! Our team's on it, working hard to fix things pronto. Your input is pure gold—stay tuned for updates. Appreciate you!</p></td>
                                    </tr>
                                </table></td>
                                </tr>
                            </table></td>
                            </tr>
                            <tr>
                            <td class="esdev-adapt-off" align="left" background="https://eewwwlv.stripocdn.email/content/guids/CABINET_beef27fd72bf04f5ec347afb3c9242a7a6cb9763af3e70ce8481235882b7a5b6/images/rectangle_5445.png" style="Margin:0;padding-left:20px;padding-right:20px;padding-top:30px;padding-bottom:30px;background-image:url(https://eewwwlv.stripocdn.email/content/guids/CABINET_beef27fd72bf04f5ec347afb3c9242a7a6cb9763af3e70ce8481235882b7a5b6/images/rectangle_5445.png);background-repeat:no-repeat;background-position:center center">
                            <table cellpadding="0" cellspacing="0" class="esdev-mso-table" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:560px">
                                <tr>
                                <td class="esdev-mso-td" valign="top" style="padding:0;Margin:0">
                                <table cellpadding="0" cellspacing="0" class="es-left" align="left" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                                    <tr>
                                    <td align="left" style="padding:0;Margin:0;width:223px">
                                    <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                        <tr>
                                        <td align="right" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#FFFFFF;font-size:18px"><img class="adapt-img" src="https://eewwwlv.stripocdn.email/content/guids/CABINET_beef27fd72bf04f5ec347afb3c9242a7a6cb9763af3e70ce8481235882b7a5b6/images/32226255_m001t0311_a_message_01sep22.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="100"></a></td>
                                        </tr>
                                    </table></td>
                                    </tr>
                                </table></td>
                                <td style="padding:0;Margin:0;width:20px"></td>
                                <td class="esdev-mso-td" valign="top" style="padding:0;Margin:0">
                                <table cellpadding="0" cellspacing="0" class="es-right" align="right" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                                    <tr>
                                    <td align="left" style="padding:0;Margin:0;width:317px">
                                    <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                        <tr>
                                        <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-bottom:20px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Manrope, sans-serif;line-height:27px;color:#FFFFFF;font-size:18px">Have a question?<br><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#FFFFFF;font-size:18px">Reach out to our team</a></p></td>
                                        </tr>
                                    </table></td>
                                    </tr>
                                </table></td>
                                </tr>
                            </table></td>
                            </tr>
                        </table></td>
                        </tr>
                    </table>
                    <table cellpadding="0" cellspacing="0" class="es-footer" align="center" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
                        <tr>
                        <td align="center" style="padding:0;Margin:0">
                        <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#07021F;width:600px">
                            <tr>
                            <td align="left" style="Margin:0;padding-left:20px;padding-right:20px;padding-top:40px;padding-bottom:40px">
                            <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                <tr>
                                <td align="left" style="padding:0;Margin:0;width:560px">
                                <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                    <tr>
                                    <td align="center" style="padding:0;Margin:0;font-size:0">
                                    <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                        <tr>
                                        <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#CCCCCC;font-size:12px"><img src="https://eewwwlv.stripocdn.email/content/assets/img/social-icons/logo-gray/facebook-logo-gray.png" alt="Fb" title="Facebook" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                                        <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#CCCCCC;font-size:12px"><img src="https://eewwwlv.stripocdn.email/content/assets/img/social-icons/logo-gray/twitter-logo-gray.png" alt="Tw" title="Twitter" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                                        <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#CCCCCC;font-size:12px"><img src="https://eewwwlv.stripocdn.email/content/assets/img/social-icons/logo-gray/instagram-logo-gray.png" alt="Ig" title="Instagram" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                                        <td align="center" valign="top" style="padding:0;Margin:0"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#CCCCCC;font-size:12px"><img src="https://eewwwlv.stripocdn.email/content/assets/img/social-icons/logo-gray/youtube-logo-gray.png" alt="Yt" title="Youtube" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                                        </tr>
                                    </table></td>
                                    </tr>
                                    <tr>
                                    <td align="center" style="padding:20px;Margin:0;font-size:0">
                                    <table border="0" width="65%" height="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                        <tr>
                                        <td style="padding:0;Margin:0;border-bottom:1px solid #cccccc;background:unset;height:1px;width:100%;margin:0px"></td>
                                        </tr>
                                    </table></td>
                                    </tr>
                                    <tr>
                                    <td style="padding:0;Margin:0">
                                    <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                        <tr class="links">
                                        <td align="right" valign="top" style="Margin:0;padding-top:10px;padding-bottom:10px;padding-left:15px;padding-right:15px;border:0"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Manrope, sans-serif;color:#CCCCCC;font-size:12px;font-weight:normal">Privacy Policy</a></td>
                                        <td align="left" valign="top" style="Margin:0;padding-top:10px;padding-bottom:10px;padding-left:15px;padding-right:15px;border:0"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Manrope, sans-serif;color:#CCCCCC;font-size:12px;font-weight:normal">Terms of use</a></td>
                                        </tr>
                                    </table></td>
                                    </tr>
                                    <tr>
                                    <td align="center" style="padding:0;Margin:0;padding-top:15px;padding-bottom:40px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Manrope, sans-serif;line-height:18px;color:#CCCCCC;font-size:12px">No longer want to receive these emails? <a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#CCCCCC;font-size:12px">Unsubscribe.</a></p></td>
                                    </tr>
                                    <tr>
                                    <td align="center" class="es-infoblock made_with" style="padding:0;Margin:0;line-height:14px;font-size:0;color:#CCCCCC"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#CCCCCC;font-size:12px"><img src="https://startapperp.africa/img/logo/white.svg" alt width="125" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                                    </tr>
                                </table></td>
                                </tr>
                            </table></td>
                            </tr>
                        </table></td>
                        </tr>
                    </table></td>
                    </tr>
                </table>
                </div>
                </body>
                </html>
        """,

    @classmethod
    def appointment(cls, customer, appointment_date, appointment_time, venue, description, company, logo=None):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>New User</title>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height:170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 20px; margin: auto; text-align: center; margin-top: 30px;">New Appointment</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                    <div style="background-color: #ffffff; color: #1f2937; padding: 1.5rem; margin-top: 1.5rem; border-radius: 0.5rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);">
                        <ul style="list-style: none; margin-bottom: 1rem; padding-left: 0;">
                            <li style="margin-bottom: 0.5rem;">Dear {customer}, you have an appointment with {company}</li>
                            <li style="margin-bottom: 0.5rem;">Appointment Date: {appointment_date} at {appointment_time}</li>
                            <li style="margin-bottom: 0.5rem;">Venue: {venue}</li>
                            <p style="font-size: 0.875rem; margin-top: 1rem;">Description: {description}</p>
                        </ul>
                    </div>
                    <div style="width:80%; text-align: center; margin: 0 auto; margin-top: 40px;">
                    </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px gray solid; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;"><img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;"></a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """   
    @classmethod
    def feedback(cls, subject, description):
            return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #172554; color: #FFFFFF;">
                <div style="max-width: 28rem; width: 80%; margin: 0 auto; padding: 2rem;">
                    <img src="your_logo.png" alt="Your Logo" style="display: block; margin: 0 auto; width: 6rem; height: auto; margin-bottom: 1.5rem;">
                    <h2 style="text-align: center; font-size: 1.875rem; font-weight: 800; margin-top: 0; margin-bottom: 0.75rem; color: #FFFFFF;">TICKET FEEDBACK</h2>
                    <div style="background-color: rgba(255, 255, 255, 0.9); border-radius: 1rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); color: #FFFFFF; overflow: hidden; padding: 1.5rem;">
                        <ul style="margin-bottom: 1rem; list-style: none; padding-left: 0;">
                            <li style="margin-bottom: 0.75rem; color:#172554;"><span style="color: #0f172a; font-size: 1.1rem;">Feedback :</span> {description}</li>
                        </ul>
                        <div>
                        </div>                    
                    </div>
                    
                    <footer style="text-align: center; color: #64748b; margin-top: 2rem; font-size: 1.1rem;">
                        <p>&copy; 2024 PBS. All rights reserved.</p>
                    </footer>
                </div>
            </body>
            </html>
            """ 
    @classmethod
    def tickets(cls, subject, description):
                return f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>
                <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #172554; color: #FFFFFF;">
                    <div style="max-width: 28rem; width: 80%; margin: 0 auto; padding: 2rem;">
                        <img src="your_logo.png" alt="Your Logo" style="display: block; margin: 0 auto; width: 6rem; height: auto; margin-bottom: 1.5rem;">
                        <h2 style="text-align: center; font-size: 1.875rem; font-weight: 800; margin-top: 0; margin-bottom: 0.75rem; color: #FFFFFF;">NEW TICKET/ISSUE</h2>
                        <div style="background-color: rgba(255, 255, 255, 0.9); border-radius: 1rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); color: #FFFFFF; overflow: hidden; padding: 1.5rem;">
                            <h1 style="font-size: 1.875rem; font-weight: 800; margin-bottom: 1rem; color: #172554; text-align: center;">{subject}</h1>
                            <ul style="margin-bottom: 1rem; list-style: none; padding-left: 0;">
                                <li style="margin-bottom: 0.75rem; color:#172554;"><span style="color: #0f172a; font-size: 1.1rem;">Description:</span> {description}</li>
                            </ul>
                            <div>
                            </div>                    
                        </div>
                        
                        <footer style="text-align: center; color: #64748b; margin-top: 2rem; font-size: 1.1rem;">
                            <p>&copy; 2024 PBS. All rights reserved.</p>
                        </footer>
                    </div>
                </body>
                </html>
                """ 
    @classmethod
    def news_letter(cls, subject, description):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #172554; color: #FFFFFF;">
            <div style="max-width: 28rem; width: 80%; margin: 0 auto; padding: 2rem;">
                <img src="your_logo.png" alt="Your Logo" style="display: block; margin: 0 auto; width: 6rem; height: auto; margin-bottom: 1.5rem;">
                <h2 style="text-align: center; font-size: 1.875rem; font-weight: 800; margin-top: 0; margin-bottom: 0.75rem; color: #FFFFFF;">OUR NEWS LETTER</h2>
                <div style="background-color: rgba(255, 255, 255, 0.9); border-radius: 1rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); color: #FFFFFF; overflow: hidden; padding: 1.5rem;">
                    <h1 style="font-size: 1.875rem; font-weight: 800; margin-bottom: 1rem; color: #172554; text-align: center;">{subject}</h1>
                    <ul style="margin-bottom: 1rem; list-style: none; padding-left: 0;">
                        <li style="margin-bottom: 0.75rem; color:#172554;"><span style="color: #0f172a; font-size: 1.1rem;">Description:</span> {description}</li>
                    </ul>
                    <div>
                    </div>                    
                </div>
                
                <footer style="text-align: center; color: #64748b; margin-top: 2rem; font-size: 1.1rem;">
                    <p>&copy; 2024 PBS. All rights reserved.</p>
                </footer>
            </div>
        </body>
        </html>
        """ 
    @classmethod
    def lead_assignment(cls, first_name, subject, memo_body,logo=None):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>New User</title>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height:170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px;">New Assignemnt</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                        <h3 style="width: 80%; margin: 0 auto; margin-top: 30px;">{subject}</h3>
                        <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 30px;">{memo_body}</p>
                        <div style="width:80%; text-align: center; margin: 0 auto; margin-top: 40px;">
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px gray solid; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;"><img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;"></a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """ 
                    
            
