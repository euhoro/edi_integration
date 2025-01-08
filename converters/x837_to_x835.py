from models.EDI835.EDI835_idets import EDI835Idets
from models.EDI837.EDI837_idets import Edi837Idets
from models.EctonBill.ecton_bill import SecondaryBill


def convert_x837_to_x835(x837: Edi837Idets) -> EDI835Idets:
    return None


def convert_x837_to_ecton_bill(x837: Edi837Idets) -> SecondaryBill:
    #sec_bill = SecondaryBill()
    sec_bill = {
        "bill_id": "26407789",
        "creation_date": "2024-01-01",
        "billing_provider": {
            "npi": "1999996666",
            "tax_id": "123456789",
            "name": "KILDARE ASSOCIATES",
            "contact_name": "CONNIE",
            "contact_phone": "3055551234",
            "address": {
                "address_line1": "1234 SEAWAY ST",
                "city": "MIAMI",
                "state": "FL",
                "zip_code": "33111",
            },
        },
        "service_facility": {
            "npi": "1581234567",
            "tax_id": "987654321",
            "name": "KILDARE ASSOCIATES",
            "address": {
                "address_line1": "2345 OCEAN BLVD",
                "city": "MIAMI",
                "state": "FL",
                "zip_code": "33111",
            },
        },
        "patient": {
            "first_name": "TED",
            "last_name": "SMITH",
            "date_of_birth": "1973-05-01",
            "gender": "M",
            "member_id": "222334444",
            "relationship_code": "19",
            "address": {
                "address_line1": "236 N MAIN ST",
                "city": "MIAMI",
                "state": "FL",
                "zip_code": "33413",
            },
        },
        "primary_insurance": {
            "payer_name": "KEY INSURANCE COMPANY",
            "payer_id": "999996666",
            "claim_number": "26407789",
            "paid_date": "2005-10-15",
            "total_paid": "39.15",
            "total_adjusted": "36.89",
            "total_patient_responsibility": "3.00",
        },
        "original_claim_date": "2005-10-03",
        "total_charge": "79.04",
        "place_of_service": "11",
        "diagnoses": [
            {"code": "4779", "pointer": 1},
            {"code": "2724", "pointer": 2},
            {"code": "2780", "pointer": 3},
            {"code": "53081", "pointer": 4},
        ],
        "service_lines": [
            {
                "line_number": 1,
                "service_date": "2005-10-03",
                "procedure_code": "99213",
                "procedure_code_qualifier": "HC",
                "charge_amount": "43.00",
                "units": 1,
                "diagnosis_pointers": [1, 2, 3, 4],
                "primary_paid": "40.00",
                "primary_adjusted": "3.00",
                "primary_adjustment_reason": "42",
                "remaining_balance": "3.00",
            },
            {
                "line_number": 2,
                "service_date": "2005-10-03",
                "procedure_code": "90782",
                "procedure_code_qualifier": "HC",
                "charge_amount": "15.00",
                "units": 1,
                "diagnosis_pointers": [1, 2],
                "primary_paid": "15.00",
                "primary_adjusted": "0.00",
                "remaining_balance": "0.00",
            },
            {
                "line_number": 3,
                "service_date": "2005-10-03",
                "procedure_code": "J3301",
                "procedure_code_qualifier": "HC",
                "charge_amount": "21.04",
                "units": 1,
                "diagnosis_pointers": [1, 2],
                "primary_paid": "21.04",
                "primary_adjusted": "0.00",
                "remaining_balance": "0.00",
            },
        ],
        "total_remaining": "3.00",
    }
    return SecondaryBill.model_validate(sec_bill)
