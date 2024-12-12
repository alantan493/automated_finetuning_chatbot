import os
import time
from datetime import datetime, timedelta
import threading

# Define the paths to the scripts for VM environment
scripts = {
    "STEP1smartscraper.py": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/STEP1smartscraper.py",
    "STEP1smartscraperdruglaws.py": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/STEP1smartscraperdruglaws.py",
    "STEP1smartscrapervapelaws.py": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/STEP1smartscrapervapelaws.py",
    "STEP2convertingwebscraptofinetuning.py": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/STEP2convertingwebscraptofinetuning.py",
    "STEP3updating_new_json_finetuning.py": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/STEP3updating_new_json_finetuning.py",
    "STEP4upload_newfinetune_model.py": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/STEP4upload_newfinetune_model.py",
}

# Max retry attempts for failed scripts
MAX_RETRIES = 3

def run_script(script_name, script_path, retry_count=0):
    """
    Runs the script and retries if it fails. 
    """
    try:
        print(f"Running {script_name}... (Attempt {retry_count + 1})")
        exit_code = os.system(f"python3 {script_path}")
        
        # If script ran successfully, return True
        if exit_code == 0:
            print(f"{script_name} ran successfully.")
            return True
        else:
            print(f"{script_name} failed to run.")
            return False

    except Exception as e:
        print(f"An error occurred while running {script_name}: {e}")
        return False

def run_scripts():
    success_list = []
    failure_list = []
    
    for script_name, script_path in scripts.items():
        retries = 0
        success = False

        # Retry until success or max retries reached
        while retries < MAX_RETRIES and not success:
            success = run_script(script_name, script_path, retries)
            retries += 1
        
        if success:
            success_list.append(script_name)
        else:
            failure_list.append(script_name)
            print(f"Max retries reached for {script_name}. It did not run successfully.")

    # Summary after running all scripts
    print("\nSummary of script execution:")
    
    if success_list:
        print("Scripts that ran successfully:")
        for script in success_list:
            print(f" - {script}")
    else:
        print("No scripts ran successfully.")
    
    if failure_list:
        print("Scripts that failed to run:")
        for script in failure_list:
            print(f" - {script}")
    else:
        print("No scripts failed.")

def run_at_midnight():
    """
    This function calculates the time difference between now and the next midnight (12 AM),
    then sleeps until that time and executes the script.
    """
    now = datetime.now()
    # Calculate the next midnight time (12:00 AM)
    next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # Calculate how many seconds until the next midnight
    sleep_duration = (next_midnight - now).total_seconds()
    print(f"Sleeping for {sleep_duration} seconds until next midnight (12:00 AM)...")
    time.sleep(sleep_duration)  # Sleep until midnight
    
    # Run the scripts at midnight
    while True:
        print("Starting to run the scripts at 12 AM.")
        run_scripts()
        
        # Sleep for 24 hours (86400 seconds) until the next midnight
        print("Sleeping for 24 hours until the next run...")
        time.sleep(86400)

if __name__ == "__main__":
    # Run the function in a separate thread to avoid blocking the main process
    thread = threading.Thread(target=run_at_midnight)
    thread.start()
