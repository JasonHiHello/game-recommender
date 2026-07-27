from fastapi import FastAPI, HTTPException
from curl_cffi import requests

app = FastAPI(title="Exophase Scraper API", version="2.0.0")

@app.get("/games/{username}")
def get_games(username: str):
    # Your internal Exophase Player ID
    player_id = "2416490"
    
    all_games = []
    
    # Let's fetch the first 2 pages of your library 
    for page in range(1, 3):
        # We hit the raw API endpoint you found
        url = f"https://api.exophase.com/public/player/{player_id}/games?page={page}&sort=1"
        response = requests.get(url, impersonate="chrome")
        
        if response.status_code == 200:
            # We don't even need to parse HTML. We just grab the raw JSON!
            data = response.json()
            all_games.append(data)
            
    if not all_games:
        raise HTTPException(status_code=404, detail="Failed to fetch from Exophase API")

    # We hand the raw JSON directly back to the AI. 
    # LLMs are native JSON readers and will understand the data perfectly.
    return {"username": username, "exophase_data": all_games}
