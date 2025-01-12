import json
import os

import jsonata
import pytest

from converters.x837_to_ecton_bill import convert_x837_to_ecton_bill
from converters.x837_to_x835 import convert_x837_to_x835
from mapping.x222 import transform_json_aws837_after_jsonata
from mapping.x222_to_aws import transform_json_ecton835_after_jsonata
from models.EDI835.EDI835_idets import load_edi_835
from models.EDI837.EDI837_idets import Edi837Idets
from tests.common_test_utils import (read_as_json, read_as_str, write_as_json)
from utils.json_processor import transform_jsonata

# File paths
PAYER_B_JSON = "resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.json"
AFTER_MAPPING_JSON = "resources/f03_837_input_json_idets/X222-COB-claim-from-billing-provider-to-payer-b.after_mapping_837.json"
IDETS_837_JSON = "resources/f02_837_input_json_aws/X222-COB-claim-from-billing-provider-to-payer-b.aws.json"
IDETS_835_JSON = "resources/f04_835_output_json_idets/idets-multiple-claims.json"
MAPPING_837_JSN = "resources/f02_837_input_json_aws/x222-837.jsn"
MAPPING_835_JSN = "resources/f04_835_output_json_idets/x221-835.jsn"
EXPECTED_835_MAPPING = (
    "resources/f05_835_output_json_aws/idets-multiple-claims.aws.after_mapping.json"
)
EXPECTED_835_MAPPING_AWS = (
    "resources/f05_835_output_json_aws/idets-multiple-claims.aws.expected.json"
)


def check_jsonata(
    input_json_path, jsn_mapping_path, expected_json_path, transform_func=None,
        write_tmp_file:bool=False):
    """
    Generic function to check JSON transformation using JSONata mappings.

    Parameters:
        input_json_path (str): Path to the input JSON file.
        jsn_mapping_path (str): Path to the JSONata mapping file.
        expected_json_path (str): Path to the file containing the expected JSON output.
        transform_func (callable): Optional function to transform the resultant JSON before validation.
        write_tmp_file (bool): Optional function to transform the resultant JSON before validation.
    """
    #root_path = get_root_path()

    # Read input JSON and JSN mapping
    input_json = read_as_json(input_json_path)
    jsn_mapping = read_as_str(jsn_mapping_path)

    # Apply JSONata mapping
    expr = jsonata.Jsonata(jsn_mapping)
    result = expr.evaluate(input_json)

    # Apply optional transformation
    if transform_func:
        result = transform_func(result)
        tmp_tile = input_json_path.replace(".json", ".out-tmp.json")
        write_as_json(result, tmp_tile)
        #assert os.path.exists(tmp_tile), "Failed to write the resulting file."

    # Load the expected JSON file
    expected_data = read_as_json(expected_json_path)

    # Assert result matches the expected data
    assert (
        result == expected_data
    ), "The data in the file does not match the generated result."


def test_jsonata_835_idets_to_aws():
    check_jsonata(
        input_json_path=IDETS_835_JSON,
        jsn_mapping_path=MAPPING_835_JSN,
        expected_json_path=EXPECTED_835_MAPPING,
    )


def test_jsonata_837_aws_to_idets():
    check_jsonata(
        input_json_path=IDETS_837_JSON,
        jsn_mapping_path=MAPPING_837_JSN,
        expected_json_path=AFTER_MAPPING_JSON,
    )


def test_simple_sample837():
    check_jsonata(
        input_json_path="resources/basics-837/jsonata-in.json",
        jsn_mapping_path="resources/basics-837/jsonata-in.mapping.jsn",
        expected_json_path="resources/basics-837/jsonata-in.after_mapping.json",
    )


def test_simple_sample835():
    check_jsonata(
        input_json_path="resources/basic-835/sample-in.json",
        jsn_mapping_path="resources/basic-835/sample.mapping.jsn",
        expected_json_path="resources/basic-835/sample-expected.json",
    )


def test_jsonata_835_idets_to_aws_after_py():
    check_jsonata(
        input_json_path=IDETS_835_JSON,
        jsn_mapping_path=MAPPING_835_JSN,
        expected_json_path=EXPECTED_835_MAPPING_AWS,
        transform_func=transform_json_ecton835_after_jsonata
    )


def test_jsonata_837_aws_to_idets_after_py():
    check_jsonata(
        input_json_path=IDETS_837_JSON,
        jsn_mapping_path=MAPPING_837_JSN,
        expected_json_path=PAYER_B_JSON,
        transform_func=transform_json_aws837_after_jsonata
    )


def test_end2end_jsonata_837_aws_to_idets_after_py_and_convert():
    edi_837_dict = transform_jsonata(IDETS_837_JSON,read_as_str(MAPPING_837_JSN),transform_json_aws837_after_jsonata)
    edi837 = Edi837Idets.model_validate(edi_837_dict)

    ecton_bill = convert_x837_to_ecton_bill(edi837)

    check_835(edi837, 'resources/f04_835_output_json_idets/X222-COB-payerb_paid.json')
    check_835(edi837, 'resources/f04_835_output_json_idets/X222-COB-payerb_not_paid.json', False)


    check_jsonata(
        input_json_path='resources/f04_835_output_json_idets/X222-COB-payerb_not_paid.json',
        jsn_mapping_path=MAPPING_835_JSN,
        expected_json_path='resources/f04_835_output_json_idets/X222-COB-payerb_not_paid.out-mapping.json',
        transform_func=transform_json_ecton835_after_jsonata,
    )

    check_jsonata(
        input_json_path='resources/f04_835_output_json_idets/X222-COB-payerb_paid.json',
        jsn_mapping_path=MAPPING_835_JSN,
        expected_json_path='resources/f04_835_output_json_idets/X222-COB-payerb_paid.out-mapping.json',
        transform_func=transform_json_ecton835_after_jsonata,
        write_tmp_file=True
    )


    pass


def check_835(edi837,expected_file, paid = True):
    edi835_result = convert_x837_to_x835(edi837, paid=paid)
    json_output = 'resources/f04_835_output_json_idets/X222-COB-payerb_paid.out.json'
    write_as_json(edi835_result, '%s' % json_output)
    edi835_expected = read_as_json(expected_file)
    edi835_json_output = read_as_json(json_output)
    # Assert result matches the expected data
    assert (
            edi835_json_output == edi835_expected
    ), "The data in the file does not match the generated result."


if __name__ == "__main__":
    pytest.main([__file__])
