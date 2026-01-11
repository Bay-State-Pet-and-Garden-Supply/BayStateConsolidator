from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FieldMetadata(BaseModel):
    """
    Metadata for a single field in the golden record.
    Tracks where the value came from and how confident we are.
    """

    value: Any
    source: str  # e.g. "scraper:amazon", "excel", "ocr", "manual"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)


class GoldenRecord(BaseModel):
    """
    The Perfect Model (Golden Record).
    """

    sku: str
    name: str
    description: Optional[str] = None
    price: float
    brand: Optional[str] = None
    category: Optional[str] = None
    product_type: Optional[str] = None
    weight: Optional[str] = None
    images: List[str] = Field(default_factory=list)

    # Special Source of Truth
    excel_price: Optional[float] = None

    # Lineage Tracking
    # Maps field_name -> FieldMetadata
    consolidation_metadata: Dict[str, FieldMetadata] = Field(default_factory=dict)

    model_config = {"extra": "ignore"}
