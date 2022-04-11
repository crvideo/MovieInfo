# MovieInfo

MovieInfo is a tool to search specific number or keyword from a set of av and get information of videos and output json. This json is use for a discord bot or automation torrent download.


### Installation

```bash
pip install getmovieinfo
```

### Requirements

#### python packages
- python = "^3.7"
- selenium = "^4.1.3"
- requests = "^2.27.1"
- lxml = "^4.8.0"
- argparse = "^1.4.0"
- jsons = "^1.6.1"
- secrets

#### other packages

- firefox
- [geckodriver](https://github.com/mozilla/geckodriver)

### Usage

```bash
MovieInfo --number SSIS-356

MovieInfo --keyword 涼森れむ
```


#### Parameters

- --number
  - Specify a video number
- --keyword
  - SPecify a keyword
- --cache_dir
  - specify a dir to store the result json


# License

This project is licensed under the MIT License


# Acknowledgement

This project is based on [Movie_data_Capture](https://github.com/yoshiko2/Movie_Data_Capture). 

I implement a keyword searching and standardize the infomation extractor from html.

I update crawler to substitue python requests;

Selenium is great at loading js on a web and enable the extracttion of torrent/magnet infomation. However this slows each request very much. Pay attention if you use this script to do massive query.
