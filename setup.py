from espn_api.basketball import League, Player, Team
import json 

SWID = '{C516A8C5-D0C6-4FD1-982D-26689751FD9B}'
ESPN_S2 = 'AECrrKfCQkc5u%2ByUq7EbH6UlJflGGLaIugPfTKIIeRsv9L2e0ZmRnUxB8bezLO5YYsi%2Bo0XhHLWmL9Maar7tW4SFPFbpwM2UuZmtNgqZdiioH8xTGIHFK5EbUE%2BOWRGs9hKzyi7%2FyYIBco0tfoAh5lsC9%2BEIa7ne3nTMonWGOMZR%2FMbyEQqPh967ztVCAF0QFk%2BHjkhI2Fx2TV4ahhno42uZTtIgalMYElMsu%2BqReL2wYj2z8B7IArCH9D7IzLd8moIZCDh1NTGrwlKM9oAGJ6iTcvrZlGw4FbnAnM8BHZ2Edw%3D%3D'
LEAGUE_ID = 852079681

league = League(league_id=LEAGUE_ID, year=2024, espn_s2=ESPN_S2, swid=SWID)
# print(json.dumps(league.current_week, index=2))

