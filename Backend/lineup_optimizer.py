
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "fantasy_db"

PLAYERS = [
    # --- EXPANDED QUARTERBACKS (QB) - IDs 101-132 ---
    {"id": 101, "name": "Josh Allen", "team": "BUF", "position": "QB", "projection": 24.5},
    {"id": 102, "name": "Lamar Jackson", "team": "BAL", "position": "QB", "projection": 23.9},
    {"id": 103, "name": "Jayden Daniels", "team": "WAS", "position": "QB", "projection": 22.8},
    {"id": 104, "name": "Jalen Hurts", "team": "PHI", "position": "QB", "projection": 22.5},
    {"id": 105, "name": "Joe Burrow", "team": "CIN", "position": "QB", "projection": 22.2},
    {"id": 106, "name": "Patrick Mahomes II", "team": "KC", "position": "QB", "projection": 21.9},
    {"id": 107, "name": "Bo Nix", "team": "DEN", "position": "QB", "projection": 21.6},
    {"id": 108, "name": "Baker Mayfield", "team": "TB", "position": "QB", "projection": 20.5},
    {"id": 109, "name": "Kyler Murray", "team": "ARI", "position": "QB", "projection": 20.3},
    {"id": 110, "name": "Dak Prescott", "team": "DAL", "position": "QB", "projection": 20.1},
    {"id": 111, "name": "Brock Purdy", "team": "SF", "position": "QB", "projection": 19.8},
    {"id": 112, "name": "Justin Fields", "team": "NYJ", "position": "QB", "projection": 19.5},
    {"id": 113, "name": "Drake Maye", "team": "NE", "position": "QB", "projection": 19.2},
    {"id": 114, "name": "Caleb Williams", "team": "CHI", "position": "QB", "projection": 18.9},
    {"id": 115, "name": "Justin Herbert", "team": "LAC", "position": "QB", "projection": 18.6},
    {"id": 116, "name": "Jared Goff", "team": "DET", "position": "QB", "projection": 18.3},
    {"id": 117, "name": "Jordan Love", "team": "GB", "position": "QB", "projection": 18.0},
    {"id": 118, "name": "Trevor Lawrence", "team": "JAC", "position": "QB", "projection": 17.5},
    {"id": 119, "name": "C.J. Stroud", "team": "HOU", "position": "QB", "projection": 17.1},
    {"id": 120, "name": "J.J. McCarthy", "team": "MIN", "position": "QB", "projection": 16.8},
    {"id": 121, "name": "Tua Tagovailoa", "team": "MIA", "position": "QB", "projection": 16.5},
    {"id": 122, "name": "Bryce Young", "team": "CAR", "position": "QB", "projection": 16.2},
    {"id": 123, "name": "Michael Penix Jr.", "team": "ATL", "position": "QB", "projection": 15.9},
    {"id": 124, "name": "Geno Smith", "team": "LV", "position": "QB", "projection": 15.6},
    {"id": 125, "name": "Matthew Stafford", "team": "LAR", "position": "QB", "projection": 15.3},
    {"id": 126, "name": "Cam Ward", "team": "TEN", "position": "QB", "projection": 15.0},
    {"id": 127, "name": "Sam Darnold", "team": "SEA", "position": "QB", "projection": 14.8},
    {"id": 128, "name": "Aaron Rodgers", "team": "PIT", "position": "QB", "projection": 14.5},
    {"id": 129, "name": "Daniel Jones", "team": "IND", "position": "QB", "projection": 14.2},
    {"id": 130, "name": "Russell Wilson", "team": "NYG", "position": "QB", "projection": 14.0},
    {"id": 131, "name": "Joe Flacco", "team": "CIN", "position": "QB", "projection": 13.8},
    {"id": 132, "name": "Anthony Richardson Sr.", "team": "IND", "position": "QB", "projection": 13.5},
    
    # --- EXPANDED RUNNING BACKS (RB) - IDs 201-234 ---
    {"id": 201, "name": "Bijan Robinson", "team": "ATL", "position": "RB", "projection": 22.0},
    {"id": 202, "name": "Jahmyr Gibbs", "team": "DET", "position": "RB", "projection": 21.0},
    {"id": 203, "name": "Saquon Barkley", "team": "PHI", "position": "RB", "projection": 19.5},
    {"id": 204, "name": "Christian McCaffrey", "team": "SF", "position": "RB", "projection": 18.9},
    {"id": 205, "name": "Ashton Jeanty", "team": "LV", "position": "RB", "projection": 17.5},
    {"id": 206, "name": "De'Von Achane", "team": "MIA", "position": "RB", "projection": 17.0},
    {"id": 207, "name": "Derrick Henry", "team": "BAL", "position": "RB", "projection": 16.5},
    {"id": 208, "name": "Chase Brown", "team": "CIN", "position": "RB", "projection": 16.0},
    {"id": 209, "name": "Bucky Irving", "team": "TB", "position": "RB", "projection": 15.5},
    {"id": 210, "name": "Josh Jacobs", "team": "GB", "position": "RB", "projection": 15.0},
    {"id": 211, "name": "Jonathan Taylor", "team": "IND", "position": "RB", "projection": 14.8},
    {"id": 212, "name": "Kyren Williams", "team": "LAR", "position": "RB", "projection": 14.5},
    {"id": 213, "name": "Alvin Kamara", "team": "NO", "position": "RB", "projection": 14.2},
    {"id": 214, "name": "James Cook III", "team": "BUF", "position": "RB", "projection": 14.0},
    {"id": 215, "name": "Omarion Hampton", "team": "LAC", "position": "RB", "projection": 13.7},
    {"id": 216, "name": "Kenneth Walker III", "team": "SEA", "position": "RB", "projection": 13.5},
    {"id": 217, "name": "Breece Hall", "team": "NYJ", "position": "RB", "projection": 13.2},
    {"id": 218, "name": "TreVeyon Henderson", "team": "NE", "position": "RB", "projection": 13.0},
    {"id": 219, "name": "Chuba Hubbard", "team": "CAR", "position": "RB", "projection": 12.8},
    {"id": 220, "name": "James Conner", "team": "ARI", "position": "RB", "projection": 12.5},
    {"id": 221, "name": "Tony Pollard", "team": "TEN", "position": "RB", "projection": 12.3},
    {"id": 222, "name": "D'Andre Swift", "team": "CHI", "position": "RB", "projection": 12.1},
    {"id": 223, "name": "RJ Harvey", "team": "DEN", "position": "RB", "projection": 11.9},
    {"id": 224, "name": "Isiah Pacheco", "team": "KC", "position": "RB", "projection": 11.7},
    {"id": 225, "name": "David Montgomery", "team": "DET", "position": "RB", "projection": 11.5},
    {"id": 226, "name": "Aaron Jones Sr.", "team": "MIN", "position": "RB", "projection": 11.3},
    {"id": 227, "name": "Jaylen Warren", "team": "PIT", "position": "RB", "projection": 11.1},
    {"id": 228, "name": "Tyrone Tracy Jr.", "team": "NYG", "position": "RB", "projection": 10.9},
    {"id": 229, "name": "Travis Etienne Jr.", "team": "JAC", "position": "RB", "projection": 10.7},
    {"id": 230, "name": "Kaleb Johnson", "team": "PIT", "position": "RB", "projection": 10.5},
    {"id": 231, "name": "Zach Charbonnet", "team": "SEA", "position": "RB", "projection": 10.3},
    {"id": 232, "name": "Jordan Mason", "team": "MIN", "position": "RB", "projection": 10.1},
    {"id": 233, "name": "Javonte Williams", "team": "DAL", "position": "RB", "projection": 9.9},
    {"id": 234, "name": "J.K. Dobbins", "team": "DEN", "position": "RB", "projection": 9.7},
    
    # --- EXPANDED WIDE RECEIVERS (WR) - IDs 301-359 ---
    {"id": 301, "name": "Ja'Marr Chase", "team": "CIN", "position": "WR", "projection": 22.5},
    {"id": 302, "name": "CeeDee Lamb", "team": "DAL", "position": "WR", "projection": 22.1},
    {"id": 303, "name": "Justin Jefferson", "team": "MIN", "position": "WR", "projection": 21.8},
    {"id": 304, "name": "Malik Nabers", "team": "NYG", "position": "WR", "projection": 21.4},
    {"id": 305, "name": "Amon-Ra St. Brown", "team": "DET", "position": "WR", "projection": 21.0},
    {"id": 306, "name": "Nico Collins", "team": "HOU", "position": "WR", "projection": 20.6},
    {"id": 307, "name": "Puka Nacua", "team": "LAR", "position": "WR", "projection": 20.2},
    {"id": 308, "name": "Brian Thomas Jr.", "team": "JAC", "position": "WR", "projection": 19.8},
    {"id": 309, "name": "Drake London", "team": "ATL", "position": "WR", "projection": 19.4},
    {"id": 310, "name": "A.J. Brown", "team": "PHI", "position": "WR", "projection": 19.0},
    {"id": 311, "name": "Ladd McConkey", "team": "LAC", "position": "WR", "projection": 18.6},
    {"id": 312, "name": "Jaxon Smith-Njigba", "team": "SEA", "position": "WR", "projection": 18.2},
    {"id": 313, "name": "Tee Higgins", "team": "CIN", "position": "WR", "projection": 17.8},
    {"id": 314, "name": "Garrett Wilson", "team": "NYJ", "position": "WR", "projection": 17.4},
    {"id": 315, "name": "Mike Evans", "team": "TB", "position": "WR", "projection": 17.0},
    {"id": 316, "name": "Tyreek Hill", "team": "MIA", "position": "WR", "projection": 16.6},
    {"id": 317, "name": "Davante Adams", "team": "LAR", "position": "WR", "projection": 16.2},
    {"id": 318, "name": "Terry McLaurin", "team": "WAS", "position": "WR", "projection": 15.8},
    {"id": 319, "name": "Marvin Harrison Jr.", "team": "ARI", "position": "WR", "projection": 15.4},
    {"id": 320, "name": "Tetairoa McMillan", "team": "CAR", "position": "WR", "projection": 15.0},
    {"id": 321, "name": "DJ Moore", "team": "CHI", "position": "WR", "projection": 14.6},
    {"id": 322, "name": "Courtland Sutton", "team": "DEN", "position": "WR", "projection": 14.2},
    {"id": 323, "name": "DK Metcalf", "team": "PIT", "position": "WR", "projection": 13.8},
    {"id": 324, "name": "DeVonta Smith", "team": "PHI", "position": "WR", "projection": 13.4},
    {"id": 325, "name": "Xavier Worthy", "team": "KC", "position": "WR", "projection": 13.0},
    {"id": 326, "name": "Calvin Ridley", "team": "TEN", "position": "WR", "projection": 12.7},
    {"id": 327, "name": "Jaylen Waddle", "team": "MIA", "position": "WR", "projection": 12.4},
    {"id": 328, "name": "George Pickens", "team": "DAL", "position": "WR", "projection": 12.1},
    {"id": 329, "name": "Jameson Williams", "team": "DET", "position": "WR", "projection": 11.8},
    {"id": 330, "name": "Zay Flowers", "team": "BAL", "position": "WR", "projection": 11.5},
    {"id": 331, "name": "Chris Olave", "team": "NO", "position": "WR", "projection": 11.2},
    {"id": 332, "name": "Emeka Egbuka", "team": "TB", "position": "WR", "projection": 10.9},
    {"id": 333, "name": "Travis Hunter", "team": "JAC", "position": "WR", "projection": 10.6},
    {"id": 334, "name": "Rome Odunze", "team": "CHI", "position": "WR", "projection": 10.3},
    {"id": 335, "name": "Jerry Jeudy", "team": "CLE", "position": "WR", "projection": 10.0},
    {"id": 336, "name": "Stefon Diggs", "team": "NE", "position": "WR", "projection": 9.8},
    {"id": 337, "name": "Ricky Pearsall", "team": "SF", "position": "WR", "projection": 9.6},
    {"id": 338, "name": "Rashee Rice", "team": "KC", "position": "WR", "projection": 9.4},
    {"id": 339, "name": "Jakobi Meyers", "team": "JAC", "position": "WR", "projection": 9.2},
    {"id": 340, "name": "Matthew Golden", "team": "GB", "position": "WR", "projection": 9.0},
    {"id": 341, "name": "Deebo Samuel Sr.", "team": "WAS", "position": "WR", "projection": 8.8},
    {"id": 342, "name": "Jauan Jennings", "team": "SF", "position": "WR", "projection": 8.6},
    {"id": 343, "name": "Khalil Shakir", "team": "BUF", "position": "WR", "projection": 8.4},
    {"id": 344, "name": "Michael Pittman Jr.", "team": "IND", "position": "WR", "projection": 8.2},
    {"id": 345, "name": "Josh Downs", "team": "IND", "position": "WR", "projection": 8.0},
    {"id": 346, "name": "Jordan Addison", "team": "MIN", "position": "WR", "projection": 7.8},
    {"id": 347, "name": "Cooper Kupp", "team": "SEA", "position": "WR", "projection": 7.6},
    {"id": 348, "name": "Chris Godwin Jr.", "team": "TB", "position": "WR", "projection": 7.4},
    {"id": 349, "name": "Jayden Reed", "team": "GB", "position": "WR", "projection": 7.2},
    {"id": 350, "name": "Darnell Mooney", "team": "ATL", "position": "WR", "projection": 7.0},
    {"id": 351, "name": "Keon Coleman", "team": "BUF", "position": "WR", "projection": 6.8},
    {"id": 352, "name": "Rashid Shaheed", "team": "SEA", "position": "WR", "projection": 6.6},
    {"id": 353, "name": "Christian Kirk", "team": "HOU", "position": "WR", "projection": 6.4},
    {"id": 354, "name": "Marvin Mims Jr.", "team": "DEN", "position": "WR", "projection": 6.2},
    {"id": 355, "name": "Cedric Tillman", "team": "CLE", "position": "WR", "projection": 6.0},
    {"id": 356, "name": "Rashod Bateman", "team": "BAL", "position": "WR", "projection": 5.8},
    {"id": 357, "name": "Luther Burden III", "team": "CHI", "position": "WR", "projection": 5.6},
    {"id": 358, "name": "Jayden Higgins", "team": "HOU", "position": "WR", "projection": 5.4},
    {"id": 359, "name": "Keenan Allen", "team": "LAC", "position": "WR", "projection": 5.2},
    
    # --- EXPANDED TIGHT ENDS (TE) - IDs 401-428 ---
    {"id": 401, "name": "Brock Bowers", "team": "LV", "position": "TE", "projection": 17.0},
    {"id": 402, "name": "Trey McBride", "team": "ARI", "position": "TE", "projection": 16.5},
    {"id": 403, "name": "George Kittle", "team": "SF", "position": "TE", "projection": 16.0},
    {"id": 404, "name": "Sam LaPorta", "team": "DET", "position": "TE", "projection": 15.5},
    {"id": 405, "name": "T.J. Hockenson", "team": "MIN", "position": "TE", "projection": 15.0},
    {"id": 406, "name": "Travis Kelce", "team": "KC", "position": "TE", "projection": 14.5},
    {"id": 407, "name": "David Njoku", "team": "CLE", "position": "TE", "projection": 14.0},
    {"id": 408, "name": "Mark Andrews", "team": "BAL", "position": "TE", "projection": 13.5},
    {"id": 409, "name": "Evan Engram", "team": "DEN", "position": "TE", "projection": 13.0},
    {"id": 410, "name": "Tyler Warren", "team": "IND", "position": "TE", "projection": 12.5},
    {"id": 411, "name": "Tucker Kraft", "team": "GB", "position": "TE", "projection": 12.0},
    {"id": 412, "name": "Jake Ferguson", "team": "DAL", "position": "TE", "projection": 11.5},
    {"id": 413, "name": "Dalton Kincaid", "team": "BUF", "position": "TE", "projection": 11.0},
    {"id": 414, "name": "Colston Loveland", "team": "CHI", "position": "TE", "projection": 10.5},
    {"id": 415, "name": "Dallas Goedert", "team": "PHI", "position": "TE", "projection": 10.0},
    {"id": 416, "name": "Kyle Pitts Sr.", "team": "ATL", "position": "TE", "projection": 9.5},
    {"id": 417, "name": "Hunter Henry", "team": "NE", "position": "TE", "projection": 9.0},
    {"id": 418, "name": "Zach Ertz", "team": "WAS", "position": "TE", "projection": 8.5},
    {"id": 419, "name": "Jonnu Smith", "team": "PIT", "position": "TE", "projection": 8.0},
    {"id": 420, "name": "Brenton Strange", "team": "JAC", "position": "TE", "projection": 7.5},
    {"id": 421, "name": "Chig Okonkwo", "team": "TEN", "position": "TE", "projection": 7.0},
    {"id": 422, "name": "Cade Otton", "team": "TB", "position": "TE", "projection": 6.5},
    {"id": 423, "name": "Isaiah Likely", "team": "BAL", "position": "TE", "projection": 6.0},
    {"id": 424, "name": "Mason Taylor", "team": "NYJ", "position": "TE", "projection": 5.5},
    {"id": 425, "name": "Mike Gesicki", "team": "CIN", "position": "TE", "projection": 5.0},
    {"id": 426, "name": "Pat Freiermuth", "team": "PIT", "position": "TE", "projection": 4.5},
    {"id": 427, "name": "Dalton Schultz", "team": "HOU", "position": "TE", "projection": 4.0},
    {"id": 428, "name": "Juwan Johnson", "team": "NO", "position": "TE", "projection": 3.5},
]

def get_player_data():

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping') # Checks if connection is valid
        
        
        db = client[DB_NAME]
        collection = db['players'] 
        return list(collection.find({})) 
    
    except Exception as e:
        print(f"MongoDB connection failed: {e}. Using fallback data.")
        return PLAYERS

app = Flask(__name__)

CORS(app)

@app.route('/api/players', methods=['GET'])
def get_players():
    """
    API endpoint to retrieve and format player data.
    """
    try:
        
        players_data = get_player_data()
        
        
        for player in players_data:
            if '_id' in player:
                player['_id'] = str(player['_id']) 

        
        return jsonify({
            "status": "Success",
            "count": len(players_data),
            "players": players_data
        })

    except Exception as e:
        print(f"Error fetching player data: {e}")
        return jsonify({
            "status": "Error",
            "message": f"Server error: {str(e)}"
        }), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

    
