from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class ScrapedData(BaseModel):
    """
    Raw data model mirroring the output from BayStateScraper.
    """

    price: Optional[float] = None
    title: Optional[str] = None
    description: Optional[str] = None
    images: List[str] = Field(default_factory=list)
    availability: Optional[str] = None
    ratings: Optional[float] = None
    reviews_count: Optional[int] = None
    url: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.now)
    scraper_name: str


class ConsolidatedData(BaseModel):
    """
    Final consolidated data model mirroring the BayStateApp expectation.
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
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    source_ids: List[str] = Field(
        default_factory=list, description="IDs/URLs of source records used"
    )
