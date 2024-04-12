from concurrent.futures import ThreadPoolExecutor
import json
import requests
from bs4 import BeautifulSoup


def validateInputs(region, mode):
    availableModes = {"1v1", "2v2"}
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

    if mode not in availableModes:
        raise ValueError(
            "Invalid Mode. Allowed modes are {}".format(", ".join(availableModes))
        )

    if region not in availableRegions:
        raise ValueError(
            "Invalid Region. Allowed regions are {}".format(", ".join(availableRegions))
        )


def getRatingData(region="all", mode="1v1"):
    validateInputs(region, mode)

    allRatingData = []

    pageNumber = 1
    isEnd = False

    while not isEnd:
        URL = "https://www.brawlhalla.com/rankings/game/{}/{}/{}?sortBy=rank".format(
            region, mode, pageNumber
        )
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "lxml")

        htmlData = soup.select("td[data-id='seasonRating']")
        rankData = [td.getText(strip=True) for td in htmlData]
        isEnd = len(rankData) == 0

        allRatingData.extend(rankData)

        pageNumber += 1

        if pageNumber % 50 == 0:
            print(pageNumber)

    print(len(allRatingData))
    print(pageNumber)


def getRatingDataWithThreads(region="all", mode="1v1", batchAmount=50):
    validateInputs(region, mode)

    maxPage = getMaximumPage(region, mode)
    print("Maximum Page for {}, {}: {}".format(region, mode, maxPage))

    allRatingData = []

    with ThreadPoolExecutor() as executor:
        futures = []

        for pageNumber in range(1, maxPage + 1, batchAmount):
            upperPage = min(maxPage + 1, pageNumber + batchAmount - 1)
            futures.append(
                executor.submit(
                    fetchPageDataPageRange, region, mode, pageNumber, upperPage
                )
            )

        for future in futures:
            rankData = future.result()
            allRatingData.extend(rankData)
            if len(allRatingData) % 1250 == 0:
                print("Current Page: " + str(len(allRatingData) / 25))

    with open("{}_{}_RatingData.json".format(region, mode), "w") as json_file:
        json.dump(allRatingData, json_file)

    print("Length: " + str(len(allRatingData)))


def getMaximumPage(region="all", mode="1v1", lowerPage=0, upperPage=1000000):

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


def fetchPageDataPageRange(region, mode, lowerPage, upperPage):
    rankData = []
    for pageNumber in range(lowerPage, upperPage + 1):
        url = "https://www.brawlhalla.com/rankings/game/{}/{}/{}?sortBy=rank".format(
            region, mode, pageNumber
        )
        rankData.extend(fetchPageData(url))

    return rankData


def fetchPageData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")

    htmlData = soup.select("td[data-id='seasonRating']")
    rankData = [td.getText(strip=True) for td in htmlData]
    return rankData


if __name__ == "__main__":
    getRatingDataWithThreads(batchAmount=200)
