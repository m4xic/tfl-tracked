# 🛤️ TfL Tracked

> _(this was going to be called TfL Wrapped but I fell in love with the "train tracks" pun)_

Get detailed stats about your travel across London

## 🚨 Warning

TfL only allows you to get 8 weeks worth of journey history from your online account. This means that to get a year's worth, you'll need to log on every couple of months and export it to a CSV file.

In addition, I've only tested this using the CSV files generated when you get journey history for an Oyster card. Your mileage may vary when using a contactless card.

I've also only tested it with bus, Tube, DLR, Overground and Elizabeth Line journeys - I don't live near the Trams and have no desire to use the Emirates Air thing. Sorry.

This is still very early, I'm going to improve on this over time (eventually adding options to export to JSON, change the input folder, etc)

## 🔨 How-to

No external dependencies or anything!

Just clone the repo, pop your CSVs in a folder called `journey-history` (I'll be including an example, with an example file too) and run `parse.py`.

```
$ git clone https://github.com/m4xic/tfl-tracked.git
$ python3 parse.py
```
