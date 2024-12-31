import json
import os.path

import pytest
from datetime import date
from decimal import Decimal
from typing import Dict, Any

from models.EctonBill.ecton_bill import SecondaryBill, Address, Provider, Patient, ServiceLine
from tests.common_test_utils import get_root_path

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

mapping = """{
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

def test_jsonata():
    import jsonata
    # data = {"example": [{"value": 4}, {"value": 7}, {"value": 13}]}
    # expr = jsonata.Jsonata("$sum(example.value)")
    # result = expr.evaluate(data)
    data = idets835
    expr = jsonata.Jsonata(mapping)
    result = expr.evaluate(data)
    js_dict = json.dumps(result)
    root_path = get_root_path()
    file_path = os.path.join(root_path, 'resources/04_835_output_aws_json/after_mapping.json')
    with open(file_path, 'r') as file:
      file_data = json.load(file)  # Parse the JSON file into a dictionary


    # Assert if the loaded dictionary matches the `js_dict`
      assert file_data == result, "The data in the file does not match the generated result."



if __name__ == "__main__":
    pytest.main([__file__])