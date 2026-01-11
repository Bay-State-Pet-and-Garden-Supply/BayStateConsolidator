from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from supabase import create_client

from baystate_consolidator.core.normalization import (
    normalize_consolidation_result,
    SurvivorshipEngine,
)
from baystate_consolidator.core.taxonomy import TaxonomyService
from baystate_consolidator.services.ocr import OCRService
from baystate_consolidator.models.golden_record import GoldenRecord, FieldMetadata

router = APIRouter()


class ConsolidateRequest(BaseModel):
    job_id: str


def run_consolidation_pipeline(job_id: str):
    try:
        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_KEY", "")
        if not url or not key:
            print("Skipping DB ops: Missing env vars")
            return

        supabase = create_client(url, key)

        # taxonomy_service = TaxonomyService() # unused in stub
        # ocr_service = OCRService() # unused in stub
        survivorship = SurvivorshipEngine()

        print(f"Processing job {job_id}")

        # Stub implementation for pipeline
        # 1. Fetch raw rows
        # rows = supabase.table("products_ingestion").select("*").eq("job_id", job_id).execute()

        # 2. Process
        # for row in rows.data:
        #    ...

    except Exception as e:
        print(f"Pipeline error: {e}")


@router.post("/consolidate")
async def consolidate(request: ConsolidateRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_consolidation_pipeline, request.job_id)
    return {"status": "processing", "job_id": request.job_id}
