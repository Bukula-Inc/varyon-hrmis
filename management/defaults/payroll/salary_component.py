salary_component = {
    "model":"Salary_Component",
    "data": [
        {
            "name": "NAPSA",
            "component_type": "Deduction",
            "percentage": 10,
            "shared_deduction": 1,
            "is_standard_component": 1,
            "is_statutory_component": 1,
            "has_ceiling": 1,
            "ceiling_amount":"1490.80",
            "fixed_amount": 0.0,
            "value_type":"Percentage",
            "apply_on":"Gross",
            "shared_deduction_custom_company": 50,
            "shared_deduction_custom_emp": 50,
            "shared_deduction_custom": 1,
            "accounts": [{
                "company": "",
                "account": "NAPSA Control",
                "expense_account": "NAPSA Contributions"
            }]
        },
        {
            "name": "NHIMA",
            "component_type": "Deduction",
            "percentage": 2,
            "shared_deduction":1,
            "is_standard_component": 1,
            "is_statutory_component": 1,
            "fixed_amount": 0.0,
            "value_type":"Percentage",
            "apply_on":"Basic",
            "shared_deduction_custom_company": 50,
            "shared_deduction_custom_emp": 50,
            "shared_deduction_custom": 1,
            "accounts": [{
            "company": "",
                "account": "NHIMA Control",
                "expense_account": "NHIMA Contributions"
            }]
        },
        {
            "name": "Housing Allowance",
            "component_type": "Earning",
            "percentage": 30.0,
            "fixed_amount": 0.0,
            "value_type":"Percentage",
            "accounts": [{
                "company": "",
                "account": "Housing Allowance"
            }]
        },
        {
            "name": "Salary Advance",
            "component_type": "Deduction",
            "percentage": 0.0,
            "apply_on":"Net",
            "fixed_amount": 0.0,
            "is_type": "Advance",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "Overtime",
            "is_type": "Overtime",
            "component_type": "Earning",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "is_overtime":1,
            "accounts": [{
                "company": "",
                "account": "Overtime"
            }]
        },
        {
            "name": "Gratuity",
            "is_type": "Gratuity",
            "component_type": "Earning",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "accounts": [{
                "company": "",
                "account": "Corporate Social Responsibility"
            }]
        },
        {
            "name": "Personal Loan",
            "component_type": "Deduction",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "value_type":"Custom",
            "apply_on":"Net",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "Medical Recovery",
            "component_type": "Deduction",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "value_type":"Custom",
            "apply_on":"Net",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "Professional Membership Subscription",
            "component_type": "Deduction",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "value_type":"Custom",
            "apply_on":"Net",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "Long Term Sponsorship",
            "component_type": "Deduction",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "value_type":"Custom",
            "apply_on":"Net",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "House Loan",
            "component_type": "Deduction",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "value_type":"Custom",
            "apply_on":"Net",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "Personal Loan",
            "component_type": "Deduction",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "value_type":"Custom",
            "apply_on":"Net",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "Tuition Advance",
            "component_type": "Deduction",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "value_type":"Custom",
            "apply_on":"Net",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "Petty Cash Retirement",
            "component_type": "Deduction",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "value_type":"Custom",
            "apply_on":"Net",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "Imprest Retirement",
            "component_type": "Deduction",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "value_type":"Custom",
            "apply_on":"Net",
            "accounts": [{
                "company": "",
                "account": "Loans and Advances (Assets)"
            }]
        },
        {
            "name": "Separation Package",
            "component_type": "Earning",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "is_type": "",
            "accounts": [{
                "company": "",
                "account": "Corporate Social Responsibility"
            }]
        },
    ]
}