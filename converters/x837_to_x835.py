from datetime import datetime

from models.EDI835.EDI835_idets import EDI835Idets
from models.EDI837.EDI837_idets import Edi837Idets, CompositeDiagnosisCodePointer
from models.EctonBill.ecton_bill import SecondaryBill
from tests.common_test_utils import read_as_json


def convert_x837_to_x835(x837: Edi837Idets) -> EDI835Idets:
    e835 = read_as_json("resources/f04_835_output_json_idets/X222-COB-payerb.json")
    ecton835 = EDI835Idets.model_validate(e835)
    return ecton835
