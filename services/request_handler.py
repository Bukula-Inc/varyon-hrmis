# necessary imports
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from . import Services
from .validation import Validation
from controllers.utils import Utils
from controllers.dbms import DBMS
utils = Utils()
services = Services()
validation = Validation()


@csrf_exempt
@require_POST
def new_tenant(request):
    try:
        validated = validation.validate_request(request)
        dbms = DBMS(init_admin=True)
        if validated.status != utils.ok:
            return JsonResponse(validated, status=validated.status)
        result = services.register_tenant(validated.data, dbms)
        return JsonResponse(result, status=result.status, safe=False)
    except Exception as e:
        return JsonResponse(utils.internal_server_error, f"FAILD TO RUN THIS SERVICE: {e}")


@csrf_exempt
@require_POST
def migrate(request):
    try:
        validated = validation.validate_request(request)
        if validated.status!= utils.ok:
            return JsonResponse(validated, status=validated.status)
        result = services.migrate_tenant(validated.data)
        return JsonResponse(result, status=result.status, safe=False)
    except Exception as e:
        return JsonResponse(utils.internal_server_error, f"FAILD TO RUN THIS SERVICE: {e}")
    

@csrf_exempt
@require_POST
def delete_module_migrations(request):
    try:
        validated = validation.validate_request(request)
        if validated.status != utils.ok:
            return JsonResponse(validated, status=validated.status)
        result = services.delete_module_migrations(validated.data)
        return JsonResponse(result, status=result.status, safe=False)
    except Exception as e:
        return JsonResponse(utils.internal_server_error, f"FAILD TO RUN THIS SERVICE: {e}")


@csrf_exempt
@require_POST
def delete_module_tables(request):
    try:
        validated = validation.validate_request(request)
        if validated.get("status") != utils.ok:
            return JsonResponse(validated, status=validated.status)
        result = services.delete_module_tables(validated.data)
        return JsonResponse(result, status=result.status, safe=False)
    except Exception as e:
        return JsonResponse(utils.internal_server_error, f"FAILD TO RUN THIS SERVICE: {e}")


@csrf_exempt
@require_POST
def full_migration(request):
    try:
        validated = validation.validate_request(request)
        if validated.status!= utils.ok:
            return JsonResponse(validated, status=validated.get("status"))
        result = services.full_migration(validated.data)
        return JsonResponse(result, status=result.status, safe=False)
    except Exception as e:
        return JsonResponse(utils.internal_server_error, f"FAILD TO RUN THIS SERVICE: {e}")
    
@csrf_exempt
@require_POST
def create_tenant_default_data(request):
    try:
        validated = validation.validate_request(request)        
        dbms = DBMS(validated.data, skip_user_validation=True)
        if validated.status != utils.ok:
            return JsonResponse(validated, status=validated.status)
        result = services.create_tenant_default_data(dbms, validated.data)
        return JsonResponse(result, status=result.status, safe=False)
    except Exception as e:
        return JsonResponse(utils.internal_server_error, f"FAILD TO RUN THIS SERVICE: {e}")

