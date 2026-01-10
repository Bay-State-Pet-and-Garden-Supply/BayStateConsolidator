import os
from typing import List, Dict, Any
from supabase import create_client, Client


class DatabaseIngestor:
    def __init__(self, url: str = None, key: str = None):
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")
        if not self.url or not self.key:
            raise ValueError("Supabase URL and Key must be provided or set in env vars.")
        self.supabase: Client = create_client(self.url, self.key)

    def fetch_pending_products(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetches products with status 'scraped' and flattens their sources.
        """
        response = (
            self.supabase.table("products_ingestion")
            .select("sku, sources")
            .eq("pipeline_status", "scraped")
            .limit(limit)
            .execute()
        )

        flattened_records = []

        for row in response.data:
            sku = row.get("sku")
            sources = row.get("sources", {})

            if not sources:
                continue

            # Flatten sources: each source becomes a record for deduplication
            for scraper_name, data in sources.items():
                # Merge sku and scraper_name into the data payload
                record = data.copy()
                record["sku"] = sku
                record["scraper_name"] = scraper_name

                # Ensure we have an ID for Splink (composite key)
                record["unique_id"] = f"{sku}_{scraper_name}"

                flattened_records.append(record)

        return flattened_records

    def update_status(self, skus: List[str], status: str):
        """
        Updates the pipeline_status for a batch of SKUs.
        """
        if not skus:
            return

        (
            self.supabase.table("products_ingestion")
            .update({"pipeline_status": status})
            .in_("sku", skus)
            .execute()
        )
