export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/assets",
                app: "asset_dashboard",
                title: "Assets Dashboard",
                url: "assets/",
                icon: "",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
    {
        title: "Asset Master",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/assets",
                app: "asset_default",
                title: "Asset Settings",
                url: "asset_default/",
                icon: "layers",
                page: "list",
                content_type: "asset default",
            },
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_category",
                title: "Asset Category",
                url: "asset_category",
                icon: "list",
                page: "list",
                content_type: "asset category",
                child_items: [
                   {
                        is_linked: true,
                        module: "app/assets",
                        app: "asset_category",
                        title: "New Asset Category",
                        url: "asset_category",
                        icon: "list",
                        page: "new-form",
                        content_type: "asset category",
                        child_items: []
                    }
                ]
            },
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_insurance",
                title: "Asset Insurance",
                url: "asset_insurance",
                icon: "privacy_tip",
                page: "list",
                content_type: "asset insurance",
                child_items: [
                    {
                        is_linked: true,
                        module: "app/assets",
                        app: "asset_insurance",
                        title: "New Asset Insurance",
                        url: "asset_insurance",
                        icon: "add_moderator",
                        page: "new-form",
                        content_type: "asset insurance",
                    },

                ]
            },
        ]
    },   
    {
        title: "Asset Management",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/assets",
                app: "asset",
                title: "Asset",
                url: "asset/",
                icon: "layers",
                page: "list",
                content_type: "asset",
                child_items:[
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/assets",
                        app: "asset",
                        title: "New Asset",
                        url: "asset/",
                        icon: "report",
                        page: "new-form",
                        content_type: "asset",
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/assets",
                app: "asset_group",
                title: "Asset Group",
                url: "asset_group/",
                icon: "layers",
                page: "list",
                content_type: "asset group",
                child_items:[
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/assets",
                        app: "asset_group",
                        title: "New Asset Group",
                        url: "asset_group/",
                        icon: "report",
                        page: "new-form",
                        content_type: "asset_group",
                    },
                ]
            },
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_value_adjustment",
                title: "Assets Value Adjustment",
                url: "asset_value_adjustment",
                icon: "equalizer",
                page: "list",
                content_type: "asset value adjustment",
                child_items: [
                    {
                        is_linked: false,
                        module: "app/assets",
                        app: "asset_value_adjustment",
                        title: "New Asset Value Adjustment",
                        url: "asset_value_adjustment",
                        icon: "equalizer",
                        page: "new-form",
                        content_type: "asset value adjustment",
                    },

                ]
            }, 
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_movement",
                title: "Asset Movement",
                url: "asset_movement",
                icon: "local_shipping",
                page: "list",
                content_type: "asset movement",
                child_items: [
                    {
                        is_linked: true,
                        module: "app/assets",
                        app: "asset_movement",
                        title: "New Asset Transfer",
                        url: "asset_movement",
                        icon: "local_shipping",
                        page: "new-form",
                        content_type: "asset movement",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_disposal",
                title: "Asset Disposal",
                url: "asset_disposal/",
                icon: "delete_sweep",
                page: "list",
                content_type: "asset disposal",
            },
        ]
    }, {
        title: "Assets Maintenance",
        routes: [
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_maintenance",
                title: "Asset Maintenance",
                url: "asset_maintenance/",
                icon: "safety_check",
                page: "list",
                content_type: "asset maintenance",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_maintenance_team",
                title: "Asset Maintenance Team",
                url: "asset_maintenance_team",
                icon: "group",
                page: "list",
                content_type: "asset maintenance team",
                child_items: [
                    {
                        is_linked: true,
                        module: "app/assets",
                        app: "asset_maintenance_team",
                        title: "Asset Maintenance Team",
                        url: "asset_maintenance_team",
                        icon: "group",
                        page: "new-form",
                        content_type: "asset maintenance team",
                        child_items: []
                    }

                ]
            },   
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/assets",
                app: "scheduled_records",
                title: "Scheduled Records",
                url: "scheduled_records/",
                icon: "layers",
                page: "list",
                content_type: "scheduled records",
                child_items:[
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/assets",
                        app: "scheduled_records",
                        title: "Scheduled Records",
                        url: "scheduled_records/",
                        icon: "report",
                        page: "new-form",
                        content_type: "scheduled records",
                    },
                ]
            },        
        ]
    },
    {
        title: "Reports",
        routes: [
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_reports",
                title: "Asset Net Book Value",
                url: "asset_reports/asset_netbook_value/",
                icon: "savings",
                page: "report",
                content_type: "asset netbook value",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_reports",
                title: "Asset Depreciation Report",
                url: "asset_reports/asset_depreciation_report/",
                icon: "lab_profile",
                page: "report",
                content_type: "asset depreciation report",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_reports",
                title: "Asset Maintenance Report",
                url: "asset_reports/asset_maintenance_report/",
                icon: "summarize",
                page: "report",
                content_type: "asset maintenance report",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_reports",
                title: "Asset Depreciations and Balances",
                url: "asset_reports/asset_depreciation_and_balances/",
                icon: "balance",
                page: "report",
                content_type: "asset depreciation and balances",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/assets",
                app: "asset_reports",
                title: "Asset Disposal Report",
                url: "asset_reports/asset_disposal_report/",
                icon: "delete_sweep",
                page: "report",
                content_type: "asset disposal report",
                child_items: []
            },
        ]
    },
]