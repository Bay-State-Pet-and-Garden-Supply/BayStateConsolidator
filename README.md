# BayStateConsolidator

**BayStateConsolidator** is the intelligence layer for the Bay State ecosystem, responsible for ingesting raw scraped data, normalizing it, and consolidating duplicates into a "Golden Record" for the e-commerce storefront.

## Architecture: Hybrid 3-Tier
1.  **Normalization**: Standardize inputs (prices, units, dimensions) using `price-parser` and `quantulum3`.
2.  **Entity Resolution (ER)**: Probabilistic matching using `Splink` (DuckDB backend) to identify duplicate products across different scrapers/sites.
3.  **Consolidation**: Semantic merging of attributes (potentially via LLM or rule-based logic).

## Key Components
- **Ingestor**: Loads raw JSON data from `BayStateScraper` output.
- **Normalizer**: Cleans and standardizes text, prices, and physical units.
- **Pipeline**: Runs the Splink deduplication jobs.
- **Loader**: Pushes consolidated results to `BayStateApp` (Supabase).

## Tech Stack
- **Polars**: High-performance DataFrame library for data manipulation.
- **Splink**: Probabilistic record linkage at scale.
- **Pydantic**: Strict data validation and schema definition.
- **DuckDB**: Embedded SQL OLAP database for efficient local processing.
