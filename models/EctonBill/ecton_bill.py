from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from decimal import Decimal


class Address(BaseModel):
    address_line1: str
    city: str
    state: str
    zip_code: str


class Provider(BaseModel):
    npi: str  # National Provider Identifier
    tax_id: str
    name: str
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Address


class Patient(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    address: Address
    member_id: str
    relationship_code: str  # e.g., "01" for self, "19" for child


class PrimaryInsurance(BaseModel):
    payer_name: str
    payer_id: str
    claim_number: str  # Primary payer's claim control number
    paid_date: date
    total_paid: Decimal
    total_adjusted: Decimal
    total_patient_responsibility: Decimal


class ServiceLine(BaseModel):
    line_number: int
    service_date: date
    procedure_code: str
    procedure_code_qualifier: str  # e.g., "HC" for HCPCS
    charge_amount: Decimal
    units: int
    diagnosis_pointers: List[int]

    # Primary insurance adjudication
    primary_paid: Decimal
    primary_adjusted: Decimal
    primary_adjustment_reason: Optional[str] = None

    # Amount to bill secondary
    remaining_balance: Decimal


class Diagnosis(BaseModel):
    code: str
    pointer: int  # Position in diagnosis list (1-based)


class SecondaryBill(BaseModel):
    # Metadata
    bill_id: str
    creation_date: date

    # Participants
    billing_provider: Provider
    service_facility: Optional[Provider]
    patient: Patient

    # Primary Insurance Information
    primary_insurance: PrimaryInsurance

    # Claim Information
    original_claim_date: date
    total_charge: Decimal
    place_of_service: str

    # Clinical Information
    diagnoses: List[Diagnosis]
    service_lines: List[ServiceLine]

    # Totals for Secondary Billing
    total_remaining: Decimal  # Total amount to bill to secondary

    class Config:
        json_schema_extra = {
            "example": {
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
                        "zip_code": "33111"
                    }
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
                        "zip_code": "33413"
                    }
                },
                "primary_insurance": {
                    "payer_name": "KEY INSURANCE COMPANY",
                    "payer_id": "999996666",
                    "claim_number": "26407789",
                    "paid_date": "2005-10-15",
                    "total_paid": 39.15,
                    "total_adjusted": 36.89,
                    "total_patient_responsibility": 3.00
                },
                "original_claim_date": "2005-10-03",
                "total_charge": 79.04,
                "place_of_service": "11",
                "diagnoses": [
                    {"code": "4779", "pointer": 1},
                    {"code": "2724", "pointer": 2},
                    {"code": "2780", "pointer": 3},
                    {"code": "53081", "pointer": 4}
                ],
                "service_lines": [
                    {
                        "line_number": 1,
                        "service_date": "2005-10-03",
                        "procedure_code": "99213",
                        "procedure_code_qualifier": "HC",
                        "charge_amount": 43.00,
                        "units": 1,
                        "diagnosis_pointers": [1, 2, 3, 4],
                        "primary_paid": 40.00,
                        "primary_adjusted": 3.00,
                        "primary_adjustment_reason": "42",
                        "remaining_balance": 3.00
                    }
                ],
                "total_remaining": 3.00
            }
        }