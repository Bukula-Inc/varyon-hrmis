from controllers.hooks import form_hooks, listview_hooks, report_hooks, script_reports, x_fetch, x_post, dashboards
from controllers.utils import Utils

utils = Utils()
pp = utils.pretty_print
throw = utils.throw
class Hooks_Controller:
    def __init__(self, dbms, object) -> None:
        self.params = object
        self.dbms = dbms
        self.method = getattr(object, "method", None)
        self.url_object = getattr(object, "url_params", None)
        self.body = getattr(object, "body", None)
        self.model = getattr(object, "model", None)
        self.get_single = getattr(object, "get_single", None)
        self.xfunction = getattr(object, "xfunction", None)
        self.filters = getattr(object, "filters", None)
        self.page_size = getattr(object, "page_size", None)
        self.current_page = getattr(object, "current_page", None)
        self.order_by = getattr(object, "order_by", None)
        self.group_by = getattr(object, "group_by", None)
        self.fields = getattr(object, "fields", None)
        self.headers = getattr(object, "headers", None)
        self.is_report = getattr(object, "is_report", None)
        self.has_fetched = False
        self.fetch_result= None
        self.fetch_linked_tables = getattr(object, "fetch_linked_tables", None)
        self.fetch_linked_fields = getattr(object, "fetch_linked_fields", None)
        self.params.user = getattr(self.headers, "user", None)
        self.files = getattr(self.params, "files",None)
        self.hook_type = None

    def init_hooks(self, request_types):
        self.method = request_types
        # HOOKS FOR POSTING DATA
        if self.method == utils.REQUEST_TYPE_POST:
            events = form_hooks.get(self.model)
            if events:
                if  self.hook_type == "before_save":
                    before_save = events.get("before_save")
                    if before_save:
                        for event in before_save:
                            event(self.dbms,self.params)
                else:
                    after_save = events.get("after_save")
                    if after_save:
                        for event in after_save:
                            event(self.dbms,self.params, self.result)

        # HOOKS FOR POSTING DATA
        if self.method == utils.REQUEST_TYPE_PATCH:
            events = form_hooks.get(self.model)
            if events:
                if self.hook_type == "before_update":
                    before_update = events.get("before_update")
                    if before_update:
                        for event in before_update:
                            event(self.dbms,self.params)
                elif self.hook_type == "after_update":
                    after_update = events.get("after_update")
                    if after_update:
                        for event in after_update:
                            event(self.dbms,self.params, self.result)

        if self.method == utils.REQUEST_TYPE_PUT:
            events = form_hooks.get(self.model)
            if events:
                if self.hook_type == "before_submit":
                    before_submit = events.get("before_submit")
                    if before_submit:
                        for event in before_submit:
                            event(self.dbms, self.params)
                            
                elif self.hook_type == "after_submit":
                    
                    after_submit = events.get("after_submit")
                    if after_submit:
                        for event in after_submit:
                            try:
                                event(self.dbms,self.params, self.result)
                            except Exception as e:
                                pp(f"After Submit Hook error:{e}")

        # HOOKS FOR FETCHING DATA
        if self.method == utils.REQUEST_TYPE_GET:
            # if self.is_single_doc:
            events = form_hooks.get(self.model)
            if events:
                if self.hook_type == "before_fetch":
                    before_fetch = events.get("before_fetch")
                    if before_fetch:
                        for event in before_fetch:
                            event(self.dbms, self.params)

                if self.hook_type == "after_fetch":
                    after_fetch = events.get("after_fetch")
                    if after_fetch:
                        for event in after_fetch:
                            event(self.dbms, self.params, self.params.body)


        if self.method == utils.REQUEST_TYPE_CANCEL:
            events = form_hooks.get(self.model)
            if events:
                before_cancel = events.get("before_cancel")
                if before_cancel:
                    for event in before_cancel:
                        event(self.dbms,self.params)

        if self.method == utils.REQUEST_TYPE_DELETE:
            events = form_hooks.get(self.model)
            if events:
                before_delete = events.get("before_delete")
                if before_delete:
                    for event in before_delete:
                        event(self.dbms,self.params)
