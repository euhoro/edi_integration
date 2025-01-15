Authorization Information Qualifier
00No Authorization Information Present (No Meaningful Information in I02)
01
Authorization Information
02
Security Information Qualifier
00No Security Information Present (No Meaningful Information in I04)
03
Security Information
04
Interchange ID Qualifier
27Carrier Identification Number as assigned by Health Care Financing Administration (HCFA)
05
Interchange Sender ID
SSSSSS
06
Interchange ID Qualifier
27Carrier Identification Number as assigned by Health Care Financing Administration (HCFA)
07
Interchange Receiver ID
PPPPP
08
Interchange Date
2009-10-06
09
Interchange Time
12:48
10
Repetition Separator
`
11
Interchange Control Version Number
00501Standards Approved for Publication by ASC X12 Procedures Review Board through October 2003
12
Interchange Control Number
000000001
13
Acknowledgment Requested
1Interchange Acknowledgment Requested (TA1)
14
Interchange Usage Indicator
PProduction Data
15
Component Element Separator
:
16

GS
Functional Group Header
Functional Identifier Code
HCHealth Care Claim (837)
01
Application Sender's Code
SSSSSS
02
Application Receiver's Code
PPPPP
03
Date
2009-10-06
04
Time
12:48
05
Group Control Number
3001
06
Responsible Agency Code
XAccredited Standards Committee X12
07
Version / Release / Industry Identifier Code
005010X222A1
08
heading

ST
Transaction Set Header
Transaction Set Identifier Code
837Health Care Claim
01
Transaction Set Control Number
1234
02
Implementation Guide Version Name
005010X222A1
03

BHT
Beginning of Hierarchical Transaction
Hierarchical Structure Code
0019Information Source, Subscriber, Dependent
01
Transaction Set Purpose Code
00Original
02
Originator Application Transaction Identifier
0123
03
Transaction Set Creation Date
2005-10-15
04
Transaction Set Creation Time
10:23
05
Claim or Encounter Identifier
CHChargeable
06

1000A Loop
Submitter Name Loop

NM1
Submitter Name
Entity Identifier Code
41Submitter
01
Entity Type Qualifier
2Non-Person Entity
02
Submitter Last or Organization Name
PREMIER BILLING SERVICE
03
Identification Code Qualifier
46Electronic Transmitter Identification Number (ETIN)
08
Submitter Identifier
12EEER 000TY
09

PER
Submitter EDI Contact Information
Contact Function Code
ICInformation Contact
01
Submitter Contact Name
JERRY
02
Communication Number Qualifier
TETelephone
03
Communication Number
3055552222
04

1000B Loop
Receiver Name Loop

NM1
Receiver Name
Entity Identifier Code
40Receiver
01
Entity Type Qualifier
2Non-Person Entity
02
Receiver Name
GREAT PRAIRIES HEALTH
03
Identification Code Qualifier
46Electronic Transmitter Identification Number (ETIN)
08
Receiver Primary Identifier
567890
09
detail

2000A Loop
Billing Provider Hierarchical Level Loop

2010AA Loop
Billing Provider Name Loop

NM1
Billing Provider Name
Entity Identifier Code
85Billing Provider
01
Entity Type Qualifier
1Person
02
Billing Provider Last or Organizational Name
KILDARE
03
Billing Provider First Name
BEN
04
Identification Code Qualifier
XXCenters for Medicare and Medicaid Services National Provider Identifier
08
Billing Provider Identifier
1999996666
09

N3
Billing Provider Address
Billing Provider Address Line
1234SEAWAY ST
01

N4
Billing Provider City, State, ZIP Code
Billing Provider City Name
MIAMI
01
Billing Provider State or Province Code
FL
02
Billing Provider Postal Zone or ZIP Code
33111
03

REF
Billing Provider Tax Identification
Reference Identification Qualifier
EIEmployer's Identification Number
01
Billing Provider Tax Identification Number
123456789
02

PER
Billing Provider Contact Information
Contact Function Code
ICInformation Contact
01
Billing Provider Contact Name
CONNIE
02
Communication Number Qualifier
TETelephone
03
Communication Number
3055551234
04

2010AB Loop
Pay-to Address Name Loop

NM1
Pay-to Address Name
Entity Identifier Code
87Pay-to Provider
01
Entity Type Qualifier
2Non-Person Entity
02

N3
Pay-to Address - ADDRESS
Pay-To Address Line
2345
01
Pay-To Address Line
OCEAN BLVD
02

N4
Pay-To Address City, State, ZIP Code
Pay-to Address City Name
MIAMI
01
Pay-to Address State Code
FL
02
Pay-to Address Postal Zone or ZIP Code
3111
03

2000B Loop
Subscriber Hierarchical Level Loop

SBR
Subscriber Information
Payer Responsibility Sequence Number Code
SSecondary
01
Claim Filing Indicator Code
CICommercial Insurance Co.
09

2010BA Loop
Subscriber Name Loop

NM1
Subscriber Name
Entity Identifier Code
ILInsured or Subscriber
01
Entity Type Qualifier
1Person
02
Subscriber Last Name
SMITH
03
Subscriber First Name
JACK
04
Identification Code Qualifier
MIMember Identification Number
08
Subscriber Primary Identifier
222334444
09

DMG
Subscriber Demographic Information
Date Time Period Format Qualifier
D8Date Expressed in Format CCYYMMDD
01
Subscriber Birth Date
19431022
02
Subscriber Gender Code
MMale
03

2010BB Loop
Payer Name Loop

NM1
Payer Name
Entity Identifier Code
PRPayer
01
Entity Type Qualifier
2Non-Person Entity
02
Payer Name
GREAT PRAIRIES HEALTH
03
Identification Code Qualifier
PIPayor Identification
08
Payer Identifier
567890
09

N3
Payer Address
Payer Address Line
4456 SOUTH SHORE BLVD
01

N4
Payer City, State, ZIP Code
Payer City Name
CHICAGO
01
Payer State or Province Code
IL
02
Payer Postal Zone or ZIP Code
44444
03

REF
Billing Provider Secondary Identification
Reference Identification Qualifier
G2Provider Commercial Number
01
Billing Provider Secondary Identifier
567890
02

2000C Loop
Patient Hierarchical Level Loop

PAT
Patient Information
Individual Relationship Code
19Child
01

2010CA Loop
Patient Name Loop

NM1
Patient Name
Entity Identifier Code
QCPatient
01
Entity Type Qualifier
1Person
02
Patient Last Name
SMITH
03
Patient First Name
TED
04

N3
Patient Address
Patient Address Line
236 N MAIN ST
01

N4
Patient City, State, ZIP Code
Patient City Name
MIAMI
01
Patient State Code
FL
02
Patient Postal Zone or ZIP Code
33413
03

DMG
Patient Demographic Information
Date Time Period Format Qualifier
D8Date Expressed in Format CCYYMMDD
01
Patient Birth Date
19730501
02
Patient Gender Code
MMale
03

2300 Loop
Claim Information Loop

CLM
Claim Information
Patient Control Number
26407789
01
Total Claim Charge Amount
79.04
02

C023
Health Care Service Location Information
Place of Service Code
11
01
Facility Code Qualifier
BPlace of Service Codes for Professional or Dental Services
02
Claim Frequency Code
1
03
Provider or Supplier Signature Indicator
YYes
06
Assignment or Plan Participation Code
AAssigned
07
Benefits Assignment Certification Indicator
YYes
08
Release of Information Code
IInformed Consent to Release Medical Information for Conditions or Diagnoses Regulated by Federal Statutes
09

HI
Health Care Diagnosis Code

C022
Health Care Code Information
Diagnosis Type Code
BKInternational Classification of Diseases Clinical Modification (ICD-9-CM) Principal Diagnosis
01
Diagnosis Code
4779
02

C022
Health Care Code Information
Diagnosis Type Code
BFInternational Classification of Diseases Clinical Modification (ICD-9-CM) Diagnosis
01
Diagnosis Code
2724
02

C022
Health Care Code Information
Diagnosis Type Code
BFInternational Classification of Diseases Clinical Modification (ICD-9-CM) Diagnosis
01
Diagnosis Code
2780
02

C022
Health Care Code Information
Diagnosis Type Code
BFInternational Classification of Diseases Clinical Modification (ICD-9-CM) Diagnosis
01
Diagnosis Code
53081
02

2310B Loop
Rendering Provider Name Loop

NM1
Rendering Provider Name
Entity Identifier Code
82Rendering Provider
01
Entity Type Qualifier
1Person
02
Rendering Provider Last or Organization Name
KILDARE
03
Rendering Provider First Name
BEN
04
Identification Code Qualifier
XXCenters for Medicare and Medicaid Services National Provider Identifier
08
Rendering Provider Identifier
1999996666
09

PRV
Rendering Provider Specialty Information
Provider Code
PEPerforming
01
Reference Identification Qualifier
PXCHealth Care Provider Taxonomy Code
02
Provider Taxonomy Code
204C00000X
03

REF
Rendering Provider Secondary Identification
Reference Identification Qualifier
G2Provider Commercial Number
01
Rendering Provider Secondary Identifier
88877
02

2310C Loop
Service Facility Location Name Loop

NM1
Service Facility Location Name
Entity Identifier Code
77Service Location
01
Entity Type Qualifier
2Non-Person Entity
02
Laboratory or Facility Name
KILDARE ASSOCIATES
03
Identification Code Qualifier
XXCenters for Medicare and Medicaid Services National Provider Identifier
08
Laboratory or Facility Primary Identifier
1581234567
09

N3
Service Facility Location Address
Laboratory or Facility Address Line
2345 OCEAN BLVD
01

N4
Service Facility Location City, State, ZIP Code
Laboratory or Facility City Name
MIAMI
01
Laboratory or Facility State or Province Code
FL
02
Laboratory or Facility Postal Zone or ZIP Code
33111
03

2320 Loop
Other Subscriber Information Loop

SBR
Other Subscriber Information
Payer Responsibility Sequence Number Code
PPrimary
01
Individual Relationship Code
01Spouse
02
Claim Filing Indicator Code
CICommercial Insurance Co.
09

CAS
Claim Level Adjustments
Claim Adjustment Group Code
PRPatient Responsibility
01
Adjustment Reason Code
1
02
Adjustment Amount
21.89
03
Adjustment Reason Code
2
05
Adjustment Amount
15
06

AMT
Coordination of Benefits (COB) Payer Paid Amount
Amount Qualifier Code
DPayor Amount Paid
01
Payer Paid Amount
39.15
02

AMT
Remaining Patient Liability
Amount Qualifier Code
EAFAmount Owed
01
Remaining Patient Liability
36.89
02

OI
Other Insurance Coverage Information
Benefits Assignment Certification Indicator
YYes
03
Patient Signature Source Code
PSignature generated by provider because the patient was not physically present for services
04
Release of Information Code
YYes, Provider has a Signed Statement Permitting Release of Medical Billing Data Related to a Claim
06

2330A Loop
Other Subscriber Name Loop

NM1
Other Subscriber Name
Entity Identifier Code
ILInsured or Subscriber
01
Entity Type Qualifier
1Person
02
Other Insured Last Name
SMITH
03
Other Insured First Name
JANE
04
Identification Code Qualifier
MIMember Identification Number
08
Other Insured Identifier
JS00111223333
09

N3
Other Subscriber Address
Other Subscriber Address Line
236 N MAIN ST
01

N4
Other Subscriber City, State, ZIP Code
Other Subscriber City Name
MIAMI
01
Other Subscriber State or Province Code
FL
02
Other Subscriber Postal Zone or ZIP Code
33111
03

2330B Loop
Other Payer Name Loop

NM1
Other Payer Name
Entity Identifier Code
PRPayer
01
Entity Type Qualifier
2Non-Person Entity
02
Other Payer Organization Name
KEY INSURANCE COMPANY
03
Identification Code Qualifier
PIPayor Identification
08
Other Payer Primary Identifier
999996666
09

2400 Loop
Service Line Number Loop

LX
Service Line Number
Assigned Number
1
01

SV1
Professional Service

C003
Composite Medical Procedure Identifier
Product or Service ID Qualifier
HCHealth Care Financing Administration Common Procedural Coding System (HCPCS) Codes
01
Procedure Code
99213
02
Line Item Charge Amount
43
02
Unit or Basis for Measurement Code
UNUnit
03
Service Unit Count
1
04

C004
Composite Diagnosis Code Pointer
Diagnosis Code Pointer
1
01
Diagnosis Code Pointer
2
02
Diagnosis Code Pointer
3
03
Diagnosis Code Pointer
4
04

DTP
Date - Service Date
Date Time Qualifier
472Service
01
Date Time Period Format Qualifier
D8Date Expressed in Format CCYYMMDD
02
Service Date
20051003
03

2430 Loop
Line Adjudication Information Loop

SVD
Line Adjudication Information
Other Payer Primary Identifier
999996666
01
Service Line Paid Amount
40
02

C003
Composite Medical Procedure Identifier
Product or Service ID Qualifier
HCHealth Care Financing Administration Common Procedural Coding System (HCPCS) Codes
01
Procedure Code
99213
02
Paid Service Unit Count
1
05

CAS
Line Adjustment
Claim Adjustment Group Code
COContractual Obligations
01
Adjustment Reason Code
42
02
Adjustment Amount
3
03

DTP
Line Check or Remittance Date
Date Time Qualifier
573Date Claim Paid
01
Date Time Period Format Qualifier
D8Date Expressed in Format CCYYMMDD
02
Adjudication or Payment Date
20051015
03

LX
Service Line Number
Assigned Number
2
01

SV1
Professional Service

C003
Composite Medical Procedure Identifier
Product or Service ID Qualifier
HCHealth Care Financing Administration Common Procedural Coding System (HCPCS) Codes
01
Procedure Code
90782
02
Line Item Charge Amount
15
02
Unit or Basis for Measurement Code
UNUnit
03
Service Unit Count
1
04

C004
Composite Diagnosis Code Pointer
Diagnosis Code Pointer
1
01
Diagnosis Code Pointer
2
02

DTP
Date - Service Date
Date Time Qualifier
472Service
01
Date Time Period Format Qualifier
D8Date Expressed in Format CCYYMMDD
02
Service Date
20051003
03

2430 Loop
Line Adjudication Information Loop

SVD
Line Adjudication Information
Other Payer Primary Identifier
999996666
01
Service Line Paid Amount
15
02

C003
Composite Medical Procedure Identifier
Product or Service ID Qualifier
HCHealth Care Financing Administration Common Procedural Coding System (HCPCS) Codes
01
Procedure Code
90782
02
Paid Service Unit Count
1
05

DTP
Line Check or Remittance Date
Date Time Qualifier
573Date Claim Paid
01
Date Time Period Format Qualifier
D8Date Expressed in Format CCYYMMDD
02
Adjudication or Payment Date
20051015
03

LX
Service Line Number
Assigned Number
3
01

SV1
Professional Service

C003
Composite Medical Procedure Identifier
Product or Service ID Qualifier
HCHealth Care Financing Administration Common Procedural Coding System (HCPCS) Codes
01
Procedure Code
J3301
02
Line Item Charge Amount
21.04
02
Unit or Basis for Measurement Code
UNUnit
03
Service Unit Count
1
04

C004
Composite Diagnosis Code Pointer
Diagnosis Code Pointer
1
01
Diagnosis Code Pointer
2
02

DTP
Date - Service Date
Date Time Qualifier
472Service
01
Date Time Period Format Qualifier
D8Date Expressed in Format CCYYMMDD
02
Service Date
20051003
03

2430 Loop
Line Adjudication Information Loop

SVD
Line Adjudication Information
Other Payer Primary Identifier
999996666
01
Service Line Paid Amount
21.04
02

C003
Composite Medical Procedure Identifier
Product or Service ID Qualifier
HCHealth Care Financing Administration Common Procedural Coding System (HCPCS) Codes
01
Procedure Code
J3301
02
Paid Service Unit Count
1
05

DTP
Line Check or Remittance Date
Date Time Qualifier
573Date Claim Paid
01
Date Time Period Format Qualifier
D8Date Expressed in Format CCYYMMDD
02
Adjudication or Payment Date
20051015
03

SE
Transaction Set Trailer
Transaction Segment Count
62
01
Transaction Set Control Number
1234
02

GE
Functional Group Trailer
Number of Transaction Sets Included
1
01
Group Control Number
3001
02

IEA
Interchange Control Trailer
Number of Included Functional Groups
1
01
Interchange Control Number
000000001
02
X12 HIPAA 837 Health Care Claim: Professional (X222A1) - Stedi EDI Inspector