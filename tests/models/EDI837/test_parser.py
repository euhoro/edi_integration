import json  # Example for parsing JSON data
import os
import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

from models.EDI837.EDI837_idets import Edi837Idets
from tests.common_test_utils import get_root_path

edi_837_json = """{
  "heading": {
    "transaction_set_header_ST": {
      "transaction_set_identifier_code_01": "EDI837",
      "transaction_set_control_number_02": 2,
      "implementation_guide_version_name_03": "005010X222A1"
    },
    "beginning_of_hierarchical_transaction_BHT": {
      "hierarchical_structure_code_01": "0019",
      "transaction_set_purpose_code_02": "00",
      "originator_application_transaction_identifier_03": "000001142",
      "transaction_set_creation_date_04": "2005-02-14",
      "transaction_set_creation_time_05": "11:51:01",
      "claim_or_encounter_identifier_06": "CH"
    },
    "submitter_name_NM1_loop": {
      "submitter_name_NM1": {
        "entity_identifier_code_01": "41",
        "entity_type_qualifier_02": "2",
        "submitter_last_or_organization_name_03": "SPECIALISTS",
        "identification_code_qualifier_08": "46",
        "submitter_identifier_09": "1111111"
      },
      "submitter_edi_contact_information_PER": [
        {
          "contact_function_code_01": "IC",
          "submitter_contact_name_02": "SUE",
          "communication_number_qualifier_03": "TE",
          "communication_number_04": "8005558888"
        }
      ]
    },
    "receiver_name_NM1_loop": {
      "receiver_name_NM1": {
        "entity_identifier_code_01": "40",
        "entity_type_qualifier_02": "2",
        "receiver_name_03": "MEDICARE PENNSYLVANIA",
        "identification_code_qualifier_08": "46",
        "receiver_primary_identifier_09": "10234"
      }
    }
  },
  "detail": {
    "billing_provider_hierarchical_level_HL_loop": [
      {
        "billing_provider_name_NM1_loop": {
          "billing_provider_name_NM1": {
            "entity_identifier_code_01": "85",
            "entity_type_qualifier_02": "2",
            "billing_provider_last_or_organizational_name_03": "SPECIALISTS",
            "identification_code_qualifier_08": "XX",
            "billing_provider_identifier_09": "0100000090"
          },
          "billing_provider_address_N3": {
            "billing_provider_address_line_01": "5 MAP COURT"
          },
          "billing_provider_city_state_zip_code_N4": {
            "billing_provider_city_name_01": "MAYNE",
            "billing_provider_state_or_province_code_02": "PA",
            "billing_provider_postal_zone_or_zip_code_03": "17111"
          },
          "billing_provider_upin_license_information_REF": [
            {
              "reference_identification_qualifier_01": "1G",
              "billing_provider_license_and_or_upin_information_02": "110101"
            }
          ],
          "billing_provider_tax_identification_REF": {
            "reference_identification_qualifier_01": "EI",
            "billing_provider_tax_identification_number_02": "890123456"
          }
        },
        "subscriber_hierarchical_level_HL_loop": [
          {
            "subscriber_information_SBR": {
              "payer_responsibility_sequence_number_code_01": "S",
              "individual_relationship_code_02": "18",
              "subscriber_group_or_policy_number_03": "MEDICARE",
              "subscriber_group_name_04": "12",
              "claim_filing_indicator_code_09": "MB"
            },
            "subscriber_name_NM1_loop": {
              "subscriber_name_NM1": {
                "entity_identifier_code_01": "IL",
                "entity_type_qualifier_02": "1",
                "subscriber_last_name_03": "MEDYUM",
                "subscriber_first_name_04": "WAYNE",
                "subscriber_middle_name_or_initial_05": "M",
                "identification_code_qualifier_08": "MI",
                "subscriber_primary_identifier_09": "102200221B1"
              },
              "subscriber_address_N3": {
                "subscriber_address_line_01": "1010 THOUSAND OAK LANE"
              },
              "subscriber_city_state_zip_code_N4": {
                "subscriber_city_name_01": "MAYN",
                "subscriber_state_code_02": "PA",
                "subscriber_postal_zone_or_zip_code_03": "17089"
              },
              "subscriber_demographic_information_DMG": {
                "date_time_period_format_qualifier_01": "D8",
                "subscriber_birth_date_02": "19560110",
                "subscriber_gender_code_03": "M"
              }
            },
            "payer_name_NM1_loop": {
              "payer_name_NM1": {
                "entity_identifier_code_01": "PR",
                "entity_type_qualifier_02": "2",
                "payer_name_03": "MEDICARE PENNSYLVANIA",
                "identification_code_qualifier_08": "PI",
                "payer_identifier_09": "10234"
              },
              "payer_address_N3": {
                "payer_address_line_01": "5232 MAYNE AVENUE"
              },
              "payer_city_state_zip_code_N4": {
                "payer_city_name_01": "LYGHT",
                "payer_state_or_province_code_02": "PA",
                "payer_postal_zone_or_zip_code_03": "17009"
              }
            },
            "claim_information_CLM_loop": [
              {
                "claim_information_CLM": {
                  "patient_control_number_01": "101KEN6055",
                  "total_claim_charge_amount_02": 120,
                  "health_care_service_location_information_05": {
                    "place_of_service_code_01": "11",
                    "facility_code_qualifier_02": "B",
                    "claim_frequency_code_03": "1"
                  },
                  "provider_or_supplier_signature_indicator_06": "Y",
                  "assignment_or_plan_participation_code_07": "A",
                  "benefits_assignment_certification_indicator_08": "Y",
                  "release_of_information_code_09": "Y",
                  "patient_signature_source_code_10": "P"
                },
                "health_care_diagnosis_code_HI": {
                  "health_care_code_information_01": {
                    "diagnosis_type_code_01": "BK",
                    "diagnosis_code_02": "71516"
                  },
                  "health_care_code_information_02": {
                    "diagnosis_type_code_01": "BF",
                    "diagnosis_code_02": "71906"
                  }
                },
                "referring_provider_name_NM1_loop": [
                  {
                    "referring_provider_name_NM1": {
                      "entity_identifier_code_01": "DN",
                      "entity_type_qualifier_02": "1",
                      "referring_provider_last_name_03": "BRYHT",
                      "referring_provider_first_name_04": "LEE",
                      "referring_provider_middle_name_or_initial_05": "T"
                    },
                    "referring_provider_secondary_identification_REF": [
                      {
                        "reference_identification_qualifier_01": "1G",
                        "referring_provider_secondary_identifier_02": "B01010"
                      }
                    ]
                  }
                ],
                "rendering_provider_name_NM1_loop": {
                  "rendering_provider_name_NM1": {
                    "entity_identifier_code_01": "82",
                    "entity_type_qualifier_02": "1",
                    "rendering_provider_last_or_organization_name_03": "HENZES",
                    "rendering_provider_first_name_04": "JACK",
                    "identification_code_qualifier_08": "XX",
                    "rendering_provider_identifier_09": "9090909090"
                  },
                  "rendering_provider_specialty_information_PRV": {
                    "provider_code_01": "PE",
                    "reference_identification_qualifier_02": "PXC",
                    "provider_taxonomy_code_03": "207X00000X"
                  },
                  "rendering_provider_secondary_identification_REF": [
                    {
                      "reference_identification_qualifier_01": "G2",
                      "rendering_provider_secondary_identifier_02": "110102CCC"
                    }
                  ]
                },
                "other_subscriber_information_SBR_loop": [
                  {
                    "other_subscriber_information_SBR": {
                      "payer_responsibility_sequence_number_code_01": "P",
                      "individual_relationship_code_02": "01",
                      "other_insured_group_name_04": "COMMERCE",
                      "claim_filing_indicator_code_09": "CI"
                    },
                    "coordination_of_benefits_cob_payer_paid_amount_AMT": {
                      "amount_qualifier_code_01": "D",
                      "payer_paid_amount_02": 80
                    },
                    "coordination_of_benefits_cob_total_non_covered_amount_AMT": {
                      "amount_qualifier_code_01": "A8",
                      "non_covered_charge_amount_02": 15
                    },
                    "other_insurance_coverage_information_OI": {
                      "benefits_assignment_certification_indicator_03": "Y",
                      "patient_signature_source_code_04": "P",
                      "release_of_information_code_06": "Y"
                    },
                    "other_subscriber_name_NM1_loop": {
                      "other_subscriber_name_NM1": {
                        "entity_identifier_code_01": "IL",
                        "entity_type_qualifier_02": "1",
                        "other_insured_last_name_03": "MEDYUM",
                        "other_insured_first_name_04": "CAROL",
                        "identification_code_qualifier_08": "MI",
                        "other_insured_identifier_09": "COM188-404777"
                      },
                      "other_subscriber_address_N3": {
                        "other_subscriber_address_line_01": "PO BOX 45"
                      },
                      "other_subscriber_city_state_zip_code_N4": {
                        "other_subscriber_city_name_01": "MAYN",
                        "other_subscriber_state_or_province_code_02": "PA",
                        "other_subscriber_postal_zone_or_zip_code_03": "17089"
                      }
                    },
                    "other_payer_name_NM1_loop": {
                      "other_payer_name_NM1": {
                        "entity_identifier_code_01": "PR",
                        "entity_type_qualifier_02": "2",
                        "other_payer_organization_name_03": "COMMERCE",
                        "identification_code_qualifier_08": "PI",
                        "other_payer_primary_identifier_09": "59999"
                      }
                    }
                  }
                ],
                "service_line_number_LX_loop": [
                  {
                    "service_line_number_LX": {
                      "assigned_number_01": 1
                    },
                    "professional_service_SV1": {
                      "composite_medical_procedure_identifier_01": {
                        "product_or_service_id_qualifier_01": "HC",
                        "procedure_code_02": "99203",
                        "procedure_modifier_03": "25"
                      },
                      "line_item_charge_amount_02": 120,
                      "unit_or_basis_for_measurement_code_03": "UN",
                      "service_unit_count_04": 1,
                      "composite_diagnosis_code_pointer_07": {
                        "diagnosis_code_pointer_01": 1,
                        "diagnosis_code_pointer_02": 2
                      }
                    },
                    "date_service_date_DTP": {
                      "date_time_qualifier_01": "472",
                      "date_time_period_format_qualifier_02": "D8",
                      "service_date_03": "20050119"
                    },
                    "line_adjudication_information_SVD_loop": [
                      {
                        "line_adjudication_information_SVD": {
                          "other_payer_primary_identifier_01": "59999",
                          "service_line_paid_amount_02": 80,
                          "composite_medical_procedure_identifier_03": {
                            "product_or_service_id_qualifier_01": "HC",
                            "procedure_code_02": "99203",
                            "procedure_modifier_03": "25"
                          },
                          "paid_service_unit_count_05": 1
                        },
                        "line_adjustment_CAS": [
                          {
                            "claim_adjustment_group_code_01": "CO",
                            "adjustment_reason_code_02": "42",
                            "adjustment_amount_03": 25
                          },
                          {
                            "claim_adjustment_group_code_01": "PR",
                            "adjustment_reason_code_02": "2",
                            "adjustment_amount_03": 15
                          }
                        ],
                        "line_check_or_remittance_date_DTP": {
                          "date_time_qualifier_01": "573",
                          "date_time_period_format_qualifier_02": "D8",
                          "adjudication_or_payment_date_03": "20050128"
                        }
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ],
    "transaction_set_trailer_SE": {
      "transaction_segment_count_01": 43,
      "transaction_set_control_number_02": 2
    }
  }
}"""  # Replace with the modified JSON string


class TestDataParsing(unittest.TestCase):
    def test_parse_from_string(self):
        """Test parsing data from a string."""

        # Parsing the JSON into the Python POJO
        import json

        # edi_837_data = EDI837idests.model_validate(edi_837_json)
        edi_837_data = json.loads(edi_837_json)
        #edi_837_data = read_as_json('resources/f02_837_input_json_aws/X222-COB-claim-from-billing-provider-to-payer-b.aws.json')

        # Use the updated EDI837 model to parse the JSON
        edi_837 = Edi837Idets.parse_obj(edi_837_data)

        # Accessing parts of the EDI837
        print(edi_837.heading)
        print(edi_837.detail)

        # self.assertIsInstance(parsed_data, dict)
        # self.assertEqual(parsed_data['name'], 'John Doe')
        # self.assertEqual(parsed_data['age'], 30)
        # self.assertEqual(parsed_data['city'], 'New York')

    def test_parse_from_file(self):
        """Test parsing data from a file."""
        # file_path = os.path.dirname(os.path.abspath(__file__))  #
        root_path = get_root_path()

        file_path = os.path.join(
            str(root_path),
            "resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.json",
        )
        edi_837 = self.load_edi_from_file(file_path)
        # Verify the parsed data matches expected values
        self.assertIsInstance(edi_837, Edi837Idets)
        # self.assertEqual(edi_837.name, "John Doe")
        # self.assertEqual(edi_837.age, 30)
        # self.assertEqual(edi_837.city, "New York")

    def test_parse_edi_837_with_temp_file(self):
        # Create a temporary file and write the edi_837_json string to it
        with tempfile.NamedTemporaryFile(
            mode="w+", delete=True, suffix=".json"
        ) as temp_file:
            temp_file.write(edi_837_json)
            temp_file.seek(0)

            # Read the content of the temporary file and load as JSON
            parsed_data = json.load(temp_file)

            # Validate and parse the JSON content using the EDI837idests model
            try:
                edi_837 = Edi837Idets.parse_obj(parsed_data)
            except ValidationError as e:
                self.fail(f"Failed to parse EDI837 JSON: {e}")

            # Verify the parsed data matches expected values
            self.assertIsInstance(edi_837, Edi837Idets)
            # self.assertEqual(edi_837.name, "John Doe")
            # self.assertEqual(edi_837.age, 30)
            # self.assertEqual(edi_837.city, "New York")

    def load_edi_from_file(self, file_path):
        # Open the same file to read its content and load it as JSON
        with open(file_path, "r") as file:
            parsed_data = json.load(file)

        # Validate and parse the JSON content using the EDI837idests model
        try:
            edi_837 = Edi837Idets.parse_obj(parsed_data)
            return edi_837
        except ValidationError as e:
            self.fail(f"Failed to parse EDI837 JSON: {e}")


if __name__ == "__main__":
    unittest.main()
