from fastapi import FastAPI, HTTPException
from curl_cffi import requests
from bs4 import BeautifulSoup

app = FastAPI(title="Exophase Scraper API", version="1.0.0")

@app.get("/games/{username}")
def get_games(username: str):
    url = f"https://www.exophase.com/user/{username}/"
    response = requests.get(url, impersonate="chrome")
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f"HTTP Error {response.status_code}")
        
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
            
    # --- NEW DEBUGGING LOGIC ---
    if len(games_list) == 0:
        page_title = soup.title.text.strip() if soup.title else "No Title"
        return {
            "username": username,
            "error": "The scraper loaded a page, but found 0 games.",
            "page_title": page_title,
            "html_snippet": response.text[:800] # Returns the first 800 characters of the page
        }
        
    return {"username": username, "games": games_list}
