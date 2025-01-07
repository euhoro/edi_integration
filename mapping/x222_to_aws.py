
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



def transform_json_ecton835_after_jsonata(json_data):
    """
        Recursively searches the JSON object for the 'CLP-2100_loop' node, merges elements from
        'abc' into the 'CLP-2100_loop' node, and removes the 'abc' node.

        Parameters:
            json_data (dict | list): The input JSON object or list to process.

        Returns:
            dict | list: The updated JSON structure with 'abc' elements merged and the 'abc' node removed.
        """
    if isinstance(json_data, dict):
        # Check if the current dictionary contains the 'CLP-2100_loop' key
        if 'CLP-2100_loop' in json_data and isinstance(json_data['CLP-2100_loop'], list):
            # for i, l in enumerate(json_data['CLP-2100_loop']):
            #     if len(l)==0:
            #         json_data['CLP-2100_loop'].remove(l)
            for line in json_data['abc']:
                l = {}
                dict1={}
                dict2={}
                dict3={}
                dict4={}
                dict1['SVC_01']={}
                dict2={}
                dict3={}
                dict4={}
                dict1['SVC_01'] =line['SVC-2110_loop']['SVC_01']
                for k in line['SVC-2110_loop']:
                    if k!='SVC_01':
                        if k.split('_')[0]=='SVC':
                            dict1[k]=line['SVC-2110_loop'][k]
                        elif k.split('_')[0]=='DTM':
                            dict2[k]=line['SVC-2110_loop'][k]
                        elif k.split('_')[0]=='CAS':
                            dict3[k]=line['SVC-2110_loop'][k]
                        else:#AMT
                            dict4[k] = line['SVC-2110_loop'][k]
                l['SVC-2110_loop']=[]
                l['SVC-2110_loop'].append(dict1)
                l['SVC-2110_loop'].append(dict2)
                l['SVC-2110_loop'].append(dict3)
                if len(dict4)>0:
                    l['SVC-2110_loop'].append(dict4)
                json_data['CLP-2100_loop'].append(l)

            json_data.pop('abc')
            # for item in clp_2100_list:
            #     if isinstance(item, dict) and 'abc' in item:
            #         # Ensure 'abc' is a list and merge its elements into 'CLP-2100_loop'
            #         abc_elements = item.pop('abc', None)  # Remove 'abc' from the parent node
            #         if isinstance(abc_elements, list):
            #             clp_2100_list.extend(abc_elements)  # Merge 'abc' elements into 'CLP-2100_loop'

        # Recursively process all other keys in the current dictionary
        for key in json_data:
            json_data[key] = transform_json_ecton835_after_jsonata(json_data[key])

    elif isinstance(json_data, list):
        # If the current node is a list, process each element
        for index, item in enumerate(json_data):
            json_data[index] = transform_json_ecton835_after_jsonata(item)

    return json_data

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
