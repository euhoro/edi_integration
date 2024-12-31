from typing import Optional, List

from pydantic import BaseModel


class OtherSubscriberNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: str
    other_insured_last_name_03: str
    other_insured_first_name_04: str
    identification_code_qualifier_08: str
    other_insured_identifier_09: Optional[str]


class OtherSubscriberAddressN3(BaseModel):
    other_subscriber_address_line_01: str


class OtherSubscriberCityStateZipCodeN4(BaseModel):
    other_subscriber_city_name_01: str
    other_subscriber_state_or_province_code_02: str
    other_subscriber_postal_zone_or_zip_code_03: Optional[str]=None


class OtherSubscriberNameNM1Loop(BaseModel):
    other_subscriber_name_NM1: OtherSubscriberNameNM1
    other_subscriber_address_N3: OtherSubscriberAddressN3
    other_subscriber_city_state_zip_code_N4: Optional[OtherSubscriberCityStateZipCodeN4]=None


class OtherPayerNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: str
    other_payer_organization_name_03: str
    identification_code_qualifier_08: str
    other_payer_primary_identifier_09: Optional[str]


class OtherPayerNameNM1Loop(BaseModel):
    other_payer_name_NM1: OtherPayerNameNM1


class OtherInsuranceCoverageInformationOI(BaseModel):
    benefits_assignment_certification_indicator_03: str
    patient_signature_source_code_04: str
    release_of_information_code_06: str


class CoordinationOfBenefitsCobbPayerPaidAmountAMT(BaseModel):
    amount_qualifier_code_01: str
    payer_paid_amount_02: float


class CoordinationOfBenefitsCobbTotalNonCoveredAmountAMT(BaseModel):
    amount_qualifier_code_01: str
    non_covered_charge_amount_02: float


class OtherSubscriberInformationSBR(BaseModel):
    payer_responsibility_sequence_number_code_01: Optional[str]
    individual_relationship_code_02: Optional[str] =None
    other_insured_group_name_04: Optional[str]  # Optional based on JSON structure
    claim_filing_indicator_code_09: Optional[str]


class OtherSubscriberInformationSBRLoopItem(BaseModel):
    other_subscriber_information_SBR: Optional[OtherSubscriberInformationSBR]=None
    coordination_of_benefits_cob_payer_paid_amount_AMT: CoordinationOfBenefitsCobbPayerPaidAmountAMT
    coordination_of_benefits_cob_total_non_covered_amount_AMT: CoordinationOfBenefitsCobbTotalNonCoveredAmountAMT
    other_insurance_coverage_information_OI: OtherInsuranceCoverageInformationOI
    other_subscriber_name_NM1_loop: OtherSubscriberNameNM1Loop
    other_payer_name_NM1_loop: OtherPayerNameNM1Loop


class OtherSubscriberInformationSBRLoop(BaseModel):
    other_subscriber_information_SBR_loop: Optional[List[OtherSubscriberInformationSBRLoopItem]]=None