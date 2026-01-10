import polars as pl
from typing import List, Dict, Any
from splink.duckdb.linker import DuckDBLinker
from splink.duckdb.blocking_rule_library import block_on
import splink.duckdb.comparison_library as cl
import splink.duckdb.comparison_level_library as cll


class DeduplicationPipeline:
    def __init__(self, output_path: str = "./matches.parquet"):
        self.output_path = output_path

    def _get_settings(self) -> Dict[str, Any]:
        return {
            "link_type": "dedupe_only",
            "blocking_rules_to_generate_predictions": [
                block_on("brand"),
                block_on("category"),
            ],
            "comparisons": [
                cl.LevenshteinAtThresholds("name", [2, 5]),
                cl.ExactMatch("brand"),
                cl.ExactMatch("weight"),
                # Custom price comparison
                {
                    "output_column_name": "price",
                    "comparison_description": "Price difference",
                    "comparison_levels": [
                        cll.NullLevel("price"),
                        cll.ExactMatchLevel("price"),
                        {
                            "sql_condition": "abs(price_l - price_r) <= 1.0",
                            "label_for_charts": "Difference <= 1.0",
                            "is_match": True,
                        },
                        {
                            "sql_condition": "abs(price_l - price_r) <= 5.0",
                            "label_for_charts": "Difference <= 5.0",
                            "is_match": True,
                        },
                        cll.ElseLevel("price"),
                    ],
                },
            ],
            "retain_matching_columns": True,
            "retain_intermediate_calculation_columns": True,
        }

    def run(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Runs the deduplication pipeline on the input data.
        Returns a list of clusters, where each cluster contains the source records.
        """
        if not data:
            return []

        # Convert to Polars DataFrame for efficient handling
        df = pl.DataFrame(data)

        # Ensure we have a unique ID for Splink
        if "unique_id" not in df.columns:
            df = df.with_columns(pl.arange(0, pl.len()).alias("unique_id"))

        # Initialize Linker
        linker = DuckDBLinker(df.to_pandas(), self._get_settings())

        # Predict Matches
        df_predictions = linker.predict(threshold_match_probability=0.9)

        # Cluster
        df_clusters = linker.cluster_pairwise_predictions_at_threshold(df_predictions, 0.9)

        # Convert back to list of dicts for return
        # Group by cluster_id
        clusters = (
            df_clusters.as_pandas_dataframe()
            .groupby("cluster_id")["unique_id"]
            .apply(list)
            .to_dict()
        )

        result = []
        # Map back to original data
        # Note: In a real scenario, we'd join back. Here we just return the grouped IDs.
        for cluster_id, record_ids in clusters.items():
            result.append({"cluster_id": cluster_id, "record_ids": record_ids})

        return result
