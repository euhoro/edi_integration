from typing import List, Optional
from pydantic import BaseModel

# Define models based on the provided JSON structure

# -------------------------------
# Line Items
# -------------------------------

class CompositeMedicalProcedureIdentifier(BaseModel):
    product_or_service_id_qualifier_01: str
    procedure_code_02: str
    procedure_modifier_03: Optional[str] = None  # Modifiers may not always be present


class CompositeDiagnosisCodePointer(BaseModel):
    diagnosis_code_pointer_01: int
    diagnosis_code_pointer_02: Optional[int] = None
    diagnosis_code_pointer_03: Optional[int] = None
    diagnosis_code_pointer_04: Optional[int] = None


class ProfessionalServiceSV1(BaseModel):
    composite_medical_procedure_identifier_01: CompositeMedicalProcedureIdentifier
    line_item_charge_amount_02: float
    unit_or_basis_for_measurement_code_03: str
    service_unit_count_04: int
    composite_diagnosis_code_pointer_07: CompositeDiagnosisCodePointer


class DateServiceDateDTP(BaseModel):
    date_time_qualifier_01: str
    date_time_period_format_qualifier_02: str
    adjudication_or_payment_date_03: str


class LineAdjustmentCAS(BaseModel):
    claim_adjustment_group_code_01: str
    adjustment_reason_code_02: str
    adjustment_amount_03: float


class LineAdjudicationInformationSVD(BaseModel):
    other_payer_primary_identifier_01: str
    service_line_paid_amount_02: float
    composite_medical_procedure_identifier_03: CompositeMedicalProcedureIdentifier
    paid_service_unit_count_05: int


class LineAdjudicationInformationSVDLoop(BaseModel):
    line_adjudication_information_SVD: LineAdjudicationInformationSVD
    line_adjustment_CAS: Optional[List[LineAdjustmentCAS]] = None
    line_check_or_remittance_date_DTP: Optional[DateServiceDateDTP] = None


class ServiceLineNumberLX(BaseModel):
    assigned_number_01: int


class ServiceLineNumberLXLoopItem(BaseModel):
    service_line_number_LX: ServiceLineNumberLX
    professional_service_SV1: ProfessionalServiceSV1
    line_adjudication_information_SVD_loop: List[LineAdjudicationInformationSVDLoop]


class ServiceLineNumberLXLoop(BaseModel):
    service_line_number_LX_loop: List[ServiceLineNumberLXLoopItem]

# -------------------------------
# Patient Information
# -------------------------------

class PatientInformationPAT(BaseModel):
    individual_relationship_code_01: str


class PatientNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: Optional[str] = None
    patient_last_name_03: Optional[str] = None
    patient_first_name_04: Optional[str] = None


class PatientAddressN3(BaseModel):
    patient_address_line_01: Optional[str] = None


class PatientCityStateZipCodeN4(BaseModel):
    patient_city_name_01: Optional[str] = None
    patient_state_code_02: Optional[str] = None
    patient_postal_zone_or_zip_code_03: Optional[str] = None


class PatientDemographicInformationDMG(BaseModel):
    date_time_period_format_qualifier_01: Optional[str] = None
    patient_birth_date_02: Optional[str] = None
    patient_gender_code_03: Optional[str] = None


class PatientNameNM1Loop(BaseModel):
    patient_name_NM1: PatientNameNM1
    patient_address_N3: PatientAddressN3
    patient_city_state_zip_code_N4: PatientCityStateZipCodeN4
    patient_demographic_information_DMG: PatientDemographicInformationDMG

# -------------------------------
# Claim Information
# -------------------------------

class ClaimInformationCLM(BaseModel):
    patient_control_number_01: str
    total_claim_charge_amount_02: float


class ClaimInformationCLMLoop(BaseModel):
    claim_information_CLM: ClaimInformationCLM
    service_line_number_LX_loop: List[ServiceLineNumberLXLoopItem]

# -------------------------------
# Subscriber Information
# -------------------------------

class SubscriberInformationSBR(BaseModel):
    payer_responsibility_sequence_number_code_01: Optional[str] = None
    individual_relationship_code_02: Optional[str] = None


class SubscriberNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: str
    subscriber_last_name_03: str
    subscriber_first_name_04: str


class SubscriberNameNM1Loop(BaseModel):
    subscriber_name_NM1: SubscriberNameNM1


class SubscriberHierarchicalLevelHLLoop(BaseModel):
    subscriber_information_SBR: Optional[SubscriberInformationSBR] = None
    subscriber_name_NM1_loop: SubscriberNameNM1Loop
    claim_information_CLM_loop: Optional[List[ClaimInformationCLMLoop]] = None

# -------------------------------
# Main Model
# -------------------------------

class BillingProviderHierarchicalLevelHLLoop(BaseModel):
    subscriber_hierarchical_level_HL_loop: List[SubscriberHierarchicalLevelHLLoop]


class Detail(BaseModel):
    billing_provider_hierarchical_level_HL_loop: List[BillingProviderHierarchicalLevelHLLoop]


class Edi837Idets(BaseModel):
    class Config:
        extra = "allow"  # Allows additional unexpected fields in parsing

    detail: Detail
