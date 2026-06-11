# Amazon Product Data API Python Quickstart

Python examples for creating ParseShelf Amazon product data jobs, polling live progress, and downloading CSV, JSONL, XLSX, or Markdown exports.

ParseShelf turns Amazon search URLs, category URLs, product URLs, and ASIN lists into structured product rows for ecommerce teams, Amazon agencies, FBA operators, catalog QA workflows, competitor price checks, and internal data pipelines.

## What You Can Build

- Amazon search results to CSV
- Amazon category URL export
- Bulk ASIN enrichment
- Competitor price tracking datasets
- Product research spreadsheets
- Catalog QA and marketplace monitoring workflows
- JSONL exports for data pipelines

## Useful Links

- Product landing page: <https://parseshelf.com/amazon/>
- Python docs: <https://parseshelf.com/docs/amazon-api/python/>
- Amazon Scraper API: <https://parseshelf.com/amazon-scraper-api/>
- Amazon Product Data API: <https://parseshelf.com/amazon-product-data-api/>
- Amazon ASIN API: <https://parseshelf.com/amazon-asin-api/>
- Sample dataset: <https://parseshelf.com/amazon-product-data-sample/>
- Proof run: <https://parseshelf.com/amazon-product-data-proof/>

## Quick Start

Install dependencies:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Set your API key:

```bash
export PARSESHELF_API_KEY="ps_live_or_test_key"
```

Create a job from an Amazon search URL and download CSV:

```bash
python examples/create_job_and_download_csv.py \
  --input-type search_url \
  --input-value "https://www.amazon.com/s?k=vitamin+c+serum" \
  --mode full_product \
  --target-count 25 \
  --output results.csv
```

Create a job from ASINs:

```bash
python examples/create_job_and_download_csv.py \
  --input-type asin_list \
  --input-value "B0060OUV5Y,B08H3JPH74,B000GAWSDG" \
  --mode full_product \
  --target-count 3 \
  --output asin-enrichment.csv
```

## API Flow

1. Create a job with marketplace, input type, input value, mode, and target count.
2. Poll the job until it reaches `succeeded` or `failed`.
3. Inspect live counters such as delivered rows, failed rows, speed, and charged units.
4. Download a structured export.

```python
import os
import requests

base_url = "https://parseshelf.com"
headers = {"Authorization": f"Bearer {os.environ['PARSESHELF_API_KEY']}"}

payload = {
    "marketplace": "amazon",
    "input_type": "search_url",
    "input_value": "https://www.amazon.com/s?k=vitamin+c+serum",
    "mode": "full_product",
    "target_count": 25,
}

job = requests.post(f"{base_url}/api/v1/jobs", json=payload, headers=headers, timeout=30).json()
print(job["id"], job["status"])
```

## Input Types

| Input type | Use it for |
| --- | --- |
| `search_url` | Amazon keyword/search result pages |
| `category_url` | Amazon category and browse node pages |
| `product_url_list` | A pasted list of product URLs |
| `asin_list` | Bulk ASIN enrichment |

## Modes

| Mode | Best for | Unit model |
| --- | --- | --- |
| `listing_only` | discovery, quick category/search exports | 1 Data Unit per delivered listing row |
| `full_product` | ASIN enrichment, price/rating/stock/image/detail workflows | 5 Data Units per delivered full product row |

Unused reserved units are returned when a job completes with fewer delivered rows than requested.

## Example Output Fields

Exports normalize practical Amazon product data fields:

- `product_id`
- `asin`
- `title`
- `brand`
- `price`
- `currency`
- `rating`
- `reviews_count`
- `stock_status`
- `category_path`
- `product_url`
- `source_url`

See `samples/amazon-product-data-sample.csv` and `samples/amazon-product-data-sample.jsonl`.

## Postman And OpenAPI

- OpenAPI spec: `openapi/parseshelf-amazon-api.openapi.json`
- Postman collection: `postman/parseshelf-amazon-api.postman_collection.json`

Use an environment variable named `PARSESHELF_API_KEY` in Postman and pass it as:

```text
Authorization: Bearer {{PARSESHELF_API_KEY}}
```

## Why ParseShelf

Most Amazon scraping projects become an operations problem: listing discovery, product enrichment, retries, exports, and non-technical review all need different tooling. ParseShelf is built as a dashboard plus API workflow:

- paste an Amazon input;
- watch discovery and enrichment progress live;
- inspect preview rows;
- download CSV, XLSX, JSONL, or Markdown;
- automate the same flow through API keys.

## Notes

This repository does not include scraping, proxy bypass, credential collection, or browser automation code. It is a client quickstart for the ParseShelf API. Customers are responsible for using exported data lawfully and according to their own compliance requirements.

## License

MIT. See `LICENSE`.
