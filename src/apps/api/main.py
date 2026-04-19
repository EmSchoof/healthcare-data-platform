# import modules to connect and process DEMO FHIR data into Snowflakw DB
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Response, status
from src.apps.api.schemas import CapabilityStatement, PatientResource, SearchBundle
from src.apps.api.snowflake_service import create_patient, get_patient_by_id, search_patients
from src.apps.ingestion.ingest_fhir import insert_raw_fhir_patients

@asynccontextmanager
async def lifespan(app: FastAPI):
    # verify table exists with data in snowflake before workflow
    insert_raw_fhir_patients("src/data/sample_fhir.json")
    print("Snowflake table ensured.")
    yield
    print("Shutting down...")

# Create Mini App
app = FastAPI(title="Healthcare Data Platform FHIR Demo API",
              lifespan=lifespan)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/metadata", response_model=CapabilityStatement)
def metadata() -> CapabilityStatement:
    return CapabilityStatement(
        rest=[
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [
                            {"code": "read"},
                            {"code": "search-type"},
                            {"code": "create"},
                        ],
                    }
                ],
            }
        ]
    )


@app.get("/Patient/{patient_id}", response_model=PatientResource)
def read_patient(patient_id: str) -> PatientResource:
    patient = get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return PatientResource(**patient)


@app.get("/Patient", response_model=SearchBundle)
def search_patient(
    identifier: str | None = Query(default=None),
    family: str | None = Query(default=None),
) -> SearchBundle:
    patients = search_patients(identifier=identifier, family=family)
    return SearchBundle(
        total=len(patients),
        entry=[{"resource": p} for p in patients],
    )


@app.post("/Patient", response_model=PatientResource, status_code=status.HTTP_201_CREATED)
def post_patient(patient: PatientResource, response: Response) -> PatientResource:
    created = create_patient(patient.model_dump())
    response.headers["Location"] = f"/Patient/{created['id']}"
    return PatientResource(**created)