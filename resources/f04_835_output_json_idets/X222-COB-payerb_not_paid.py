cob_not_paid = \
    {
        "heading": {
            "transaction_set_header_ST": {
                "transaction_set_identifier_code_01": "835",
                "transaction_set_control_number_02": 1234
            },
            "financial_information_BPR": {
                "transaction_handling_code_01": "H",  # H = Notification only, no payment
                "total_actual_provider_payment_amount_02": 0,
                "credit_or_debit_flag_code_03": "C",
                "payment_method_code_04": "NON",  # Non-payment
                "check_issue_or_eft_effective_date_16": "2005-10-15"
            },
            "reassociation_trace_number_TRN": {
                "trace_type_code_01": "1",
                "check_or_eft_trace_number_02": "26407789",
                "payer_identifier_03": "1999996666"
            },
            "receiver_identification_REF": {
                "reference_identification_qualifier_01": "EV",
                "receiver_identifier_02": "FAC"
            },
            "production_date_DTM": {
                "date_time_qualifier_01": "405",
                "production_date_02": "2005-10-15"
            },
            "payer_identification_N1_loop": {
                "payer_identification_N1": {
                    "entity_identifier_code_01": "PR",
                    "payer_name_02": "KEY INSURANCE COMPANY"
                },
                "payer_address_N3": {
                    "payer_address_line_01": "4456 SOUTH SHORE BLVD"
                },
                "payer_city_state_zip_code_N4": {
                    "payer_city_name_01": "CHICAGO",
                    "payer_state_code_02": "IL",
                    "payer_postal_zone_or_zip_code_03": "44444"
                }
            },
            "payee_identification_N1_loop": {
                "payee_identification_N1": {
                    "entity_identifier_code_01": "PE",
                    "payee_name_02": "KILDARE",
                    "identification_code_qualifier_03": "XX",
                    "payee_identification_code_04": "1999996666"
                },
                "payee_address_N3": {
                    "payee_address_line_01": "1234 SEAWAY ST"
                },
                "payee_city_state_zip_code_N4": {
                    "payee_city_name_01": "MIAMI",
                    "payee_state_code_02": "FL",
                    "payee_postal_zone_or_zip_code_03": "33111"
                }
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
                                "patient_control_number_01": "26407789",
                                "claim_status_code_02": "4",  # 4 = Denied
                                "total_claim_charge_amount_03": 79.04,
                                "claim_payment_amount_04": 0,
                                "claim_filing_indicator_code_06": "MC",
                                "payer_claim_control_number_07": "CLAIM1234",
                                "facility_type_code_08": "11",
                                "claim_frequency_code_09": "1"
                            },
                            "claim_adjustment_CAS": [
                                {
                                    "claim_adjustment_group_code_01": "PR",  # Patient Responsibility
                                    "adjustment_reason_code_02": "204",  # Service not covered
                                    "adjustment_amount_03": 79.04
                                }
                            ],
                            "patient_name_NM1": {
                                "entity_identifier_code_01": "QC",
                                "entity_type_qualifier_02": "1",
                                "patient_last_name_03": "SMITH",
                                "patient_first_name_04": "TED",
                                "patient_middle_name_or_initial_05": "N",
                                "identification_code_qualifier_08": "MI",
                                "patient_identifier_09": "ABC123456789"
                            },
                            "service_payment_information_SVC_loop": [
                                {
                                    "service_payment_information_SVC": {
                                        "composite_medical_procedure_identifier_01": {
                                            "product_or_service_id_qualifier_01": "HC",
                                            "adjudicated_procedure_code_02": "99213"
                                        },
                                        "line_item_charge_amount_02": 43.00,
                                        "line_item_provider_payment_amount_03": 0,
                                        "units_of_service_paid_count_05": 1
                                    },
                                    "service_adjustment_CAS": [
                                        {
                                            "claim_adjustment_group_code_01": "CO",
                                            "adjustment_reason_code_02": "45",  # Contractual obligation
                                            "adjustment_amount_03": 43.00
                                        }
                                    ],
                                    "service_date_DTM": [
                                        {
                                            "date_time_qualifier_01": "472",
                                            "service_date_02": "2005-10-03"
                                        }
                                    ]
                                },
                                {
                                    "service_payment_information_SVC": {
                                        "composite_medical_procedure_identifier_01": {
                                            "product_or_service_id_qualifier_01": "HC",
                                            "adjudicated_procedure_code_02": "90782"
                                        },
                                        "line_item_charge_amount_02": 15.00,
                                        "line_item_provider_payment_amount_03": 0,
                                        "units_of_service_paid_count_05": 1
                                    },
                                    "service_adjustment_CAS": [
                                        {
                                            "claim_adjustment_group_code_01": "CO",
                                            "adjustment_reason_code_02": "204",  # Not covered
                                            "adjustment_amount_03": 15.00
                                        }
                                    ],
                                    "service_date_DTM": [
                                        {
                                            "date_time_qualifier_01": "472",
                                            "service_date_02": "2005-10-03"
                                        }
                                    ]
                                },
                                {
                                    "service_payment_information_SVC": {
                                        "composite_medical_procedure_identifier_01": {
                                            "product_or_service_id_qualifier_01": "HC",
                                            "adjudicated_procedure_code_02": "J3301"
                                        },
                                        "line_item_charge_amount_02": 21.04,
                                        "line_item_provider_payment_amount_03": 0,
                                        "units_of_service_paid_count_05": 1
                                    },
                                    "service_adjustment_CAS": [
                                        {
                                            "claim_adjustment_group_code_01": "CO",
                                            "adjustment_reason_code_02": "204",  # Not covered
                                            "adjustment_amount_03": 21.04
                                        }
                                    ],
                                    "service_date_DTM": [
                                        {
                                            "date_time_qualifier_01": "472",
                                            "service_date_02": "2005-10-03"
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
                "transaction_segment_count_01": 25,
                "transaction_set_control_number_02": 1234
            }
        }
    }
