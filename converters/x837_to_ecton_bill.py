from datetime import datetime

from models.EDI835.EDI835_idets import EDI835Idets
from models.EDI837.EDI837_idets import Edi837Idets, CompositeDiagnosisCodePointer
from models.EctonBill.ecton_bill import SecondaryBill




def get_diagnosis_pointers(line:CompositeDiagnosisCodePointer):
    pointers = []
    if line.diagnosis_code_pointer_01:
        pointers.append(1)
    if line.diagnosis_code_pointer_02:
        pointers.append(2)
    if line.diagnosis_code_pointer_03:
        pointers.append(3)
    if line.diagnosis_code_pointer_04:
        pointers.append(4)
    return pointers

def convert_x837_to_ecton_bill(x837: Edi837Idets) -> SecondaryBill:

    bill_provider =             x837.detail.billing_provider_hierarchical_level_HL_loop[0].billing_provider_name_NM1_loop
    subscriber =                x837.detail.billing_provider_hierarchical_level_HL_loop[0].subscriber_hierarchical_level_HL_loop[0]
    claim_patient_hierarchy =   x837.detail.billing_provider_hierarchical_level_HL_loop[0].subscriber_hierarchical_level_HL_loop[0].patient_hierarchical_level_HL_loop[0]
    patient_loop =      claim_patient_hierarchy.patient_name_NM1_loop
    service_facility =  claim_patient_hierarchy.claim_information_CLM_loop[0].service_facility_location_name_NM1_loop
    secondary_payer =  claim_patient_hierarchy.claim_information_CLM_loop[0].other_subscriber_information_SBR_loop
    service_lines =  claim_patient_hierarchy.claim_information_CLM_loop[0].service_line_number_LX_loop
    lines_cas =  []
    for x in service_lines:
        for svd in x.line_adjudication_information_SVD_loop:
            if svd.line_adjustment_CAS:
                lines_cas.append(svd.line_adjustment_CAS)
    sum_cas = sum([x[0].adjustment_amount_03 for x in lines_cas])
    bill_id = claim_patient_hierarchy.claim_information_CLM_loop[0].claim_information_CLM.patient_control_number_01
    sec_bill = {
        "bill_id": bill_id,
        "creation_date": "2024-01-01",
        "billing_provider": {
            "npi":     bill_provider.billing_provider_name_NM1.billing_provider_identifier_09,
            "tax_id": bill_provider.billing_provider_tax_identification_REF.billing_provider_tax_identification_number_02,
            "name": bill_provider.billing_provider_name_NM1.billing_provider_last_or_organizational_name_03,
            "contact_name": bill_provider.billing_provider_contact_information_PER[0].billing_provider_contact_name_02,
            "contact_phone": bill_provider.billing_provider_contact_information_PER[0].communication_number_04,
            "address": {
                "address_line1": bill_provider.billing_provider_address_N3.billing_provider_address_line_01,
                "city":bill_provider.billing_provider_city_state_zip_code_N4.billing_provider_city_name_01,
                "state": bill_provider.billing_provider_city_state_zip_code_N4.billing_provider_state_or_province_code_02,
                "zip_code": bill_provider.billing_provider_city_state_zip_code_N4.billing_provider_postal_zone_or_zip_code_03,
            },
        },
        "service_facility": {
            "npi": service_facility.service_facility_location_name_NM1.laboratory_or_facility_primary_identifier_09,
            "tax_id": service_facility.service_facility_location_name_NM1.identification_code_qualifier_08,
            "name": service_facility.service_facility_location_name_NM1.laboratory_or_facility_name_03,
            "address": {
                "address_line1": service_facility.service_facility_location_address_N3.laboratory_or_facility_address_line_01,
                "city": service_facility.service_facility_location_city_state_zip_code_N4.laboratory_or_facility_city_name_01,
                "state": service_facility.service_facility_location_city_state_zip_code_N4.laboratory_or_facility_state_or_province_code_02,
                "zip_code": service_facility.service_facility_location_city_state_zip_code_N4.laboratory_or_facility_postal_zone_or_zip_code_03,
            },
        },
        "patient": {
            "first_name": patient_loop.patient_name_NM1.patient_first_name_04,
            "last_name": patient_loop.patient_name_NM1.patient_last_name_03,
            "date_of_birth": datetime.strptime(patient_loop.patient_demographic_information_DMG.patient_birth_date_02, '%Y%m%d').date(),
            "gender": patient_loop.patient_demographic_information_DMG.patient_gender_code_03,
            "member_id": subscriber.subscriber_name_NM1_loop.subscriber_name_NM1.subscriber_primary_identifier_09,
            "relationship_code": subscriber.subscriber_name_NM1_loop.subscriber_name_NM1.entity_type_qualifier_02,#make enum eugen?
            "address": {
                "address_line1": patient_loop.patient_address_N3.patient_address_line_01,
                "city": patient_loop.patient_city_state_zip_code_N4.patient_city_name_01,
                "state":  patient_loop.patient_city_state_zip_code_N4.patient_state_code_02,
                "zip_code": patient_loop.patient_city_state_zip_code_N4.patient_postal_zone_or_zip_code_03,
            },
        },
        "primary_insurance": {
            # primary payer ??? payer ecton
            "payer_name": secondary_payer[0].other_payer_name_NM1_loop.other_payer_name_NM1.other_payer_organization_name_03,
            "payer_id": secondary_payer[0].other_payer_name_NM1_loop.other_payer_name_NM1.other_payer_primary_identifier_09,
            "claim_number": bill_id,
            "paid_date": x837.heading.beginning_of_hierarchical_transaction_BHT.transaction_set_creation_date_04,
            "total_paid": str(secondary_payer[0].coordination_of_benefits_cob_payer_paid_amount_AMT.payer_paid_amount_02),
            "total_adjusted": str(secondary_payer[0].remaining_patient_liability_AMT.remaining_patient_liability_02),
            #"total_patient_responsibility": round(secondary_payer[0].coordination_of_benefits_cob_payer_paid_amount_AMT.payer_paid_amount_02-secondary_payer[0].remaining_patient_liability_AMT.remaining_patient_liability_02),
            "total_patient_responsibility": str(sum_cas),
        },
        "original_claim_date": datetime.strptime(service_lines[0].line_adjudication_information_SVD_loop[0].line_check_or_remittance_date_DTP.adjudication_or_payment_date_03, '%Y%m%d').date(),
        "total_charge": str(claim_patient_hierarchy.claim_information_CLM_loop[0].claim_information_CLM.total_claim_charge_amount_02),
        "place_of_service": claim_patient_hierarchy.claim_information_CLM_loop[0].claim_information_CLM.health_care_service_location_information_05.place_of_service_code_01,
        "diagnoses": [
            {"code": claim_patient_hierarchy.claim_information_CLM_loop[0].health_care_diagnosis_code_HI.health_care_code_information_01.diagnosis_code_02, "pointer": 1},
            {"code": claim_patient_hierarchy.claim_information_CLM_loop[0].health_care_diagnosis_code_HI.health_care_code_information_02.diagnosis_code_02, "pointer": 2},
            {"code": claim_patient_hierarchy.claim_information_CLM_loop[0].health_care_diagnosis_code_HI.health_care_code_information_03.diagnosis_code_02, "pointer": 3},
            {"code": claim_patient_hierarchy.claim_information_CLM_loop[0].health_care_diagnosis_code_HI.health_care_code_information_04.diagnosis_code_02, "pointer": 4},
        ],
        "service_lines": [
            {
                "line_number": i+1,
                "service_date": datetime.strptime(line.line_adjudication_information_SVD_loop[0].line_check_or_remittance_date_DTP.adjudication_or_payment_date_03, '%Y%m%d').date(),
                "procedure_code": line.professional_service_SV1.composite_medical_procedure_identifier_01.procedure_code_02,
                "procedure_code_qualifier": line.professional_service_SV1.composite_medical_procedure_identifier_01.product_or_service_id_qualifier_01,
                "charge_amount": line.professional_service_SV1.line_item_charge_amount_02,
                "units": line.professional_service_SV1.service_unit_count_04,
                "diagnosis_pointers": get_diagnosis_pointers(line.professional_service_SV1.composite_diagnosis_code_pointer_07),
                "primary_paid": line.line_adjudication_information_SVD_loop[0].line_adjudication_information_SVD.paid_service_unit_count_05,
                "primary_adjusted": get_cas_adjusted_amount(line),#eugen should be multi
                "primary_adjustment_reason": line.line_adjudication_information_SVD_loop[0].line_adjustment_CAS[0].adjustment_reason_code_02 if has_cas(line) else '  ',
                "remaining_balance": get_remaining_cas_amount(line),#remaining_patient_liability_AMT
            } for i, line in enumerate(service_lines)],
        "total_remaining": str(secondary_payer[0].remaining_patient_liability_AMT.remaining_patient_liability_02),#remaining_patient_liability_AMT  sum cas
    }
    return SecondaryBill.model_validate(sec_bill)


def get_remaining_cas_amount(line):
    res =  str(
        line.line_adjudication_information_SVD_loop[0].line_adjudication_information_SVD.paid_service_unit_count_05
        ) if not has_cas(line) else\
        str(line.line_adjudication_information_SVD_loop[0].line_adjudication_information_SVD.paid_service_unit_count_05 -
            has_cas(line)[0].adjustment_amount_03)
    return res


def has_cas(line):
    return line.line_adjudication_information_SVD_loop[0].line_adjustment_CAS


def get_cas_adjusted_amount(line):
    return line.line_adjudication_information_SVD_loop[0].line_adjustment_CAS[0].adjustment_amount_03 if \
    has_cas(line) else 0.0
