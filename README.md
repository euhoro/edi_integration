# EDI Integration

## Overview

This project focuses on integrating EDI (Electronic Data Interchange) processes, specifically for handling `837` and `835` transactions. The workflow involves multiple processing steps, field mapping, and validations to ensure seamless integration with clearing houses.

---

## Workflow Steps

### Step 1: 837 Processing
- `edi837-222a1` -> `aws-837-json` -> `idets-837-json` -> `ectonBill`

### Step 2: 835 Processing
- `idets-835-json` -> `aws-835-json` -  `edi835-222a1`

---


Understand the important fields from the JSON (part from partner settings )
   documentation/stedi-X12-HIPAA-837-Health-Care-Claim-Professional-(X222A1).json

Extract and create a Bill object (patient, provider, origin amount, amount left, due date, and any other field(s) that makes sense to represent a bill)
   models/EctonBill/ecton_bill.py

Map the needed fields to create a proper 835 for the given 837 ( 100 %)
   - TBD
   ---what happens when not valid 
   ---rejecct instead of ack ? 

ecton_bill_to_835    OR      idets-837-json to ecton_bill
what will happen when x223 received ? secondary claim ? ( maybe in clearing house)

demo - put inside an edi file - export ecton_bill and 835edi
60% - 70%

do smtp ( clearing house settings )

do 5tedi demo to see what is missing ????

more samples !! - default ack - test end to end 
what happens with not recognized / wrong (what percentage) - not secondary/ not 822a1 823a2 / not parsed / not hippa / 


ENUM FROM CODES AND SCHEMA
(no reffering provider )
(one line item - multiple adjustments with codes and percentage or amount )

298 299 double check 

222 and 223 without version double check 

x222a1 x222a1 double checking 

profile_name                    :   eugen_off
business_name                   :   eugen_part@eugen_part.com
primary_contact_name            :   eugen_comp
primary_phone                   :   15558912457

    partner (clearning house)   :   eugen_part
    name                        :   eugen_part@eugen_part.com
    email                       :   eugen_part@eugen_part.com
    
            INTERCHANGE HEADER

    ISA 05 - Sender Qualifier           :   15 ( 01, 02, 37, AM , NR , SN ZZ )  ( no 05) 
    ISA 06 - Sender ID                  :   666666666666666 ( 15 chars ) 
    ISA 07 - Receiver Qualifier         :   17 ( 01, 02, 37, AM , NR , SN ZZ )  ( no 05) 
    ISA 11 - Repetition Separator       :   888888888888888 ( 15 chars ) 
    ISA 14 - Acknowledgement Requested  :   1 ( 0 OR 1 )
    ISA 15 - Usage Indicator            :   I ( I T P )
                
            FUNCTIONAL
    GS 02 - Application Sender Code     :   0022 (Application Sender must have length greater than or equal to 2 but less than 16.)
    GS 03 - Application Receiver Code   :   0033 (Application Receiver must have length greater than or equal to 2 but less than 16.)                                :   
    GS 07 - Agency Code                 :   X ( X T ) 

    Component separator                 :  :
    Data Element Separator              :  *
    Segment terminator                  : $

    validations edi                     : TRUE
    
        trading capabitilies 835hippa / 837hippa

    

    

    








