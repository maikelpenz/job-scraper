# job-scraper

# Run it locally
/c/Data/Solutions/DataEngineering/job-scraper
> python -m job_scraper
> pytest -v --disable-pytest-warnings --cov=job_scraper
> flake8 --statistics

# Run as part of CI/CD
/c/Data/Solutions/DataEngineering/job-scraper
> pytest -v --disable-pytest-warnings --cov=job_scraper
> flake8 --statistics