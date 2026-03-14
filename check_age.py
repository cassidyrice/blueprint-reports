import json
from calculate_blueprint import calculate_blueprint
from datetime import date

res = calculate_blueprint(2, 17, 1991, date(2027, 2, 18))
print("Age:", res['timing']['age'])

bc_periods = res['birth_card_spread']['period_cards']
prc_periods = res['prc_spread']['period_cards']

print("BC Mercury:", bc_periods.get('Mercury'))
print("BC Venus:", bc_periods.get('Venus'))
print("PRC Mercury:", prc_periods.get('Mercury'))
print("PRC Venus:", prc_periods.get('Venus'))
