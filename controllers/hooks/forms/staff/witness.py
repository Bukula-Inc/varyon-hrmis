from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion


dates = Dates ()

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw

def on_witness_submit (dbms, object):
    core_hr = Core_Hr (dbms)
    obj = DataConversion.safe_get (object, "body")
    doc = DataConversion.safe_get (obj, "doc")
    document_type = DataConversion.safe_get (obj, "document_type")
    employee = DataConversion.safe_get (obj, "employee")
    witnesses = DataConversion.safe_get (obj, "witnesses")
    consent = DataConversion.safe_get (obj, "consent")

    get_doc = core_hr.get_doc (document_type, doc)
    ref_doc = DataConversion.safe_get (get_doc, "ref_doc")
    application = DataConversion.safe_get (get_doc, "application")
    application_doc = core_hr.get_doc (ref_doc, application)
    
    if not doc:
        throw ("<strong class='text-rose-600'>Document Name is Missing</strong>")
    if not document_type:
        throw ("<strong class='text-rose-600'>Document Type is Missing</strong>")
    if not employee:
        throw ("<strong class='text-rose-600'>Applicant is Missing</strong>")
    if not witnesses:
        throw ("<strong class='text-rose-600'>Witness is Missing</strong>")
    emp = core_hr.get_doc ("Employee", employee)
    witness = core_hr.get_doc ("Employee", witnesses)
    if not emp:
        throw (f"<strong class='text-rose-600'>Applicant with No/ID {employee} was not FOUND</strong>")
    if not witness:
        throw (f"<strong class='text-rose-600'>Witness with No/ID {witnesses} was Not FOUND</strong>")
    if not consent:
        throw ("<strong class='text-rose-600'>Select your consent</strong>")
    if consent not in ["Agree", "Disagree"]:
        throw ("Select a valid consent either be <strong class='text-rose-600'>(Disagree/Agree) </strong>")
    
    witnessing_doc = core_hr.get_doc ("Witnesses_Doc", doc)
    
    if not witnessing_doc:
        throw ("<strong class='text-rose-600'>Document Name is Missing</strong>")
    
    constent_ = False
    if DataConversion.safe_e (consent, "Agree", str, True):
        constent_ = True

    total_witnesses = DataConversion.safe_get (witnessing_doc, "total_witnesses")
    total_witnessed = DataConversion.convert_to_float(DataConversion.safe_get (witnessing_doc, "total_witnessed")) + 1 if constent_ else DataConversion.convert_to_float(DataConversion.safe_get (witnessing_doc, "total_witnessed")) + 0

    if DataConversion.safe_e (total_witnessed, total_witnesses, int):
        DataConversion.safe_set (get_doc, "status", "Witnessed")
        DataConversion.safe_set (get_doc, "has_witnesses", 1)
        r = dbms.update (document_type, get_doc, update_submitted=True)
        pp ("=================>>>>>>>>>>>>>>>>APPLICATION UPDATE<<<<<<<<<<<<<<<=====================",r)
    DataConversion.safe_set (witnessing_doc, "total_witnessed", total_witnessed)
    u = dbms.update ("Witnesses_Doc", witnessing_doc, update_submitted=True)
    pp ("=================>>>>>>>>>>>>>>>>WITNESSES DOC UPDATE<<<<<<<<<<<<<<<=====================", u)

    if application_doc:
        linked_fields = DataConversion.safe_get (application_doc, "linked_fields", {})
        emp = DataConversion.safe_get (linked_fields, "employee_no", DataConversion.safe_get (application_doc, "employee"))
        if emp:
            body = ""
            if not constent_:
                body = f"""
                    <!DOCTYPE html>
                        <html>
                        <head>
                        <meta charset="UTF-8" />
                        <title>Email Notification</title>
                        </head>
                        <body style="margin:0; padding:0; background-color:#f5f5f5; font-family:Arial, sans-serif;">

                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f5f5; padding:20px 0;">
                            <tr>
                            <td align="center">
                                <!-- Container -->
                                <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; padding:20px; border:1px solid #e0e0e0;">
                                
                                <!-- Header -->
                                <tr>
                                    <td style="text-align:center; padding-bottom:20px;">
                                    <h2 style="margin:0; font-size:24px; color:#333;">Notification: Witness Rejection - {doc}</h2>
                                    </td>
                                </tr>

                                <!-- Message -->
                                <tr>
                                    <td style="font-size:15px; color:#555; line-height:1.6;">
                                    <p>Hi {DataConversion.safe_get (emp, "full_name")},</p>

                                    <p>
                                        I hope you’re doing well. I'm reaching out to notify you about 
                                        <strong style="color:#000;">Your Request For {witnesses} to be a witness for {doc} which is linked to {str (ref_doc).replace ("_", " ")} Application has been rejected</strong>.
                                    </p>
                                    <p>Thank you for your attention.</p>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>

                        </body>
                    </html>
                """
            else:
                body = f"""
                    <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="UTF-8" />
                            <title>Email Notification</title>
                        </head>
                        <body style="margin:0; padding:0; background-color:#f5f5f5; font-family:Arial, sans-serif;">

                            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f5f5; padding:20px 0;">
                                <tr>
                                <td align="center">
                                    <!-- Container -->
                                    <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; padding:20px; border:1px solid #e0e0e0;">
                                    
                                    <!-- Header -->
                                    <tr>
                                        <td style="text-align:center; padding-bottom:20px;">
                                        <h2 style="margin:0; font-size:24px; color:#333;">Notification: Witness Accepted - {doc}</h2>
                                        </td>
                                    </tr>

                                    <!-- Message -->
                                    <tr>
                                        <td style="font-size:15px; color:#555; line-height:1.6;">
                                        <p>Hi {DataConversion.safe_get (emp, "full_name")},</p>

                                        <p>
                                            I hope you’re doing well. I'm reaching out to notify you about 
                                            <strong style="color:#000;">Your Request For {witnesses} to be a witness for {doc} which is linked to {str (ref_doc).replace ("_", " ")} Application has been accepted</strong>.
                                        </p>
                                        <p>Thank you for your attention.</p>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </table>
                        </body>
                    </html>
                """
            r = core_hr.mailing.send_mail (recipient=DataConversion.safe_get (emp, "email"), body=body, subject=f"""WITNESSING OF {str (document_type).replace ('_', '')}""")


def on_witness_save (dbms, object):
    core_hr = Core_Hr (dbms)
    obj = DataConversion.safe_get (object, "body")
    doc = DataConversion.safe_get (obj, "doc")
    document_type = DataConversion.safe_get (obj, "document_type")
    employee = DataConversion.safe_get (obj, "employee")
    witnesses = DataConversion.safe_get (obj, "witnesses")
    consent = DataConversion.safe_get (obj, "consent")

    if not doc:
        throw ("<strong class='text-rose-600'>Document Name is Missing</strong>")
    if not document_type:
        throw ("<strong class='text-rose-600'>Document Type is Missing</strong>")
    if not employee:
        throw ("<strong class='text-rose-600'>Applicant is Missing</strong>")
    if not witnesses:
        throw ("<strong class='text-rose-600'>Witness is Missing</strong>")
    emp = core_hr.get_doc ("Employee", employee)
    witness = core_hr.get_doc ("Employee", witnesses)
    if not emp:
        throw (f"<strong class='text-rose-600'>Applicant with No/ID {employee} was not FOUND</strong>")
    if not witness:
        throw (f"<strong class='text-rose-600'>Witness with No/ID {witnesses} was Not FOUND</strong>")
    if not consent:
        throw ("<strong class='text-rose-600'>Select your consent</strong>")
    if consent not in ["Agree", "Disagree"]:
        throw ("Select a valid consent either be <strong class='text-rose-600'>(Disagree/Agree) </strong>")
    
    witnessing_doc = core_hr.get_doc ("Witnesses_Doc", doc)
    
    if not witnessing_doc:
        throw ("<strong class='text-rose-600'>Document Name is Missing</strong>")