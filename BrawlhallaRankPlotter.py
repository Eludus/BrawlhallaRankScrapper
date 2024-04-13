import BrawlhallaRankScrapper as BHRS
from matplotlib import pyplot as plt
import mplcursors
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys


def plotRatingGraph(
    region="all", mode="1v1", start_elo=1000, end_elo=3000, interval=100
):
    data = BHRS.getCachedRatingData(region=region, mode=mode)
    eloData = [int(x) for x in data["data"]]

    bins = range(start_elo, end_elo + 1, interval)

    fig, ax = plt.subplots(figsize=(15, 6))
    n, bins, patches = plt.hist(eloData, bins=bins)
    plt.title("Rating Data of {} {} ({})".format(region, mode, data["date"]))
    plt.xticks(bins, fontsize=10)
    plt.xlabel("Rating Range")
    plt.ylabel("Number of Players")

    mplcursors.cursor(hover=True).connect(
        "add",
        lambda sel: sel.annotation.set_text(
            f"Players: {int(n[int(sel.index)])}\nElo: {int(bins[sel.index])} - {int(bins[sel.index + 1])}"
        ),
    )

    plt.show()
    # return fig


def displayUI():
    root = tk.Tk()
    root.title("Brawlhalla Rating Data")

    content_frame = tk.Frame(root, padx=20, pady=20)
    content_frame.pack()

    # Elo Selector
    eloRangeLabel = tk.Label(content_frame, text="Elo Range: ")
    dashLabel = tk.Label(content_frame, text="-")
    eloStartRangeLabel = tk.Entry(content_frame)
    eloStartRangeLabel.insert(0, 500)
    eloEndRangeLabel = tk.Entry(content_frame)
    eloEndRangeLabel.insert(0, 3000)

    # Interval Selector
    intervalLabel = tk.Label(content_frame, text="Interval: ")
    intervalEntry = tk.Entry(content_frame)
    intervalEntry.insert(0, 100)

    # Region Selector
    regionLabel = tk.Label(content_frame, text="Select Region")
    regionVar = tk.StringVar()
    regionVar.set("All")
    availableRegions = [
        "All",
        "US-E",
        "EU",
        "SEA",
        "BRZ",
        "AUS",
        "US-W",
        "JPN",
        "SA",
        "ME",
    ]
    for index, region in enumerate(availableRegions):
        regionButton = tk.Radiobutton(
            content_frame, text=region, variable=regionVar, value=region
        )
        regionButton.grid(row=int(index % 5) + 3, column=int(index / 5), sticky=tk.W)

    # Mode Selector
    modeLabel = tk.Label(content_frame, text="Select Game Mode")
    modeVar = tk.StringVar()
    modeVar.set("1v1")
    availableModes = ["1v1", "2v2"]
    for index, mode in enumerate(availableModes):
        modeButton = tk.Radiobutton(
            content_frame, text=mode, variable=modeVar, value=mode
        )
        modeButton.grid(row=index + 3, column=3, sticky=tk.W)

    # Elo Selector Grid Layout
    eloRangeLabel.grid(row=0, column=0, sticky=tk.W)
    eloStartRangeLabel.grid(row=0, column=1, sticky=tk.W)
    dashLabel.grid(row=0, column=2, sticky=tk.W)
    eloEndRangeLabel.grid(row=0, column=3, sticky=tk.W)

    # Interval Selector Gird Layout
    intervalLabel.grid(row=1, column=0, sticky=tk.W, pady=(0, 20))
    intervalEntry.grid(row=1, column=1, sticky=tk.W, pady=(0, 20))

    # Generate Button Grid Layout
    generateButton = tk.Button(
        content_frame,
        text="Generate",
        command=lambda: plotRatingGraph(
            region=regionVar.get().lower(),
            mode=modeVar.get().lower(),
            start_elo=int(eloStartRangeLabel.get()),
            end_elo=int(eloEndRangeLabel.get()),
            interval=int(intervalEntry.get()),
        ),
    )
    generateButton.grid(row=0, column=4, padx=(5, 5))

    # Region and Mode Selector Grid Layout
    regionLabel.grid(row=2, column=0, sticky=tk.W, pady=(0, 3))
    modeLabel.grid(row=2, column=3, sticky=tk.W, pady=(0, 3))

    # Fetch New Data Button Layout
    fetchDataButton = tk.Button(
        content_frame, text="Fetch Latest Data", command=fetchDataWarning
    )
    fetchDataButton.grid(row=8, column=5, sticky=tk.E)

    root.mainloop()


def fetchDataWarning():
    warning_window = tk.Toplevel()
    warning_window.title("Warning!")
    warning_window.geometry("400x200")

    content_frame = tk.Frame(warning_window, padx=10, pady=10)
    content_frame.pack()

    warning_label = tk.Label(
        content_frame,
        text="Running this function will start scrapping thousands of \nBrawlhalla Rank Webpage to update the rating data.\n\nUSE IT AT YOUR OWN RISK!!!.\n\n PS: This function is very slow. (and I mean VERY SLOW).",
    )
    warning_label.pack()

    button_frame = tk.Frame(content_frame)
    button_frame.pack(side=tk.BOTTOM, pady=(20, 0))

    def proceed():
        BHRS.updateAllRatingData()
        warning_window.destroy()

    proceed_button = tk.Button(button_frame, text="Proceed", command=proceed)
    proceed_button.pack(side=tk.RIGHT, padx=5, pady=5)

    cancel_button = tk.Button(
        button_frame, text="Cancel", command=lambda: warning_window.destroy()
    )
    cancel_button.pack(side=tk.LEFT, padx=5, pady=5)


if __name__ == "__main__":
    # plotRatingGraph(end_elo=2000)
    displayUI()
