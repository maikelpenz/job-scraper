import boto3

from job_scraper import scrape

if __name__ == "__main__":
    classification = 6281  # Information & Communication Technology
    keyword = "data"

    boto3.setup_default_session(
        profile_name="maikel_cli_access", region_name="us-east-1"
    )

    job_filters = [
        {
            "classification": 6281,
            "keyword": "data",
            "slack_webhook_secret": "mpenz-ws-slack-webhook",
        },
        {
            "classification": 6281,
            "keyword": "cloud",
            "slack_webhook_secret": "mpenz-ws-slack-webhook",
        },
        {
            "classification": 6281,
            "keyword": "test",
            "slack_webhook_secret": "gcelmer-ws-slack-webhook",
        },
    ]

    for job_filter in job_filters:
        classification = job_filter.get("classification")
        keyword = job_filter.get("keyword")
        slack_webhook_secret = job_filter.get("slack_webhook_secret")

        scrape.main(
            classification=classification,
            keyword=keyword,
            slack_webhook_secret=slack_webhook_secret,
        )
