# Brawlhalla Ranking Page Scrapper
This is a project to scrape through Brawlhalla's Ranking Page data and have the elo data plotted in a histogram.
It allows for filtering of Elo Range, Region and Gamemode

## For people who just wants to view the data
For the people that don't care how it works, I've packed the program into an EXE file in "/dist" folder for easy use. Just download the /dist folder, run the .exe and you're good to go (Probably).

__After Running BrawlhallaRankPlotter.exe__
1. Enter the Elo Range you want
2. Enter the x-axis elo interval
3. Choose the Region and Game Mode
4. Click Generate

**Warning** The "Fetch Latest Data" Button will scrape through the thousands of brawlhalla ranking page to get the latest data. It is VERY SLOW. And it will scrape through every region's 1v1 and 2v2 ranking data. I **DO NOT** recommend using it. Does it even work? Honestly, I don't know, I've never used it. 

## Getting Rank Data
To get Rank Data, the `BrawlhallaRankScrapper.py` API script contains two functions for it `fetchRatingData()` and `getCachedRatingData()`.

### fetchRatingData()
FetchRatingData() accepts Region and Gamemode as parameters to scrape the data from and returns an array of elo from highest to lowest.
It will also save the data in a json file with the file format of `<region>_<mode>_RatingData.json`.

It is painfully slow, I'm assuming from the thousands of http requests to Brawlhalla Rank page.
I've implemented threading to speed it up but its still disgustingly slow.

### getCachedRatingData()
getCachedRatingData() accepts Region and Gamemode as parameters and just return the .json file's data as a dictionary.
It is a lot faster but the data is from the last time you've called the `fetchRatingData()` function OR the `Fetch Latest Data` Button from the GUI.

## Plotting Rank Data
For plotting, `BrawlhallaRankScrapper.py` plot the elo data as a histogram using matplotlib. A disgusting GUI is also added to allow for filtering of Elo Range, Region and Gamemode.
**Run this script if you want to use the program**

## Help
Let me know if there is a better / faster way if you know it. I may or may not do anymore update on it, but it will be a good learning experience.

If you did go through the trouble and generate with the latest data, feel free to do a pull request and I'll update it if I see it, it might save others the trouble of doing it.
