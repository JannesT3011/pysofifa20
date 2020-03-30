# Pysofifa20

Python package for seaching Fifa20 Teams/Players on https://sofifa.com !
NOTE: This project is in development and it isn't beautfiul code!

## Install
``python3 setup.py install --user``

### Reference

All functions:
``search_player_by_name(name)``
``get_player_info_by_link(link)``
``get_player_info_by_name(name)``
``search_team_by_name(name)``
``get_team_info_by_link(link)`` - without tactics! (coming soon)
``get_team_info_by_name(name)`` - without tactics! (coming soon)
``get_team_player(team)`` - coming soon

Example:
``Class: Client(USER_AGENT)`` </br>
``get_player_info_by_link(link)``:

```json
{
    "id": "",
    "name": "", 
    "age": "",
    "birthday": "",
    "positions": "",
    "rating": "",
    "potential": "", 
    "value": "",
    "wage": "",
    "link": "",
    "club": {
        "name": "",
        "link": "",
        "jersey_nr": "",
        "player_join_at": "",
        "contract_end": ""
    },
    "preferred_foot": "",
    "weak_foot": "",
    "skill_move": "",
    "work_rate": "",
    "international_reputation": "",
    "body_type": "",
    "real_face": "",
    "release_clause": ""
}
```

## TODO:
- add sphinx
- teams stuff