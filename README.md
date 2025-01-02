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
   ---reject instead of ack ? 


---

## Missing Components

1. **Important Fields from JSON**
   - Understand the significant fields based on partner settings.
   - Extract and create a `Bill` object including:
     - Patient
     - Provider
     - Origin amount
     - Amount left
     - Due date
     - Other relevant fields to represent a bill.

2. **Field Mapping**
   - Map fields to create a proper `835` for the given `837`.
   - Handle invalid scenarios:
     - Reject instead of acknowledgment?

3. **Secondary Claims**
   - What happens when `x223` is received? 
   - Handle secondary claims (e.g., in clearing house).

4. **Demo Workflow**
   - Input an EDI file.
   - Export `ecton_bill` and `835edi`.
   - Progress: 60%-70%.

5. **SMTP Integration**
   - Add settings for clearing house email communication.

6. **Sample Testing**
   - Add more samples.
   - Test end-to-end workflows.
   - Handle unrecognized or incorrect cases:
     - Invalid versions (e.g., not `822a1`, `823a2`).
     - Non-parsed or non-HIPAA-compliant cases.

---

## Validation Requirements

### Enum Checks
- Validate codes and schema:
  - No referring provider.
  - Single line item with multiple adjustments (codes + percentage or amount).
- Double-check `298`, `299`, `222`, and `223` without version.

### Version-Specific Checks
- Validate `x222a1` and `x223a1`.

---

## Partner Configuration

### Profile Details
- **Profile Name**: `eugen_off`
- **Business Name**: `eugen_part@eugen_part.com`
- **Primary Contact**: `eugen_comp`
- **Primary Phone**: `15558912457`

### Partner (Clearing House) Details
- **Name**: `eugen_part`
- **Email**: `eugen_part@eugen_part.com`

---

## Interchange Header Settings

### ISA Settings
- **ISA 05**: Sender Qualifier - `15` (Options: `01`, `02`, `37`, `AM`, `NR`, `SN`, `ZZ`).
- **ISA 06**: Sender ID - `666666666666666` (15 chars).
- **ISA 07**: Receiver Qualifier - `17` (Options: `01`, `02`, `37`, `AM`, `NR`, `SN`, `ZZ`).
- **ISA 11**: Repetition Separator - `888888888888888` (15 chars).
- **ISA 14**: Acknowledgement Requested - `1` (`0` or `1`).
- **ISA 15**: Usage Indicator - `I` (`I`, `T`, `P`).

---

## Functional Group Settings

### GS Settings
- **GS 02**: Application Sender Code - `0022` (Length: 2-16).
- **GS 03**: Application Receiver Code - `0033` (Length: 2-16).
- **GS 07**: Agency Code - `X` (`X`, `T`).

---

## Additional Details

### Separators
- **Component Separator**: `:`
- **Data Element Separator**: `*`
- **Segment Terminator**: `$`

### Validations
- EDI Validations Enabled: `TRUE`

### Trading Capabilities
- Supports: `835 HIPAA`, `837 HIPAA`

---

## Next Steps
1. **Enhance Field Mapping**: Improve field mapping and validations.
2. **Coherent Example**: Make one example instead of 2 ( one for import one for export )
3. **Fix EctonBill**: Collect feedback (one line item - multiple adjustments with codes and percentage or amount )
4. **Finalize Demo**: Complete and test the demo setup.

5. **Expand Testing**: Include additional scenarios and edge cases.
6. **SMTP Integration**: Configure email settings for clearing house communication.
7. **STEDI DEMO**: Conduct evaluation

8. **Check other files **: x223
9. **Create Enums from schema **: (no referring provider )


----------------------------
focus on : 

mapping 
variants ???
835 from 837 ( check if we have all the data / check what will store in the DB ) 

is claim valid to process ? 
what user can do - > 
   autopay 
   no autopay 
   
-----------------
   835 paid in multiple instalments
   835 won't pay (reject)
   835 paid 
-----------------
-----------------
Questions

what happens when not valid 
what happens when checked -Enable Validation
what is the file next to 999 and how does it look if rejected 
what happens if non secondary claim
how the BUSINESS LOGIC (spider) will look like 
what happens with not recognized / wrong (what percentage) - not secondary/ not 822a1 823a2 / not parsed / not hippa /
more samples 
298 299 double check
222 and 223 without version double check
what happens with not recognized / wrong (what percentage) - not secondary/ not 822a1 823a2 / not parsed / not hippa / 
298 299 double check 
222 and 223 without version double check 

mapping 837 :
---------------

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

    

    

    








