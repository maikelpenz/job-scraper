import boto3
import json

from job_scraper import scrape

if __name__ == "__main__":
    boto3.setup_default_session(
        profile_name="maikel_cli_access", region_name="us-east-1"
    )

    with open("job_scraper/job_filters.json") as f:
        job_filters = json.load(f)

    for job_filter in job_filters:
        classification = job_filter.get("classification")
        keyword = job_filter.get("keyword")
        slack_webhook_secret = job_filter.get("slack_webhook_secret")

        scrape.main(
            classification=classification,
            keyword=keyword,
            slack_webhook_secret=slack_webhook_secret,
        )
