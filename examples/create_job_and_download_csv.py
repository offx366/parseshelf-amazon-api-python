#!/usr/bin/env python3
"""Create a ParseShelf Amazon job, wait for completion, and download CSV."""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=os.environ.get("PARSESHELF_BASE_URL", "https://parseshelf.com"))
    parser.add_argument("--input-type", choices=("search_url", "category_url", "product_url_list", "asin_list"), required=True)
    parser.add_argument("--input-value", required=True)
    parser.add_argument("--mode", choices=("listing_only", "full_product"), default="full_product")
    parser.add_argument("--target-count", type=int, default=25)
    parser.add_argument("--output", default="results.csv")
    parser.add_argument("--poll-seconds", type=float, default=3.0)
    parser.add_argument("--timeout-seconds", type=float, default=900.0)
    return parser.parse_args()


def api_key() -> str:
    value = os.environ.get("PARSESHELF_API_KEY", "").strip()
    if not value:
        raise SystemExit("Set PARSESHELF_API_KEY before running this example.")
    return value


def request_json(method: str, url: str, *, headers: dict[str, str], **kwargs: Any) -> dict[str, Any]:
    response = requests.request(method, url, headers=headers, timeout=30, **kwargs)
    try:
        payload = response.json()
    except ValueError:
        payload = {"error": response.text[:500]}
    if response.status_code >= 400:
        raise RuntimeError(f"{method} {url} failed: HTTP {response.status_code}: {payload}")
    return payload


def create_job(args: argparse.Namespace, headers: dict[str, str]) -> dict[str, Any]:
    payload = {
        "marketplace": "amazon",
        "input_type": args.input_type,
        "input_value": args.input_value,
        "mode": args.mode,
        "target_count": args.target_count,
    }
    return request_json("POST", f"{args.base_url}/api/v1/jobs", headers=headers, json=payload)


def poll_job(args: argparse.Namespace, headers: dict[str, str], job_id: str) -> dict[str, Any]:
    deadline = time.time() + args.timeout_seconds
    last_status = ""
    while time.time() < deadline:
        job = request_json("GET", f"{args.base_url}/api/v1/jobs/{job_id}", headers=headers)
        status = str(job.get("status", "unknown"))
        delivered = job.get("records_delivered", job.get("delivered", 0))
        failed = job.get("records_failed", job.get("failed", 0))
        speed = job.get("speed_per_min", job.get("speed", "-"))
        line = f"status={status} delivered={delivered} failed={failed} speed={speed}"
        if line != last_status:
            print(line, flush=True)
            last_status = line
        if status == "succeeded":
            return job
        if status in {"failed", "canceled"}:
            raise RuntimeError(f"Job {job_id} ended with status={status}: {job}")
        time.sleep(args.poll_seconds)
    raise TimeoutError(f"Timed out waiting for job {job_id}")


def download_csv(args: argparse.Namespace, headers: dict[str, str], job_id: str) -> Path:
    response = requests.get(f"{args.base_url}/api/v1/jobs/{job_id}/download/csv", headers=headers, timeout=60)
    if response.status_code >= 400:
        raise RuntimeError(f"CSV download failed: HTTP {response.status_code}: {response.text[:500]}")
    output = Path(args.output)
    output.write_bytes(response.content)
    return output


def main() -> int:
    args = parse_args()
    headers = {"Authorization": f"Bearer {api_key()}"}
    job = create_job(args, headers)
    job_id = str(job["id"])
    print(f"created job={job_id}")
    done = poll_job(args, headers, job_id)
    print(f"completed job={job_id} charged_units={done.get('charged_units', '-')}")
    output = download_csv(args, headers, job_id)
    print(f"downloaded {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
