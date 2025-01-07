from datetime import date
from decimal import Decimal
from typing import Any, Dict

import pytest

from models.EctonBill.ecton_bill import (Address, Patient, Provider,
                                         SecondaryBill, ServiceLine)

# Assuming the previous model is in secondary_bill.py
# from secondary_bill import SecondaryBill, Provider, Patient, Address, PrimaryInsurance, ServiceLine, Diagnosis


@pytest.fixture
def valid_test_data() -> Dict[str, Any]:
    return {
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


def test_create_secondary_bill(valid_test_data):
    """Test creating a valid secondary bill"""
    test_data = valid_test_data
    bill = SecondaryBill.model_validate(test_data)

    assert bill.bill_id == "26407789"
    assert bill.creation_date == date(2024, 1, 1)
    assert bill.total_charge == Decimal("79.04")
    assert len(bill.service_lines) == 3
    assert len(bill.diagnoses) == 4


def test_address_validation():
    """Test address validation"""
    address_data = {
        "address_line1": "1234 SEAWAY ST",
        "city": "MIAMI",
        "state": "FL",
        "zip_code": "33111",
    }
    address = Address.model_validate(address_data)
    assert address.state == "FL"
    assert address.zip_code == "33111"


def test_provider_validation(valid_test_data):
    """Test provider validation"""
    provider_data = valid_test_data["billing_provider"]
    provider = Provider.model_validate(provider_data)
    assert provider.npi == "1999996666"
    assert provider.tax_id == "123456789"


def test_patient_validation(valid_test_data):
    """Test patient validation"""
    patient_data = valid_test_data["patient"]
    patient = Patient.model_validate(patient_data)
    assert patient.first_name == "TED"
    assert patient.date_of_birth == date(1973, 5, 1)


def test_service_line_validation(valid_test_data):
    """Test service line validation"""
    line_data = valid_test_data["service_lines"][0]
    line = ServiceLine.model_validate(line_data)
    assert line.procedure_code == "99213"
    assert line.charge_amount == Decimal("43.00")
    assert line.primary_paid == Decimal("40.00")


def test_invalid_dates(valid_test_data):
    """Test invalid date handling"""
    test_data = valid_test_data
    test_data["creation_date"] = "invalid-date"

    with pytest.raises(ValueError):
        SecondaryBill.model_validate(test_data)


def test_invalid_decimal_amounts(valid_test_data):
    """Test invalid decimal amount handling"""
    test_data = valid_test_data
    test_data["total_charge"] = "invalid-amount"

    with pytest.raises(ValueError):
        SecondaryBill.model_validate(test_data)


def test_missing_required_fields(valid_test_data):
    """Test handling of missing required fields"""
    test_data = valid_test_data
    del test_data["bill_id"]

    with pytest.raises(ValueError):
        SecondaryBill.model_validate(test_data)


def test_diagnosis_pointers_validation(valid_test_data):
    """Test validation of diagnosis pointers"""
    test_data = valid_test_data
    # Add an invalid diagnosis pointer that doesn't exist
    # test_data["service_lines"][0]["diagnosis_pointers"] = [1, 2, 3, 4, 5]
    test_data["service_lines"][0]["diagnosis_pointers"] = 9

    with pytest.raises(ValueError):
        SecondaryBill.model_validate(test_data)


def test_total_remaining_calculation(valid_test_data):
    """Test that total remaining matches sum of service line remaining balances"""
    test_data = valid_test_data
    bill = SecondaryBill.model_validate(test_data)

    calculated_total = sum(line.remaining_balance for line in bill.service_lines)
    assert bill.total_remaining == calculated_total


# Helper function to convert EDI 837 to SecondaryBill format
def convert_837_to_secondary_bill(edi_837_data: dict) -> dict:
    """Convert EDI 837 data to SecondaryBill format"""

    # Extract claim information
    claim_info = edi_837_data["detail"]["billing_provider_hierarchical_level_HL_loop"][
        0
    ]["subscriber_hierarchical_level_HL_loop"][0]["patient_hierarchical_level_HL_loop"][
        0
    ][
        "claim_information_CLM_loop"
    ][
        0
    ]

    # Extract billing provider information
    billing_provider = edi_837_data["detail"][
        "billing_provider_hierarchical_level_HL_loop"
    ][0]["billing_provider_name_NM1_loop"]

    return {
        "bill_id": claim_info["claim_information_CLM"]["patient_control_number_01"],
        "creation_date": date.today().isoformat(),
        "billing_provider": {
            "npi": billing_provider["billing_provider_name_NM1"][
                "billing_provider_identifier_09"
            ],
            "tax_id": billing_provider["billing_provider_tax_identification_REF"][
                "billing_provider_tax_identification_number_02"
            ],
            "name": f"{billing_provider['billing_provider_name_NM1']['billing_provider_last_or_organizational_name_03']}, {billing_provider['billing_provider_name_NM1']['billing_provider_first_name_04']}",
            "contact_name": billing_provider[
                "billing_provider_contact_information_PER"
            ][0]["billing_provider_contact_name_02"],
            "contact_phone": billing_provider[
                "billing_provider_contact_information_PER"
            ][0]["communication_number_04"],
            "address": {
                "address_line1": billing_provider["billing_provider_address_N3"][
                    "billing_provider_address_line_01"
                ],
                "city": billing_provider["billing_provider_city_state_zip_code_N4"][
                    "billing_provider_city_name_01"
                ],
                "state": billing_provider["billing_provider_city_state_zip_code_N4"][
                    "billing_provider_state_or_province_code_02"
                ],
                "zip_code": billing_provider["billing_provider_city_state_zip_code_N4"][
                    "billing_provider_postal_zone_or_zip_code_03"
                ],
            },
        },
        # ... Add more field mappings as needed
    }


#
# # Helper function to convert EDI 837 to SecondaryBill format
# def convert_837_to_secondary_bill(edi_837_data: dict) -> dict:
#     """Convert EDI 837 data to SecondaryBill format"""
#     # Extract claim information
#     claim_info = (edi_837_data["detail"]["billing_provider_hierarchical_level_HL_loop"][0]
#     ["subscriber_hierarchical_level_HL_loop"][0]
#     ["patient_hierarchical_level_HL_loop"][0]
#     ["claim_information_CLM_loop"][0])
#
#     # Extract billing provider information
#     billing_provider = edi_837_data["detail"]["billing_provider_hierarchical_level_HL_loop"][0][
#         "billing_provider_name_NM1_loop"]
#
#     # Extract subscriber information
#     subscriber = edi_837_data["detail"]["billing_provider_hierarchical_level_HL_loop"][0][
#         "subscriber_hierarchical_level_HL_loop"][0]["subscriber_name_NM1"]
#
#     # Extract patient information
#     patient = (edi_837_data["detail"]["billing_provider_hierarchical_level_HL_loop"][0]
#     ["subscriber_hierarchical_level_HL_loop"][0]
#     ["patient_hierarchical_level_HL_loop"][0]
#     ["patient_name_NM1"])
#
#     # Extract service line details
#     service_lines = claim_info["service_line_loop"]
#     service_details = []
#
#     for line in service_lines:
#         service_details.append({
#             "service_date_from": line["service_date_DTP"]["date_time_period_03"],  # Start date of service
#             "service_date_to": line["service_date_DTP"]["date_time_period_03"],  # End date of service
#             "procedure_code": line["service_procedure_information_SV1"]["product_service_id_02"],
#             "procedure_description": line["service_procedure_information_SV1"].get("description", ""),
#             "service_charge": line["service_procedure_information_SV1"]["line_item_charge_amount_03"]
#         })
#
#     # Return the full mapped SecondaryBill format
#     return {
#         "bill_id": claim_info["claim_information_CLM"]["patient_control_number_01"],
#         "creation_date": date.today().isoformat(),
#         "billing_provider": {
#             "npi": billing_provider["billing_provider_name_NM1"]["billing_provider_identifier_09"],
#             "tax_id": billing_provider["billing_provider_tax_identification_REF"][
#                 "billing_provider_tax_identification_number_02"],
#             "name": f"{billing_provider['billing_provider_name_NM1']['billing_provider_last_or_organizational_name_03']}, {billing_provider['billing_provider_name_NM1']['billing_provider_first_name_04']}",
#             "contact_name": billing_provider["billing_provider_contact_information_PER"][0][
#                 "billing_provider_contact_name_02"],
#             "contact_phone": billing_provider["billing_provider_contact_information_PER"][0]["communication_number_04"],
#             "address": {
#                 "address_line1": billing_provider["billing_provider_address_N3"]["billing_provider_address_line_01"],
#                 "city": billing_provider["billing_provider_city_state_zip_code_N4"]["billing_provider_city_name_01"],
#                 "state": billing_provider["billing_provider_city_state_zip_code_N4"][
#                     "billing_provider_state_or_province_code_02"],
#                 "zip_code": billing_provider["billing_provider_city_state_zip_code_N4"][
#                     "billing_provider_postal_zone_or_zip_code_03"]
#             }
#         },
#         "patient": {
#             "first_name": patient["patient_first_name_04"],
#             "last_name": patient["patient_last_name_03"],
#             "dob": patient["patient_date_of_birth"]["date_01"],
#             "gender": patient["patient_gender_code_08"]
#         },
#         "subscriber": {
#             "first_name": subscriber["subscriber_first_name_04"],
#             "last_name": subscriber["subscriber_last_name_03"],
#             "relationship": subscriber["subscriber_relationship_code_09"],
#             "id": subscriber["subscriber_identification_code_12"]
#         },
#         "claim": {
#             "claim_amount": claim_info["claim_information_CLM"]["monetary_amount_02"],
#             "facility_code": claim_info["claim_information_CLM"]["place_of_service_code_05"],
#             "diagnosis_codes": [diagnosis["diagnosis_code_01"] for diagnosis in
#                                 claim_info["diagnosis_code_list"]],
#             "claim_type": claim_info["claim_information_CLM"]["claim_frequency_code_07"]
#         },
#         "service_details": service_details
#     }


def test_convert_837_to_secondary_bill():
    """Test converting EDI 837 data to SecondaryBill format"""
    # Sample EDI 837 data (you would need to provide actual test data)
    edi_837_data = {
        "detail": {
            "billing_provider_hierarchical_level_HL_loop": [
                {
                    "billing_provider_name_NM1_loop": {
                        "billing_provider_name_NM1": {
                            "billing_provider_identifier_09": "1999996666",
                            "billing_provider_last_or_organizational_name_03": "KILDARE",
                            "billing_provider_first_name_04": "BEN",
                        },
                        "billing_provider_tax_identification_REF": {
                            "billing_provider_tax_identification_number_02": "123456789"
                        },
                        "billing_provider_contact_information_PER": [
                            {
                                "billing_provider_contact_name_02": "CONNIE",
                                "communication_number_04": "3055551234",
                            }
                        ],
                        "billing_provider_address_N3": {
                            "billing_provider_address_line_01": "1234SEAWAY ST"
                        },
                        "billing_provider_city_state_zip_code_N4": {
                            "billing_provider_city_name_01": "MIAMI",
                            "billing_provider_state_or_province_code_02": "FL",
                            "billing_provider_postal_zone_or_zip_code_03": "33111",
                        },
                    },
                    "subscriber_hierarchical_level_HL_loop": [
                        {
                            "patient_hierarchical_level_HL_loop": [
                                {
                                    "claim_information_CLM_loop": [
                                        {
                                            "claim_information_CLM": {
                                                "patient_control_number_01": "26407789"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                }
            ]
        }
    }

    converted_data = convert_837_to_secondary_bill(edi_837_data)
    assert converted_data["bill_id"] == "26407789"
    assert converted_data["billing_provider"]["npi"] == "1999996666"
    assert converted_data["billing_provider"]["name"] == "KILDARE, BEN"


if __name__ == "__main__":
    pytest.main([__file__])
