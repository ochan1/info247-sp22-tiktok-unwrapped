import numpy as np
import pandas as pd

tiktok_data = pd.read_csv("results.csv")

# id / view time / url / hashtags (exploded or not) / author
tiktok_data.columns = ["id", "view time", "author", "sound", "url", "hashtags"]

tiktok_data["hashtags"] = tiktok_data["hashtags"].str.split(",")

print(tiktok_data[["id", "hashtags"]])
tiktok_data_id_hashtags = tiktok_data[["id", "hashtags"]].explode("hashtags")
print(tiktok_data)
tiktok_data_no_hashtags = tiktok_data.drop("hashtags", axis=1)

tiktok_data_no_hashtags.to_csv("tiktok_video_data.csv", index=False)
tiktok_data_id_hashtags.to_csv("tiktok_video_hashtags_exploded.csv", index=False)
