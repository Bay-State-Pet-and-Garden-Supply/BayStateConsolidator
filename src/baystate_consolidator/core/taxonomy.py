import os
from functools import lru_cache
from typing import List, Optional
from supabase import create_client, Client


class TaxonomyService:
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL", "")
        key: str = os.environ.get("SUPABASE_KEY", "")
        if url and key:
            self.supabase: Client = create_client(url, key)
        else:
            self.supabase = None

    @lru_cache(maxsize=1)
    def get_categories(self) -> List[str]:
        if not self.supabase:
            return []
        response = self.supabase.table("categories").select("name").execute()
        return [item["name"] for item in response.data]

    @lru_cache(maxsize=1)
    def get_product_types(self) -> List[str]:
        if not self.supabase:
            return []
        response = self.supabase.table("product_types").select("name").execute()
        return [item["name"] for item in response.data]

    def validate_category(self, value: str, valid_options: List[str]) -> str:
        if value in valid_options:
            return value
        return valid_options[0] if valid_options else value
