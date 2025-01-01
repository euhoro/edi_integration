# edi_integration
edi_integration

file goes to the different steps 

1. edi837-222a1 -> aws-837-json -> idets-837-json -> ectonBill

2. idets-835-json -> aws-835-json

still missing : 


Understand the important fields from the JSON (part from partner settings )
Extract and create a Bill object (patient, provider, origin amount, amount left, due date, and any other field(s) that makes sense to represent a bill)
Map the needed fields to create a proper 835 for the given 837 

ecton_bill_to_835    OR      idets-837-json to ecton_bill
what will happen when x223 received ? secondary claim ? 
demo - put inside an edi file - export ecton_bill and 835edi
do smtp 
do 5tedi demo to see what is missing
more samples !! - default ack - test end to end
what happens with not recognized / wrong (what percentage)









