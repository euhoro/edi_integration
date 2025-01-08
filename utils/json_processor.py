import jsonata

from tests.common_test_utils import read_as_json, read_as_str


# from utils.common_utils import read_as_json, read_as_str


def transform_jsonata(input_json_file:str, mapping:str, transform_func=None) -> dict:
    """
    :param input_json_file: A string representing the file path to the input JSON file.
    :param mapping: A string containing the JSONata mapping that specifies the transformation logic.
    :param transform_func: An optional function that can be applied to the result of the transformation.
    :return: A dictionary containing the result of applying the JSONata transformation, optionally modified by the transform_func.
    """
    # Read input JSON and JSONata mapping
    input_json = read_as_json(input_json_file)
    #mapping = read_as_str(mapping_file)

    # Apply JSONata transformation
    expr = jsonata.Jsonata(mapping)
    result = expr.evaluate(input_json)

    if transform_func:
        result = transform_func(result)

    return result

