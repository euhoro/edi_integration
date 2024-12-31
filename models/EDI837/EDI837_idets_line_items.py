from typing import List, Optional
from pydantic import BaseModel


class CompositeMedicalProcedureIdentifier(BaseModel):
    product_or_service_id_qualifier_01: str
    procedure_code_02: str
    procedure_modifier_03: Optional[str]  # Optional as modifiers may not always be present


class CompositeDiagnosisCodePointer(BaseModel):
    diagnosis_code_pointer_01: int
    diagnosis_code_pointer_02: Optional[int]  # Optional as second pointer may not always be present


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
    line_adjustment_CAS: List[LineAdjustmentCAS]
    line_check_or_remittance_date_DTP: DateServiceDateDTP


class ServiceLineNumberLX(BaseModel):
    assigned_number_01: int


class ServiceLineNumberLXLoopItem(BaseModel):
    service_line_number_LX: ServiceLineNumberLX
    professional_service_SV1: ProfessionalServiceSV1
    # date_service_date_DTP: DateServiceDateDTP
    line_adjudication_information_SVD_loop: List[LineAdjudicationInformationSVDLoop]


class ServiceLineNumberLXLoop(BaseModel):
    service_line_number_LX_loop: List[ServiceLineNumberLXLoopItem]