import boto3

from job_scraper import main

if __name__ == "__main__":
    boto3.setup_default_session(
        profile_name="maikel_cli_access", region_name="us-east-1"
    )

    config = main.load_configuration("job_scraper/job_filters.json")

    for job_filter in config:
        main.process_job_filter(job_filter)
