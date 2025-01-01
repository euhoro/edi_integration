import json
import os.path

import pytest
from datetime import date
from decimal import Decimal
from typing import Dict, Any

from models.EctonBill.ecton_bill import SecondaryBill, Address, Provider, Patient, ServiceLine
from tests.common_test_utils import get_root_path

mapping_837 = """{
  "heading": {
    "transaction_set_header_ST": {
      "transaction_set_identifier_code_01": **.ST_01_TransactionSetIdentifierCode,
      "transaction_set_control_number_02": $number(**.ST_02_TransactionSetControlNumber),
      "implementation_guide_version_name_03": **.ST_03_ImplementationConventionReference
    },
    "beginning_of_hierarchical_transaction_BHT": {
      "hierarchical_structure_code_01": **.BHT_01,
      "transaction_set_purpose_code_02": **.BHT_02,
      "originator_application_transaction_identifier_03": **.BHT_03,
      "transaction_set_creation_date_04": $fromMillis($toMillis(**.BHT_04, "[Y0001][M01][D01]"), "[Y0001]-[M01]-[D01]"),
      "transaction_set_creation_time_05": $substring(**.BHT_05, 0, 2) & ":" & $substring(**.BHT_05, 2),
      "claim_or_encounter_identifier_06": **.BHT_06
    },
    "submitter_name_NM1_loop": {
      "submitter_name_NM1": {
        "entity_identifier_code_01": **."NM1-1000A_loop"[0].NM1_01,
        "entity_type_qualifier_02": **."NM1-1000A_loop"[0].NM1_02,
        "submitter_last_or_organization_name_03": **."NM1-1000A_loop"[0].NM1_03,
        "identification_code_qualifier_08": **."NM1-1000A_loop"[0].NM1_08,
        "submitter_identifier_09": **."NM1-1000A_loop"[0].NM1_09
      },
      "submitter_edi_contact_information_PER": [
        {
          "contact_function_code_01": **."NM1-1000A_loop"[0].PER_01,
          "submitter_contact_name_02": **."NM1-1000A_loop"[0].PER_02,
          "communication_number_qualifier_03": **."NM1-1000A_loop"[0].PER_03,
          "communication_number_04": **."NM1-1000A_loop"[0].PER_04
        }
      ]
    },
    "receiver_name_NM1_loop": {
      "receiver_name_NM1": {
        "entity_identifier_code_01": **."NM1-1000B_loop"[0].NM1_01,
        "entity_type_qualifier_02": **."NM1-1000B_loop"[0].NM1_02,
        "receiver_name_03": **."NM1-1000B_loop"[0].NM1_03,
        "identification_code_qualifier_08": **."NM1-1000B_loop"[0].NM1_08,
        "receiver_primary_identifier_09": **."NM1-1000B_loop"[0].NM1_09
      }
    }
  },
  "detail": {
    "billing_provider_hierarchical_level_HL_loop": [
      {
        "pay_to_address_name_NM1_loop": {
          "pay_to_address_name_NM1": {
            "entity_identifier_code_01": **."NM1-2010AB_loop"[0].NM1_01,
            "entity_type_qualifier_02": **."NM1-2010AB_loop"[0].NM1_02
          },
          "pay_to_address_address_N3": {
            "pay_to_address_line_01": **."NM1-2010AB_loop"[0].N3_01,
            "pay_to_address_line_02": **."NM1-2010AB_loop"[0].N3_02
          },
          "pay_to_address_city_state_zip_code_N4": {
            "pay_to_address_city_name_01": **."NM1-2010AB_loop"[0].N4_01,
            "pay_to_address_state_code_02": **."NM1-2010AB_loop"[0].N4_02,
            "pay_to_address_postal_zone_or_zip_code_03": **."NM1-2010AB_loop"[0].N4_03
          }
        },
        "billing_provider_name_NM1_loop": {
          "billing_provider_name_NM1": {
            "entity_identifier_code_01": **."NM1-2010AA_loop"[0].NM1_01,
            "entity_type_qualifier_02": **."NM1-2010AA_loop"[0].NM1_02,
            "billing_provider_last_or_organizational_name_03": **."NM1-2010AA_loop"[0].NM1_03,
            "billing_provider_first_name_04": **."NM1-2010AA_loop"[0].NM1_04,
            "identification_code_qualifier_08": **."NM1-2010AA_loop"[0].NM1_08,
            "billing_provider_identifier_09": **."NM1-2010AA_loop"[0].NM1_09
          },
          "billing_provider_address_N3": {
            "billing_provider_address_line_01": **."NM1-2010AA_loop"[0].N3_01
          },
          "billing_provider_city_state_zip_code_N4": {
            "billing_provider_city_name_01": **."NM1-2010AA_loop"[0].N4_01,
            "billing_provider_state_or_province_code_02": **."NM1-2010AA_loop"[0].N4_02,
            "billing_provider_postal_zone_or_zip_code_03": **."NM1-2010AA_loop"[0].N4_03
          },
          "billing_provider_tax_identification_REF": {
            "reference_identification_qualifier_01": **."NM1-2010AA_loop"[0].REF_01,
            "billing_provider_tax_identification_number_02": **."NM1-2010AA_loop"[0].REF_02
          },
          "billing_provider_contact_information_PER": [
            {
              "contact_function_code_01": **."NM1-2010AA_loop"[0].PER_01,
              "billing_provider_contact_name_02": **."NM1-2010AA_loop"[0].PER_02,
              "communication_number_qualifier_03": **."NM1-2010AA_loop"[0].PER_03,
              "communication_number_04": **."NM1-2010AA_loop"[0].PER_04
            }
          ]
        },
        "subscriber_hierarchical_level_HL_loop": [
          {
            "subscriber_information_SBR": {
              "payer_responsibility_sequence_number_code_01": **."HL-2000B_loop"[0].SBR_01,
              "claim_filing_indicator_code_09": **."HL-2000B_loop"[0].SBR_09
            },
            "payer_name_NM1_loop": {
              "payer_name_NM1": {
                "entity_identifier_code_01": **."NM1-2010BB_loop"[0].NM1_01,
                "entity_type_qualifier_02": **."NM1-2010BB_loop"[0].NM1_02,
                "payer_name_03": **."NM1-2010BB_loop"[0].NM1_03,
                "identification_code_qualifier_08": **."NM1-2010BB_loop"[0].NM1_08,
                "payer_identifier_09": **."NM1-2010BB_loop"[0].NM1_09
              },
              "payer_address_N3": {
                "payer_address_line_01": **."NM1-2010BB_loop"[0].N3_01
              },
              "payer_city_state_zip_code_N4": {
                "payer_city_name_01": **."NM1-2010BB_loop"[0].N4_01,
                "payer_state_or_province_code_02": **."NM1-2010BB_loop"[0].N4_02,
                "payer_postal_zone_or_zip_code_03": **."NM1-2010BB_loop"[0].N4_03
              },
              "billing_provider_secondary_identification_REF": [
                {
                  "reference_identification_qualifier_01": **."NM1-2010BB_loop"[0].REF_01,
                  "billing_provider_secondary_identifier_02": **."NM1-2010BB_loop"[0].REF_02
                }
              ]
            },
            "subscriber_name_NM1_loop": {
              "subscriber_name_NM1": {
                "entity_identifier_code_01": **."NM1-2010BA_loop"[0].NM1_01,
                "entity_type_qualifier_02": **."NM1-2010BA_loop"[0].NM1_02,
                "subscriber_last_name_03": **."NM1-2010BA_loop"[0].NM1_03,
                "subscriber_first_name_04": **."NM1-2010BA_loop"[0].NM1_04,
                "identification_code_qualifier_08": **."NM1-2010BA_loop"[0].NM1_08,
                "subscriber_primary_identifier_09": **."NM1-2010BA_loop"[0].NM1_09
              },
              "subscriber_demographic_information_DMG": {
                "date_time_period_format_qualifier_01": **."NM1-2010BA_loop"[0].DMG_01,
                "subscriber_birth_date_02": **."NM1-2010BA_loop"[0].DMG_02,
                "subscriber_gender_code_03": **."NM1-2010BA_loop"[0].DMG_03
              }
            },
            "patient_hierarchical_level_HL_loop": [
              {
                "patient_information_PAT": {
                  "individual_relationship_code_01": **."HL-2000C_loop"[0].PAT_01
                },
                "patient_name_NM1_loop": {
                  "patient_name_NM1": {
                    "entity_identifier_code_01": **."NM1-2010CA_loop"[0].NM1_01,
                    "entity_type_qualifier_02": **."NM1-2010CA_loop"[0].NM1_02,
                    "patient_last_name_03": **."NM1-2010CA_loop"[0].NM1_03,
                    "patient_first_name_04": **."NM1-2010CA_loop"[0].NM1_04
                  },
                  "patient_address_N3": {
                    "patient_address_line_01": **."NM1-2010CA_loop"[0].N3_01
                  },
                  "patient_city_state_zip_code_N4": {
                    "patient_city_name_01": **."NM1-2010CA_loop"[0].N4_01,
                    "patient_state_code_02": **."NM1-2010CA_loop"[0].N4_02,
                    "patient_postal_zone_or_zip_code_03": **."NM1-2010CA_loop"[0].N4_03
                  },
                  "patient_demographic_information_DMG": {
                    "date_time_period_format_qualifier_01": **."NM1-2010CA_loop"[0].DMG_01,
                    "patient_birth_date_02": **."NM1-2010CA_loop"[0].DMG_02,
                    "patient_gender_code_03": **."NM1-2010CA_loop"[0].DMG_03
                  }
                },
                "claim_information_CLM_loop": [
                  {
                    "claim_information_CLM": {
                      "patient_control_number_01": **."CLM-2300_loop"[0].CLM_01,
                      "total_claim_charge_amount_02": $number(**."CLM-2300_loop"[0].CLM_02),
                      "health_care_service_location_information_05": {
                        "place_of_service_code_01": **."CLM-2300_loop"[0].CLM_05.CLM_05_01,
                        "facility_code_qualifier_02": **."CLM-2300_loop"[0].CLM_05.CLM_05_02,
                        "claim_frequency_code_03": **."CLM-2300_loop"[0].CLM_05.CLM_05_03
                      },
                      "provider_or_supplier_signature_indicator_06": **."CLM-2300_loop"[0].CLM_06,
                      "assignment_or_plan_participation_code_07": **."CLM-2300_loop"[0].CLM_07,
                      "benefits_assignment_certification_indicator_08": **."CLM-2300_loop"[0].CLM_08,
                      "release_of_information_code_09": **."CLM-2300_loop"[0].CLM_09
                    },
                    "health_care_diagnosis_code_HI": {
                      "health_care_code_information_01": {
                        "diagnosis_type_code_01": **."CLM-2300_loop"[0].HI_01.HI_01_01,
                        "diagnosis_code_02": **."CLM-2300_loop"[0].HI_01.HI_01_02
                      },
                      "health_care_code_information_02": {
                        "diagnosis_type_code_01": **."CLM-2300_loop"[0].HI_02.HI_02_01,
                        "diagnosis_code_02": **."CLM-2300_loop"[0].HI_02.HI_02_02
                      },
                      "health_care_code_information_03": {
                        "diagnosis_type_code_01": **."CLM-2300_loop"[0].HI_03.HI_03_01,
                        "diagnosis_code_02": **."CLM-2300_loop"[0].HI_03.HI_03_02
                      },
                      "health_care_code_information_04": {
                        "diagnosis_type_code_01": **."CLM-2300_loop"[0].HI_04.HI_04_01,
                        "diagnosis_code_02": **."CLM-2300_loop"[0].HI_04.HI_04_02
                      }
                    },
                    "rendering_provider_name_NM1_loop": {
                      "rendering_provider_name_NM1": {
                        "entity_identifier_code_01": **."NM1-2310B_loop"[0].NM1_01,
                        "entity_type_qualifier_02": **."NM1-2310B_loop"[0].NM1_02,"rendering_provider_last_or_organization_name_03": **."NM1-2310B_loop"[0].NM1_03,
                        "rendering_provider_first_name_04": **."NM1-2310B_loop"[0].NM1_04,
                        "identification_code_qualifier_08": **."NM1-2310B_loop"[0].NM1_08,
                        "rendering_provider_identifier_09": **."NM1-2310B_loop"[0].NM1_09
                      },
                      "rendering_provider_specialty_information_PRV": {
                        "provider_code_01": **."NM1-2310B_loop"[0].PRV_01,
                        "reference_identification_qualifier_02": **."NM1-2310B_loop"[0].PRV_02,
                        "provider_taxonomy_code_03": **."NM1-2310B_loop"[0].PRV_03
                      },
                      "rendering_provider_secondary_identification_REF": [
                        {
                          "reference_identification_qualifier_01": **."NM1-2310B_loop"[0].REF_01,
                          "rendering_provider_secondary_identifier_02": **."NM1-2310B_loop"[0].REF_02
                        }
                      ]
                    },
                    "service_facility_location_name_NM1_loop": {
                      "service_facility_location_name_NM1": {
                        "entity_identifier_code_01": **."NM1-2310C_loop"[0].NM1_01,
                        "entity_type_qualifier_02": **."NM1-2310C_loop"[0].NM1_02,
                        "laboratory_or_facility_name_03": **."NM1-2310C_loop"[0].NM1_03,
                        "identification_code_qualifier_08": **."NM1-2310C_loop"[0].NM1_08,
                        "laboratory_or_facility_primary_identifier_09": **."NM1-2310C_loop"[0].NM1_09
                      },
                      "service_facility_location_address_N3": {
                        "laboratory_or_facility_address_line_01": **."NM1-2310C_loop"[0].N3_01
                      },
                      "service_facility_location_city_state_zip_code_N4": {
                        "laboratory_or_facility_city_name_01": **."NM1-2310C_loop"[0].N4_01,
                        "laboratory_or_facility_state_or_province_code_02": **."NM1-2310C_loop"[0].N4_02,
                        "laboratory_or_facility_postal_zone_or_zip_code_03": **."NM1-2310C_loop"[0].N4_03
                      }
                    },
                    "other_subscriber_information_SBR_loop": [
                      {
                        "other_subscriber_information_SBR": {
                          "payer_responsibility_sequence_number_code_01": **."SBR-2320_loop"[0].SBR_01,
                          "individual_relationship_code_02": **."SBR-2320_loop"[0].SBR_02,
                          "claim_filing_indicator_code_09": **."SBR-2320_loop"[0].SBR_09
                        },
                        "claim_level_adjustments_CAS": [
                          {
                            "claim_adjustment_group_code_01": **."SBR-2320_loop"[0].CAS_01,
                            "adjustment_reason_code_02": **."SBR-2320_loop"[0].CAS_02,
                            "adjustment_amount_03": $number(**."SBR-2320_loop"[0].CAS_03),
                            "adjustment_reason_code_05": **."SBR-2320_loop"[0].CAS_05,
                            "adjustment_amount_06": $number(**."SBR-2320_loop"[0].CAS_06)
                          }
                        ],
                        "coordination_of_benefits_cob_payer_paid_amount_AMT": {
                          "amount_qualifier_code_01": **."SBR-2320_loop"[0].AMT[AMT_01="D"].AMT_01,
                          "payer_paid_amount_02": $number(**."SBR-2320_loop"[0].AMT[AMT_01="D"].AMT_02)
                        },
                        "remaining_patient_liability_AMT": {
                          "amount_qualifier_code_01": **."SBR-2320_loop"[0].AMT[AMT_01="EAF"].AMT_01,
                          "remaining_patient_liability_02": $number(**."SBR-2320_loop"[0].AMT[AMT_01="EAF"].AMT_02)
                        },
                        "other_insurance_coverage_information_OI": {
                          "benefits_assignment_certification_indicator_03": **."SBR-2320_loop"[0].OI_03,
                          "patient_signature_source_code_04": **."SBR-2320_loop"[0].OI_04,
                          "release_of_information_code_06": **."SBR-2320_loop"[0].OI_06
                        },
                        "other_subscriber_name_NM1_loop": {
                          "other_subscriber_name_NM1": {
                            "entity_identifier_code_01": **."NM1-2330A_loop"[0].NM1_01,
                            "entity_type_qualifier_02": **."NM1-2330A_loop"[0].NM1_02,
                            "other_insured_last_name_03": **."NM1-2330A_loop"[0].NM1_03,
                            "other_insured_first_name_04": **."NM1-2330A_loop"[0].NM1_04,
                            "identification_code_qualifier_08": **."NM1-2330A_loop"[0].NM1_08,
                            "other_insured_identifier_09": **."NM1-2330A_loop"[0].NM1_09
                          },
                          "other_subscriber_address_N3": {
                            "other_subscriber_address_line_01": **."NM1-2330A_loop"[0].N3_01
                          },
                          "other_subscriber_city_state_zip_code_N4": {
                            "other_subscriber_city_name_01": **."NM1-2330A_loop"[0].N4_01,
                            "other_subscriber_state_or_province_code_02": **."NM1-2330A_loop"[0].N4_02,
                            "other_subscriber_postal_zone_or_zip_code_03": **."NM1-2330A_loop"[0].N4_03
                          }
                        },
                        "other_payer_name_NM1_loop": {
                          "other_payer_name_NM1": {
                            "entity_identifier_code_01": **."NM1-2330B_loop"[0].NM1_01,
                            "entity_type_qualifier_02": **."NM1-2330B_loop"[0].NM1_02,
                            "other_payer_organization_name_03": **."NM1-2330B_loop"[0].NM1_03,
                            "identification_code_qualifier_08": **."NM1-2330B_loop"[0].NM1_08,
                            "other_payer_primary_identifier_09": **."NM1-2330B_loop"[0].NM1_09
                          }
                        }
                      }
                    ],
                    "service_line_number_LX_loop": **."LX-2400_loop".{
                      "service_line_number_LX": {
                        "assigned_number_01": $number(LX_01)
                      },
                      "professional_service_SV1": {
                        "composite_medical_procedure_identifier_01": {
                          "product_or_service_id_qualifier_01": SV1_01.SV1_01_01,
                          "procedure_code_02": SV1_01.SV1_01_02
                        },
                        "line_item_charge_amount_02": $number(SV1_02),
                        "unit_or_basis_for_measurement_code_03": SV1_03,
                        "service_unit_count_04": $number(SV1_04),
                        "composite_diagnosis_code_pointer_07": {
                          "diagnosis_code_pointer_01": $number(SV1_07.SV1_07_01),
                          "diagnosis_code_pointer_02": $number(SV1_07.SV1_07_02),
                          "diagnosis_code_pointer_03": $number(SV1_07.SV1_07_03),
                          "diagnosis_code_pointer_04": $number(SV1_07.SV1_07_04)
                        }
                      },
                      "date_service_date_DTP": {
                        "date_time_qualifier_01": DTP_01,
                        "date_time_period_format_qualifier_02": DTP_02,
                        "service_date_03": DTP_03
                      },
                      "line_adjudication_information_SVD_loop": "SVD-2430_loop".{
                        "line_adjudication_information_SVD": {
                          "other_payer_primary_identifier_01": SVD_01,
                          "service_line_paid_amount_02": $number(SVD_02),
                          "composite_medical_procedure_identifier_03": {
                            "product_or_service_id_qualifier_01": SVD_03.SVD_03_01,
                            "procedure_code_02": SVD_03.SVD_03_02
                          },
                          "paid_service_unit_count_05": $number(SVD_05)
                        },
                        "line_adjustment_CAS": CAS.{
                          "claim_adjustment_group_code_01": CAS_01,
                          "adjustment_reason_code_02": CAS_02,
                          "adjustment_amount_03": $number(CAS_03)
                        },
                        "line_check_or_remittance_date_DTP": {
                          "date_time_qualifier_01": DTP_01,
                          "date_time_period_format_qualifier_02": DTP_02,
                          "adjudication_or_payment_date_03": DTP_03
                        }
                      }
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "transaction_set_trailer_SE": {
    "transaction_segment_count_01": $count(**.segments),
    "transaction_set_control_number_02": $number(**.ST_02_TransactionSetControlNumber)
  }
}"""

idets837={
  "interchanges": [
    {
      "ISA_01_AuthorizationQualifier": "00",
      "ISA_02_AuthorizationInformation": "          ",
      "ISA_03_SecurityQualifier": "00",
      "ISA_04_SecurityInformation": "          ",
      "ISA_05_SenderQualifier": "27",
      "ISA_06_SenderId": "SSSSSS         ",
      "ISA_07_ReceiverQualifier": "27",
      "ISA_08_ReceiverId": "PPPPP          ",
      "ISA_09_Date": "091006",
      "ISA_10_Time": "1248",
      "ISA_11_RepetitionSeparator": "`",
      "ISA_12_Version": "00501",
      "ISA_13_InterchangeControlNumber": "000000001",
      "ISA_14_AcknowledgmentRequested": "1",
      "ISA_15_TestIndicator": "P",
      "functional_groups": [
        {
          "GS_01_FunctionalIdentifierCode": "HC",
          "GS_02_ApplicationSenderCode": "SSSSSS",
          "GS_03_ApplicationReceiverCode": "PPPPP",
          "GS_04_Date": "20091006",
          "GS_05_Time": "1248",
          "GS_06_GroupControlNumber": "3001",
          "GS_07_ResponsibleAgencyCode": "X",
          "GS_08_Version": "005010X222A1",
          "transactions": [
            {
              "ST_01_TransactionSetIdentifierCode": "837",
              "ST_02_TransactionSetControlNumber": "1234",
              "ST_03_ImplementationConventionReference": "005010X222A1",
              "segments": [
                {
                  "BHT_01": "0019",
                  "BHT_02": "00",
                  "BHT_03": "0123",
                  "BHT_04": "20051015",
                  "BHT_05": "1023",
                  "BHT_06": "CH"
                },
                {
                  "NM1-1000A_loop": [
                    {
                      "NM1_01": "41",
                      "NM1_02": "2",
                      "NM1_03": "PREMIER BILLING SERVICE",
                      "NM1_08": "46",
                      "NM1_09": "12EEER 000TY"
                    },
                    {
                      "PER_01": "IC",
                      "PER_02": "JERRY",
                      "PER_03": "TE",
                      "PER_04": "3055552222"
                    }
                  ]
                },
                {
                  "NM1-1000B_loop": [
                    {
                      "NM1_01": "40",
                      "NM1_02": "2",
                      "NM1_03": "GREAT PRAIRIES HEALTH",
                      "NM1_08": "46",
                      "NM1_09": "567890"
                    }
                  ]
                },
                {
                  "HL-2000A_loop": [
                    {
                      "HL_01": "1",
                      "HL_03": "20",
                      "HL_04": "1"
                    },
                    {
                      "NM1-2010AA_loop": [
                        {
                          "NM1_01": "85",
                          "NM1_02": "1",
                          "NM1_03": "KILDARE",
                          "NM1_04": "BEN",
                          "NM1_08": "XX",
                          "NM1_09": "1999996666"
                        },
                        {
                          "N3_01": "1234SEAWAY ST"
                        },
                        {
                          "N4_01": "MIAMI",
                          "N4_02": "FL",
                          "N4_03": "33111"
                        },
                        {
                          "REF_01": "EI",
                          "REF_02": "123456789"
                        },
                        {
                          "PER_01": "IC",
                          "PER_02": "CONNIE",
                          "PER_03": "TE",
                          "PER_04": "3055551234"
                        }
                      ]
                    },
                    {
                      "NM1-2010AB_loop": [
                        {
                          "NM1_01": "87",
                          "NM1_02": "2"
                        },
                        {
                          "N3_01": "2345",
                          "N3_02": "OCEAN BLVD"
                        },
                        {
                          "N4_01": "MIAMI",
                          "N4_02": "FL",
                          "N4_03": "3111"
                        }
                      ]
                    },
                    {
                      "HL-2000B_loop": [
                        {
                          "HL_01": "2",
                          "HL_02": "1",
                          "HL_03": "22",
                          "HL_04": "1"
                        },
                        {
                          "SBR_01": "S",
                          "SBR_09": "CI"
                        },
                        {
                          "NM1-2010BA_loop": [
                            {
                              "NM1_01": "IL",
                              "NM1_02": "1",
                              "NM1_03": "SMITH",
                              "NM1_04": "JACK",
                              "NM1_08": "MI",
                              "NM1_09": "222334444"
                            },
                            {
                              "DMG_01": "D8",
                              "DMG_02": "19431022",
                              "DMG_03": "M"
                            }
                          ]
                        },
                        {
                          "NM1-2010BB_loop": [
                            {
                              "NM1_01": "PR",
                              "NM1_02": "2",
                              "NM1_03": "GREAT PRAIRIES HEALTH",
                              "NM1_08": "PI",
                              "NM1_09": "567890"
                            },
                            {
                              "N3_01": "4456 SOUTH SHORE BLVD"
                            },
                            {
                              "N4_01": "CHICAGO",
                              "N4_02": "IL",
                              "N4_03": "44444"
                            },
                            {
                              "REF_01": "G2",
                              "REF_02": "567890"
                            }
                          ]
                        },
                        {
                          "HL-2000C_loop": [
                            {
                              "HL_01": "3",
                              "HL_02": "2",
                              "HL_03": "23",
                              "HL_04": "0"
                            },
                            {
                              "PAT_01": "19"
                            },
                            {
                              "NM1-2010CA_loop": [
                                {
                                  "NM1_01": "QC",
                                  "NM1_02": "1",
                                  "NM1_03": "SMITH",
                                  "NM1_04": "TED"
                                },
                                {
                                  "N3_01": "236 N MAIN ST"
                                },
                                {
                                  "N4_01": "MIAMI",
                                  "N4_02": "FL",
                                  "N4_03": "33413"
                                },
                                {
                                  "DMG_01": "D8",
                                  "DMG_02": "19730501",
                                  "DMG_03": "M"
                                }
                              ]
                            },
                            {
                              "CLM-2300_loop": [
                                {
                                  "CLM_01": "26407789",
                                  "CLM_02": "79.04",
                                  "CLM_05": {
                                    "CLM_05_01": "11",
                                    "CLM_05_02": "B",
                                    "CLM_05_03": "1"
                                  },
                                  "CLM_06": "Y",
                                  "CLM_07": "A",
                                  "CLM_08": "Y",
                                  "CLM_09": "I"
                                },
                                {
                                  "HI_01": {
                                    "HI_01_01": "BK",
                                    "HI_01_02": "4779"
                                  },
                                  "HI_02": {
                                    "HI_02_01": "BF",
                                    "HI_02_02": "2724"
                                  },
                                  "HI_03": {
                                    "HI_03_01": "BF",
                                    "HI_03_02": "2780"
                                  },
                                  "HI_04": {
                                    "HI_04_01": "BF",
                                    "HI_04_02": "53081"
                                  }
                                },
                                {
                                  "NM1-2310B_loop": [
                                    {
                                      "NM1_01": "82",
                                      "NM1_02": "1",
                                      "NM1_03": "KILDARE",
                                      "NM1_04": "BEN",
                                      "NM1_08": "XX",
                                      "NM1_09": "1999996666"
                                    },
                                    {
                                      "PRV_01": "PE",
                                      "PRV_02": "PXC",
                                      "PRV_03": "204C00000X"
                                    },
                                    {
                                      "REF_01": "G2",
                                      "REF_02": "88877"
                                    }
                                  ]
                                },
                                {
                                  "NM1-2310C_loop": [
                                    {
                                      "NM1_01": "77",
                                      "NM1_02": "2",
                                      "NM1_03": "KILDARE ASSOCIATES",
                                      "NM1_08": "XX",
                                      "NM1_09": "1581234567"
                                    },
                                    {
                                      "N3_01": "2345 OCEAN BLVD"
                                    },
                                    {
                                      "N4_01": "MIAMI",
                                      "N4_02": "FL",
                                      "N4_03": "33111"
                                    }
                                  ]
                                },
                                {
                                  "SBR-2320_loop": [
                                    {
                                      "SBR_01": "P",
                                      "SBR_02": "01",
                                      "SBR_09": "CI"
                                    },
                                    {
                                      "CAS_01": "PR",
                                      "CAS_02": "1",
                                      "CAS_03": "21.89",
                                      "CAS_05": "2",
                                      "CAS_06": "15"
                                    },
                                    {
                                      "AMT_01": "D",
                                      "AMT_02": "39.15"
                                    },
                                    {
                                      "AMT_01": "EAF",
                                      "AMT_02": "36.89"
                                    },
                                    {
                                      "OI_03": "Y",
                                      "OI_04": "P",
                                      "OI_06": "Y"
                                    },
                                    {
                                      "NM1-2330A_loop": [
                                        {
                                          "NM1_01": "IL",
                                          "NM1_02": "1",
                                          "NM1_03": "SMITH",
                                          "NM1_04": "JANE",
                                          "NM1_08": "MI",
                                          "NM1_09": "JS00111223333"
                                        },
                                        {
                                          "N3_01": "236 N MAIN ST"
                                        },
                                        {
                                          "N4_01": "MIAMI",
                                          "N4_02": "FL",
                                          "N4_03": "33111"
                                        }
                                      ]
                                    },
                                    {
                                      "NM1-2330B_loop": [
                                        {
                                          "NM1_01": "PR",
                                          "NM1_02": "2",
                                          "NM1_03": "KEY INSURANCE COMPANY",
                                          "NM1_08": "PI",
                                          "NM1_09": "999996666"
                                        }
                                      ]
                                    }
                                  ]
                                },
                                {
                                  "LX-2400_loop": [
                                    {
                                      "LX_01": "1"
                                    },
                                    {
                                      "SV1_01": {
                                        "SV1_01_01": "HC",
                                        "SV1_01_02": "99213"
                                      },
                                      "SV1_02": "43",
                                      "SV1_03": "UN",
                                      "SV1_04": "1",
                                      "SV1_07": {
                                        "SV1_07_01": "1",
                                        "SV1_07_02": "2",
                                        "SV1_07_03": "3",
                                        "SV1_07_04": "4"
                                      }
                                    },
                                    {
                                      "DTP_01": "472",
                                      "DTP_02": "D8",
                                      "DTP_03": "20051003"
                                    },
                                    {
                                      "SVD-2430_loop": [
                                        {
                                          "SVD_01": "999996666",
                                          "SVD_02": "40",
                                          "SVD_03": {
                                            "SVD_03_01": "HC",
                                            "SVD_03_02": "99213"
                                          },
                                          "SVD_05": "1"
                                        },
                                        {
                                          "CAS_01": "CO",
                                          "CAS_02": "42",
                                          "CAS_03": "3"
                                        },
                                        {
                                          "DTP_01": "573",
                                          "DTP_02": "D8",
                                          "DTP_03": "20051015"
                                        }
                                      ]
                                    }
                                  ]
                                },
                                {
                                  "LX-2400_loop": [
                                    {
                                      "LX_01": "2"
                                    },
                                    {
                                      "SV1_01": {
                                        "SV1_01_01": "HC",
                                        "SV1_01_02": "90782"
                                      },
                                      "SV1_02": "15",
                                      "SV1_03": "UN",
                                      "SV1_04": "1",
                                      "SV1_07": {
                                        "SV1_07_01": "1",
                                        "SV1_07_02": "2"
                                      }
                                    },
                                    {
                                      "DTP_01": "472",
                                      "DTP_02": "D8",
                                      "DTP_03": "20051003"
                                    },
                                    {
                                      "SVD-2430_loop": [
                                        {
                                          "SVD_01": "999996666",
                                          "SVD_02": "15",
                                          "SVD_03": {
                                            "SVD_03_01": "HC",
                                            "SVD_03_02": "90782"
                                          },
                                          "SVD_05": "1"
                                        },
                                        {
                                          "DTP_01": "573",
                                          "DTP_02": "D8",
                                          "DTP_03": "20051015"
                                        }
                                      ]
                                    }
                                  ]
                                },
                                {
                                  "LX-2400_loop": [
                                    {
                                      "LX_01": "3"
                                    },
                                    {
                                      "SV1_01": {
                                        "SV1_01_01": "HC",
                                        "SV1_01_02": "J3301"
                                      },
                                      "SV1_02": "21.04",
                                      "SV1_03": "UN",
                                      "SV1_04": "1",
                                      "SV1_07": {
                                        "SV1_07_01": "1",
                                        "SV1_07_02": "2"
                                      }
                                    },
                                    {
                                      "DTP_01": "472",
                                      "DTP_02": "D8",
                                      "DTP_03": "20051003"
                                    },
                                    {
                                      "SVD-2430_loop": [
                                        {
                                          "SVD_01": "999996666",
                                          "SVD_02": "21.04",
                                          "SVD_03": {
                                            "SVD_03_01": "HC",
                                            "SVD_03_02": "J3301"
                                          },
                                          "SVD_05": "1"
                                        },
                                        {
                                          "DTP_01": "573",
                                          "DTP_02": "D8",
                                          "DTP_03": "20051015"
                                        }
                                      ]
                                    }
                                  ]
                                }
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}

idets835 = {
  "heading": {
    "transaction_set_header_ST": {
      "transaction_set_identifier_code_01": "835",
      "transaction_set_control_number_02": 10060875
    },
    "financial_information_BPR": {
      "transaction_handling_code_01": "I",
      "total_actual_provider_payment_amount_02": 80,
      "credit_or_debit_flag_code_03": "C",
      "payment_method_code_04": "CHK",
      "check_issue_or_eft_effective_date_16": "2019-08-16"
    },
    "reassociation_trace_number_TRN": {
      "trace_type_code_01": "1",
      "check_or_eft_trace_number_02": "CK NUMBER 1",
      "payer_identifier_03": "1234567890"
    },
    "receiver_identification_REF": {
      "reference_identification_qualifier_01": "EV",
      "receiver_identifier_02": "FAC"
    },
    "production_date_DTM": {
      "date_time_qualifier_01": "405",
      "production_date_02": "2019-08-27"
    },
    "payer_identification_N1_loop": {
      "payer_identification_N1": {
        "entity_identifier_code_01": "PR",
        "payer_name_02": "ANY PLAN USA"
      },
      "payer_address_N3": {
        "payer_address_line_01": "1 WALK THIS WAY"
      },
      "payer_city_state_zip_code_N4": {
        "payer_city_name_01": "ANYCITY",
        "payer_state_code_02": "OH",
        "payer_postal_zone_or_zip_code_03": "45209"
      },
      "payer_technical_contact_information_PER": [
        {
          "contact_function_code_01": "BL",
          "payer_technical_contact_name_02": "EDI",
          "communication_number_qualifier_03": "TE",
          "payer_contact_communication_number_04": "8002223333",
          "communication_number_qualifier_05": "EM",
          "payer_technical_contact_communication_number_06": "EDI.SUPPORT@ANYPAYER.COM"
        }
      ],
      "payer_web_site_PER": {
        "contact_function_code_01": "IC",
        "communication_number_qualifier_03": "UR",
        "communication_number_04": "WWW.ANYPAYER.COM"
      },
      "payer_business_contact_information_PER": {
        "contact_function_code_01": "CX",
        "communication_number_qualifier_03": "TE",
        "payer_contact_communication_number_04": "8661112222"
      }
    },
    "payee_identification_N1_loop": {
      "payee_identification_N1": {
        "entity_identifier_code_01": "PE",
        "payee_name_02": "PROVIDER",
        "identification_code_qualifier_03": "XX",
        "payee_identification_code_04": "1123454567"
      },
      "payee_address_N3": {
        "payee_address_line_01": "2255 ANY ROAD"
      },
      "payee_city_state_zip_code_N4": {
        "payee_city_name_01": "ANY CITY",
        "payee_state_code_02": "CA",
        "payee_postal_zone_or_zip_code_03": "12211"
      },
      "payee_additional_identification_REF": [
        {
          "reference_identification_qualifier_01": "TJ",
          "additional_payee_identifier_02": "123456789"
        }
      ]
    }
  },
  "detail": {
    "header_number_LX_loop": [
      {
        "header_number_LX": {
          "assigned_number_01": 1
        },
        "claim_payment_information_CLP_loop": [
          {
            "claim_payment_information_CLP": {
              "patient_control_number_01": "PATACCT",
              "claim_status_code_02": "1",
              "total_claim_charge_amount_03": 400,
              "claim_payment_amount_04": 80,
              "claim_filing_indicator_code_06": "MC",
              "payer_claim_control_number_07": "CLAIMNUMBER",
              "facility_type_code_08": "11",
              "claim_frequency_code_09": "1"
            },
            "patient_name_NM1": {
              "entity_identifier_code_01": "QC",
              "entity_type_qualifier_02": "1",
              "patient_last_name_03": "DOE",
              "patient_first_name_04": "JOHN",
              "patient_middle_name_or_initial_05": "N",
              "identification_code_qualifier_08": "MI",
              "patient_identifier_09": "ABC123456789"
            },
            "other_claim_related_identification_REF": [
              {
                "reference_identification_qualifier_01": "1L",
                "other_claim_related_identifier_02": "12345F"
              }
            ],
            "claim_received_date_DTM": {
              "date_time_qualifier_01": "050",
              "date_02": "2019-02-09"
            },
            "claim_contact_information_PER": [
              {
                "contact_function_code_01": "CX",
                "claim_contact_name_02": "G CUSTOMER SERVICE DEPARTMENT",
                "communication_number_qualifier_03": "TE",
                "claim_contact_communications_number_04": "8004074627"
              }
            ],
            "claim_supplemental_information_AMT": [
              {
                "amount_qualifier_code_01": "AU",
                "claim_supplemental_information_amount_02": 150
              }
            ],
            "service_payment_information_SVC_loop": [
              {
                "service_payment_information_SVC": {
                  "composite_medical_procedure_identifier_01": {
                    "product_or_service_id_qualifier_01": "HC",
                    "adjudicated_procedure_code_02": "99213"
                  },
                  "line_item_charge_amount_02": 150,
                  "line_item_provider_payment_amount_03": 80,
                  "units_of_service_paid_count_05": 1
                },
                "service_date_DTM": [
                  {
                    "date_time_qualifier_01": "472",
                    "service_date_02": "2019-01-01"
                  }
                ],
                "service_adjustment_CAS": [
                  {
                    "claim_adjustment_group_code_01": "CO",
                    "adjustment_reason_code_02": "45",
                    "adjustment_amount_03": 70
                  }
                ],
                "service_supplemental_amount_AMT": [
                  {
                    "amount_qualifier_code_01": "B6",
                    "service_supplemental_amount_02": 80
                  }
                ]
              },
              {
                "service_payment_information_SVC": {
                  "composite_medical_procedure_identifier_01": {
                    "product_or_service_id_qualifier_01": "HC",
                    "adjudicated_procedure_code_02": "85003"
                  },
                  "line_item_charge_amount_02": 100,
                  "line_item_provider_payment_amount_03": 0,
                  "units_of_service_paid_count_05": 1
                },
                "service_date_DTM": [
                  {
                    "date_time_qualifier_01": "472",
                    "service_date_02": "2019-01-01"
                  }
                ],
                "service_adjustment_CAS": [
                  {
                    "claim_adjustment_group_code_01": "CO",
                    "adjustment_reason_code_02": "204",
                    "adjustment_amount_03": 100
                  }
                ]
              },
              {
                "service_payment_information_SVC": {
                  "composite_medical_procedure_identifier_01": {
                    "product_or_service_id_qualifier_01": "HC",
                    "adjudicated_procedure_code_02": "36415"
                  },
                  "line_item_charge_amount_02": 150,
                  "line_item_provider_payment_amount_03": 0,
                  "units_of_service_paid_count_05": 1
                },
                "service_date_DTM": [
                  {
                    "date_time_qualifier_01": "472",
                    "service_date_02": "2019-01-01"
                  }
                ],
                "service_adjustment_CAS": [
                  {
                    "claim_adjustment_group_code_01": "CO",
                    "adjustment_reason_code_02": "97",
                    "adjustment_amount_03": 150
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "summary": {
    "transaction_set_trailer_SE": {
      "transaction_segment_count_01": 33,
      "transaction_set_control_number_02": 10060875
    }
  }
}

mapping_835 = """{
  "interchanges": [{
    "ISA_01_AuthorizationQualifier": "00",
    "ISA_02_AuthorizationInformation": "          ",
    "ISA_03_SecurityQualifier": "00",
    "ISA_04_SecurityInformation": "          ",
    "ISA_05_SenderQualifier": "ZZ",
    "ISA_06_SenderId": "ABCPAYER       ",
    "ISA_07_ReceiverQualifier": "ZZ",
    "ISA_08_ReceiverId": "ABCPAYER       ",
    "ISA_09_Date": $substring(heading.production_date_DTM.production_date_02, 2, 2) & $substring(heading.production_date_DTM.production_date_02, 5, 2) & $substring(heading.production_date_DTM.production_date_02, 8, 2),
    "ISA_10_Time": "0212",
    "ISA_11_RepetitionSeparator": "^",
    "ISA_12_Version": "00501",
    "ISA_13_InterchangeControlNumber": "191511902",
    "ISA_14_AcknowledgmentRequested": "0",
    "ISA_15_TestIndicator": "P",
    "functional_groups": [{
      "GS_01_FunctionalIdentifierCode": "HP",
      "GS_02_ApplicationSenderCode": "ABCD",
      "GS_03_ApplicationReceiverCode": "ABCD",
      "GS_04_Date": $replace(heading.production_date_DTM.production_date_02,"-",""),
      "GS_05_Time": "12345678",
      "GS_06_GroupControlNumber": "12345678",
      "GS_07_ResponsibleAgencyCode": "X",
      "GS_08_Version": "005010X221A1",
      "transactions": [{
        "ST_01_TransactionSetIdentifierCode": heading.transaction_set_header_ST.transaction_set_identifier_code_01,
        "ST_02_TransactionSetControlNumber": $string(heading.transaction_set_header_ST.transaction_set_control_number_02),
        "segments": [
          {
            "BPR_01": heading.financial_information_BPR.transaction_handling_code_01,
            "BPR_02": $string(heading.financial_information_BPR.total_actual_provider_payment_amount_02) & ".00",
            "BPR_03": heading.financial_information_BPR.credit_or_debit_flag_code_03,
            "BPR_04": heading.financial_information_BPR.payment_method_code_04,
            "BPR_16": $replace(heading.financial_information_BPR.check_issue_or_eft_effective_date_16,"-","")
          },
          {
            "TRN_01": heading.reassociation_trace_number_TRN.trace_type_code_01,
            "TRN_02": heading.reassociation_trace_number_TRN.check_or_eft_trace_number_02,
            "TRN_03": heading.reassociation_trace_number_TRN.payer_identifier_03
          },
          {
            "REF_01": heading.receiver_identification_REF.reference_identification_qualifier_01,
            "REF_02": heading.receiver_identification_REF.receiver_identifier_02
          },
          {
            "DTM_01": heading.production_date_DTM.date_time_qualifier_01,
            "DTM_02": $substring(heading.production_date_DTM.production_date_02, 0, 4) & $substring(heading.production_date_DTM.production_date_02, 5, 2) & $substring(heading.production_date_DTM.production_date_02, 8, 2)
          },
          {
            "N1-1000A_loop": [
              {
                "N1_01": heading.payer_identification_N1_loop.payer_identification_N1.entity_identifier_code_01,
                "N1_02": heading.payer_identification_N1_loop.payer_identification_N1.payer_name_02
              },
              {
                "N3_01": heading.payer_identification_N1_loop.payer_address_N3.payer_address_line_01
              },
              {
                "N4_01": heading.payer_identification_N1_loop.payer_city_state_zip_code_N4.payer_city_name_01,
                "N4_02": heading.payer_identification_N1_loop.payer_city_state_zip_code_N4.payer_state_code_02,
                "N4_03": heading.payer_identification_N1_loop.payer_city_state_zip_code_N4.payer_postal_zone_or_zip_code_03
              },
              {
                "PER_01": heading.payer_identification_N1_loop.payer_business_contact_information_PER.contact_function_code_01,
                "PER_03": heading.payer_identification_N1_loop.payer_business_contact_information_PER.communication_number_qualifier_03,
                "PER_04": heading.payer_identification_N1_loop.payer_business_contact_information_PER.payer_contact_communication_number_04
              },
              {
                "PER_01": heading.payer_identification_N1_loop.payer_technical_contact_information_PER[0].contact_function_code_01,
                "PER_02": heading.payer_identification_N1_loop.payer_technical_contact_information_PER[0].payer_technical_contact_name_02,
                "PER_03": heading.payer_identification_N1_loop.payer_technical_contact_information_PER[0].communication_number_qualifier_03,
                "PER_04": heading.payer_identification_N1_loop.payer_technical_contact_information_PER[0].payer_contact_communication_number_04,
                "PER_05": heading.payer_identification_N1_loop.payer_technical_contact_information_PER[0].communication_number_qualifier_05,
                "PER_06": heading.payer_identification_N1_loop.payer_technical_contact_information_PER[0].payer_technical_contact_communication_number_06
              },
              {
                "PER_01": heading.payer_identification_N1_loop.payer_web_site_PER.contact_function_code_01,
                "PER_03": heading.payer_identification_N1_loop.payer_web_site_PER.communication_number_qualifier_03,
                "PER_04": heading.payer_identification_N1_loop.payer_web_site_PER.communication_number_04
              }
            ]
          },
          {
            "N1-1000B_loop": [
              {
                "N1_01": heading.payee_identification_N1_loop.payee_identification_N1.entity_identifier_code_01,
                "N1_02": heading.payee_identification_N1_loop.payee_identification_N1.payee_name_02,
                "N1_03": heading.payee_identification_N1_loop.payee_identification_N1.identification_code_qualifier_03,
                "N1_04": heading.payee_identification_N1_loop.payee_identification_N1.payee_identification_code_04
              },
              {
                "N3_01": heading.payee_identification_N1_loop.payee_address_N3.payee_address_line_01
              },
              {
                "N4_01": heading.payee_identification_N1_loop.payee_city_state_zip_code_N4.payee_city_name_01,
                "N4_02": heading.payee_identification_N1_loop.payee_city_state_zip_code_N4.payee_state_code_02,
                "N4_03": heading.payee_identification_N1_loop.payee_city_state_zip_code_N4.payee_postal_zone_or_zip_code_03
              },
              {
                "REF_01": heading.payee_identification_N1_loop.payee_additional_identification_REF[0].reference_identification_qualifier_01,
                "REF_02": heading.payee_identification_N1_loop.payee_additional_identification_REF[0].additional_payee_identifier_02
              }
            ]
          },
          {
            "LX-2000_loop": [
              {
                "LX_01": $string(detail.header_number_LX_loop[0].header_number_LX.assigned_number_01)
              },
              {
                "CLP-2100_loop": [detail.header_number_LX_loop[0].claim_payment_information_CLP_loop.{
                  "CLP_01": claim_payment_information_CLP.patient_control_number_01,
                  "CLP_02": claim_payment_information_CLP.claim_status_code_02,
                  "CLP_03": $string(claim_payment_information_CLP.total_claim_charge_amount_03),
                  "CLP_04": $string(claim_payment_information_CLP.claim_payment_amount_04),
                  "CLP_06": claim_payment_information_CLP.claim_filing_indicator_code_06,
                  "CLP_07": claim_payment_information_CLP.payer_claim_control_number_07,
                  "CLP_08": claim_payment_information_CLP.facility_type_code_08,
                  "CLP_09": claim_payment_information_CLP.claim_frequency_code_09},
                  detail.header_number_LX_loop[0].claim_payment_information_CLP_loop.{
                  "NM1_01": patient_name_NM1.entity_identifier_code_01,
                  "NM1_02": patient_name_NM1.entity_type_qualifier_02,
                  "NM1_03": patient_name_NM1.patient_last_name_03,
                  "NM1_04": patient_name_NM1.patient_first_name_04,
                  "NM1_05": patient_name_NM1.patient_middle_name_or_initial_05,
                  "NM1_08": patient_name_NM1.identification_code_qualifier_08,
                  "NM1_09": patient_name_NM1.patient_identifier_09},
                  detail.header_number_LX_loop[0].claim_payment_information_CLP_loop.{
                  "REF_01": other_claim_related_identification_REF[0].reference_identification_qualifier_01,
                  "REF_02": other_claim_related_identification_REF[0].other_claim_related_identifier_02},
                  detail.header_number_LX_loop[0].claim_payment_information_CLP_loop.{
                  "DTM_01": claim_received_date_DTM.date_time_qualifier_01,
                  "DTM_02": $substring(claim_received_date_DTM.date_02, 0, 4) & $substring(claim_received_date_DTM.date_02, 5, 2) & $substring(claim_received_date_DTM.date_02, 8, 2)},
                  detail.header_number_LX_loop[0].claim_payment_information_CLP_loop.{
                  "PER_01": claim_contact_information_PER[0].contact_function_code_01,
                  "PER_02": claim_contact_information_PER[0].claim_contact_name_02,
                  "PER_03": claim_contact_information_PER[0].communication_number_qualifier_03,
                  "PER_04": claim_contact_information_PER[0].claim_contact_communications_number_04},
                  detail.header_number_LX_loop[0].claim_payment_information_CLP_loop.{
                  "AMT_01": claim_supplemental_information_AMT[0].amount_qualifier_code_01,
                  "AMT_02": $string(claim_supplemental_information_AMT[0].claim_supplemental_information_amount_02)},
                  {
                  "SVC-2110_loop":[
                detail.header_number_LX_loop[0].claim_payment_information_CLP_loop.{
                  "NM1_01": patient_name_NM1.entity_identifier_code_01
                  
                  }]
                  }],
                  "SVC-2110_loop": service_payment_information_SVC_loop.{
                    "SVC_01": {
                      "SVC_01_01": service_payment_information_SVC.composite_medical_procedure_identifier_01.product_or_service_id_qualifier_01,
                      "SVC_01_02": service_payment_information_SVC.composite_medical_procedure_identifier_01.adjudicated_procedure_code_02
                    },
                    "SVC_02": service_payment_information_SVC.line_item_charge_amount_02,
                    "SVC_03": service_payment_information_SVC.line_item_provider_payment_amount_03,
                    "SVC_05": service_payment_information_SVC.units_of_service_paid_count_05,
                    "DTM_01": service_date_DTM[0].date_time_qualifier_01,
                    "DTM_02": $substring(service_date_DTM[0].service_date_02, 0, 4) & $substring(service_date_DTM[0].service_date_02, 5, 2) & $substring(service_date_DTM[0].service_date_02, 8, 2),
                    "CAS_01": service_adjustment_CAS[0].claim_adjustment_group_code_01,
                    "CAS_02": service_adjustment_CAS[0].adjustment_reason_code_02,
                    "CAS_03": service_adjustment_CAS[0].adjustment_amount_03,
                    "AMT_01": $exists(service_supplemental_amount_AMT[0]) ? service_supplemental_amount_AMT[0].amount_qualifier_code_01 : undefined,
                    "AMT_02": $exists(service_supplemental_amount_AMT[0]) ? service_supplemental_amount_AMT[0].service_supplemental_amount_02 : undefined
                }
              }
            ]
          }
        ]
      }]
    }]
  }]
}"""

def test_jsonata_835_idets_to_aws():
    import jsonata
    # data = {"example": [{"value": 4}, {"value": 7}, {"value": 13}]}
    # expr = jsonata.Jsonata("$sum(example.value)")
    # result = expr.evaluate(data)
    data = idets835
    expr = jsonata.Jsonata(mapping_835)
    result = expr.evaluate(data)
    js_dict = json.dumps(result)
    root_path = get_root_path()
    file_path = os.path.join(root_path, 'resources/05_835_output_json_aws/after_mapping.json')
    with open(file_path, 'r') as file:
      file_data = json.load(file)  # Parse the JSON file into a dictionary


    # Assert if the loaded dictionary matches the `js_dict`
      assert file_data == result, "The data in the file does not match the generated result."


def test_jsonata_837_aws_to_idets():
  import jsonata
  # data = {"example": [{"value": 4}, {"value": 7}, {"value": 13}]}
  # expr = jsonata.Jsonata("$sum(example.value)")
  # result = expr.evaluate(data)
  data = idets837
  expr = jsonata.Jsonata(mapping_837)
  result = expr.evaluate(data)
  js_dict = json.dumps(result)
  root_path = get_root_path()
  file_path = os.path.join(root_path, 'resources/03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.after_translation_837.json')
  with open(file_path, 'r') as file:
    file_data = json.load(file)  # Parse the JSON file into a dictionary

    # Assert if the loaded dictionary matches the `js_dict`
    assert file_data == result, "The data in the file does not match the generated result."



if __name__ == "__main__":
    pytest.main([__file__])