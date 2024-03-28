import logging

from job_scraper.job_listings import JobListings, JobListing
from job_scraper.job_scraper import JobScraper
from job_scraper.logger import configure_logging

import pytest


@pytest.fixture
def sample_url_payload():
    """
    Fixture to mock the payload returned from the scrape URL request
    """
    return [
        {
            'advertiser': {'id': '123', 'description': 'Advertiser'},
            'automaticInclusion': False,
            'branding': {
                'id': 'd5eff96a-c4cf-45a7-bc24-5d895f29b78d.1',
                'assets': {
                    'logo': {
                        'strategies': {
                            'jdpLogo': 'logovalue', 'serpLogo': 'logovalue'
                        }
                    }
                }
            },
            'bulletPoints': ['Join us'],
            'classification': {
                'id': '6281', 'description': 'Information & Communication Technology'  # noqa
            },
            'companyProfileStructuredDataId': 0,
            'displayStyle': {'search': 'A'},
            'displayType': 'promoted',
            'listingDateDisplay': '10h ago',
            'location': 'Wellington',
            'locationId': 1019,
            'locationWhereValue': 'All Wellington',
            'id': 11111111,
            'isPremium': True,
            'isStandOut': True,
            'jobLocation': {
                'label': 'Wellington', 'countryCode': 'NZ', 'seoHierarchy':
                [{'contextualName': 'All Wellington'}]
            },
            'listingDate': '2024-04-14T21:52:04Z',
            'logo': {'id': '', 'description': None},
            'roleId': 'modeller',
            'salary': '$100818 - $108992 p.a.',
            'solMetadata': {'searchRequestToken': 'b8abfd83-cb81-4561-bb57-62b3913176ce', 'token': '0~b8abfd83-cb81-4561-bb57-62b3913176ce', 'jobId': '75113922', 'section': 'MAIN', 'sectionRank': 1, 'jobAdType': 'SPONSORED', 'tags': {'mordor__flights': 'mordor_441', 'mordor__s': '0'}},  # noqa
            'subClassification': {'id': '6283', 'description': 'Business/Systems Analysts'},  # noqa
            'tags': [{'type': 'EARLY_APPLICANT', 'label': 'Early applicant'}],
            'teaser': "Be part of a high performing team",
            'title': 'Data Warehouse Modeller',
            'tracking': '123==',
            'workType': 'Full time',
            'isPrivateAdvertiser': False
        },
        {
            'advertiser': {'id': '', 'description': 'Private Advertiser'},
            'area': 'Auckland Central',
            'areaId': 5118,
            'areaWhereValue': 'Auckland Central Auckland',
            'automaticInclusion': False,
            'bulletPoints': ['Brand new role', 'Opportunity to lead and develop a team', 'ERP systems experience preferred'],  # noqa
            'classification': {'id': '6281', 'description': 'Information & Communication Technology'},  # noqa
            'companyName': 'Private Advertiser',
            'companyProfileStructuredDataId': 0,
            'displayStyle': {'search': 'A'},
            'displayType': 'promoted',
            'listingDateDisplay': '5d ago',
            'location': 'Auckland',
            'locationId': 1018,
            'locationWhereValue': 'All Auckland',
            'id': 2222222,
            'isPremium': True,
            'isStandOut': True,
            'jobLocation': {'label': 'Mount Wellington, Auckland', 'countryCode': 'NZ', 'seoHierarchy': [{'contextualName': 'Mount Wellington Auckland'}, {'contextualName': 'All Auckland'}]},  # noqa
            'listingDate': '2024-04-09T21:24:16Z',
            'logo': {'id': '', 'description': None},
            'roleId': 'information-technology-manager',
            'salary': '$150,000 – $170,000 per year',
            'solMetadata': {'searchRequestToken': 'b8abfd83-cb81-4561-bb57-62b3913176ce', 'token': '0~b8abfd83-cb81-4561-bb57-62b3913176ce', 'jobId': '75031952', 'section': 'MAIN', 'sectionRank': 2, 'jobAdType': 'SPONSORED', 'tags': {'mordor__flights': 'mordor_441', 'mordor__s': '0'}},  # noqa
            'subClassification': {'id': '6292', 'description': 'Management'},
            'suburb': 'Mount Wellington',
            'suburbId': 30133,
            'suburbWhereValue': 'Mount Wellington Auckland',
            'teaser': 'Brand new role',
            'title': 'IT Manager',
            'tracking': '123==',
            'workType': 'Full time',
            'isPrivateAdvertiser': True
        }
    ]


@pytest.fixture
def sample_listings():
    """
    Fixture function that provides a list of sample job listings for testing.
    """
    # Define some sample job listings
    listings = JobListings()
    listings.add_listing(
        JobListing(
            id=1,
            title="Software Engineer",
            advertiser="Tech Company A",
            location="Levin",
            area="Software Development",
            work_type="Full-time",
            salary="$100,000 - $120,000",
            url="https://example.com/job1",
            logo_url="https://example.com/logo1.png"
        )
    )
    listings.add_listing(
        JobListing(
            id=2,
            title="Data Analyst",
            advertiser="Data Company B",
            location="Timaru",
            area="Data Analysis",
            work_type="Part-time",
            salary="$80,000 - $90,000",
            url="https://example.com/job2",
            logo_url="https://example.com/logo2.png"
        )
    ),
    listings.add_listing(
        JobListing(
            id=3,
            title="Data Engineer",
            advertiser="Data Company C",
            location="Napier",
            area="Data Engineering",
            work_type="Part-time",
            salary="$100,000 - $110,000",
            url="https://example.com/job2",
            logo_url="https://example.com/logo2.png"
        )
    )
    return listings


@pytest.fixture
def job_scraper(sample_listings):
    """
    Job Scraper fixture
    """
    configure_logging()
    logger = logging.getLogger(__name__)
    job_scraper = JobScraper(
        logger=logger, country="NZ",
        classification=6281, keyword="data engineer"
    )
    job_scraper.listings = sample_listings

    return job_scraper
