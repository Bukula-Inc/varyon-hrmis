from django.shortcuts import render
from jinja2 import Environment, FileSystemLoader
from django.http import HttpResponse
from controllers.utils import Utils
from controllers.dbms import DBMS
from controllers.print_controller import Print_Controller
utils = Utils()

def print_doc(request, print_format, model, doc,is_download_request):
    pc = Print_Controller(request,model,print_format,doc,is_download_request)
    __format = pc.generate_print_doc()
    if __format.get("status") != utils.ok:
        utils.throw(f"SOMETHING WENT WRONG WHILE RENDERING THE PRINT FORMAT")
    response = __format.get("data")
    return response

