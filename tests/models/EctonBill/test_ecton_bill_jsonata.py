import json
import os
import pytest
import jsonata
from tests.common_test_utils import get_root_path, read_as_json, read_as_str
from mapping.x222 import transform_json_aws837_after_jsonata

# File paths
PAYER_B_JSON = 'resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.json'
AFTER_MAPPING_JSON = 'resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.after_mapping_837.json'
IDETS_837_JSON = 'resources/f02_837_input_json_aws/X222-COB-claim-from-billing-provider-to-payer-b.aws.json'
IDETS_835_JSON = 'resources/f04_835_output_json_idets/idets-multiple-claims.json'
MAPPING_837_JSN = 'resources/f02_837_input_json_aws/x222-837.jsn'
MAPPING_835_JSN = 'resources/f04_835_output_json_idets/x221-835.jsn'
EXPECTED_835_MAPPING = 'resources/f05_835_output_json_aws/idets-multiple-claims.aws.after_mapping.json'


def check_jsonata(input_json_path, jsn_mapping_path, expected_json_path, transform_func=None):
    """
    Generic function to check JSON transformation using JSONata mappings.

    Parameters:
        input_json_path (str): Path to the input JSON file.
        jsn_mapping_path (str): Path to the JSONata mapping file.
        expected_json_path (str): Path to the file containing the expected JSON output.
        transform_func (callable): Optional function to transform the resultant JSON before validation.
    """
    root_path = get_root_path()

    # Read input JSON and JSN mapping
    input_json = read_as_json(input_json_path)
    jsn_mapping = read_as_str(jsn_mapping_path)

    # Apply JSONata mapping
    expr = jsonata.Jsonata(jsn_mapping)
    result = expr.evaluate(input_json)

    # Apply optional transformation
    if transform_func:
        result = transform_func(result)

        # temp_output_path = os.path.join(
        #     root_path,
        #     "resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-c.after_mapping_837c.json"
        # )
        # with open(temp_output_path, "w") as temp_file:
        #     json.dump(result, temp_file, indent=2)
        #
        # assert os.path.exists(temp_output_path), "Failed to write the resulting file."

    # Load the expected JSON file
    expected_path = os.path.join(root_path, expected_json_path)
    with open(expected_path, 'r') as expected_file:
        expected_data = json.load(expected_file)

    # Assert result matches the expected data
    assert result == expected_data, "The data in the file does not match the generated result."


def test_jsonata_835_idets_to_aws():
    check_jsonata(
        input_json_path=IDETS_835_JSON,
        jsn_mapping_path=MAPPING_835_JSN,
        expected_json_path=EXPECTED_835_MAPPING
    )


def test_jsonata_837_aws_to_idets():
    check_jsonata(
        input_json_path=IDETS_837_JSON,
        jsn_mapping_path=MAPPING_837_JSN,
        expected_json_path=AFTER_MAPPING_JSON,
    )


def test_simple_sample837():
    check_jsonata(
        input_json_path='resources/basics-837/jsonata-in.json',
        jsn_mapping_path='resources/basics-837/jsonata-in.mapping.jsn',
        expected_json_path='resources/basics-837/jsonata-in.after_mapping.json',
    )

def test_simple_sample835():
    check_jsonata(
        input_json_path='resources/basic-835/sample-in.json',
        jsn_mapping_path='resources/basic-835/sample.mapping.jsn',
        expected_json_path='resources/basic-835/sample-expected.json',
    )

def test_jsonata_837_aws_to_idets_after_py():
    check_jsonata(
        input_json_path=IDETS_837_JSON,
        jsn_mapping_path=MAPPING_837_JSN,
        expected_json_path=PAYER_B_JSON,
        transform_func=transform_json_aws837_after_jsonata
    )


if __name__ == "__main__":
    pytest.main([__file__])
