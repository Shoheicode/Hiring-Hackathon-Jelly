# Import Required Module
import requests
from bs4 import BeautifulSoup
 
# Web URL
Web_url = "http://localhost:3000/"
 
# Get URL Content
r = requests.get(Web_url)
 
# Parse HTML Code
soup = BeautifulSoup(r.content, 'html.parser')

print(soup)
 
# List of all video tag
video_tags = soup.findAll('button')
videoa = soup.findAll('div')
print("Total ", len(videoa))
print("Total ", len(video_tags), "videos found")
 
if len(video_tags) != 0:
    for video_tag in video_tags:
        video_url = video_tag.find("video")['src']
        print(video_url)
else:
    print("no videos found")