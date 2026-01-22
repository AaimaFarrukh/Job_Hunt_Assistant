import requests
from utils.config import USAJOBS_API_KEY

def fetch_usajobs(keyword, location="remote", results_per_page=5):
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": "aaimafarrukh@gmail.com",
        "Authorization-Key": USAJOBS_API_KEY
    }
    params={
        "keyword": keyword,
        "location": location,
        "results_per_page": results_per_page

    }
    url =f"https://data.usajobs.gov/api/search?Keyword={keyword}&LocationName={location}&ResultsPerPage={results_per_page}"
    response= requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("SearchResult",{}).get("SearchResultItems", [])
    else:
        return []
if __name__ == "__main__":
    jobs= fetch_usajobs("data scientist")
    #print(f"Total jobs returned: {len(jobs)}") 
    for job in jobs:
        title = job['MatchedObjectDescriptor']['PositionTitle']
        agency = job['MatchedObjectDescriptor']['OrganizationName']
        print(f"{title} at {agency}")

