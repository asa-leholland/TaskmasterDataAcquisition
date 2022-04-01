import pandas as pd

# series name
provided_series = "Series 1"

infile_name = "Series 1 (6).csv"



def get_task_episode(task_description, complete_df):
    task_episode = None
    df = complete_df
    # new_df = df.iloc[1: , :]

    new_header = df.iloc[0] #grab the first row for the header
    new_df = df[1:] #take the data less the header row
    new_df.columns = new_header #set the he

    # obtain the index of the row containing task description
    match_condition = new_df["Description"] == task_description
    description_index = new_df.index[match_condition].tolist()[0]
    
    # starting at that index, decrement the index by one, checking if the row contains the term "Episode"
    for i in range(description_index, 0, -1):
        if 'Episode' in df.iloc[i][0]:
            task_episode = df.iloc[i][0]
            break

    # return the string of that episode
    if task_episode is None:
        print('Error: episode not found for', task_description)

    return task_episode

def get_task_score(contestant, task_description, complete_df):
    df = complete_df
    score = 0

    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the he

    final_df = df[df["Description"] == task_description]
    result_list = final_df[contestant].tolist()
    score = result_list[0]

    score_translations = {
        '✔': 1,
        '✘': 0,
        '-': 0,
        '–': 0,
        "DQ": 0,
        '-1': -1,
        '-2': -2,
        '-3': -3,
        '-4': -4,
        '-5': -5
    }

    if not score.isdigit():

        if score in score_translations:
            score = score_translations[score]
        else:
            print("Error: unhandled score value:", score, task_description)

    return score

def generate_end_csv(task_list, contestant_names, provided_series, complete_df):



    # put it all together
    # Season, Episode, Task Description, Contestant, Score
    final_task_list = []

    for task_description_string in task_list:
        task = {}
        season = None
        task_episode = None
        task_contestant = None
        task_score = None

        for contestant_name in contestant_names:

            task_details = {}
            season = provided_series
            task_episode = get_task_episode(task_description=task_description_string, complete_df=complete_df)
            task_contestant = contestant_name
            task_score = get_task_score(contestant=contestant_name, task_description=task_description_string, complete_df=complete_df)
            task_details["season"] = season
            task_details["task_episode"] = task_episode
            task_details["task_description"] = task_description_string
            task_details["task_contestant"] = task_contestant
            task_details["task_score"] = task_score

            final_task_list.append(task_details)


    final_result_df = pd.DataFrame(final_task_list)
    final_result_df.to_csv(f"{provided_series} Task Data.csv")

def parse_taskmaster_csv(infile, series_name):

    # episode names
    df = pd.read_csv(infile, skiprows=1)
    full_df = pd.read_csv(infile)
    df_episode_names = pd.DataFrame(df, columns= ['Task'])
    mask = df['Task'].str.contains('Episode', case=False, na=False)
    df_episode_names = df[mask]
    episode_list = df_episode_names['Task'].tolist()

    # contestant names
    series_contestant_names = [value for value in df.columns if value not in ['Task', 'Description']]

    # task descriptions
    task_descriptions = df['Description'][df['Description'].notna()]
    task_descriptions = task_descriptions[~task_descriptions.str.contains(r'^[^a-z]*$')]
    series_task_list = task_descriptions.tolist()

    generate_end_csv(task_list=series_task_list, contestant_names=series_contestant_names, provided_series=series_name, complete_df=full_df)


# parse_taskmaster_csv(infile=infile_name, series_name=provided_series)