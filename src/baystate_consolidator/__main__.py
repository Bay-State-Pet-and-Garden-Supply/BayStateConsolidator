import argparse
import sys
import os

# Add src to path to allow direct execution
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from baystate_consolidator.main import run_consolidation


def main():
    parser = argparse.ArgumentParser(description="BayState Consolidator Engine")
    parser.add_argument("--limit", type=int, default=100, help="Number of products to process")

    args = parser.parse_args()

    print(f"Starting consolidation job (limit={args.limit})...")
    run_consolidation(limit=args.limit)


if __name__ == "__main__":
    main()
