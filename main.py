
import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
import pandas as pd
import os
from parse import parse_taskmaster_csv
 

def url_get_contents(url):
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()

def scrape_tm_details_to_dfs():
    xhtml = url_get_contents('https://taskmaster.fandom.com/wiki/Episode_list').decode('utf-8')
    p = HTMLTableParser()
    p.feed(xhtml)
    all_dfs = []
    for i, table in enumerate(p.tables):
        if i in range(0, 15):
            all_dfs.append(pd.DataFrame(table))
    return all_dfs

def build_temp_csvs(all_dfs, temp_dir):
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))

    for i, df in enumerate(all_dfs):
        index_value = "%02d" % (i,)
        df.to_csv(f"{temp_dir}/df_{index_value}.csv", index=False)

def determine_series_names(all_input_dfs):
    count = len(all_input_dfs)
    current = 0
    series_coc_count = 1
    multiplier = 0
    series_names = []
    while current <= count:
        if current == 14:
            series_names.append("New Years")
        else:
            series_names.append("Series " + str(series_coc_count+(5*multiplier)))
            series_coc_count += 1
            if series_coc_count >= 6:
                series_coc_count = 1
                series_names.append("COC")
                current += 1
                multiplier += 1
        current += 1
    return series_names


if __name__ == "__main__":
    dir_path = "temp_csvs"
    taskmaster_dfs = scrape_tm_details_to_dfs()
    build_temp_csvs(all_dfs=taskmaster_dfs, temp_dir=dir_path)
    series_names = determine_series_names(all_input_dfs=taskmaster_dfs)
    for i, filename in enumerate(os.listdir(dir_path)):
        f = os.path.join(dir_path, filename)
        if os.path.isfile(f):
            parse_taskmaster_csv(infile=f, series_name=series_names[i])