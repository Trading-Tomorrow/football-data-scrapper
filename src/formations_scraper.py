import pandas as pd
import time
import json
import os
from datafc.utils._setup_webdriver import setup_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------------
# 1. Load your CSV
# ----------------------------
CSV_PATH = "premierleague_2015_16_stats.csv"
df = pd.read_csv(CSV_PATH)

# Column name – adjust if needed
GAME_ID_COL = "game_id"

# Output file
OUTPUT_FILE = "lineups_data_2015_16.csv"

# ----------------------------
# 2. Setup Webdriver
# ----------------------------
driver = setup_webdriver()

# ----------------------------
# 3. Loop through all game_ids and fetch lineups
# ----------------------------
unique_game_ids = df[GAME_ID_COL].unique()
print(f"Found {len(unique_game_ids)} unique games.")


if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

all_records = []
records_buffer = []

try:
    for i, gid in enumerate(unique_game_ids):
        try:
            print(f"[{i+1}/{len(unique_game_ids)}] Fetching {gid} ...")
            
            url = f"https://api.sofascore.com/api/v1/event/{gid}/lineups"
            driver.get(url)
            
            pre_tag = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, "pre"))
            )
            
            data = json.loads(pre_tag.text)
            
            # Extract data for both teams
            for side in ['home', 'away']:
                team_data = data.get(side, {})
                formation = team_data.get('formation')
                players = team_data.get('players', [])
                
                # Get team name from CSV if possible
                row = df[df[GAME_ID_COL] == gid].iloc[0]
                team_name = row.get(f"{side}_team")
                
                for p_entry in players:
                    player = p_entry.get('player', {})
                    stats = p_entry.get('statistics', {})
                    
                    # Base record
                    rec = {
                        'game_id': gid,
                        'side': side,
                        'team_name': team_name,
                        'formation': formation,
                        'player_name': player.get('name'),
                        'player_id': player.get('id'),
                        'position': p_entry.get('position'),
                        'shirt_number': p_entry.get('shirtNumber'),
                        'substitute': p_entry.get('substitute'),
                        'rating': stats.get('rating'),
                        'minutes_played': stats.get('minutesPlayed'),
                    }
                    
                    # Add all stats flattened
                    for k, v in stats.items():
                        if isinstance(v, (int, float, str)):
                            rec[f'stat_{k}'] = v
                            
                    records_buffer.append(rec)

            # Add to main list
            all_records.extend(records_buffer)
            records_buffer = [] # Clear buffer

            # Save every 10 games (overwrite file to ensure column alignment)
            if (i + 1) % 10 == 0:
                pd.DataFrame(all_records).to_csv(OUTPUT_FILE, index=False)
                print(f"Saved progress to {OUTPUT_FILE} ({len(all_records)} records)")

            # Optional: avoid rate-limits
            time.sleep(5) # Reduced slightly from 10s to be faster, but safe.

        except Exception as e:
            print(f"Error for {gid}: {e}")

finally:
    if driver:
        driver.quit()
        
    # Save final
    if all_records:
        pd.DataFrame(all_records).to_csv(OUTPUT_FILE, index=False)
        print(f"Saved final records to {OUTPUT_FILE} ({len(all_records)} records)")
