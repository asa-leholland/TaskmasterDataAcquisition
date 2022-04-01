
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
    total_coc_count = 1
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
                series_names.append("COC " + str(total_coc_count))
                current += 1
                multiplier += 1
                total_coc_count += 1
        current += 1
    return series_names

def create_final_raw_csv(dir_path_to_temp_csvs, dir_path_final_csvs):
    for f in os.listdir(dir_path_final_csvs):
        os.remove(os.path.join(dir_path_final_csvs, f))

    taskmaster_dfs = scrape_tm_details_to_dfs()
    build_temp_csvs(all_dfs=taskmaster_dfs, temp_dir=dir_path_to_temp_csvs)
    series_names = determine_series_names(all_input_dfs=taskmaster_dfs)
    for i, filename in enumerate(os.listdir(dir_path_to_temp_csvs)):
        print('processing', i, filename, series_names[i])
        f = os.path.join(dir_path_to_temp_csvs, filename)
        if os.path.isfile(f):
            parse_taskmaster_csv(infile=f, series_name=series_names[i], result_path=dir_path_final_csvs)

def merge_final_dataset(inpath_final_individual_csvs):
    arr = os.listdir(inpath_final_individual_csvs)
    os.chdir(inpath_final_individual_csvs)
    df = pd.concat(map(pd.read_csv, [val for val in arr if val.endswith(".csv")]), ignore_index=True)
    os.chdir("..")
    df.to_csv("Taskmaster Full Dataset.csv")

if __name__ == "__main__":
    dir_path_to_temp_csvs="temp_csvs"
    dir_path_final_csvs="final_season_csvs"
    create_final_raw_csv(dir_path_to_temp_csvs, dir_path_final_csvs)
    merge_final_dataset(inpath_final_individual_csvs=dir_path_final_csvs)