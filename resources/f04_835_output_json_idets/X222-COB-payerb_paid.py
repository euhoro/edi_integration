cob_paid = \
    {
        "heading": {
            "transaction_set_header_ST": {
                "transaction_set_identifier_code_01": "835",  # Transaction type: 835 = Payment/Advice
                "transaction_set_control_number_02": 1234  # Unique transaction identifier
            },
            "financial_information_BPR": {
                "transaction_handling_code_01": "I",  # I = Remittance info only
                "total_actual_provider_payment_amount_02": 39.15,  # Total payment to provider
                "credit_or_debit_flag_code_03": "C",  # C = Credit
                "payment_method_code_04": "CHK",  # CHK = Check payment
                "check_issue_or_eft_effective_date_16": "2005-10-15"  # Date payment issued
            },
            "reassociation_trace_number_TRN": {
                "trace_type_code_01": "1",  # 1 = Transaction trace number
                "check_or_eft_trace_number_02": "26407789",  # Trace/check number
                "payer_identifier_03": "999996666"  # Payer's unique identifier
            },
            "receiver_identification_REF": {
                "reference_identification_qualifier_01": "EV",  # EV = Event code
                "receiver_identifier_02": "FAC"  # Facility identifier
            },
            "production_date_DTM": {
                "date_time_qualifier_01": "405",  # 405 = Production date
                "production_date_02": "2005-10-15"  # Date of remittance creation
            },
            "payer_identification_N1_loop": {
                "payer_identification_N1": {
                    "entity_identifier_code_01": "PR",  # PR = Payer
                    "payer_name_02": "KEY INSURANCE COMPANY"  # Name of payer
                },
                "payer_address_N3": {
                    "payer_address_line_01": "4456 SOUTH SHORE BLVD"  # Payer's address
                },
                "payer_city_state_zip_code_N4": {
                    "payer_city_name_01": "CHICAGO",  # City
                    "payer_state_code_02": "IL",  # State
                    "payer_postal_zone_or_zip_code_03": "44444"  # ZIP Code
                },
                "payer_technical_contact_information_PER": [
                    {
                        "contact_function_code_01": "BL",  # BL = Billing contact
                        "payer_technical_contact_name_02": "EDI",  # Contact name
                        "communication_number_qualifier_03": "TE",  # TE = Telephone
                        "payer_contact_communication_number_04": "8005551212",  # Phone number
                        "communication_number_qualifier_05": "EM",  # EM = Email
                        "payer_technical_contact_communication_number_06": "EDI.SUPPORT@ANYPAYER.COM"  # Email
                    }
                ],
                "payer_web_site_PER": {
                    "contact_function_code_01": "IC",  # IC = Information contact
                    "communication_number_qualifier_03": "UR",  # UR = URL
                    "communication_number_04": "WWW.ANYPAYER.COM"  # Payer's website
                },
                "payer_business_contact_information_PER": {
                    "contact_function_code_01": "CX",  # CX = Customer service
                    "communication_number_qualifier_03": "TE",  # TE = Telephone
                    "payer_contact_communication_number_04": "8661112222"  # Customer service number
                }
            },
            "payee_identification_N1_loop": {
                "payee_identification_N1": {
                    "entity_identifier_code_01": "PE",  # PE = Payee
                    "payee_name_02": "KILDARE",  # Payee's name
                    "identification_code_qualifier_03": "XX",  # XX = NPI (National Provider Identifier)
                    "payee_identification_code_04": "1999996666"  # Payee's NPI
                },
                "payee_address_N3": {
                    "payee_address_line_01": "1234 SEAWAY ST"  # Payee's address
                },
                "payee_city_state_zip_code_N4": {
                    "payee_city_name_01": "MIAMI",  # City
                    "payee_state_code_02": "FL",  # State
                    "payee_postal_zone_or_zip_code_03": "33111"  # ZIP Code
                },
                "payee_additional_identification_REF": [
                    {
                        "reference_identification_qualifier_01": "EI",  # EI = Employer ID
                        "additional_payee_identifier_02": "123456789"  # Employer ID number
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
                                "patient_control_number_01": "26407789",  # Patient's account number
                                "claim_status_code_02": "1",  # 1 = Processed as primary claim
                                "total_claim_charge_amount_03": 79.04,  # Original charge amount
                                "claim_payment_amount_04": 39.15,  # Paid amount
                                "claim_filing_indicator_code_06": "MC",  # MC = Medicaid
                                "payer_claim_control_number_07": "CLAIM1234",  # Payer's claim ID
                                "facility_type_code_08": "11",  # Facility code for the service
                                "claim_frequency_code_09": "1"  # 1 = Original claim
                            },
                            "claim_adjustment_CAS": [
                                {
                                    "claim_adjustment_group_code_01": "PR",  # PR = Patient Responsibility
                                    "adjustment_reason_code_02": "1",  # Deductible
                                    "adjustment_amount_03": 21.89  # Deductible amount
                                },
                                {
                                    "claim_adjustment_group_code_01": "CO",  # CO = Contractual Obligation
                                    "adjustment_reason_code_02": "2",  # Coinsurance
                                    "adjustment_amount_03": 15.00  # Coinsurance amount
                                }
                            ],
                            "patient_name_NM1": {
                                "entity_identifier_code_01": "QC",  # QC = Patient
                                "entity_type_qualifier_02": "1",  # 1 = Person
                                "patient_last_name_03": "SMITH",  # Last name
                                "patient_first_name_04": "TED",  # First name
                                "patient_middle_name_or_initial_05": "N",  # Middle initial
                                "identification_code_qualifier_08": "MI",  # MI = Member ID
                                "patient_identifier_09": "ABC123456789"  # Member's ID
                            },
                            "service_payment_information_SVC_loop": [
                                {
                                    "service_payment_information_SVC": {
                                        "composite_medical_procedure_identifier_01": {
                                            "product_or_service_id_qualifier_01": "HC",
                                            # HC = Healthcare procedure code
                                            "adjudicated_procedure_code_02": "99213"  # Procedure code
                                        },
                                        "line_item_charge_amount_02": 43.00,  # Charge for the service
                                        "line_item_provider_payment_amount_03": 40.00,  # Paid amount for the service
                                        "units_of_service_paid_count_05": 1  # Number of units
                                    },
                                    "service_date_DTM": [
                                        {
                                            "date_time_qualifier_01": "472",  # 472 = Service date
                                            "service_date_02": "2005-10-03"  # Date of service
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
                "transaction_segment_count_01": 33,  # Total number of segments
                "transaction_set_control_number_02": 1234  # Matches the control number in ST
            }
        }
    }
