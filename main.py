from fastapi import FastAPI, HTTPException
from curl_cffi import requests
import json

app = FastAPI(title="Exophase Scraper API", version="3.0.0")

@app.get("/games/{username}")
def get_games(username: str):
    player_id = "2416490"  # Your Exophase ID
    formatted_games = []
    
    for page in range(1, 3):
        url = f"https://api.exophase.com/public/player/{player_id}/games?page={page}&sort=1"
        response = requests.get(url, impersonate="chrome")
        
        if response.status_code == 200:
            res_json = response.json()
            
            # The API might store games in res_json["list"] or res_json["games"]["list"]
            # This safely finds the list wherever it is.
            raw_games = res_json.get("list", [])
            if not raw_games and "games" in res_json:
                raw_games = res_json["games"].get("list", [])
                
            for item in raw_games:
                title = item.get("title", "Unknown Title")
                hours = item.get("hours", item.get("playtime", 0))
                
                # Exophase sometimes uses "last_played_timestamp" or similar. 
                # We pull whatever they have, or default to "Unknown" to satisfy Coze.
                last_played = item.get("last_played", item.get("last_played_str", "Recently"))
                
                formatted_games.append({
                    "title": str(title),
                    "playtime": f"{hours} hours",
                    "last_played": str(last_played) # Required by Coze schema
                })

    if not formatted_games:
        raise HTTPException(status_code=404, detail="No games found. Exophase API structure may have changed.")

    return {"username": username, "games": formatted_games}
