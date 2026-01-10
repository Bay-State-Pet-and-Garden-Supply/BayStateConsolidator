import logging
from typing import List, Dict, Any
from baystate_consolidator.utils.database import DatabaseIngestor
from baystate_consolidator.pipelines.dedupe import DeduplicationPipeline
from baystate_consolidator.normalizers.price import normalize_price
from baystate_consolidator.normalizers.text import normalize_text, normalize_weight

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("BayStateConsolidator")


def run_consolidation(limit: int = 100):
    """
    Main execution flow:
    1. Ingest Pending Data
    2. Normalize
    3. Deduplicate
    4. (Future) Consolidate & Push
    """
    try:
        # 1. Ingest
        logger.info("Connecting to Supabase...")
        # Note: Ensure SUPABASE_URL and SUPABASE_KEY are set in env
        db = DatabaseIngestor()

        logger.info(f"Fetching up to {limit} pending records...")
        raw_data = db.fetch_pending_products(limit=limit)

        if not raw_data:
            logger.info("No pending products found.")
            return

        logger.info(f"Fetched {len(raw_data)} source records.")

        # 2. Normalize
        logger.info("Normalizing data...")
        normalized_data = []
        for record in raw_data:
            norm_record = record.copy()

            # Normalize Price
            if "price" in record:
                norm_record["price"] = normalize_price(record["price"])

            # Normalize Title (Name)
            if "title" in record:
                norm_record["name"] = normalize_text(record["title"])

            # Normalize Brand
            if "brand" in record:
                norm_record["brand"] = normalize_text(record["brand"])

            # Normalize Weight
            # Assuming 'weight' might be in attributes or direct field
            if "weight" in record:
                norm_record["weight"] = normalize_weight(record["weight"])

            normalized_data.append(norm_record)

        # 3. Deduplicate
        logger.info("Running Splink deduplication...")
        pipeline = DeduplicationPipeline()
        clusters = pipeline.run(normalized_data)

        logger.info(f"Found {len(clusters)} unique clusters.")

        for cluster in clusters:
            cluster_id = cluster["cluster_id"]
            record_ids = cluster["record_ids"]
            if len(record_ids) > 1:
                logger.info(f"Cluster {cluster_id} has duplicates: {record_ids}")

        # 4. Update Status (Dry Run for now)
        # logger.info("Updating pipeline status...")
        # db.update_status(processed_skus, "consolidated")

        logger.info("Job completed successfully.")

    except Exception as e:
        logger.error(f"Consolidation job failed: {e}", exc_info=True)
        raise
