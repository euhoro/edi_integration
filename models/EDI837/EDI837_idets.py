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
    adjudication_or_payment_date_03:str

class DateServiceDateDTP2(BaseModel):
    date_time_qualifier_01: Optional[str]=None
    date_time_period_format_qualifier_02: Optional[str]=None
    service_date_03: Optional[str]=None


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
    date_service_date_DTP:Optional[DateServiceDateDTP2]=None

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

class HealthCareServiceLocationInformation05(BaseModel):
    place_of_service_code_01: str
    facility_code_qualifier_02: str
    claim_frequency_code_03: str

class ClaimInformationCLM(BaseModel):
    patient_control_number_01: str
    total_claim_charge_amount_02: float
    health_care_service_location_information_05: Optional[HealthCareServiceLocationInformation05]=None

#------

class ServiceFacilityLocationNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: Optional[str]
    laboratory_or_facility_name_03: Optional[str]
    identification_code_qualifier_08: Optional[str]
    laboratory_or_facility_primary_identifier_09: Optional[str]


class ServiceFacilityLocationAddressN3(BaseModel):
    laboratory_or_facility_address_line_01: Optional[str]


class ServiceFacilityLocationCityStateZipCodeN4(BaseModel):
    laboratory_or_facility_city_name_01: Optional[str]
    laboratory_or_facility_state_or_province_code_02: Optional[str]
    laboratory_or_facility_postal_zone_or_zip_code_03: Optional[str]

class ServiceFacilityLocationNM1Loop(BaseModel):
    service_facility_location_name_NM1: ServiceFacilityLocationNameNM1
    service_facility_location_address_N3: ServiceFacilityLocationAddressN3
    service_facility_location_city_state_zip_code_N4: ServiceFacilityLocationCityStateZipCodeN4


# Rendering Provider NM1 Loop
class RenderingProviderNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: Optional[str]
    rendering_provider_last_or_organization_name_03: Optional[str]
    rendering_provider_first_name_04: Optional[str]
    identification_code_qualifier_08: Optional[str]
    rendering_provider_identifier_09: Optional[str]


class RenderingProviderSpecialtyInformationPRV(BaseModel):
    provider_code_01: Optional[str]
    reference_identification_qualifier_02: Optional[str]
    provider_taxonomy_code_03: Optional[str]


class RenderingProviderSecondaryIdentificationREF(BaseModel):
    reference_identification_qualifier_01: Optional[str]
    rendering_provider_secondary_identifier_02: Optional[str]


class RenderingProviderNM1Loop(BaseModel):
    rendering_provider_name_NM1: RenderingProviderNameNM1
    rendering_provider_specialty_information_PRV: Optional[RenderingProviderSpecialtyInformationPRV]
    rendering_provider_secondary_identification_REF: Optional[
        List[RenderingProviderSecondaryIdentificationREF]
    ]


# Other Subscriber Information SBR Loop
class OtherSubscriberInformationSBR(BaseModel):
    payer_responsibility_sequence_number_code_01: Optional[str]
    individual_relationship_code_02: Optional[str]
    claim_filing_indicator_code_09: Optional[str]

class CoordinationOfBenefitsPayerPaidAmountAMT(BaseModel):
    amount_qualifier_code_01: Optional[str]
    payer_paid_amount_02: Optional[float]


class RemainingPatientLiabilityAMT(BaseModel):
    amount_qualifier_code_01: Optional[str]
    remaining_patient_liability_02: Optional[float]


class OtherInsuranceCoverageInformationOI(BaseModel):
    benefits_assignment_certification_indicator_03: Optional[str]
    patient_signature_source_code_04: Optional[str]
    release_of_information_code_06: Optional[str]


class OtherSubscriberNameNM1(BaseModel):
    entity_identifier_code_01: Optional[str]
    entity_type_qualifier_02: Optional[str]
    other_insured_last_name_03: Optional[str]
    other_insured_first_name_04: Optional[str]
    identification_code_qualifier_08: Optional[str]
    other_insured_identifier_09: Optional[str]


class OtherSubscriberAddressN3(BaseModel):
    other_subscriber_address_line_01: Optional[str]


class OtherSubscriberCityStateZipCodeN4(BaseModel):
    other_subscriber_city_name_01: Optional[str]
    other_subscriber_state_or_province_code_02: Optional[str]
    other_subscriber_postal_zone_or_zip_code_03: Optional[str]


class OtherSubscriberNameNM1Loop(BaseModel):
    other_subscriber_name_NM1: OtherSubscriberNameNM1
    other_subscriber_address_N3: Optional[OtherSubscriberAddressN3]
    other_subscriber_city_state_zip_code_N4: Optional[OtherSubscriberCityStateZipCodeN4]


class OtherPayerNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: Optional[str]
    other_payer_organization_name_03: Optional[str]
    identification_code_qualifier_08: Optional[str]
    other_payer_primary_identifier_09: Optional[str]

class OtherPayerNameNM1Loop(BaseModel):
    other_payer_name_NM1: OtherPayerNameNM1

#------

class ClaimCASLine(BaseModel):
    claim_adjustment_group_code_01: Optional[str]=None #'PR'
    adjustment_reason_code_02:Optional[str]=None
    adjustment_amount_03:Optional[float]=None
    adjustment_reason_code_05: Optional[str]=None # '2'
    adjustment_amount_06:Optional[float]=None




class OtherSubscriberInformationSBRLoop(BaseModel):
    other_subscriber_information_SBR: OtherSubscriberInformationSBR
    claim_level_adjustments_CAS: Optional[List[ClaimCASLine]]=None
    coordination_of_benefits_cob_payer_paid_amount_AMT: Optional[
        CoordinationOfBenefitsPayerPaidAmountAMT
    ]
    remaining_patient_liability_AMT: Optional[RemainingPatientLiabilityAMT]=None
    other_insurance_coverage_information_OI: Optional[OtherInsuranceCoverageInformationOI]
    other_subscriber_name_NM1_loop: Optional[OtherSubscriberNameNM1Loop]
    other_payer_name_NM1_loop: Optional[OtherPayerNameNM1Loop]

class HealthCareCodeInformation(BaseModel):
    diagnosis_type_code_01: str
    diagnosis_code_02: str

class HealthCareDiagnosisCodeHI(BaseModel):
    health_care_code_information_01: Optional[HealthCareCodeInformation]=None
    health_care_code_information_02: Optional[HealthCareCodeInformation]=None
    health_care_code_information_03: Optional[HealthCareCodeInformation]=None
    health_care_code_information_04: Optional[HealthCareCodeInformation]=None

class ClaimInformationCLMLoop(BaseModel):
    claim_information_CLM: ClaimInformationCLM
    service_line_number_LX_loop: Optional[List[ServiceLineNumberLXLoopItem]] = None

    service_facility_location_name_NM1_loop: Optional[ServiceFacilityLocationNM1Loop] = None
    rendering_provider_name_NM1_loop: RenderingProviderNM1Loop
    other_subscriber_information_SBR_loop: Optional[List[OtherSubscriberInformationSBRLoop]]
    health_care_diagnosis_code_HI:Optional[HealthCareDiagnosisCodeHI]=None
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

    identification_code_qualifier_08: str
    subscriber_primary_identifier_09: str


class SubscriberNameNM1Loop(BaseModel):
    subscriber_name_NM1: SubscriberNameNM1


class PayerNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: str
    payer_name_03: str
    identification_code_qualifier_08: str
    payer_identifier_09: Optional[str]

class PayerAddressN3(BaseModel):
    payer_address_line_01: str

class PayerCityStateZipCodeN4(BaseModel):
    payer_city_name_01: str
    payer_state_or_province_code_02: str
    payer_postal_zone_or_zip_code_03: str

class PayerNameNM1Loop(BaseModel):
    payer_name_NM1: PayerNameNM1
    payer_address_N3: PayerAddressN3
    payer_city_state_zip_code_N4: PayerCityStateZipCodeN4

# Envelope Class
class PatientHierarchicalLevelHLLoop(BaseModel):
    patient_information_PAT: PatientInformationPAT
    patient_name_NM1_loop: PatientNameNM1Loop
    claim_information_CLM_loop: List[ClaimInformationCLMLoop]

class SubscriberHierarchicalLevelHLLoop(BaseModel):
    subscriber_information_SBR: Optional[SubscriberInformationSBR] = None
    subscriber_name_NM1_loop: SubscriberNameNM1Loop
    claim_information_CLM_loop: Optional[List[ClaimInformationCLMLoop]] = None
    payer_name_NM1_loop: PayerNameNM1Loop
    patient_hierarchical_level_HL_loop: Optional[List[PatientHierarchicalLevelHLLoop]] = None

# -------------------------------
# Main Model
# -------------------------------

class TransactionSetHeaderST(BaseModel):
    transaction_set_identifier_code_01: str
    transaction_set_control_number_02: int
    implementation_guide_version_name_03: str

class BeginningOfHierarchicalTransactionBHT(BaseModel):
    hierarchical_structure_code_01: str
    transaction_set_purpose_code_02: str
    originator_application_transaction_identifier_03: str
    transaction_set_creation_date_04: str
    transaction_set_creation_time_05: str
    claim_or_encounter_identifier_06: str

class SubmitterEDIContactInformationPER(BaseModel):
    contact_function_code_01: str
    submitter_contact_name_02: str
    communication_number_qualifier_03: str
    communication_number_04: Optional[str]

class SubmitterNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: str
    submitter_last_or_organization_name_03: str
    identification_code_qualifier_08: str
    submitter_identifier_09: Optional[str]

class SubmitterNameNM1Loop(BaseModel):
    submitter_name_NM1: SubmitterNameNM1
    submitter_edi_contact_information_PER: List[SubmitterEDIContactInformationPER]

class ReceiverNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: str
    receiver_name_03: str
    identification_code_qualifier_08: str
    receiver_primary_identifier_09: Optional[str]

class ReceiverNameNM1Loop(BaseModel):
    receiver_name_NM1: ReceiverNameNM1

class Heading(BaseModel):
    transaction_set_header_ST: TransactionSetHeaderST
    beginning_of_hierarchical_transaction_BHT: BeginningOfHierarchicalTransactionBHT
    submitter_name_NM1_loop: SubmitterNameNM1Loop
    receiver_name_NM1_loop: ReceiverNameNM1Loop

class BillingProviderNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: str
    billing_provider_last_or_organizational_name_03: str
    identification_code_qualifier_08: str
    billing_provider_identifier_09: Optional[str]

class BillingProviderAddressN3(BaseModel):
    billing_provider_address_line_01: str

class BillingProviderCityStateZipCodeN4(BaseModel):
    billing_provider_city_name_01: str
    billing_provider_state_or_province_code_02: str
    billing_provider_postal_zone_or_zip_code_03: str

class BillingProviderUpinLicenseInformationREF(BaseModel):
    reference_identification_qualifier_01: str
    billing_provider_license_and_or_upin_information_02: Optional[str]

class BillingProviderTaxIdentificationREF(BaseModel):
    reference_identification_qualifier_01: str
    billing_provider_tax_identification_number_02: str

class BillingProviderContactInformationPER(BaseModel):
    contact_function_code_01: str
    billing_provider_contact_name_02: str
    communication_number_qualifier_03: str
    communication_number_04: str


class BillingProviderNameNM1Loop(BaseModel):
    billing_provider_name_NM1: BillingProviderNameNM1
    billing_provider_address_N3: BillingProviderAddressN3
    billing_provider_city_state_zip_code_N4: BillingProviderCityStateZipCodeN4
    billing_provider_upin_license_information_REF: Optional[List[BillingProviderUpinLicenseInformationREF]] = None
    billing_provider_tax_identification_REF: BillingProviderTaxIdentificationREF
    billing_provider_contact_information_PER: Optional[List[BillingProviderContactInformationPER]] = None

class BillingProviderHierarchicalLevelHLLoop(BaseModel):
    billing_provider_name_NM1_loop: BillingProviderNameNM1Loop
    subscriber_hierarchical_level_HL_loop: List[SubscriberHierarchicalLevelHLLoop]

class TransactionSetTrailerSE(BaseModel):
    transaction_segment_count_01: int
    transaction_set_control_number_02: int

class Detail(BaseModel):
    billing_provider_hierarchical_level_HL_loop: List[BillingProviderHierarchicalLevelHLLoop]
    transaction_set_trailer_SE: TransactionSetTrailerSE

class Edi837Idets(BaseModel):
    class Config:
        extra = "allow"  # Allows additional unexpected fields in parsing

    heading: Heading
    detail: Detail
