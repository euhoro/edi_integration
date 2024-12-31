from typing import List, Optional

from pydantic import BaseModel

from models.EDI837.EDI837_idets_line_items import ServiceLineNumberLXLoopItem
from models.EDI837.EDI837_idets_others import OtherSubscriberInformationSBRLoopItem
from models.EDI837.EDI837_idets_patient import PatientHierarchicalLevelHLLoop


# Define models based on the provided JSON structure

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

class BillingProviderNameNM1Loop(BaseModel):
    billing_provider_name_NM1: BillingProviderNameNM1
    billing_provider_address_N3: BillingProviderAddressN3
    billing_provider_city_state_zip_code_N4: BillingProviderCityStateZipCodeN4
    billing_provider_upin_license_information_REF: Optional[List[BillingProviderUpinLicenseInformationREF]] = None
    billing_provider_tax_identification_REF: BillingProviderTaxIdentificationREF

class SubscriberInformationSBR(BaseModel):
    payer_responsibility_sequence_number_code_01: Optional[str]
    individual_relationship_code_02: Optional[str]=None
    subscriber_group_or_policy_number_03: Optional[str]=None
    subscriber_group_name_04: Optional[str]=None
    claim_filing_indicator_code_09: Optional[str]

class SubscriberNameNM1(BaseModel):
    entity_identifier_code_01: str
    entity_type_qualifier_02: str
    subscriber_last_name_03: str
    subscriber_first_name_04: str
    subscriber_middle_name_or_initial_05: Optional[str]=None
    identification_code_qualifier_08: str
    subscriber_primary_identifier_09: Optional[str]

class SubscriberAddressN3(BaseModel):
    subscriber_address_line_01: str

class SubscriberCityStateZipCodeN4(BaseModel):
    subscriber_city_name_01: str
    subscriber_state_code_02: str
    subscriber_postal_zone_or_zip_code_03: str

class SubscriberDemographicInformationDMG(BaseModel):
    date_time_period_format_qualifier_01: str
    subscriber_birth_date_02: str
    subscriber_gender_code_03: Optional[str]=None

class SubscriberNameNM1Loop(BaseModel):
    subscriber_name_NM1: SubscriberNameNM1
    subscriber_address_N3: SubscriberAddressN3
    subscriber_city_state_zip_code_N4: SubscriberCityStateZipCodeN4
    subscriber_demographic_information_DMG: SubscriberDemographicInformationDMG
    subscriber_city_state_zip_code_N4:Optional[dict]=None
    subscriber_address_N3:Optional[dict]=None

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

class ClaimInformationCLM(BaseModel):
    patient_control_number_01: str
    total_claim_charge_amount_02: float

class ClaimInformationCLMLoop(BaseModel):
    claim_information_CLM: ClaimInformationCLM
    # health_care_diagnosis_code_HI:dict
    # referring_provider_name_NM1_loop:dict
    # rendering_provider_name_NM1_loop:dict
    other_subscriber_information_SBR_loop:Optional[List[OtherSubscriberInformationSBRLoopItem]]=None
    service_line_number_LX_loop:List[ServiceLineNumberLXLoopItem]


class SubscriberHierarchicalLevelHLLoop(BaseModel):
    subscriber_information_SBR: Optional[SubscriberInformationSBR]=None
    subscriber_name_NM1_loop: SubscriberNameNM1Loop
    payer_name_NM1_loop: PayerNameNM1Loop
    claim_information_CLM_loop: Optional[List[ClaimInformationCLMLoop]]=None
    patient_hierarchical_level_HL_loop:Optional[List[PatientHierarchicalLevelHLLoop]]=None

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




