from django.shortcuts import render
from controllers.utils import Utils
from multitenancy.settings import TENANT_ADMIN
from django.http import Http404
utils = Utils()
pp = utils.pretty_print

class Web_Controller:
    def __init__(self, request, page="home"):
        self.request = request
        self.page = page
        self.current_page = request.path

        
    def render_page(self):
        validation = utils.validate_request(self.request,ignore_model=True)
        if validation.get("status") == utils.ok:
            data = validation.get("data")
            if self.request.tenant_db == TENANT_ADMIN.get("DB"):
                return render(self.request, f"website/main/{self.page}.html")

            return render(self.request, f"authentication/unauthorized.html")