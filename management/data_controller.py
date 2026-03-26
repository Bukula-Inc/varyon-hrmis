from controllers.utils import Utils
from controllers.utils.dates import Dates
from management.defaults import default_inserts
from management.defaults.core.doc_status import doc_status
from management.defaults.core.default_company import default_company
from management.defaults.payroll.income_tax_band import income_tax_band
from management.defaults.payroll.salary_component import salary_component
from services.raw import Raw
from management.defaults.core.nav import nav
from management.defaults.core.default_dashboard import default_dashboard
from management.defaults.core.role import role
utils = Utils()
dates = Dates()
raw = Raw()

pp = utils.pretty_print
throw = utils.throw
 
class Data_Controller:
    def __init__(self, dbms) -> None:
        self.dbms = dbms
        self.admin_dbms = raw.connect_tenant(admin=True)
        self.admin = utils.from_dict_to_object()
        
    def accrual_holidays (self):
        this_years_holiday_list = dates._init_holidays ("ZM")
        obj = utils.from_dict_to_object ({
            "calendar_holidays": this_years_holiday_list
        })
        holidays = self.dbms.create("Calender", body=obj,  privilege=True)
        


    def create_doc_statuses(self):
        model = "Doc_Status"
        rows = doc_status.get("data")
        successful = []
        failed = []

        if rows and isinstance(rows,list):
            for row in rows:
                new_status = self.dbms.create(model,utils.from_dict_to_object(row),None, privilege=True)
                if new_status.get("status") == utils.ok:
                    successful.append(new_status.get("data"))
                else:
                    error = {"message": new_status.get("error_message")} 
                    error["data"] = row
                    failed.append(error)
        return utils.respond(utils.ok,{"successful":successful,"failed":failed})

    def create_tenant_api_key(self):
        tenant = self.admin_dbms.get_doc("Tenant", self.tenant.name, skip_user_evaluation=True)
        if tenant.status == utils.ok and not tenant.data.api_key:
            tenant.data.api_key = utils.generate_client_api_key({"tnt": f"{self.tenant.db_name}&%{self.tenant.id}"})
            update = self.admin_dbms.update("Tenant", tenant.data, skip_user_evaluation=True)
            if update.status != utils.ok:
                throw("Failed to update Tenant API Key!")

    def map_existing_tenant_users_to_user_pool(self):
        users = self.dbms.get_list("Lite_User", privilege=True)
        if users.status == utils.ok:
            pool_list = utils.from_dict_to_object()
            user_pool = self.admin_dbms.get_list("User_Pool",  privilege=True)
            if user_pool.status == utils.ok:
                pool_list = utils.array_to_dict(user_pool.data.rows,"name")
            for usr in users.data.rows:
                if not pool_list.get(usr.name):
                    new_pool_user = self.admin_dbms.create("User_Pool",utils.from_dict_to_object({"name": usr.name, "tenant":self.tenant.name}), privilege=True)


    def create_admin_user(self):
        tnt = utils.from_dict_to_object({
            "email": "admin1@varyon-hrmis.com",
            "first_name":"Administrator",
            "password": "@skytech3varyon@2026",
            "doctype":"Lite_User",
            "name":"admin1@varyon-hrmis.com",
            "first_name":"Administrator",
            "middle_name":"",
            "last_name":"",
            "contact_no":"",
            "gender":"",
            "is_superuser":True,
            "is_active": True,
            "is_staff": True,
            "user_permissions":"",
            "user_roles":"",
            "groups":"",
            "main_role":"Super Admin"
        })
        tnt.email = f"admin{self.tenant.id}@varyon-hrmis.com"
        tnt.name = tnt.email
        tnt.tenant = self.tenant.name
        try: 
            admin = self.dbms.create("Lite_User", tnt, skip_user_evaluation=True, fetch_if_exists=True,)
            if admin.status == utils.ok:
                self.admin = admin.data
                return admin
            else:
                if self.dbms.admin_user:
                    self.admin = self.dbms.admin_user
        except Exception as e:
            return utils.respond(admin.get("status"),f"Admin User Creation Failed: {e}")
        
    
    def create_tenant_company(self):
        pp(self.tenant.is_admin)
        try:
            if not self.tenant.is_admin:
                field="name"
                cust = self.tenant.customer
                if not cust:
                    field = "id"
                    cust = self.tenant.customer_id
                customer = self.admin_dbms.get_doc("Customer", cust, fetch_by_field=field, privilege=True, fetch_linked_fields=True)
                if customer.status == utils.ok:
                    cust= customer.data
                    self.customer = cust
                    currency = None
                    if cust.country:
                        currency_info = self.dbms.get_list("Currency",filters={"country": cust.country or "Zambia"},privilege=True)
                        if currency_info.status == utils.ok:
                            curr = currency_info.data.rows[0].name
                            currency = curr
                        else:
                            currency = "ZMW"
                        company = utils.from_dict_to_object({})
                        company.name = cust.name
                        company.industry = cust.industry
                        company.sector = cust.sector
                        company.country = cust.country
                        company.tax_identification_no = cust.tax_identification_no
                        company.email = cust.email
                        company.contact_no = cust.contact_no
                        company.reporting_currency = currency
                        company.physical_address = cust.physical_address
                        company.postal_address = cust.postal_address
                        company.company_logo = "/media/defaults/logo/default.svg"
                        company.status = "Active"
                        company_dets = self.dbms.get_doc("Company", company.name, privilege=True)
                        if company_dets.status == utils.ok:
                            self.company = company_dets.data
                        else:
                            comp =  self.dbms.create("Company", company, privilege=True)
                            if comp.status == utils.ok:
                                self.company = comp.data
                            else:
                                throw(f"Failed to create tenant company:{comp.error_message}")
                        return self.company
            else:
                pp("Creating Admin Tenant Company...")
                admin_company = self.admin_dbms.get_doc("Company", "ECZ", privilege=True)
                pp(admin_company)
                if admin_company.status == utils.ok:
                    self.company = admin_company.data
                else:
                    comp = utils.from_dict_to_object(default_company)
                    comp.name = self.tenant.name
                    create = self.admin_dbms.create("Company", default_company, privilege=True)
                    if create.status == utils.ok:
                        self.company = create.data
                return self.company

        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{e}")

    def create_cost_center(self):
        cost_center= utils.from_dict_to_object({})
        cost_center.name = f"{self.company.name} Main"
        cost_center.company = self.company.name
        cost_center.status = "Active"
        center =  self.dbms.create("Cost_Center", cost_center, privilege=True, fetch_if_exists=True)
        return center
    
    def create_nav_menus(self):
        successful = []
        failed = []
        if nav and len(nav) > 0:
            for module_nav in  nav:
                menu_card_seq = 1
                module = module_nav.get("module")
                existing_menu_cards = utils.from_dict_to_object()
                mcds = self.dbms.get_list("Menu_Card", privilege=True, filters={"module":module}, fetch_linked_tables=True)
                if mcds.status == utils.ok:
                    existing_menu_cards = utils.array_to_dict(mcds.data.rows,"name", True)

                for card in module_nav.get("content"):
                    card = utils.from_dict_to_object(card)
                    card_title = card.title
                    if card_title:
                        card.idx = menu_card_seq
                        menu_card_seq += 1
                        new_card = { "name": card_title.strip(), "module":module}
                        new_card["idx"] = card.idx
                        new_card["card_items"] = card.get("routes")
                        existing_card = existing_menu_cards.get(card_title.lower().strip())
                        create = utils.from_dict_to_object()
                        if existing_card:
                            if existing_card.card_items and len(existing_card.card_items):
                                # update existing card index
                                if existing_card.idx != card.idx:
                                    existing_card.idx = card.idx
                                card_item_dict = utils.array_to_dict(existing_card.card_items, "title", True)
                                new_items = []
                                item_idx = 1
                                for ci in new_card["card_items"]:
                                    ci.idx = item_idx
                                    item_idx += 1
                                    if not card_item_dict.get(ci.get("title").lower().strip()):
                                        new_items.append(ci)
                                    else:
                                        card_item_dict[ci.get("title").lower().strip()].idx = ci.idx
                                        new_items.append(card_item_dict.get(ci.get("title").lower().strip()))
                                existing_card.card_items = new_items 
                                create = self.dbms.update("Menu_Card", existing_card, privilege=True)
                                # pp(create)
                            # else:
                            #     print(card_title)
                        else:
                            item_idx = 1
                            for itm in new_card["card_items"]:
                                itm["idx"] = item_idx
                                item_idx += 1
                            create = self.dbms.create("Menu_Card", utils.from_dict_to_object(new_card), privilege=True)

                        if create.status == utils.ok:
                            successful.append(new_card)
                        else:
                            new_card["error_message"] = create.error_message
                            failed.append(new_card)
                    else:
                        pp("Menu Card missing title")
        return utils.respond(utils.ok, {"successful": successful, "Failed": failed})
    
    def create_default_dashboards(self):
        for content in default_dashboard.get("data"):
            dashboards = self.dbms.get_list("Default_Dashboard", fetch_linked_tables=True, privilege=True)
            dashes = utils.from_dict_to_object()
            if dashboards.status == utils.ok:
                dashes = utils.array_to_dict(dashboards.data.rows, "name", True)
            if not dashes.get(content.get("name").lower()):
                create = self.dbms.create("Default_Dashboard", utils.from_dict_to_object(content), privilege=True)
                pp(create)
            else:
                dash = dashes.get(content.get("name").lower())
                if dash.allowed_menus:
                    allowed = utils.array_to_dict(dash.allowed_menus, "menu_card", True)
                    for ds in content.get("allowed_menus"):
                        if not allowed.get(ds.get("menu_card")):
                            dash.allowed_menus.append(allowed)
                else:
                    dash.allowed_menus = content.get("allowed_menus")
                update = self.dbms.update("Default_Dashboard", dash, privilege=True)

    def create_default_roles(self):
        for content in role.get("data"):
            cont = utils.from_dict_to_object(content)
            if cont.role_module and len(cont.role_module):
                for card in cont.role_module:
                    if card.role_cards and len(card.role_cards):
                        cards_dict = {}
                        for cd in card.role_cards:
                            keys = utils.get_object_keys(cd)
                            for key in keys:
                                menu_card = self.dbms.get_doc("Menu_Card", key, privilege=True, fetch_linked_tables=True)
                                if menu_card.status == utils.ok:
                                    items = {}
                                    card_ids = []
                                    if menu_card.data.card_items:
                                        items = utils.array_to_dict(menu_card.data.card_items, "title")
                                    if cd.get(key):
                                        for c in cd.get(key):
                                            if items.get(c):
                                                card_ids.append(items.get(c).id)
                                        cards_dict[key] = card_ids
                        del card.role_cards
                        card.cards = cards_dict
            cont.role_content = {}
            for rc in cont.role_module:
                cont.role_content[rc.role_module] = rc
            del cont.role_module
            create = self.dbms.create("Role", cont, privilege=True)
            # if found them lets just update what module the role originally belong to
            if create.status == utils.found:
                rl = self.dbms.get_doc("Role", cont.name, privilege=True,fetch_linked_fields=False)
                if rl.status == utils.ok:
                    if not rl.data.module and cont.module:
                        rl.data.module = cont.module
                        rl.data.role_content = rl.data.ole_module
                        update = self.dbms.update("Role", rl.data, privilege=True)


    def create_root_accounts(self, dbms, df):
        without_parent = df[(df["parent_account"].isnull()) | (df["parent_account"] == "")]
        without_parent = without_parent.to_dict(orient="records")
        success = []
        failed = []
        if without_parent:
            account_no = 1
            for acc in without_parent:
                acc["company"] = self.company.name
                acc["status"] = "Active"
                acc["is_root"] = 1
                acc["is_group"] = 1
                acc["currency"] = "ZMW"
                if not acc.get("account_number"):
                    acc["account_number"] = account_no
                    account_no += 1
                new_root = dbms.create("Account", utils.from_dict_to_object(acc), privilege=True)
                if new_root.status == utils.ok:
                    acc["error"] = " - "
                    acc["status"] = "Importation Successful"
                    success.append(acc)
                else:
                    acc["error"] = new_root.error_message
                    acc["status"] = "Importation Failed"
                    failed.append(acc)
        return utils.respond(utils.ok, {"successful": success, "failed":failed})


    
    def create_group_accounts(self, dbms, df, accounts):
        success = []
        failed = []
        account_no = 0
        result_dict = df[df["parent_account"].notnull() & (df["parent_account"] != "")].groupby("parent_account").apply(lambda x: x.to_dict(orient="records")).to_dict()
        new_accounts = []
        if result_dict:
            # try:
                account_no = {}
                for parent, values in result_dict.items():
                    group_acc = accounts.get(parent)
                    if group_acc:
                        group_acc["company"] = self.company.name
                        group_acc["status"] = "Active"
                        group_acc["is_group"] = 1
                        group_acc["is_root"] = 0
                        group_acc["currency"] = "ZMW"
                        # group_acc["account_number"] =
                        group_acc_doc = dbms.get_doc("Account", group_acc.get("name"), privilege=True)
                        if group_acc_doc.status == utils.ok:
                            if values and len(values) > 0:
                                for child in values:
                                    child["company"] = self.company.name
                                    child["status"] = "Active"
                                    child["is_group"] = 0
                                    child["is_root"] = 0
                                    child["currency"] = "ZMW"
                                    if not account_no.get(group_acc_doc.data.name):
                                        account_no[group_acc_doc.data.name] = 1
                                    if not child.get("account_number"):
                                        child["account_number"] = f"{group_acc_doc.data.account_number}/{account_no.get(group_acc_doc.data.name)}"
                                        account_no[group_acc_doc.data.name] += 1
                                    
                                    new_child = dbms.create("Account", utils.from_dict_to_object(child), privilege=True)
                                    if new_child.status == utils.ok:
                                        child["status"] = "Importation Successful"
                                        child["error"] = "-"
                                        success.append(child)
                                    else:
                                        child["status"] = "Importation Failed"
                                        child["error"] = new_child.error_message
                                        failed.append(child)
                        else:
                           
                            parent = dbms.get_doc("Account", group_acc.get("parent_account"), privilege=True)
                            if parent.status == utils.ok:
                                if not group_acc.get("account_number"):
                                    if not account_no.get(parent.data.name):
                                        account_no[parent.data.name] = 1
                                    group_acc["account_number"] = f"{parent.data.account_number}/{account_no.get(parent.data.name)}"
                                create = dbms.create("Account", utils.from_dict_to_object(group_acc), privilege=True)
                                if create.status == utils.ok:
                                    group_acc["status"] = "Importation Successful"
                                    group_acc["error"] = "-"
                                    success.append(group_acc)
                                    if values and len(values) > 0:
                                        for child in values:
                                            child["company"] = self.company.name
                                            child["status"] = "Active"
                                            child["is_group"] = 0
                                            child["is_root"] = 0
                                            child["currency"] = "ZMW"
                                            if not account_no.get(create.data.name):
                                                account_no[create.data.name] = 1
                                            if not child.get("account_number"):
                                                child["account_number"] = f"{create.data.account_number}/{account_no.get(create.data.name)}"
                                                account_no[create.data.name] += 1
                                            
                                            new_child = dbms.create("Account", utils.from_dict_to_object(child), privilege=True)
                                            if new_child.status == utils.ok:
                                                child["status"] = "Importation Successful"
                                                child["error"] = "-"
                                                success.append(child)
                                            else:
                                                child["status"] = "Importation Failed"
                                                child["error"] = new_child.error_message
                                                failed.append(child)
                                        else:
                                            group_acc["status"] = "Importation Successful"
                                            group_acc["error"] = "-"
                            else:
                                pp("Parent account not found!!!!!!")
        return utils.respond(utils.ok, {"successful": success, "failed":failed})


    def create_default_chart_of_accounts(self):
        accounts = coa.get("data")
        normalized = [utils.normalize_row_columns(row) for row in accounts]
        df = utils.to_data_frame(normalized)
        account_dict = df.groupby("name").apply(lambda x: x.iloc[0].to_dict()).to_dict()
        root_accounts = self.create_root_accounts(self.dbms, df)
        group_accounts = self.create_group_accounts(self.dbms, df, account_dict)
        return utils.respond(utils.ok, {"accounts":{
            "root_accounts": group_accounts, "group_accounts": group_accounts
        }})


    def create_system_settings(self):
        ss = utils.from_dict_to_object({
            "name": "System Settings",
            "default_company":self.company.name,
            "default_currency":self.company.reporting_currency,
            "default_cost_center":self.cost_center.name,
            "default_country":self.company.country,
            "currency_decimals": 2,
            "status":"Active",
            "docstatus": 0,
            # "api_key": utils.generate_password(17)
        })
        ss = self.dbms.create("System_Settings",ss, privilege=True)
        if ss.get("status") == utils.found:
            return self.dbms.get_doc("System_Settings", "System Settings", privilege=True)
        return ss
    
    def create_default_bank_accounts(self):
        banks = bank.get("data", None)
        data = []
        if banks and len(banks) > 0:
            for ba in banks:
                new_bank = utils.from_dict_to_object({
                    "name": ba.get("name"),
                    "status": "Active",
                    "company": self.company.name,
                    "branch_code": "0",
                    "swift": "Cash",
                    "branch": "",
                    "bank_account": []
                })
                for acc in ba.get("bank_account"):
                    account = self.dbms.get_doc("Account",acc.get("account"), privilege=True)
                    if account.get("status") == utils.ok:
                        account_data = account.get("data")
                        acc["currency"] = account_data.get("currency")
                        acc["account_no"] = account_data.get("account_no","")
                    new_bank.bank_account.append(acc)
                create_acc = self.dbms.create("Bank",new_bank, privilege=True)
                data.append(create_acc)
            return utils.respond(utils.ok, data)
        
    def create_tax_templates(self):
        tax_accounts = coa.get("tax_accounts")
        if len(tax_accounts) > 0:
            data = []
            for ta in tax_accounts:
                template = utils.from_dict_to_object({
                    "name": ta.get("name"),
                    "status":"Active",
                    "tax_accounts":[
                        {"tax_account": ta.get("name"), "tax_rate": ta.get("tax_rate"), "tax_code": ta.get("tax_code"),"tax_category":ta.get("tax_category")}
                    ]
                })
                create = self.dbms.create("Tax_Template",template, privilege=True)
                data.append(create)
            return utils.respond(utils.ok, data)
        
    def create_default_tax_band(self):
        success = []
        failed = []
        bands = income_tax_band.get("data")
        if bands and len(bands) > 0:
            for band in bands:
                b = utils.from_dict_to_object(band)
                # del b.name
                b.company = self.company.name
                b.status = "Active"
                b.docstatus = 0
                b.salary_bands = band.get("salary_bands")
                create = self.dbms.create("Income_Tax_Band", b, privilege=True)
                if create.get("status") == utils.ok:
                    success.append(create.get("data"))
                else:
                    band["error_message"] = create.get("error_message")
                    failed.append(band)
        return utils.respond(utils.ok,{"success":success, "failed":failed})
    

    def create_salary_components(self):
        success = []
        failed = []
        scs = salary_component.get("data")
        if scs and len(scs) > 0:
            for comp in scs:
                c = utils.from_dict_to_object(comp)
                c.company = self.company.name
                c.status = "Active"
                c.docstatus = 0
                for acc in c.accounts:
                    acc.company = self.company.name
                create = self.dbms.create("Salary_Component", c, privilege=True)
                if create.get("status") == utils.ok:
                    success.append(create.get("data"))
                else:
                    comp["error_message"] = create.get("error_message")
                    failed.append(comp)
        return utils.respond(utils.ok,{"success":success, "failed":failed})
    
        # ASSET Categories
    def imprest_petty_cash_setup(self):
        default = coa.get("imprest_setup")     
        data = []
        imprest_petty_cash_setup =utils.from_dict_to_object({
            "company_id": self.company.id,
            "name": self.company.name ,
            "imprest_account": default.get("imprest_account") ,
            "imprest_bank_account": default.get("imprest_bank_account"),
            "retirement_period": default.get("retirement_period"),
            "fund_limit": default.get("fund_limit"),
            "replenishment_threshold": default.get("replenishment_threshold"),
            "maximum_request_amount": default.get("maximum_request_amount"),
            "pt_account": default.get("pt_account"),
            "petty_cash_bank_account": default.get("petty_cash_bank_account"),
            "petty_cash_fund_limit": default.get("petty_cash_fund_limit"),
            "petty_cash_replenishment_threshold": default.get("petty_cash_replenishment_threshold"),
            "petty_cash_maximum_request_amount": default.get("petty_cash_maximum_request_amount"),
            "docstatus" : 0, 
            "status": "Active",
        })
        create = self.dbms.create("Imprest_Setup",imprest_petty_cash_setup, privilege=True)
        data.append(create)
        return utils.respond(utils.ok, data)
    
    def create_default_payroll_setup(self):
        default = coa.get("payroll_setup")[0]
        data = []
        payroll_setup =utils.from_dict_to_object({
            "name":self.company.name,
            "salary_account": default.get("salary_account"),
            "payroll_payable_account": default.get("payroll_payable_account"),
            "payment_bank_or_cash_account": default.get("payment_bank_or_cash_account"),
            "docstatus" : 0, 
            "status": "Active",
        })
        create = self.dbms.create("Payroll_Setup",payroll_setup, privilege=True)
        data.append(create)
        return utils.respond(utils.ok, data)
    
    def create_default_overtime_setup(self):
        default = coa.get("overtime_configuration")[0]    
        data = []
        overtime_setup =utils.from_dict_to_object({
            "name": self.company.name,
            "calculation_type": default.get("calculation_type"),
            "fixed_rate": default.get("fixed_rate"),
            "eligibility": default.get("eligibility"),
            "docstatus" : 0, 
            "status": "Active",
        })
            
        create = self.dbms.create("Overtime_Configuration",overtime_setup, privilege=True)
        data.append(create)
        return utils.respond(utils.ok, data)
    
      
    def create_default_advance_setup(self):
        default = coa.get("salary_advance_configuration")[0]        
        data = []
        advance_setup =utils.from_dict_to_object({
            "name": self.company.name,
            "repayment_plan": default.get("repayment_plan"),
            "allow_partial_payments": default.get("allow_partial_payments"),
            "partial_payment": default.get("partial_payment"),
            "interest_rate": default.get("interest_rate"),
            "credit_account": default.get("credit_account"),
            "debit_account": default.get("debit_account"),
            "credit_account_currency": default.get("credit_account_currency"),
            "debit_account_currency": default.get("debit_account_currency"),
            "reporting_currency": default.get("reporting_currency"),
            "eligibility": default.get("eligibility"),
            "docstatus" : 0, 
            "status": "Active",
        })
                
        # create = self.dbms.create("Salary_Advance_Configuration",advance_setup, privilege=True)
        # data.append(create)
        return utils.respond(utils.ok, data)
    
    # ==================================================================================================================================================================
    def create_default_data(self, tenant):
        self.tenant = tenant
        pp("STARTED CREATING DEFAULT DATA")
        self.create_doc_statuses()
        self.create_admin_user()

        if not self.admin:
            return utils.respond(utils.unprocessable_entity, "Failed to create admin user!")
        # return
        self.create_tenant_api_key()
        self.map_existing_tenant_users_to_user_pool()
        successful = []
        failed = []
        if self.admin:
            if default_inserts and len(default_inserts) > 0:
                for data_group in default_inserts:
                    model = data_group.get("model")
                    data = data_group.get("data")
                    if model and data and isinstance(data,list):
                        for row in data:
                            reconstructed = {}
                            for label,value in row.items():
                                reconstructed[utils.replace_character(label," ","_").lower()] = value
                            if not reconstructed.get("status"):
                                reconstructed["status"] = "Active"
                            if not reconstructed.get("doctype"):
                                reconstructed["doctype"] = model
                            try:
                                create = self.dbms.create(model, utils.from_dict_to_object(reconstructed), privilege=True)
                                if create.get("status") != utils.ok and create.get("status") != utils.found:
                                    pass
                                if create.get("status") == utils.ok:
                                    successful.append({"model":model,"data":create.get("data")})
                                else:
                                    error = {"message": create.get("error_message")} 
                                    error["data"] = row
                                    failed.append(error)
                                    failed.append({"model":model,"data":create.get("data")})
                            except Exception as e:
                                error = {"message": e} 
                                error["data"] = row
                try:
                    self.create_nav_menus()
                    pp("Test....1")
                    self.create_default_dashboards()
                    pp("Test....2")
                    self.create_default_roles()
                    pp("Test....3")
                    self.accrual_holidays()
                    pp("Test....4")

                    #create default company
                    new_company = self.create_tenant_company()
                    pp(new_company)
                    if self.company:
                        cost_center = self.create_cost_center()
                        if cost_center.get("status") != utils.ok:
                            self.dbms.delete("Company",[self.company.id],privilege=True)
                            return cost_center
                        self.cost_center = utils.from_dict_to_object(cost_center.get("data"))
                        
                        # create system settings
                        ss = self.create_system_settings()
                        if ss.get("status") == utils.ok:
                            successful.append(ss.get("data"))
                        else:
                            failed.append(ss.get("error_message"))
                        pp("Passed System Settings Creation....")

                        # create tax templates
                        # tt = self.create_tax_templates()
                        # if tt.get("status") == utils.ok:
                        #     successful.append(tt.get("data"))
                        # else:
                        #     failed.append(tt.get("error_message"))
                        # pp("Passed Tax Templates Creation....")

                        # # create income tax band
                        tb = self.create_default_tax_band()
                        if tb.get("status") == utils.ok:
                            successful.append(tb.get("data"))
                        else:
                            failed.append(tb.get("error_message"))
                        pp("Passed Tax Bands Creation....")


                        # # create salary components
                        sc = self.create_salary_components()
                        if sc.get("status") == utils.ok:
                            successful.append(sc.get("data"))
                        else:
                            failed.append(sc.get("error_message"))
                        pp("Passed Salary Components Creation....")

                        #   create default advance setup
                        # advance_setup = self.create_default_advance_setup()
                        # if advance_setup.get("status") == utils.ok:
                        #     successful.append(advance_setup.get("data"))
                        # else:
                        # #     failed.append(advance_setup.get("error_message"))
                        # pp("Passed Advance Setup Creation....")
                            # create default payroll setup data
                        # defpayrol = self.create_default_payroll_setup()
                        # if defpayrol.get("status") == utils.ok:
                        #     successful.append(defpayrol.get("data"))
                        # else:
                        #     failed.append(defpayrol.get("error_message"))
                        # pp("Passed Payroll setup Creation....")

                        # stkdflt = self.create_stock_defaults ()
                        # if stkdflt.get("status") == utils.ok:
                        #     successful.append(stkdflt.get("data"))
                        # else:
                        #     failed.append(stkdflt.get("error_message"))      
                        # pp("Passed Stock defaults Creation....")                      

                        # overtime_setup = self.create_default_overtime_setup()
                        # if overtime_setup.get("status") == utils.ok:
                        #     successful.append(overtime_setup.get("data"))
                        # else:
                        #     failed.append(overtime_setup.get("error_message"))
                        # pp("Passed Over Time Creation....")

                    else:
                        throw(f"Failed to create default company: {new_company.error_message}")
                except Exception as e:
                    return utils.respond(utils.unprocessable_entity, f"Some data did not create:{str(e)}")
        pp("CREATING DEFAULT DATA COMPLETED")
        return utils.respond(utils.ok,{"successful":successful, "failed":failed})
