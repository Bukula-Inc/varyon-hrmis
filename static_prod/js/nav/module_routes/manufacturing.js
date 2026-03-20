export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/manufacturing",
                app: "manufacturing_dashboard",
                title: "Dashboard",
                url: "manufacturing",
                icon: "bar_chart_4_bars",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
    
    {
        title: "Settings",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "production_line",
                title: "Production Line",
                url: "production_line",
                icon: "factory",
                page: "list",
                content_type: "Production Line",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "material",
                title: "Materials",
                url: "material",
                icon: "factory",
                page: "list",
                content_type: "Material",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "workstation_type",
                title: "Workstation Type",
                url: "workstation_type",
                icon: "factory",
                page: "list",
                content_type: "Workstation Type",
                child_items: []
            },
            
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "manufacturing_settings",
                title: "Manufacturing Settings",
                url: "manufacturing_settings",
                icon: "factory",
                page: "new-form",
                content_type: "Manufacturing Settings",
                child_items: []
            },
        ]
    },
    
    {
        title: "Production",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "work_order",
                title: "Work Order",
                url: "work_order",
                icon: "factory",
                page: "list",
                content_type: "Work Order",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "production_plan",
                title: "Production Plan",
                url: "production_plan",
                icon: "factory",
                page: "list",
                content_type: "Production Plan",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "stock",
                app: "stock_entry",
                title: "Stock Entry",
                url: "stock_entry",
                icon: "sell",
                page: "list",
                content_type: "Stock Entry",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "job_card",
                title: "Job Card",
                url: "job_card",
                icon: "factory",
                page: "list",
                content_type: "Job Card",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "downtime_entry",
                title: "Downtime Entry",
                url: "downtime_entry",
                icon: "factory",
                page: "list",
                content_type: "Downtime Entry",
                child_items: []
            },
        ]
    },
    {
        title: "Bill of Materials",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "stock",
                app: "items",
                title: "Items",
                url: "items",
                icon: "category",
                page: "list",
                content_type: "Items",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "bill_of_materials",
                title: "Bill Of Material",
                url: "bill_of_materials",
                icon: "factory",
                page: "list",
                content_type: "Bill Of Material",
                child_items: []
            },
            
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "workstation",
                title: "Workstation",
                url: "workstation",
                icon: "factory",
                page: "list",
                content_type: "Workstation",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "operation",
                title: "Operation",
                url: "operation",
                icon: "factory",
                page: "list",
                content_type: "Operation",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "routing",
                title: "Routing",
                url: "routing",
                icon: "factory",
                page: "list",
                content_type: "Routing",
                child_items: []
            },
        ]
    },
    {
        title: "Reports",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "production_plan_report",
                title: "Product Plan Report",
                url: "manufacturing_reports/production_plan_report",
                icon: "factory",
                page: "list",
                content_type: "Product Plan Report",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "work_order_summary",
                title: "Work Order Summary",
                url: "manufacturing_reports/work_order_summary",
                icon: "factory",
                page: "list",
                content_type: "Work Order Summary",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "quality_inspection_summary",
                title: "Quality Inspection Summary",
                url: "manufacturing_reports/quality_inspection_summary",
                icon: "factory",
                page: "list",
                content_type: "Quality Inspection Summary",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "downtime_analysis",
                title: "Downtime Analysis",
                url: "manufacturing_reports/downtime_analysis",
                icon: "factory",
                page: "list",
                content_type: "Downtime Analysis",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "job_card_summary",
                title: "Job Card Summary",
                url: "manufacturing_reports/job_card_summary",
                icon: "factory",
                page: "list",
                content_type: "Job Card Summary",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "bom_search",
                title: "BOM Search",
                url: "manufacturing_reports/bom_search",
                icon: "factory",
                page: "list",
                content_type: "BOM Search",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "bom_stock_report",
                title: "BOM Stock Report",
                url: "manufacturing_reports/bom_stock_report",
                icon: "factory",
                page: "list",
                content_type: "BOM Stock Report",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "production_analysis",
                title: "Production Analysis",
                url: "manufacturing_reports/production_analysis",
                icon: "factory",
                page: "list",
                content_type: "Production Analysis",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "bom_production_time",
                title: "BOM Production Time",
                url: "manufacturing_reports/bom_production_time",
                icon: "factory",
                page: "list",
                content_type: "BOM Production Time",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "work_order_consumed_material",
                title: "Word Order Consumed Material",
                url: "manufacturing_reports/work_order_consumed_material",
                icon: "factory",
                page: "list",
                content_type: "Word Order Consumed Material",
                child_items: []
            },
        ]
    },
    {
        title: "Tools",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/manufacturing",
                app: "bom_updated_tool",
                title: "BOM Update Tool",
                url: "bom_updated_tool",
                icon: "factory",
                page: "list",
                content_type: "BOM Update Tool",
                child_items: []
            },
        ]
    },
]