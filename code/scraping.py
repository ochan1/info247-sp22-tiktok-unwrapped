from TikTokApi import TikTokApi
from TikTokApi import exceptions
import json
from multiprocessing import Pool
import sys
import re
import os
import csv

verify_fp = ""
START = 0
SAVE_INTERVAL = 1000

# https://github.com/davidteather/TikTok-Api/issues/403#issuecomment-971818109
ERROR_CODES_SKIPPED = [10204, 10215, 10216, 10217]

def process_tiktok(data_input, api):
    vid_number, id_date_link = data_input
    id, date, vid_link = id_date_link
    output_string = []
    try:
        video = api.video(id=id)
        hashtags = video.hashtags
        hashtag_names = [h.name for h in hashtags]
        output_string.append(str(vid_number))
        output_string.append(date)
        output_string.append(video.author.username)
        sound_string = ""
        if video.sound.title:
            sound_string = video.sound.title
        if video.sound.author:
            sound_string = sound_string + " - " + video.sound.author.username
        output_string.append(sound_string)
        output_string.append(vid_link)
        output_string.append("\"" + ",".join(hashtag_names) + "\"")
        return (0, output_string, data_input)
    except exceptions.TikTokException as e:
        err_str = str(e)
        search_regex = re.match("TikTok sent an unknown StatusCode of (\\d+)", err_str)
        if search_regex:
            error_code = search_regex.group(1)
            if error_code.isnumeric():
                error_code = int(error_code)
                if error_code in ERROR_CODES_SKIPPED:
                    return (-1, "{} - {} {}".format(error_code, vid_number, id), data_input)
        output_string.append(str(vid_number))
        output_string.append(str(id))
        output_string.append(err_str)
        return (1, output_string, data_input)
    except Exception as e:
        output_string.append(str(vid_number))
        output_string.append(str(id))
        output_string.append(str(e))
        print("Python error: ", output_string)
        if (str(e) == "Target page, context or browser has been closed"):
            raise e
        return (2, output_string, data_input)

def main(api):
    global START, SAVE_INTERVAL
    f = open('user_data.json')
    data = json.load(f)
    vid_list = data['Activity']['Video Browsing History']['VideoList']
    list_of_ids_and_dates = [(v['VideoLink'].split("/")[-2], v["Date"], v['VideoLink']) for v in vid_list]
    
    size = len(list_of_ids_and_dates)
    result = []
    data_input = [None, None]

    if len(sys.argv) > 1:
        START = int(sys.argv[1])
    
    if len(sys.argv) > 2:
        SAVE_INTERVAL = int(sys.argv[2])

    for i in range(START, size):
        data_input[0] = i
        data_input[1] = list_of_ids_and_dates[i]
        print(i, "out of", size)
        
        result.append(process_tiktok(data_input, api))

        if (i != 0) and ((i % SAVE_INTERVAL == 0) or (i == size - 1)):
            print("Outputing", START, "to", i)
            outfile = open("results_3-2-2_{}-{}.txt".format(START, i), 'w', encoding="utf-8")
            error_outfile = open("errors_3-2-2_{}-{}.txt".format(START, i), 'w', encoding="utf-8")
            tiktok_data_outfile = []
            error_data_outfile = []
            for r in result:
                status, msg, cahced_input = r
                if status == -1:
                    # skipped, no questions asked
                    print("Skipped", msg, cahced_input)
                    continue
                
                if status == 0:
                    tiktok_data_outfile.append(msg)
                else:
                    error_data_outfile.append(msg)
            
            tiktok_data_outfile_write = csv.writer(outfile)
            tiktok_data_outfile_write.writerows(tiktok_data_outfile)

            error_data_outfile_write = csv.writer(error_outfile)
            error_data_outfile_write.writerows(error_data_outfile)

            result.clear()

            outfile.close()
            error_outfile.close()

            if (i < size - 1):
                print("Restart script with START at", i + 1)
                break
    print("End of Function")

if __name__ == "__main__":
    api = TikTokApi(custom_verify_fp=verify_fp)
    main(api)
    print("Completion")
    # Not a clean kill, but sometimes freeze up
    os._exit(0)


