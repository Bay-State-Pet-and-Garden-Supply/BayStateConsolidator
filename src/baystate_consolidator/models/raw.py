from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RawScrapedProduct(BaseModel):
    """
    Raw data mirroring the output from BayStateScraper.
    Supports extra fields for flexibility.
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

    model_config = {"extra": "allow"}
