# scraping-divar-apartments-sell<br/>‫


this is a practicing project to scrape data from divar.ir site (related to apartments sell segment) and cache 240 apartments pages and save its features 
to postgres database named **apartment**.
##  python necessary packages:
1. requests_cache(to cache all 240 apartments pages)
2. BeautifulSoup(to fetch data from html tages)
3. psycopg2(to connect postgresql)
## instruction for run :
> first run bash script  **./setup.sh** </span>.this script create venv ,activate it and install necessary packages on venv.
 then run bash script  **./run.sh**.
