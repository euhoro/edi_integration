from datetime import datetime

from models.EDI835.EDI835_idets import EDI835Idets
from models.EDI837.EDI837_idets import Edi837Idets


def convert_x837_to_x835(x837: Edi837Idets, paid = True) -> EDI835Idets:
    bill_provider = x837.detail.billing_provider_hierarchical_level_HL_loop[0].billing_provider_name_NM1_loop
    subscriber = x837.detail.billing_provider_hierarchical_level_HL_loop[0].subscriber_hierarchical_level_HL_loop[0]
    claim_patient_hierarchy = \
        x837.detail.billing_provider_hierarchical_level_HL_loop[0].subscriber_hierarchical_level_HL_loop[
            0].patient_hierarchical_level_HL_loop[0]

    patient_loop = claim_patient_hierarchy.patient_name_NM1_loop
    service_facility = claim_patient_hierarchy.claim_information_CLM_loop[0].service_facility_location_name_NM1_loop
    secondary_other_payer = claim_patient_hierarchy.claim_information_CLM_loop[0].other_subscriber_information_SBR_loop
    service_lines = claim_patient_hierarchy.claim_information_CLM_loop[0].service_line_number_LX_loop
    lines_cas = []
    for x in service_lines:
        for svd in x.line_adjudication_information_SVD_loop:
            if svd.line_adjustment_CAS:
                lines_cas.append(svd.line_adjustment_CAS)
    sum_cas = sum([x[0].adjustment_amount_03 for x in lines_cas])

    claim = claim_patient_hierarchy.claim_information_CLM_loop[0].claim_information_CLM
    bill_id = claim_patient_hierarchy.claim_information_CLM_loop[0].claim_information_CLM.patient_control_number_01

    cas_service_processed = [] if paid else [{
        "claim_adjustment_group_code_01": "PR",  # PR = Patient Responsibility
        "adjustment_reason_code_02": "1",  # Deductible
        # "adjustment_amount_03": get_cas_adjusted_amount(line)
        "adjustment_amount_03": 21.89  # Deductible amount
    }
    for i, line in enumerate(lines_cas)]

    line_cas_claim = []
    gr_code = secondary_other_payer[0].claim_level_adjustments_CAS[0].claim_adjustment_group_code_01
    last_item = None
    for x in secondary_other_payer[0].claim_level_adjustments_CAS[0]:
        item_dict0 = x[0]  # Extract dictionary from the object
        item_dict1 = x[1]  # Extract dictionary from the object
# Get the reason code if exists
        if 'reason_code' in item_dict0:
            last_item = {
                "claim_adjustment_group_code_01": gr_code,  # PR = Patient Responsibility
                "adjustment_reason_code_02": item_dict1,
                # Use reason code if available, else default
                "adjustment_amount_03": 0  # Deductible amount or placeholder
            }
            line_cas_claim.append(last_item)
        elif 'amount' in item_dict0:
            last_item["adjustment_amount_03"] =item_dict1


    cob_paid = \
        {
            "heading": {
                "transaction_set_header_ST": {
                    "transaction_set_identifier_code_01": "835",  # Transaction type: 835 = Payment/Advice
                    "transaction_set_control_number_02": x837.detail.transaction_set_trailer_SE.transaction_set_control_number_02
                    # Unique transaction identifier
                },
                "financial_information_BPR": {
                    "transaction_handling_code_01": "I",  # I = Remittance info only
                    "total_actual_provider_payment_amount_02": str(
                        secondary_other_payer[0].remaining_patient_liability_AMT.remaining_patient_liability_02) if paid else "0.00",
                    # "total_actual_provider_payment_amount_02": str(
                    #     secondary_other_payer[0].coordination_of_benefits_cob_payer_paid_amount_AMT.payer_paid_amount_02),
                    # 39.15,  # Total payment to provider
                    "credit_or_debit_flag_code_03": "C",  # C = Credit
                    "payment_method_code_04": "CHK" if paid else "NON",  # CHK = Check payment OR ECTON

                    "check_issue_or_eft_effective_date_16": datetime.strptime(
                        service_lines[0].line_adjudication_information_SVD_loop[
                            0].line_check_or_remittance_date_DTP.adjudication_or_payment_date_03,
                        '%Y%m%d').date(),  # "2005-10-15"  # Date payment issued
                },
                "reassociation_trace_number_TRN": {
                    "trace_type_code_01": "1",  # 1 = Transaction trace number ???
                    "check_or_eft_trace_number_02": bill_id,  # "26407789",  # Trace/check number
                    "payer_identifier_03": secondary_other_payer[
                        0].other_payer_name_NM1_loop.other_payer_name_NM1.other_payer_primary_identifier_09
                    # Payer's unique identifier
                },
                "receiver_identification_REF": {
                    "reference_identification_qualifier_01": "EV",  # EV = Event code ???
                    "receiver_identifier_02": "FAC"  # Facility identifier ????
                },
                "production_date_DTM": {
                    "date_time_qualifier_01": "405",  # 405 = Production date ???
                    "production_date_02":datetime.strptime(
                        service_lines[0].line_adjudication_information_SVD_loop[
                            0].line_check_or_remittance_date_DTP.adjudication_or_payment_date_03,
                                                        '%Y%m%d').date()
                    # "2005-10-15"  # Date of remittance creation
                },
                "payer_identification_N1_loop": {
                    "payer_identification_N1": {
                        "entity_identifier_code_01": "PR",  # PR = Payer
                        "payer_name_02": secondary_other_payer[
                            0].other_payer_name_NM1_loop.other_payer_name_NM1.other_payer_organization_name_03
                        # "KEY INSURANCE COMPANY"  # Name of payer
                    },
                    "payer_address_N3": {
                        "payer_address_line_01": subscriber.payer_name_NM1_loop.payer_address_N3.payer_address_line_01
                        # ,"4456 SOUTH SHORE BLVD"  # Payer's address
                    },
                    "payer_city_state_zip_code_N4": {
                        "payer_city_name_01": subscriber.payer_name_NM1_loop.payer_city_state_zip_code_N4.payer_city_name_01,
                        # "CHICAGO",  # City
                        "payer_state_code_02": subscriber.payer_name_NM1_loop.payer_city_state_zip_code_N4.payer_state_or_province_code_02,
                        # "IL",  # State
                        "payer_postal_zone_or_zip_code_03": subscriber.payer_name_NM1_loop.payer_city_state_zip_code_N4.payer_postal_zone_or_zip_code_03
                        # "44444"  # ZIP Code
                    },
                    "payer_technical_contact_information_PER": [
                        {
                            # ecton stuff
                            "contact_function_code_01": "BL",  # BL = Billing contact
                            "payer_technical_contact_name_02": "EDI",  # Contact name
                            "communication_number_qualifier_03": "TE",  # TE = Telephone
                            "payer_contact_communication_number_04": "8005551212",  # Phone number
                            "communication_number_qualifier_05": "EM",  # EM = Email
                            "payer_technical_contact_communication_number_06": "EDI.SUPPORT@ANYPAYER.COM"  # Email
                        }
                    ],
                    "payer_web_site_PER": {
                        # ecton stuff
                        "contact_function_code_01": "IC",  # IC = Information contact
                        "communication_number_qualifier_03": "UR",  # UR = URL
                        "communication_number_04": "WWW.ANYPAYER.COM"  # Payer's website
                    },
                    "payer_business_contact_information_PER": {
                        # ecton stuff
                        "contact_function_code_01": "CX",  # CX = Customer service
                        "communication_number_qualifier_03": "TE",  # TE = Telephone
                        "payer_contact_communication_number_04": "8661112222"  # Customer service number
                    }
                },
                "payee_identification_N1_loop": {
                    "payee_identification_N1": {
                        "entity_identifier_code_01": "PE",  # PE = Payee
                        "payee_name_02": bill_provider.billing_provider_name_NM1.billing_provider_last_or_organizational_name_03,
                        # "KILDARE",  # Payee's name
                        "identification_code_qualifier_03": bill_provider.billing_provider_name_NM1.identification_code_qualifier_08,
                        # "XX",  # XX = NPI (National Provider Identifier)
                        "payee_identification_code_04": bill_provider.billing_provider_name_NM1.billing_provider_identifier_09,
                        # "1999996666"  # Payee's NPI
                    },
                    "payee_address_N3": {
                        "payee_address_line_01": bill_provider.billing_provider_address_N3.billing_provider_address_line_01
                        # "1234 SEAWAY ST"  # Payee's address
                    },
                    "payee_city_state_zip_code_N4": {
                        "payee_city_name_01": bill_provider.billing_provider_city_state_zip_code_N4.billing_provider_city_name_01,
                        # "MIAMI",  # City
                        "payee_state_code_02": bill_provider.billing_provider_city_state_zip_code_N4.billing_provider_state_or_province_code_02,
                        # "FL",  # State
                        "payee_postal_zone_or_zip_code_03": bill_provider.billing_provider_city_state_zip_code_N4.billing_provider_postal_zone_or_zip_code_03
                        # "33111"  # ZIP Code
                    },
                    "payee_additional_identification_REF": [
                        {
                            "reference_identification_qualifier_01": bill_provider.billing_provider_tax_identification_REF.reference_identification_qualifier_01,
                            # "EI",  # EI = Employer ID
                            "additional_payee_identifier_02": bill_provider.billing_provider_tax_identification_REF.billing_provider_tax_identification_number_02
                            # "123456789"  # Employer ID number
                        }
                    ]
                }
            },
            "detail": {
                "header_number_LX_loop": [
                    {
                        "header_number_LX": {
                            "assigned_number_01": 1  # Header number for the payment details
                        },
                        "claim_payment_information_CLP_loop": [
                            {
                                "claim_payment_information_CLP": {
                                    "patient_control_number_01": bill_id,  # "26407789",  # Patient's account number
                                    "claim_status_code_02": "1" if paid else "4",  # 1 = Processed as primary claim
                                    "total_claim_charge_amount_03": claim.total_claim_charge_amount_02,
                                    # , 79.04,  # Original charge amount
                                    # "claim_payment_amount_04": secondary_other_payer[
                                    #     0].coordination_of_benefits_cob_payer_paid_amount_AMT.payer_paid_amount_02,
                                    "claim_payment_amount_04": secondary_other_payer[0].remaining_patient_liability_AMT.remaining_patient_liability_02 if paid else 0.00, ## PAID IN FULL !!!!
                                    #"claim_payment_amount_04": claim.total_claim_charge_amount_02, ## PAID IN FULL !!!!

                                    # 39.15,  # Paid amount
                                    "claim_filing_indicator_code_06": "MC",  # MC = Medicaid ???
                                    "payer_claim_control_number_07": "CLAIM1234",  # Payer's claim ID ???
                                    "facility_type_code_08": "11",  # Facility code for the service.  ???
                                    "claim_frequency_code_09": "1"  # 1 = Original claim.  ???
                                },
                                "claim_adjustment_CAS": None if paid else line_cas_claim
                                ,
                                "patient_name_NM1": {
                                    "entity_identifier_code_01": "QC",  # QC = Patient
                                    "entity_type_qualifier_02": "1",  # 1 = Person
                                    "patient_last_name_03": patient_loop.patient_name_NM1.patient_last_name_03,
                                    # "SMITH",  # Last name
                                    "patient_first_name_04": patient_loop.patient_name_NM1.patient_first_name_04,
                                    # "TED",  # First name
                                    "patient_middle_name_or_initial_05": "N",  # Middle initial ?? ??
                                    "identification_code_qualifier_08": "MI",  # MI = Member ID ???
                                    "patient_identifier_09": subscriber.subscriber_name_NM1_loop.subscriber_name_NM1.subscriber_primary_identifier_09  #"222334444"  # Member's ID  ??
                                },
                                "service_payment_information_SVC_loop": [
                                    {
                                        "service_payment_information_SVC": {
                                            "composite_medical_procedure_identifier_01": {
                                                "product_or_service_id_qualifier_01": s_line.professional_service_SV1.composite_medical_procedure_identifier_01.product_or_service_id_qualifier_01,
                                                # "HC",
                                                # HC = Healthcare procedure code
                                                "adjudicated_procedure_code_02": s_line.professional_service_SV1.composite_medical_procedure_identifier_01.procedure_code_02
                                                # "99213"  # Procedure code
                                            },
                                            "line_item_charge_amount_02": s_line.professional_service_SV1.line_item_charge_amount_02,
                                            # #43.00,  # Charge for the service
                                            "line_item_provider_payment_amount_03":
                                                s_line.line_adjudication_information_SVD_loop[
                                                    0].line_adjudication_information_SVD.service_line_paid_amount_02 if paid else 0.0,
                                            # 40.00,
                                            # Paid amount for the service
                                            "units_of_service_paid_count_05":
                                                s_line.line_adjudication_information_SVD_loop[
                                                    0].line_adjudication_information_SVD.paid_service_unit_count_05
                                            # 1  # Number of units
                                        },
                                        "service_date_DTM": [
                                            {
                                                "date_time_qualifier_01": s_line.date_service_date_DTP.date_time_qualifier_01,
                                                # "472",  # 472 = Service date

                                                # "service_date_02": service_lines[0].date_service_date_DTP.service_date_03
                                                "service_date_02":  # "2005-10-03"  # Date of service
                                                    datetime.strptime(
                                                        s_line.date_service_date_DTP.service_date_03,
                                                        '%Y%m%d').date()
                                            }]
                                    }
                                for i,s_line in enumerate(service_lines)]
                            }
                        ]
                    }
                ]
            },
            "summary": {
                "transaction_set_trailer_SE": {
                    "transaction_segment_count_01": 33,  # Total number of segments
                    "transaction_set_control_number_02": x837.detail.transaction_set_trailer_SE.transaction_set_control_number_02
                    # 1234  # Matches the control number in ST
                }
            }
        }

    ecton835 = EDI835Idets.model_validate(cob_paid)
    return ecton835
