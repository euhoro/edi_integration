
from typing import List, Optional
from pydantic import BaseModel

class Artifact(BaseModel):
    artifactType: str
    usage: str
    url: str
    sizeBytes: int
    model: str


class SenderIsa(BaseModel):
    qualifier: str
    id: str


class Sender(BaseModel):
    applicationCode: str
    isa: SenderIsa


class ReceiverIsa(BaseModel):
    qualifier: str
    id: str


class Receiver(BaseModel):
    applicationCode: str
    isa: ReceiverIsa


class Transaction(BaseModel):
    controlNumber: str
    transactionSetIdentifier: str


class FunctionalGroup(BaseModel):
    controlNumber: int
    release: str
    date: str
    time: str
    functionalIdentifierCode: str


class Interchange(BaseModel):
    acknowledgmentRequestedCode: str
    controlNumber: int


class Metadata(BaseModel):
    interchange: Interchange
    functionalGroup: FunctionalGroup
    transaction: Transaction
    receiver: Receiver
    sender: Sender


class TransactionSetting(BaseModel):
    guideId: str
    transactionSettingId: str


class X12(BaseModel):
    transactionSetting: TransactionSetting
    metadata: Metadata


class PartnershipParty(BaseModel):
    profileId: str


class Partnership(BaseModel):
    partnershipId: str
    partnershipType: str
    sender: PartnershipParty
    receiver: PartnershipParty


class Detail(BaseModel):
    transactionId: str
    direction: str
    mode: str
    fileExecutionId: str
    processedAt: str
    fragments: Optional[None]
    artifacts: List[Artifact]
    partnership: Partnership
    x12: X12
    connectionId: str


class Event(BaseModel):
    version: str
    id: str
    detail_type: str
    source: str
    account: str
    time: str
    region: str
    resources: List[str]
    detail: Detail


class RootModel(BaseModel):
    event: Event