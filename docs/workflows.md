# ParseShelf Amazon API Workflows

Use these examples to decide which input and mode fit your workflow.

## ASIN Enrichment

Input:

```text
B0060OUV5Y,B08H3JPH74,B000GAWSDG
```

Recommended mode:

```text
full_product
```

Best output:

```text
CSV or XLSX for operators, JSONL for pipelines
```

Landing page:

```text
https://parseshelf.com/amazon-asin-api/
```

## Search Results Export

Input:

```text
https://www.amazon.com/s?k=vitamin+c+serum
```

Recommended mode:

```text
listing_only for discovery, full_product for enriched rows
```

Landing page:

```text
https://parseshelf.com/amazon-search-api/
```

## Category URL Export

Input:

```text
An Amazon category or browse-node URL
```

Recommended mode:

```text
listing_only first, then full_product for selected products
```

Landing page:

```text
https://parseshelf.com/amazon-category-api/
```

## Competitor Price Tracking

Input:

```text
ASIN list, product URL list, category URL, or recurring search URL
```

Recommended mode:

```text
full_product
```

Landing page:

```text
https://parseshelf.com/amazon-price-api/
```
