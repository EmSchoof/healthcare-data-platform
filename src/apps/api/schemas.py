# import modules
from typing import Any, Optional
from pydantic import BaseModel, Field

# define class elements of each patient instance
class HumanName(BaseModel):
    use: Optional[str] = "official"
    family: Optional[str] = None
    given: list[str] = Field(default_factory=list)

class Address(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None


class Identifier(BaseModel):
    system: Optional[str] = None
    value: Optional[str] = None


class PatientResource(BaseModel):
    resourceType: str = "Patient"
    id: str
    identifier: list[Identifier] = Field(default_factory=list)
    name: list[HumanName] = Field(default_factory=list)
    gender: Optional[str] = None
    birthDate: Optional[str] = None
    address: list[Address] = Field(default_factory=list)


class BundleEntry(BaseModel):
    resource: PatientResource


class SearchBundle(BaseModel):
    resourceType: str = "Bundle"
    type: str = "searchset"
    total: int
    entry: list[BundleEntry] = Field(default_factory=list)


class CapabilityStatement(BaseModel):
    resourceType: str = "CapabilityStatement"
    status: str = "active"
    kind: str = "instance"
    fhirVersion: str = "4.0.1"
    format: list[str] = ["json"]
    rest: list[dict[str, Any]]