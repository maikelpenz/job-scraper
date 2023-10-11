import json

from job_scraper.job_scraper import JobScraper
from job_scraper.job_scraper_dynamo import JobScraperDynamo
from job_scraper.job_scraper_notify import JobScraperNotify
from job_scraper.job_scraper_pandas import JobScraperPandas


def main(
    classification: int, keyword: str, slack_webhook_secret: str, country: str
):  # noqa
    """Used to test the package locally and also to be called by the Lambda

    Arguments:
        classification {int} -- Job Classification (from the website)
        keyword {str} -- Keyword to filter listings (e.g: data)
        slack_webhook_secret {str} -- Name of the secret to retrieve the
                                    slack webhook to send the notification
                                    (e.g: mpenz-ws-slack-webhook)
        country {str} -- e.g: AU or NZ
    """
    scraper = JobScraper(
        country=country, classification=classification, keyword=keyword
    )
    job_scraper_dynamo = JobScraperDynamo()
    job_scraper_notify = JobScraperNotify()
    job_scraper_pandas = JobScraperPandas()

    print("")
    print(
        f"Starting: Country: {country} \n Classification: {classification} \n Keyword: {keyword}"  # noqa
    )
    print("")

    # Get Today's and Yesterday's Listings.
    scraper.scrape_listings()

    # Filter the keyword from the list of listings
    scraper.filter_listings()

    # Enrich listings with details
    scraper.enrich_listing_details()

    listings = scraper.get_enriched_listings()

    if len(listings) == 0:
        print("")
        print("No listings matching the keyword over the last 2 days!")
        print("")
    else:
        # Display Listings that match the keyword criteria
        job_scraper_pandas.display_listings(listings)

        # insert to dynamo
        new_listings = job_scraper_dynamo.persist_listings(listings=listings)

        # Display new Listings
        job_scraper_pandas.display_listings(new_listings)

        # display only ones that are not in dynamo
        job_scraper_notify.notify_new_listings(
            listings=new_listings, slack_webhook_secret=slack_webhook_secret
        )


def lambda_handler(event, context):
    # read configuration
    with open("job_scraper/job_filters.json") as f:
        job_filters = json.load(f)

    for job_filter in job_filters:
        classification = job_filter.get("classification")
        keyword = job_filter.get("keyword")
        slack_webhook_secret = job_filter.get("slack_webhook_secret")
        country = job_filter.get("country")

        main(
            classification=classification,
            keyword=keyword,
            slack_webhook_secret=slack_webhook_secret,
            country=country,
        )
