from flask import Flask, request
from flask_cors import CORS
from espn_api.basketball import League

SWID = '{C516A8C5-D0C6-4FD1-982D-26689751FD9B}'
ESPN_S2 = "AEBpsxN2nD86htHkH%2FR3gmJLiAzT4JaTwJgtpuY96AVxNJtgnpf6p7bXkQG26jXvo19mEz5SI7NNX%2FCfENYLByD%2BTu6fC3BKNH7%2FpEZrIyTENkpgv95UGmGkmPqlTRgVN%2FOOpnaS13WahL8F%2B1MxPHTgaHGNVHDS8ut3pXFnTdxrAfYGFjf09UaNEP5ErqR%2F2ncB3RdvXf%2FBX93m0HFCZhl87s0uP1pCRdsaDn3Ps0MsPbU%2B5Rib6636edbAdZilhizcPYeFyTJT4d0AWg7MwpaUaBg61PMlH7axMJd7C3iKFQ%3D%3D"
LEAGUE_ID = 852079681
SEASON = 2025

print("Fetching league info...")
league = League(league_id=LEAGUE_ID, year=SEASON, swid=SWID, espn_s2=ESPN_S2)
teams = league.teams

print("Fetching player info...")
players = {}
player_name_id_dict = {}

for t in league.teams:
    for p in t.roster:
        players[str(p.playerId)] = p

for p in league.free_agents():
    players[str(p.playerId)] = p

for id, player in players.items():
    player_name_id_dict[player.name.lower()] = id

print("Starting server...")
app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return "<p>Hello from Fantasy Stats API</p>"

@app.route("/teams")
def get_teams():
    team_info = [{"name": t.team_name, "id": t.team_id, "owners": t.owners, "wins": t.wins, "losses": t.losses} for t in teams]
    return {"teams": team_info}, 200

@app.route("/teams/<team_id>/players")
def get_players_by_team(team_id):
    for t in teams:
        if t.team_id == int(team_id):
            player_info = [league.player_info(p.name).__dict__ for p in t.roster]
            formatted_player_info = []

            for player in player_info:
                player["stats"]["games_played"] = []
                for key, value in player["stats"].items():
                    if type(value) is dict and "date" in value and value["date"] != None:
                        player["stats"]["games_played"].append(value)
                formatted_player_info.append(player)

            return {"players": formatted_player_info}, 200

    return {"error": "Invalid team id"}, 404

@app.route("/players/free_agents")
def get_free_agents():
    player_info = [{
        "name": p.name,
        "id": p.playerId,
        "pro_team": p.proTeam,
        "injury_status": p.injuryStatus,
        "stats": p.stats,
        "total_points": p.total_points,
        "average_points": p.avg_points,
        "position": p.position
        } for p in league.free_agents()]

    return {"players": player_info}, 200

@app.route("/players/<player_id>")
def get_player(player_id):
    if player_id in players:
        p = players[player_id]
        player = {"name": p.name,
                  "id": p.playerId,
                  "pro_team": p.proTeam,
                  "injury_status": p.injuryStatus,
                  "stats": p.stats,
                  "total_points": p.total_points,
                  "average_points": p.avg_points,
                  "position": p.position
                  }
        return {"player": player}, 200
    return {"error": "Player not found"}, 404

@app.route("/players")
def search_players():
    query = request.args.get("search_query")
    if not query:
        return {"error": "Please provide a search query"}, 400

    matching_names = [key for key in player_name_id_dict if query.lower() in key.lower()]
    if len(matching_names) == 0:
        return {"error": "No players found"}, 404

    player_ids = [player_name_id_dict[name] for name in matching_names]
    return {"player_ids": player_ids}, 200

