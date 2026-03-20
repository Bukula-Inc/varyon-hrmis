from datetime import date
from controllers.utils.dates import Dates

dates = Dates()
income_tax_band = {
    "model":"Income_Tax_Band",
    "data": [
        {
            "name": "PAYE",
            "effective_from": dates.today(),
            "is_current": 1,
            "company": "",
            "tax_free_amount":"5100.00",
            "deduct_on":"Gross",
            "salary_bands": [
                { "amount_from":"5100.01", "amount_to":"7100.00",  "deduction_percentage":20, "deduct_on": "Gross" },
                { "amount_from":"7100.01", "amount_to":"9200.00",  "deduction_percentage":30, "deduct_on": "Gross" },
                { "amount_from":"9200.01", "amount_to":"Above",  "deduction_percentage":37, "deduct_on": "Gross" },
            ]
        },
    ]
}