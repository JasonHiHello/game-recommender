from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="Exophase Scraper API", version="1.0.0")

@app.get("/games/{username}")
def get_games(username: str):
    url = f"https://www.exophase.com/user/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Profile not found or inaccessible")
        
    soup = BeautifulSoup(response.text, 'html.parser')
    games_list = []
    
    for card in soup.find_all('div', class_='game-box'):
        try:
            title = card.find('h3').text.strip()
            playtime_elem = card.find('div', class_='hours')
            playtime = playtime_elem.text.strip() if playtime_elem else "0 hours"
            last_played_elem = card.find('div', class_='last-played')
            last_played = last_played_elem.text.strip() if last_played_elem else "Unknown"
            
            games_list.append({
                "title": title,
                "playtime": playtime,
                "last_played": last_played
            })
        except AttributeError:
            continue
            
    return {"username": username, "games": games_list}