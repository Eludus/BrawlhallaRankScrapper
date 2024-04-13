from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import os
import requests
from bs4 import BeautifulSoup

availableRegions = {
    "all",
    "us-e",
    "eu",
    "sea",
    "brz",
    "aus",
    "us-w",
    "jpn",
    "sa",
    "me",
}
availableModes = {"1v1", "2v2"}


# Fetch the rating data of the specified region and mode using threading.
def fetchRatingData(region="all", mode="1v1", batchAmount=50):
    print("Fetching Rating Data from {} {}".format(region, mode))
    validateInputs(region, mode)

    maxPage = getMaximumPage(region, mode)
    print("Maximum Page for {}, {}: {}".format(region, mode, maxPage))

    allRatingData = []

    with ThreadPoolExecutor() as executor:
        futures = []

        for pageNumber in range(1, maxPage + 1, batchAmount):
            upperPage = min(maxPage, pageNumber + batchAmount - 1)
            futures.append(
                executor.submit(
                    fetchPageDataPageRange, region, mode, pageNumber, upperPage
                )
            )

        for future in futures:
            rankData = future.result()
            allRatingData.extend(rankData)
            if len(allRatingData) % (batchAmount * 25) == 0:
                print("Current Page: " + str(len(allRatingData) / 25))

    jsonData = {
        "date": str(datetime.now().date()),
        "count": len(allRatingData),
        "data": allRatingData,
    }

    # Create the directory if it doesn't exist
    directory = "data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the file
    with open(
        os.path.join(directory, "{}_{}_RatingData.json".format(region, mode)), "w"
    ) as json_file:
        json.dump(jsonData, json_file)
        print("Saved as data/{}_{}_RatingData.json".format(region, mode))

    print("Length: " + str(len(allRatingData)))
    return allRatingData


# Validate if region and mode are valid
def validateInputs(region, mode):

    if mode not in availableModes:
        raise ValueError(
            "Invalid Mode. Allowed modes are {}".format(", ".join(availableModes))
        )

    if region not in availableRegions:
        raise ValueError(
            "Invalid Region. Allowed regions are {}".format(", ".join(availableRegions))
        )


# Get the last page that contains rating data
def getMaximumPage(region="all", mode="1v1", lowerPage=0, upperPage=1000000):
    validateInputs(region, mode)

    if upperPage - lowerPage <= 1:
        return lowerPage

    mid = int((lowerPage + upperPage) / 2)
    url = "https://www.brawlhalla.com/rankings/game/{}/{}/{}?sortBy=rank".format(
        region, mode, mid
    )
    rankData = fetchPageData(url)

    if rankData:
        return getMaximumPage(region, mode, mid, upperPage)
    else:
        return getMaximumPage(region, mode, lowerPage, mid)


# Fetch the Rating Data of a specified region, mode and page range
def fetchPageDataPageRange(region, mode, lowerPage, upperPage):
    rankData = []
    for pageNumber in range(lowerPage, upperPage + 1):
        url = "https://www.brawlhalla.com/rankings/game/{}/{}/{}?sortBy=rank".format(
            region, mode, pageNumber
        )
        rankData.extend(fetchPageData(url))

    return rankData


# Fetch the Rating Data of a specific URL
def fetchPageData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")

    htmlData = soup.select("td[data-id='seasonRating']")
    rankData = [td.getText(strip=True) for td in htmlData]
    return rankData


# To update the data folder with all the updated JSON data
def updateAllRatingData(batchAmount=50):
    for region in availableRegions:
        for mode in availableModes:
            fetchRatingData(region=region, mode=mode, batchAmount=batchAmount)


if __name__ == "__main__":
    updateAllRatingData()
