from bs4 import BeautifulSoup
import requests
from .util import Postions
import re


class Pysofifa:
    """ The client to use this package
    :param useragent: Your user agent - type my user agent in your browser
    :type useragent: str
    """
    def __init__(self, useragent:str):
        """ Constructor method
        """
        self.header = {"User-Agent": useragent}
        self.BASE_URL = "https://sofifa.com/"

    
    # Player Stuff
    def search_players_by_name(self, name:str) -> dict:
        """Search a player by name
        :param name: Name of the player you want to search <https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html>
        :type name: str
        :return: Dict. of results
        :rtype: dict
        """
        name = name.replace(" ", "+")
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
        """Get all infos about a player by using a link
        :param link: link to player profile
        :type link: str
        :return: Dict with player infos
        :retype: dict
        """
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
    
    def get_player_info_by_name(self, name:str) -> dict:
        """Get all infos about a player by using a name
        :param name: Name of the player
        :type name: str
        :retrun: Dict with player infos
        :rtype: dict
        """
        players = self.search_players_by_name(name)["result"]
        infos = []
        for link in players:
            info = self.get_player_info_by_link(link["link"])
            infos.append(info)
        
        if len(infos) == 1:
            return {"result": infos[0]}

        return {"result": infos}
    
    # Team Stuff
    def search_team_by_name(self, name:str) -> dict:
        """Search a Team
        :param name: Name of the team
        :type name: str
        :return: Search results
        :ryte: dict
        """
        name = name.replace(" ", "+")
        data = {"result": []}
        search_var = f"teams/?keyword={name}"
        page = requests.get(self.BASE_URL+search_var, headers=self.header)
        soup = BeautifulSoup(page.content, "html.parser")
        for result in soup.find_all("a", href=True, text=True):
            if str(result).startswith('<a href="/team'):
                link = result.get("href")
                name = link.split("/")[3]
                new_data = {"name": name, "link": self.BASE_URL+link}
                data["result"].append(new_data)
        
        return data
    
    def get_team_info_by_link(self, link:str) -> dict:
        """Get infos about a team by using a link
        :param link: link to team
        :type link: str
        :return: Team infos
        :rtype: dict
        """
        page = requests.get(link, headers=self.header)
        soup = BeautifulSoup(page.content, "html.parser")
        info_data = soup.find(class_="info").get_text()
        ratings_data = soup.find(class_="columns").get_text()
        tactics_data_one = soup.find(class_="clearfix").get_text()
        misc_data = soup.find(class_="column col-4").get_text()

        data = {
            "id": info_data.split("ID: ")[1].split(")")[0],
            "name": info_data.split(" (")[0],
            "link": link,
            "league": info_data.split("2020\n ")[1][:-1],
            "ratings": {
                "overall": re.search(r"(.*?)Overall", ratings_data).group(1),
                "attack": re.search(r"(.*?)Attack", ratings_data).group(1),
                "midfield": re.search(r"(.*?)Midfield", ratings_data).group(1),
                "defence": re.search(r"(.*?)Defence", ratings_data).group(1)
            },
            #"tactics": {
            #    "defence": {
            #        "style": tactics_data_one.split("Style")[1],
            #        "team_width": "",
            #        "depth": ""
            #    },
            #    "offense": {
            #        "style": "",
            #        "width": "",
            #        "players_in_box": "",
            #        "corners": "",
            #        "free_kicks": ""
            #    }
            #},
            "misc": { # \n\nShort Free KickBruno Fernandes\n\nLong Free KickBruno Fernandes\n\nLeft Short Free KickBruno Fernandes\n\nRight Short Free KickBruno Fernandes\n\nPenaltiesBruno Fernandes\n\nLeft CornerBruno Fernandes\n\nRight CornerFred\n\n\n'
                "home_stadium": misc_data.split("Stadium")[1].split("Rival")[0][:-2],
                "rival_team": misc_data.split("Rival Team")[1].split("International")[0][:-1],
                "international_prestige": misc_data.split("Prestige")[1].split("Domestic")[0][-1:],
                "domestic_prestige": misc_data.split("Prestige")[2].split("Transfer")[0][1:-2],
                "transfer_budget": misc_data.split("Budget")[1].split("Starting")[0],
                "starting_team_average_age": misc_data.split("Age")[1].split("Whole")[0][:-1],
                "team_average_age": misc_data.split("Age")[2].split("Captain")[0][:-2],
                "captain": misc_data.split("Captain")[1].split("Short")[0][:-2],
                "short_free_kick": misc_data.split("Kick")[1].split("Long")[0][:-2],
                "long_free_kick": misc_data.split("Kick")[2].split("Left")[0][:-2],
                "left_short_free_kick": misc_data.split("Kick")[3].split("Right")[0][:-2],
                "right_short_free_kick": misc_data.split("Kick")[4].split("Penalties")[0][:-2],
                "penalties": misc_data.split("Penalties")[1].split("Left")[0][:-2],
                "left_corner": misc_data.split("Left Corner")[1].split("Right")[0][:-2],
                "right_corner": misc_data.split("Corner")[2][:-3]
            }
        }
        return data
    
    def get_team_info_by_name(self, name:str) -> dict:
        """Get infos about a team by using the name
        :param name: Name of the team
        :type name: str
        :return: Team infos
        :rtype: dict
        """
        team_link = self.search_team_by_name(name)["result"]
        infos = []
        for link in team_link:
            info = self.get_team_info_by_link(link["link"])
            infos.append(info)

        if len(infos) == 1:
            return {"result": infos[0]}

        return {"result": infos}
    
    def get_team_players(self, team:str) -> list:
        """Get all players of a team
        :param team: Name of the team
        :type team: str
        :return: All players of the team
        :rtype: list
        """
        return