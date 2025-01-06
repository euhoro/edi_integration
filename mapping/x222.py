
import json

def transform_service_line_number_LX_loop(service_lines_raw):
    """
    Transforms the `service_line_number_LX_loop` list to match the desired structure.
    """

    service_lines = [x for x in service_lines_raw if 'assigned_number_01' in x['service_line_number_LX']]
    dtp = [x for x in service_lines_raw if  'date_time_qualifier_01' in x['date_service_date_DTP'] and x['date_service_date_DTP']['date_time_qualifier_01'] is not None ]
    amounts = [x for x in service_lines_raw if  'line_item_charge_amount_02' in x['professional_service_SV1'] and x['professional_service_SV1']['line_item_charge_amount_02'] is not None ]
    ads = [x for x in service_lines_raw if  'line_adjudication_information_SVD_loop' in x]

    for i , l in enumerate(service_lines):
        dic = {}
        l['service_line_number_LX']['assigned_number_01'] = i+1
        l['date_service_date_DTP'] = dtp[i]['date_service_date_DTP']
        l['professional_service_SV1'] = amounts[i]['professional_service_SV1']
        l['line_adjudication_information_SVD_loop'] = ads[i]['line_adjudication_information_SVD_loop']

        for k in l['line_adjudication_information_SVD_loop']:
            if 'other_payer_primary_identifier_01' in k['line_adjudication_information_SVD'] and k['line_adjudication_information_SVD']['other_payer_primary_identifier_01'] is not None:
                if 'line_adjudication_information_SVD_loop' not in dic:
                    dic['line_adjudication_information_SVD_loop'] ={}
                dic['line_adjudication_information_SVD_loop']['line_adjudication_information_SVD'] = k['line_adjudication_information_SVD']

            if 'date_time_qualifier_01' in k['line_check_or_remittance_date_DTP'] and k['line_check_or_remittance_date_DTP']['date_time_qualifier_01'] is not None:
                if 'line_adjudication_information_SVD_loop' not in dic:
                    dic['line_adjudication_information_SVD_loop'] ={}
                dic['line_adjudication_information_SVD_loop']['line_check_or_remittance_date_DTP'] = k['line_check_or_remittance_date_DTP']

            if 'claim_adjustment_group_code_01' in k['line_adjustment_CAS'] and k['line_adjustment_CAS']['claim_adjustment_group_code_01'] is not None:
                if 'line_adjudication_information_SVD_loop' not in dic:
                    dic['line_adjudication_information_SVD_loop'] ={}
                dic['line_adjudication_information_SVD_loop']['line_adjustment_CAS'] = [k['line_adjustment_CAS']]

        l['line_adjudication_information_SVD_loop'] = [dic['line_adjudication_information_SVD_loop']]

    return service_lines


import json

# Known segment names for EDI (add more as needed)
# valid_segments = {
#     "ST", "BHT", "NM1", "PER", "N3", "N4", "REF", "SBR", "DTP", "CLM", "HI", "LX", "SV1", "SVD", "CAS", "AMT", "OI"
# }
#
# def count_valid_segments(data):
#     if isinstance(data, dict):
#         sum_of_valid_elements = 0
#         for key, value in data.items():
#             sum_of_valid_elements += (1 if key.split('_')[0] in valid_segments else 0) + count_valid_segments(value)
#         return sum_of_valid_elements
#     elif isinstance(data, list):
#         return sum(count_valid_segments(item) for item in data)
#     return 0



def transform_json_aws837_after_jsonata(input_json):
    """
    Transforms the input JSON data by restructuring `service_line_number_LX_loop`.
    """
    # Traverse to find and transform `service_line_number_LX_loop`
    for provider in input_json.get("detail", {}).get("billing_provider_hierarchical_level_HL_loop", []):
        for subscriber in provider.get("subscriber_hierarchical_level_HL_loop", []):
            for patient in subscriber.get("patient_hierarchical_level_HL_loop", []):
                for claim in patient.get("claim_information_CLM_loop", []):
                    if "service_line_number_LX_loop" in claim:
                        claim["service_line_number_LX_loop"] = transform_service_line_number_LX_loop(
                            claim["service_line_number_LX_loop"]
                        )
    #count_s = count_valid_segments(input_json)
    input_json['detail']['transaction_set_trailer_SE']['transaction_segment_count_01']=62 #hard coded
    return input_json


# def main():
#     # Read the input JSON file
#     #with open("resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.after_mapping_837b.json", "r") as file:
#     with open(
#             "/resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.after_mapping_837.json", "r") as file:
#         data = json.load(file)
#
#     # Transform the JSON
#     transformed_data = transform_json(data)
#
#     # Write the transformed JSON to a new file
#     with open(
#             "/resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.after_mapping_837c.json", "w") as file:
#         json.dump(transformed_data, file, indent=2)
#
#     print("Transformation completed. Check 'transformed_output.json'.")
#
#
# if __name__ == "__main__":
#     main()
