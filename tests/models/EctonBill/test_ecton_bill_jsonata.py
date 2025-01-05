import json
import os.path

import pytest
import jsonata
from tests.common_test_utils import get_root_path, read_as_json, read_as_str

idets837= read_as_json('resources/f02_837_input_json_aws/X222-COB-claim-from-billing-provider-to-payer-b.aws.json')
idets835 = read_as_json('resources/f04_835_output_json_idets/idets-multiple-claims.json')

#mapping_837 = read_as_str('resources/mappings/x222-837.jsn')
mapping_837 = read_as_str('resources/f02_837_input_json_aws/x222-837.jsn')
mapping_835 = read_as_str('resources/f04_835_output_json_idets/x221-835.jsn')

def test_jsonata_835_idets_to_aws():

    expr = jsonata.Jsonata(mapping_835)
    result = expr.evaluate(idets835)
    #js_dict = json.dumps(result)

    file_data = read_as_json('resources/f05_835_output_json_aws/idets-multiple-claims.aws.after_mapping.json')

    # Assert if the loaded dictionary matches the `js_dict`
    assert file_data == result, "The data in the file does not match the generated result."


def test_jsonata_837_aws_to_idets():
  import jsonata
  data = idets837
  expr = jsonata.Jsonata(mapping_837)
  result = expr.evaluate(data)
  #js_dict = json.dumps(result)
  root_path = get_root_path()
  file_path = os.path.join(root_path, 'resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.after_mapping_837.json')
  with open(file_path, 'r') as file:
    file_data = json.load(file)  # Parse the JSON file into a dictionary

    # Assert if the loaded dictionary matches the `js_dict`
    assert file_data == result, "The data in the file does not match the generated result."



if __name__ == "__main__":
    pytest.main([__file__])