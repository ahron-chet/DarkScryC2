from ninja import Schema
from darkscryc2server.Models.ModulesSchemas.Collection import CredentialType


class GatherWebCredentials(Schema):
    cred_type: CredentialType