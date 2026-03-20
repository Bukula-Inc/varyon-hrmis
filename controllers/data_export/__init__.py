from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.data_export.export_script import export_script
import csv
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
utils = Utils()
dates = Dates()

pp = utils.pretty_print
throw = utils.throw

class Data_Export:
    def __init__(self, dbms, object) -> None:
        self.exclusive = ["id", "idx", "disabled", "status_info", "doctype", "owner", "modified_by", "creation_time", "docstatus", "linked_fields"]
        self.dbms = dbms
        self.object = object
        self.docs = utils.string_to_json(self.object.headers.Docs).data
        self.model = self.object.headers.Model
        self.filters = {}
        if self.object.headers.get("File-Type"):
            self.file_type = self.object.headers.get("File-Type").lower()
        else:
            throw("File-Type not included in headers")
        if self.object.headers.get("Filters"):
            f = utils.string_to_json(self.object.headers.get("Filters"))
            if f.status == utils.ok:
                self.filters = f.data

    def export_data(self):
        filters = {**self.filters}
        if self.docs and len(self.docs) > 0:
            filters["id__in"] = self.docs
        docs = self.dbms.get_list(self.model, filters=filters, user=self.object.user, fetch_linked_tables=True, fetch_linked_fields=True)
        if docs.status == utils.ok:
            self.data = docs.data.rows
            if export_script.get(self.model):
                try:
                    result = export_script[self.model](self.dbms, self.object, self.data)
                    if result and result.status == utils.ok and result.data:
                        self.data = result.data
                    else:
                        return utils.respond(utils.internal_server_error, "Improper Response formatting!")
                except Exception as e:
                    return utils.respond(utils.internal_server_error, f"Improper Response formatting: {e}")
        
            if self.file_type == "csv":
                return self.export_csv()
            if self.file_type == "excel":
                return self.export_excel()
    
    def export_csv(self):
        df = pd.DataFrame(utils.from_object_to_dict(self.data))
        try:
            df = df.drop(columns=self.exclusive)
        except Exception as e:
            print(str(e))
        
        response = HttpResponse(df.to_csv(index=False), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        return utils.respond(utils.ok, response)

    def export_excel(self):
        df = pd.DataFrame(utils.from_object_to_dict(self.data))
        df = df.drop(columns=self.exclusive)
        buffer = BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            df.to_excel(writer, index=False)
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
        return utils.respond(utils.ok, response)
