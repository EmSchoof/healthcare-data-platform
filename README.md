## Proof of Concept:
##

### Concept:
A healthcare data platform that ingests FHIR-style patient data, transforms it into analytics-ready tables, and exposes metrics for care management.

### Data Structures
#### FHIR-like JSON of Sudo Hospital Patient Data created by ChatGPT consisting of 300 records with the following fields:
```aiignore
resourceType "Patient"
unique id per record
name (given + family)
gender
birthDate
address (US-based)
identifier (mock MRN)
```