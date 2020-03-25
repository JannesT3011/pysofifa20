from bs4 import BeautifulSoup
import requests
from util import Postions
import re


class Client:
    def __init__(self, useragent:str):
        self.header = {"User-Agent": useragent}
        self.BASE_URL = "https://sofifa.com/"

    
    # Player Stuff
    def search_player_by_name(self, name:str) -> dict:
        data = {"result": []}
        search_var = f"players/?keyword={name}"
        page = requests.get(self.BASE_URL+search_var, headers=self.header)
        soup = BeautifulSoup(page.content, "html.parser")
        data_name = soup.find_all(class_="nowrap")
        for result in data_name:
            name = result.get("title")
            link = result.get("href")
            new_data = {"name": name, "link": self.BASE_URL+link}
            data["result"].append(new_data)

        return data
    
    def get_player_info_by_link(self, link:str) -> dict:
        page = requests.get(link, headers=self.header)
        soup = BeautifulSoup(page.content, "html.parser")
        general_data = soup.find(class_="meta bp3-text-overflow-ellipsis").get_text()
        rating_data = soup.find(class_="columns spacing").get_text()
        club_data = soup.find(class_="bp3-text-overflow-ellipsis pl text-right").get_text()
        full_name = general_data.split()[0] + " "+general_data.split()[1]
        misc_data = soup.find(class_="column col-6").get_text()
        
        data = {
            "id": re.findall('\((.*?)\)', soup.find(class_="info").get_text())[0].split("ID: ")[1],
            "name": soup.find(class_="info").get_text().split(" (")[0],
            "age": general_data.split("Age")[1][1:3],
            "birthday": re.findall("\((.*?)\)", soup.find(class_="info").get_text())[1],
            "positions": Postions().convert_postions(re.search(full_name+r"\ (.*?) Age", general_data).group(1)[1:]), 
            "rating": re.search(r"(.*?) Overall", rating_data).group(1),
            "potential": re.search(r"(.*?) Potential", rating_data).group(1),
            "value": rating_data.split("\n")[-4],
            "wage": rating_data.split("\n")[-2],
            "link": link,
            "club": {
                "name": club_data.split()[0] + club_data.split()[1],
                #"link": "",
                "postion": club_data.split("Position")[1][:2],
                "jersey_nr": re.search(r"Number(.*?)Joined", club_data).group(1),
                "player_join_at": re.search(r"Joined(.*?)Contract", club_data).group(1),
                "contract_end": club_data.split("Until")[1]
            },
            "preferred_foot": misc_data.split()[1].split("Foot")[1],
            "weak_foot": misc_data.split()[3].split("Foot")[1],
            "skill_move": misc_data.split()[6].split("Moves")[1],
            "work_rate": misc_data.split()[9]+misc_data.split()[10],
            "international_reputation": misc_data.split()[12].split("Reputation")[1],
            "body_type": misc_data.split()[15].split("Type")[1]+misc_data.split()[16],
            "real_face": misc_data.split()[18].split("Face")[1],
            "release_clause": misc_data.split()[20].split("Clause")[1]
        }

        return data
    
    #def get_player_info_by_name(self, name:str) -> dict:
    #    todo: finishen
    #    return {}

    
    # Team Stuff
    # soon
