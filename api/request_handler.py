# necessary imports
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from controllers.utils import Utils
from controllers.dbms import DBMS
from .exec import Exec


utils = Utils()
pp = utils.pretty_print
throw = utils.throw
@csrf_exempt
@require_POST
def authenticate (request):
    validation = utils.validate_request(request, ignore_model=True)
    if validation.status != utils.ok:
        return JsonResponse(validation, status=validation.status)
    validated_date = validation.data
    validated_date.method = utils.REQUEST_TYPE_AUTHENTICATE
    dbms = DBMS (validated_date)
    ex = Exec (dbms, validated_date)
    result = ex.execute()
    return JsonResponse(result, status=result.status,safe=False)

@csrf_exempt
def request_password_reset(request):
    validation = utils.validate_request(request,ignore_model=True)
    if validation.get('status') != utils.ok:
        return JsonResponse(validation, status=validation.status)
    validated_date = validation.get ('data')
    validated_date.method = utils.REQUEST_TYPE_RESET_PASSWORD
    dbms = DBMS (validated_date)
    ex = Exec (dbms, validated_date)
    results = ex.execute ()
    return utils.json_respond(results.status,results)

@csrf_exempt
def request_password_reset_validation(request):
    validation = utils.validate_request(request,ignore_model=True)
    if validation.get ('status') != utils.ok:
        return JsonResponse(validation, status=validation.status)
    validated_date = validation.get ('data')
    validated_date.method = utils.REQUEST_TYPE_PASSWORD_RESET_VALIDATION
    dbms = DBMS (validated_date)
    ex = Exec (dbms, validated_date)
    results = ex.execute ()
    return utils.json_respond(results.status, results)

@csrf_exempt
@require_GET
def get_data(request):
    try:
        validation = utils.validate_request(request)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        # initialize dbms
        dbms = DBMS(validation_data)
        ex = Exec(dbms, validation_data)
        result = ex.execute()
        return JsonResponse(result, status=result.status, safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO FETCH DATA: {str(e)}")


@csrf_exempt
@require_GET
def x_fetch(request):
    try:
        validation = utils.validate_request(request,True)
        if validation.status != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        validation_data.method = utils.REQUEST_TYPE_X_FETCH
        if not validation_data.headers.Xfun:
            return JsonResponse(utils.respond(utils.not_found,"'xfun' parameter not present in your headers!"),status=utils.not_found,safe=False)
        # initialize dbms
        dbms = DBMS(validation_data)
        ex = Exec(dbms, validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status, safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO FETCH DATA: {str(e)}")
    

@csrf_exempt
@require_GET
def dashboard(request):
   
    try:
        validation = utils.validate_request(request,True)
        if validation.status != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        validation_data.method = utils.REQUEST_TYPE_DASHBOARD
        if not validation_data.headers.Xfun:
            return JsonResponse(utils.respond(utils.not_found,"'xfun' parameter not present in your headers!"),status=utils.not_found,safe=False)
        # initialize dbms
        dbms = DBMS(validation_data)
        ex = Exec(dbms, validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO FETCH DATA: {str(e)}")


@csrf_exempt
@require_POST
def post_data(request):
    try:
        validation = utils.validate_request(request)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result, status=result.status, safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO POST DATA: {str(e)}")
    

@csrf_exempt
@require_POST
def upload_data(request):
    try:
        validation = utils.validate_request(request, ignore_model=True, is_upload_request=True)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        
        validation_data.method = utils.REQUEST_TYPE_UPLOAD
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        validation_data.files = request.FILES
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO UPLOAD DATA: {str(e)}")
    
@csrf_exempt
@require_POST
def extract_doc_data(request):
    try:
        validation = utils.validate_request(request, ignore_model=True, is_upload_request=True)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation, status=validation.status)
        validation_data = validation.data
        validation_data.method = utils.REQUEST_TYPE_EXTRACT_DOC_DATA
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        validation_data.files = request.FILES
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO EXTRACT DATA: {str(e)}")
    

@csrf_exempt
@require_POST
def x_post(request):
    try:
        validation = utils.validate_request(request,True)
        if validation.status != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        validation_data.method = utils.REQUEST_TYPE_X_POST
        if not validation_data.headers.Xfun:
            return JsonResponse(utils.respond(utils.not_found,"'xfun' parameter not present in your headers!"),status=utils.not_found,safe=False)
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO POST DATA: {str(e)}")
    

@csrf_exempt
@require_POST
def core(request):
    try:
        validation = utils.validate_request(request,True)
        if validation.status != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        validation_data.method = utils.REQUEST_TYPE_CORE
        if not validation_data.headers.Xfun:
            return JsonResponse(utils.respond(utils.not_found,"'xfun' parameter not present in your headers!"),status=utils.not_found,safe=False)
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
       return utils.json_respond(utils.internal_server_error, f"FAILED TO POST DATA: {str(e)}")
    


@csrf_exempt
@require_POST
def export_data(request):
    try:
        validation = utils.validate_request(request,True)
        if validation.status != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        validation_data.method = utils.REQUEST_TYPE_EXPORT_DATA
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        if result.status == utils.ok:
            return result.data
        return result
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO EXPORT DATA: {str(e)}")



@csrf_exempt
@require_POST
def workflow_action(request):
    try:
        validation = utils.validate_request(request,True)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        validation_data.method = utils.REQUEST_TYPE_WORKFLOW_ACTION
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
       return utils.json_respond(utils.internal_server_error, f"FAILED TO UPDATE WORKFLOW: {str(e)}")


@csrf_exempt
@require_http_methods(["PATCH"])
def patch_data(request):
    try:
        validation = utils.validate_request(request)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO UPDATE DATA: {str(e)}")
    

@csrf_exempt
@require_http_methods(["PUT"])
def submit_doc(request):
    try:
        validation = utils.validate_request(request)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO SUBMIT DATA: {str(e)}")
    

@csrf_exempt
@require_http_methods(["PUT"])
def cancel_doc(request):
    try:
        validation = utils.validate_request(request)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        # initialize dbms
        validation_data.method = utils.REQUEST_TYPE_CANCEL
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO CANCEL DATA: {str(e)}")

 
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_data(request):
    try:
        validation = utils.validate_request(request)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO DELETE DATA: {str(e)}")
    


@csrf_exempt
@require_http_methods(["DELETE"])
def truncate(request):
    try:
        validation = utils.validate_request(request, ignore_model=True)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        validation_data.method = utils.REQUEST_TYPE_TRUNCATE
        # initialize dbms
        dbms = DBMS(validation_data)
        # init executor
        ex = Exec(dbms,validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO TRUNCATE DATA: {str(e)}")



@csrf_exempt
@require_GET
def get_form_fields(request):
    try:
        validation = utils.validate_request(request)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        validation_data.method = utils.REQUEST_TYPE_FETCH_FORM_FIELDS
        # initialize dbms
        dbms = DBMS(validation_data)
        validation_data.is_report = True
        ex = Exec(dbms, validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO FETCH REPORT: {str(e)}")
    
    
@csrf_exempt
@require_GET
def get_reports(request):
    try:
        validation = utils.validate_request(request)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        try:
            validation_data.filters = utils.string_to_json(validation_data.headers.Filters).get("data")
        except Exception as e:
            validation_data.filters = {}
        # initialize dbms
        dbms = DBMS(validation_data)
        validation_data.is_report = True
        ex = Exec(dbms, validation_data)
        result = ex.execute()
        return JsonResponse(result,status=result.status,safe=False)
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, f"FAILED TO FETCH REPORT: {str(e)}")
    



@csrf_exempt
@require_GET
def download_report(request):
    from controllers.download_controller import Download_Controller
    try:
        validation = utils.validate_request(request)
        if validation.get("status") != utils.ok:
            return JsonResponse(validation,status=validation.status)
        validation_data = validation.data
        fields = []
        if validation_data.fields:
            f = utils.string_to_json(validation_data.fields)
            if f.status == utils.ok:
                fields = f.data
        try:
            validation_data.filters = utils.string_to_json(validation_data.headers.Filters).get("data")
        except Exception as e:
            validation_data.filters = {}
        # initialize dbms
        dbms = DBMS(validation_data)
        validation_data.is_report = True
        ex = Exec(dbms, validation_data)
        result = ex.execute()
        if result.status == utils.ok:
            report_format = validation_data.headers.Format or "csv"
            title = validation_data.headers.Title or validation_data.model
            dc = Download_Controller(dbms,validation_data, title)
            result = dc.download_report(result.data.rows, report_format , fields, title)
            response = FileResponse(result, as_attachment=True, filename=f"{title}.{report_format}")
            response['Content-Disposition'] = f'attachment; filename="{title}.{report_format}"'
            return response
    except Exception as e:
        return utils.json_respond(utils.internal_server_error, str(e))