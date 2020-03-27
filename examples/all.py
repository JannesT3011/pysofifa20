from ..pysofifa20.client import Client

pysofifa = Client("YOUR USER AGENT")

# search a player
search_player = pysofifa.search_players_by_name("Messi")
print(search_player)

# get player info by link
player_info_link = pysofifa.get_player_info_by_link("https://sofifa.com/player/158023/lionel-messi/200030/")
print(player_info_link)

# get player info by name
player_info_name = pysofifa.get_player_info_by_name("Messi")
print(player_info_name)

# search team
search_team = pysofifa.search_team_by_name("Amsterdam")
print(search_team)
