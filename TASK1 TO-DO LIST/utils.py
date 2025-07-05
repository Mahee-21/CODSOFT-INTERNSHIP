import pandas as pd
import json
import os

def load_tasks(file_path="tasks.csv"):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Title", "Due Date", "Status"])

def save_tasks(df, file_path="tasks.csv"):
    df.to_csv(file_path, index=False)

def load_lottie(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Lottie file not found at {path}")
    except json.JSONDecodeError:
        print(f"⚠️ Invalid JSON format in {path}")
    return None
