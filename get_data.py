
from calculate_blueprint import calculate_blueprint
from datetime import date
import json

target = date(2026, 3, 14)

# Person 1: 2/17/1991 (Aquarius -> Uranus)
m1, d1, y1 = 2, 17, 1991
p1_bc_res = calculate_blueprint(m1, d1, y1, target_date=target)
prc1 = p1_bc_res["archetype"]["prc"]
p1_prc_res = calculate_blueprint(m1, d1, y1, target_date=target, anchor_card=prc1)

# Person 2: 12/13/1987 (Sagittarius -> Jupiter)
m2, d2, y2 = 12, 13, 1987
p2_bc_res = calculate_blueprint(m2, d2, y2, target_date=target)
prc2 = p2_bc_res["archetype"]["prc"]
p2_prc_res = calculate_blueprint(m2, d2, y2, target_date=target, anchor_card=prc2)

def get_bundle(res):
     return {
         "anchor": res["archetype"]["anchor"],
         "long_range": res["long_range"],
         "pluto": res["yearly_spread"]["pluto"],
         "result": res["yearly_spread"]["result"],
         "env": res["environment_displacement"]["environment"],
         "disp": res["environment_displacement"]["displacement"],
         "karma_supp": res["lifetime_karma"]["supporting"],
         "karma_chall": res["lifetime_karma"]["challenge"],
         "life_path": res["life_path"]
     }

data = {
    "P1": {
        "BC": get_bundle(p1_bc_res),
        "PRC": get_bundle(p1_prc_res)
    },
    "P2": {
        "BC": get_bundle(p2_bc_res),
        "PRC": get_bundle(p2_prc_res)
    }
}

print(json.dumps(data, indent=2))
