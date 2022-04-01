import pandas as pd

# series name
series = "Series 1"

# episode names
df = pd.read_csv("Series 1 (6).csv", skiprows=1)
df_episode_names = pd.DataFrame(df, columns= ['Task'])
mask = df['Task'].str.contains('Episode', case=False, na=False)
df_episode_names = df[mask]
episode_list = df_episode_names['Task'].tolist()
print(episode_list)

# contestant names
header_row = df.iloc[0]
contestant_names = [value for value in df.columns if value not in ['Task', 'Description']]
print(contestant_names)

# task descriptions
task_descriptions = df['Description'][df['Description'].notna()]
task_descriptions = task_descriptions[~task_descriptions.str.contains(r'^[^a-z]*$')]
task_list = task_descriptions.tolist()
print(task_list)


# put it all together
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df)


def get_task_score(contestant, task_description):
    score = 0
    try:
        # contestant_df = df[[contestant, "Description"]]
        # print(contestant_df)
        potential_task_df = df[df["Description"].str.match(task_description)][contestant]
        print(potential_task_df)
    except:
        print('errrrror')

    return score

# contestant_names = df.columns
print(get_task_score(contestant="Romesh Ranganathan", task_description="Prize: Most satisfying item."))

# print(df_episode_names[mask].sample(3))



# put it all together
# Season, Episode, Task Description, Contestant, Score
final_task_list = []

for task_description in task_list:
    task = {}
    season = None
    task_episode = None
    task_contestant = None
    task_score = None

    task_details = {}
    try:
        season = None
    except:
        pass

    try:
        task_episode = None
    except:
        pass

    try:
        task_contestant = None
    except:
        pass

    try:
        task_score = None
    except:
        pass
            
    task_details["season"] = season
    task_details["task_episode"] = task_episode
    task_details["task_description"] = task_description
    task_details["task_contestant"] = task_contestant
    task_details["task_score"] = task_score

    final_task_list.append(task_details)

