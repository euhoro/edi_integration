from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from decimal import Decimal

class TransactionSetHeaderST(BaseModel):
    transaction_set_identifier_code_01: str
    transaction_set_control_number_02: int

class FinancialInformationBPR(BaseModel):
    transaction_handling_code_01: str
    total_actual_provider_payment_amount_02: Decimal
    credit_or_debit_flag_code_03: str
    payment_method_code_04: str
    check_issue_or_eft_effective_date_16: date

class ReassociationTraceTRN(BaseModel):
    trace_type_code_01: str
    check_or_eft_trace_number_02: str
    payer_identifier_03: str

class PayerTechnicalContactPER(BaseModel):
    contact_function_code_01: str
    payer_technical_contact_name_02: Optional[str]
    communication_number_qualifier_03: str
    payer_contact_communication_number_04: str
    communication_number_qualifier_05: Optional[str]
    payer_technical_contact_communication_number_06: Optional[str]

class PayerIdentificationN1(BaseModel):
    entity_identifier_code_01: str
    payer_name_02: str

class PayerAddressN3(BaseModel):
    payer_address_line_01: str

class PayerCityStateZipN4(BaseModel):
    payer_city_name_01: str
    payer_state_code_02: str
    payer_postal_zone_or_zip_code_03: str

class PayerWebsitePER(BaseModel):
    contact_function_code_01: str
    communication_number_qualifier_03: str
    communication_number_04: str

class PayerBusinessContactPER(BaseModel):
    contact_function_code_01: str
    communication_number_qualifier_03: str
    payer_contact_communication_number_04: str

class PayerIdentificationLoop(BaseModel):
    payer_identification_N1: PayerIdentificationN1
    payer_address_N3: PayerAddressN3
    payer_city_state_zip_code_N4: PayerCityStateZipN4
    payer_technical_contact_information_PER: List[PayerTechnicalContactPER]
    payer_web_site_PER: PayerWebsitePER
    payer_business_contact_information_PER: PayerBusinessContactPER

class PayeeIdentificationN1(BaseModel):
    entity_identifier_code_01: str
    payee_name_02: str
    identification_code_qualifier_03: str
    payee_identification_code_04: str

class PayeeAddressN3(BaseModel):
    payee_address_line_01: str

class PayeeCityStateZipN4(BaseModel):
    payee_city_name_01: str
    payee_state_code_02: str
    payee_postal_zone_or_zip_code_03: str

class PayeeAdditionalIdentificationREF(BaseModel):
    reference_identification_qualifier_01: str
    additional_payee_identifier_02: str

class PayeeIdentificationLoop(BaseModel):
    payee_identification_N1: PayeeIdentificationN1
    payee_address_N3: PayeeAddressN3
    payee_city_state_zip_code_N4: PayeeCityStateZipN4
    payee_additional_identification_REF: List[PayeeAdditionalIdentificationREF]

class CompositeMedicalProcedure(BaseModel):
    product_or_service_id_qualifier_01: str
    adjudicated_procedure_code_02: str

class ServicePaymentInformationSVC(BaseModel):
    composite_medical_procedure_identifier_01: CompositeMedicalProcedure
    line_item_charge_amount_02: Decimal
    line_item_provider_payment_amount_03: Decimal
    units_of_service_paid_count_05: int

class ServiceDateDTM(BaseModel):
    date_time_qualifier_01: str
    service_date_02: date

class ServiceAdjustmentCAS(BaseModel):
    claim_adjustment_group_code_01: str
    adjustment_reason_code_02: str
    adjustment_amount_03: Decimal

class ServiceSupplementalAmountAMT(BaseModel):
    # Example field definitions - adjust to your EDI835b model schema
    adjustment_amount_01: Optional[float] = None
    adjustment_amount_02: Optional[float] = None
    adjustment_amount_03: Optional[float] = None

class ServicePaymentLoop(BaseModel):
    service_payment_information_SVC: ServicePaymentInformationSVC
    service_date_DTM: List[ServiceDateDTM]
    service_adjustment_CAS: Optional[List[ServiceAdjustmentCAS]] = None
    service_supplemental_amount_AMT: Optional[List[ServiceSupplementalAmountAMT]]= None

class ClaimPaymentInformationCLP(BaseModel):
    patient_control_number_01: str
    claim_status_code_02: str
    total_claim_charge_amount_03: Decimal
    claim_payment_amount_04: Decimal
    claim_filing_indicator_code_06: str
    payer_claim_control_number_07: str
    facility_type_code_08: str
    claim_frequency_code_09: str

class PatientNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: str
    patient_last_name_03: str
    patient_first_name_04: str
    patient_middle_name_or_initial_05: Optional[str]
    identification_code_qualifier_08: str
    patient_identifier_09: str

class ClaimPaymentLoop(BaseModel):
    claim_payment_information_CLP: ClaimPaymentInformationCLP
    patient_name_NM1: PatientNameNM1
    service_payment_information_SVC_loop: List[ServicePaymentLoop]

class HeaderNumberLX(BaseModel):
    assigned_number_01: int

class HeaderNumberLoop(BaseModel):
    header_number_LX: HeaderNumberLX
    claim_payment_information_CLP_loop: List[ClaimPaymentLoop]

class TransactionSetTrailerSE(BaseModel):
    transaction_segment_count_01: int
    transaction_set_control_number_02: int


class ReceiverIdentificationREF(BaseModel):
    reference_identification_qualifier_01: str
    receiver_identifier_02: str

class ProductionDateDTM(BaseModel):
    date_time_qualifier_01: str
    production_date_02: date

class EDI835Header(BaseModel):
    transaction_set_header_ST: TransactionSetHeaderST
    financial_information_BPR: FinancialInformationBPR
    reassociation_trace_number_TRN: ReassociationTraceTRN
    receiver_identification_REF: Optional[ReceiverIdentificationREF]=None
    production_date_DTM:Optional[ProductionDateDTM]
    payer_identification_N1_loop: PayerIdentificationLoop
    payee_identification_N1_loop: PayeeIdentificationLoop


class EDI835Detail(BaseModel):
    header_number_LX_loop: List[HeaderNumberLoop]


class EDI835Summary(BaseModel):
    transaction_set_trailer_SE: TransactionSetTrailerSE


class EDI835Idets(BaseModel):
    heading: EDI835Header
    detail: EDI835Detail
    summary: EDI835Summary


def load_edi_835(json_data: dict) -> EDI835Idets:
    # Convert date strings to date objects
    if 'heading' in json_data:
        if 'financial_information_BPR' in json_data['heading']:
            json_data['heading']['financial_information_BPR']['check_issue_or_eft_effective_date_16'] = \
                date.fromisoformat(
                    json_data['heading']['financial_information_BPR']['check_issue_or_eft_effective_date_16'])

    return EDI835Idets.model_validate(json_data)
