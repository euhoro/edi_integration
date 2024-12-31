from typing import List, Optional
from pydantic import BaseModel


# Level 1: Patient Hierarchical Level

class PatientInformationPAT(BaseModel):
    individual_relationship_code_01: str


class PatientNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: Optional[str]
    patient_last_name_03: Optional[str]
    patient_first_name_04: Optional[str]


class PatientAddressN3(BaseModel):
    patient_address_line_01: Optional[str]


class PatientCityStateZipCodeN4(BaseModel):
    patient_city_name_01: Optional[str]
    patient_state_code_02: Optional[str]
    patient_postal_zone_or_zip_code_03: Optional[str]


class PatientDemographicInformationDMG(BaseModel):
    date_time_period_format_qualifier_01: Optional[str]
    patient_birth_date_02: Optional[str]
    patient_gender_code_03: Optional[str]


# Patient Name NM1 Loop
class PatientNameNM1Loop(BaseModel):
    patient_name_NM1: PatientNameNM1
    patient_address_N3: PatientAddressN3
    patient_city_state_zip_code_N4: PatientCityStateZipCodeN4
    patient_demographic_information_DMG: PatientDemographicInformationDMG


# Level 2: Claim Information
class HealthCareServiceLocationInformation05(BaseModel):
    place_of_service_code_01: Optional[str]
    facility_code_qualifier_02: Optional[str]
    claim_frequency_code_03: Optional[str]





class HealthCareCodeInformation(BaseModel):
    diagnosis_type_code_01: str
    diagnosis_code_02: str


class HealthCareDiagnosisCodeHI(BaseModel):
    health_care_code_information_01: HealthCareCodeInformation
    health_care_code_information_02: Optional[HealthCareCodeInformation]
    health_care_code_information_03: Optional[HealthCareCodeInformation]
    health_care_code_information_04: Optional[HealthCareCodeInformation]


# Service Facility Location NM1 Loop
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


class ClaimLevelAdjustmentsCAS(BaseModel):
    claim_adjustment_group_code_01: Optional[str]
    adjustment_reason_code_02: Optional[str]
    adjustment_amount_03: Optional[float]
    adjustment_reason_code_05: Optional[str]
    adjustment_amount_06: Optional[float]


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


# Claim Information CLM
class HealthCareServiceLocationInformation05(BaseModel):
    place_of_service_code_01: Optional[str]
    facility_code_qualifier_02: Optional[str]
    claim_frequency_code_03: Optional[str]


# class ClaimInformationCLM(BaseModel):
#     patient_control_number_01: str
#     total_claim_charge_amount_02: float
#     health_care_service_location_information_05: Optional[HealthCareServiceLocationInformation05]
#     provider_or_supplier_signature_indicator_06: Optional[str]
#     assignment_or_plan_participation_code_07: Optional[str]
#     benefits_assignment_certification_indicator_08: Optional[str]
#     release_of_information_code_09: Optional[str]
class ClaimInformationCLM(BaseModel):
    patient_control_number_01: str
    total_claim_charge_amount_02: float
    health_care_service_location_information_05: Optional[HealthCareServiceLocationInformation05]
    provider_or_supplier_signature_indicator_06: Optional[str]
    assignment_or_plan_participation_code_07: Optional[str]
    benefits_assignment_certification_indicator_08: Optional[str]
    release_of_information_code_09: Optional[str]
    patient_signature_source_code_10: Optional[str]=None


# Diagnosis Information HI
class HealthCareCodeInformation(BaseModel):
    diagnosis_type_code_01: str
    diagnosis_code_02: str


class HealthCareDiagnosisCodeHI(BaseModel):
    health_care_code_information_01: HealthCareCodeInformation
    health_care_code_information_02: Optional[HealthCareCodeInformation]
    health_care_code_information_03: Optional[HealthCareCodeInformation]
    health_care_code_information_04: Optional[HealthCareCodeInformation]


# Service Facility Location NM1
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


# Rendering Provider NM1
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


# class ClaimLevelAdjustmentsCAS(BaseModel):
#     claim_adjustment_group_code_01: Optional[str]
#     adjustment_reason_code_02: Optional[str]
#     adjustment_amount_03: Optional[float]
#     adjustment_reason_code_05: Optional[str]
#     adjustment_amount_06: Optional[float]


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


class OtherSubscriberInformationSBRLoop(BaseModel):
    other_subscriber_information_SBR: OtherSubscriberInformationSBR
    claim_level_adjustments_CAS: Optional[List[dict]]
    coordination_of_benefits_cob_payer_paid_amount_AMT: Optional[
        CoordinationOfBenefitsPayerPaidAmountAMT
    ]
    remaining_patient_liability_AMT: Optional[RemainingPatientLiabilityAMT]
    other_insurance_coverage_information_OI: Optional[OtherInsuranceCoverageInformationOI]
    other_subscriber_name_NM1_loop: Optional[OtherSubscriberNameNM1Loop]
    other_payer_name_NM1_loop: Optional[OtherPayerNameNM1Loop]

#
# # Service Line Number LX
# class CompositeMedicalProcedureIdentifier(BaseModel):
#     product_or_service_id_qualifier_01: str
#     procedure_code_02: str
#
#
# class CompositeDiagnosisCodePointer(BaseModel):
#     diagnosis_code_pointer_01: int
#     diagnosis_code_pointer_02: Optional[int]
#     diagnosis_code_pointer_03: Optional[int]
#     diagnosis_code_pointer_04: Optional[int]
#
#
# class ProfessionalServiceSV1(BaseModel):
#     composite_medical_procedure_identifier_01: CompositeMedicalProcedureIdentifier
#     line_item_charge_amount_02: float
#     unit_or_basis_for_measurement_code_03: str
#     service_unit_count_04: int
#     composite_diagnosis_code_pointer_07: CompositeDiagnosisCodePointer
#
#
# class DateServiceDateDTP(BaseModel):
#     date_time_qualifier_01: str
#     date_time_period_format_qualifier_02: str
#     service_date_03: str
#
#
# class LineAdjudicationInformationSVD(BaseModel):
#     other_payer_primary_identifier_01: str
#     service_line_paid_amount_02: float
#     composite_medical_procedure_identifier_03: CompositeMedicalProcedureIdentifier
#     paid_service_unit_count_05: int
#
#
# class LineAdjustmentCAS(BaseModel):
#     claim_adjustment_group_code_01: str
#     adjustment_reason_code_02: str
#     adjustment_amount_03: float
#
#
# class LineCheckOrRemittanceDateDTP(BaseModel):
#     date_time_qualifier_01: str
#     date_time_period_format_qualifier_02: str
#     adjudication_or_payment_date_03: str
#
#
# class LineAdjudicationInformationSVDLoop(BaseModel):
#     line_adjudication_information_SVD: LineAdjudicationInformationSVD
#     line_adjustment_CAS: Optional[List[LineAdjustmentCAS]]
#     line_check_or_remittance_date_DTP: Optional[LineCheckOrRemittanceDateDTP]
#

# class ServiceLineNumberLXLoop(BaseModel):
#     service_line_number_LX: dict
#     #professional_service_SV1: ProfessionalServiceSV1
#     #date_service_date_DTP: Optional[DateServiceDateDTP]
#     # line_adjudication_information_SVD_loop: Optional[List[LineAdjudicationInformationSVDLoop]]
#
#     professional_service_SV1: dict
#     date_service_date_DTP: dict
#     line_adjudication_information_SVD_loop:dict




# -----------------
# Composite Medical Procedure Identifier
class CompositeMedicalProcedureIdentifier(BaseModel):
    product_or_service_id_qualifier_01: str
    procedure_code_02: str


# Diagnosis Code Pointer
class CompositeDiagnosisCodePointer(BaseModel):
    diagnosis_code_pointer_01: int
    diagnosis_code_pointer_02: Optional[int]
    diagnosis_code_pointer_03: Optional[int]
    diagnosis_code_pointer_04: Optional[int]


# Professional Service
class ProfessionalServiceSV1(BaseModel):
    composite_medical_procedure_identifier_01: CompositeMedicalProcedureIdentifier
    #composite_medical_procedure_identifier_01: dict
    line_item_charge_amount_02: float
    unit_or_basis_for_measurement_code_03: str
    service_unit_count_04: int
    #composite_diagnosis_code_pointer_07: CompositeDiagnosisCodePointer
    composite_diagnosis_code_pointer_07: dict


# Service Date
class DateServiceDateDTP(BaseModel):
    date_time_qualifier_01: str
    date_time_period_format_qualifier_02: str
    service_date_03: str


# Line Adjudication Information
class LineAdjudicationInformationSVD(BaseModel):
    other_payer_primary_identifier_01: str
    service_line_paid_amount_02: float
    composite_medical_procedure_identifier_03: CompositeMedicalProcedureIdentifier
    paid_service_unit_count_05: int


# Line Adjustment
class LineAdjustmentCAS(BaseModel):
    claim_adjustment_group_code_01: str
    adjustment_reason_code_02: str
    adjustment_amount_03: float


# Line Check or Remittance Date
class LineCheckOrRemittanceDateDTP(BaseModel):
    date_time_qualifier_01: str
    date_time_period_format_qualifier_02: str
    adjudication_or_payment_date_03: str


# Line Adjudication SVD Loop
class LineAdjudicationInformationSVDLoop(BaseModel):
    line_adjudication_information_SVD: LineAdjudicationInformationSVD
    line_adjustment_CAS: Optional[List[LineAdjustmentCAS]]=None
    line_check_or_remittance_date_DTP: Optional[LineCheckOrRemittanceDateDTP]

    # line_adjudication_information_SVD: dict
    # line_adjustment_CAS: dict
    # line_check_or_remittance_date_DTP: dict


# Service Line Number
class ServiceLineNumberLX(BaseModel):
    assigned_number_01: int


# Service Line Number LX Loop
class ServiceLineNumberLXLoop(BaseModel):
    service_line_number_LX: ServiceLineNumberLX
    professional_service_SV1: ProfessionalServiceSV1
    #date_service_date_DTP: Optional[DateServiceDateDTP]
    line_adjudication_information_SVD_loop: Optional[List[LineAdjudicationInformationSVDLoop]]
    #
    # service_line_number_LX: Optional[dict]=None
    #professional_service_SV1: Optional[dict]=None
    date_service_date_DTP: Optional[dict]=None
    #line_adjudication_information_SVD_loop: Optional[List[dict]]=None

# Main Claim Information CLM Loop Model
class ClaimInformationCLMLoop(BaseModel):
    claim_information_CLM: ClaimInformationCLM
    health_care_diagnosis_code_HI: HealthCareDiagnosisCodeHI
    service_facility_location_name_NM1_loop: ServiceFacilityLocationNM1Loop
    rendering_provider_name_NM1_loop: RenderingProviderNM1Loop
    other_subscriber_information_SBR_loop: Optional[List[OtherSubscriberInformationSBRLoop]]
    service_line_number_LX_loop: Optional[List[ServiceLineNumberLXLoop]]

# Envelope Class
class PatientHierarchicalLevelHLLoop(BaseModel):
    patient_information_PAT: PatientInformationPAT
    patient_name_NM1_loop: PatientNameNM1Loop
    claim_information_CLM_loop: List[ClaimInformationCLMLoop]