To use the code here, you will need to install Python

We used Python 3.9 in our case

Please note the Shell scripts were ran for a Windows computer via Git Bash. The Python is system independent (as long as it can run Python). The only thing that you may need to modify for a Linux or Mac run are a few file path strings in the `run_scraping.sh` Shell script.

If you made any significant changes to the `run_scraping.sh` Shell script, feel free to take inspiration from the `run_scraping_sanity.sh` which can output the commands that the `run_scraping.sh` will run, but won't run the Python code.

Instructions to use:

1. Start a Virtual Environment: `python3 -m venv .venv`

2. Access the virtual environment. On Linux or Mac: `source .venv/bin/activate`. On Windows: `.venv\Scripts\activate` on Windows.

3. Install the Unofficial TikTok API: `pip install TikTokApi`

4. Per the Unofficial TikTok API instructions, setup the library: `python3 -m playwright install`

5. Have the 'user_data.json' in the same folder as the Python and Shell code

6. If you know the cap, edit that in the `run_scraping.sh` script. If not, let the shell script run once during the later instructions and note the max number and then edit it.

7. Modify the Virtual Environment access line and Python execution command on top of the `run_scraping.sh` as appropriate

8. Run the `run_scraping.sh` Shell script

9. Combine all the files: `cat results_3-2-2_*.txt > results.csv`

10. Open the `results.csv` in Excel and sort by `id`, then save the file

11. To create two additional files for Video Metadata and List of Hashtags to Video IDs, run the `process_data.py` code by: `python3 process_data.py`. Please make sure you have `results.csv` from a previous step.
