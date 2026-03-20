required_fields = ["created_on", "creation_time", "docstatus", "owner", "modified_by","status","id"]

excluded_models = [
    "Currency",
    "Country",
    "Trader_Type",
    "Industry",
    "Sector",
    "LogEntry",
    "Session",
    "Permission",
    "Group",
    "ContentType",
    "Lite_User",
    "Lite_User_Permission",
    "Lite_User_Role",
    "Role",
    "Tenant",
    "Module",
    "Module_Pricing",
    "Billing_Config",
    "Subscription",
    "System_Settings",
    "Workflow_Action",
    "Workflow_Approver_Group"
]

cacheable_content = [
    "Background_Job",
    "Tenant",
    "Module",
    "Role",
    "Workflow",
    "System_Settings",
    "User_Pool",
    "Lite_User",
    "Company",
    "Exchange_Rate",
    "Currency",
    "Account_Default",
    "System_Setting",
    "Registration_Type"
]
cacheable_lists = []

shared_models = ["Account", "Cost_Center", "Warehouse", "Accounting_Period"]