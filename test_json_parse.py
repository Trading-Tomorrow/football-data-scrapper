import json
import pandas as pd

json_data = """
{"confirmed":true,"home":{"players":[{"player":{"name":"Petr \u010cech","slug":"petr-cech","shortName":"P. \u010cech","position":"G","jerseyNumber":"","height":196,"userCount":1312,"id":1185,"country":{"alpha2":"CZ","alpha3":"CZE","name":"Czechia","slug":"czechia"},"marketValueCurrency":"EUR","dateOfBirthTimestamp":390700800,"fieldTranslations":{"nameTranslation":{"ar":"\u0628\u064a\u062a\u0631 \u062a\u0634\u064a\u0643","hi":"\u092a\u0947\u091f\u094d\u0930 \u091a\u0947\u0915","bn":"\u09aa\u09bf\u099f\u09be\u09b0 \u099a\u09c7\u0995"},"shortNameTranslation":{"ar":"\u0628. \u062a\u0634\u064a\u0643","hi":"\u092a\u0940. \u091a\u0947\u0915","bn":"\u09aa\u09bf. \u099a\u09c7\u0995"}}},"teamId":241802,"shirtNumber":33,"jerseyNumber":"33","position":"G","substitute":false,"statistics":{"totalPass":21,"accuratePass":16,"totalLongBalls":11,"accurateLongBalls":6,"accurateOwnHalfPasses":11,"totalOwnHalfPasses":13,"accurateOppositionHalfPasses":5,"totalOppositionHalfPasses":8,"ballRecovery":8,"errorLeadToAGoal":1,"crossNotClaimed":1,"savedShotsFromInsideTheBox":1,"saves":2,"minutesPlayed":90,"touches":29,"rating":5.7,"totalShots":0,"statisticsType":{"sportSlug":"football","statisticsType":"player"}}},{"player":{"name":"Mathieu Debuchy","firstName":"","lastName":"","slug":"mathieu-debuchy","shortName":"M. Debuchy","position":"D","height":177,"userCount":80,"id":3579,"country":{"alpha2":"FR","alpha3":"FRA","name":"France","slug":"france"},"marketValueCurrency":"EUR","dateOfBirthTimestamp":491356800,"fieldTranslations":{"nameTranslation":{"ar":"\u0645\u0627\u062a\u064a\u0648 \u062f\u064a\u0628\u0648\u0634\u064a","hi":"\u092e\u0948\u0925\u094d\u092f\u0942 \u0926\u0947\u092c\u0941\u091a\u0940","bn":"\u09ae\u09cd\u09af\u09be\u09a5\u09bf\u0989 \u09a1\u09c7\u09ac\u09c1\u099a\u09bf"},"shortNameTranslation":{"ar":"\u0645. \u062f\u064a\u0628\u0648\u0634\u064a","hi":"\u090f\u092e. \u0926\u0947\u092c\u0941\u091a\u0940","bn":"\u098f\u09ae. \u09a1\u09c7\u09ac\u09c1\u099a\u09bf"}}},"teamId":241802,"shirtNumber":2,"jerseyNumber":"2","position":"D","substitute":false,"statistics":{"totalPass":36,"accuratePass":29,"totalLongBalls":4,"accurateLongBalls":1,"accurateOwnHalfPasses":12,"totalOwnHalfPasses":14,"accurateOppositionHalfPasses":17,"totalOppositionHalfPasses":27,"totalCross":5,"aerialLost":1,"aerialWon":5,"duelLost":3,"duelWon":6,"dispossessed":1,"blockedScoringAttempt":1,"totalClearance":1,"interceptionWon":1,"ballRecovery":5,"wasFouled":1,"fouls":1,"minutesPlayed":67,"touches":53,"rating":6.4,"keyPass":1,"totalShots":1,"statisticsType":{"sportSlug":"football","statisticsType":"player"}}}],"supportStaff":[],"formation":"4-2-3-1","playerColor":{"primary":"cc0000","number":"ffffff","outline":"cc0000","fancyNumber":"ffffff"},"goalkeeperColor":{"primary":"000000","number":"ffffff","outline":"000000","fancyNumber":"ffffff"}},"away":{"players":[],"supportStaff":[],"formation":"4-3-3","playerColor":{"primary":"66ccff","number":"ffffff","outline":"66ccff","fancyNumber":"222226"},"goalkeeperColor":{"primary":"66cc00","number":"000000","outline":"66cc00","fancyNumber":"ffffff"}},"statisticalVersion":null}
"""

data = json.loads(json_data)
records = []

for side in ['home', 'away']:
    team_data = data.get(side, {})
    formation = team_data.get('formation')
    players = team_data.get('players', [])
    
    for p_entry in players:
        player = p_entry.get('player', {})
        stats = p_entry.get('statistics', {})
        
        # Base record
        rec = {
            'side': side,
            'formation': formation,
            'player_name': player.get('name'),
            'player_id': player.get('id'),
            'position': p_entry.get('position'),
            'shirt_number': p_entry.get('shirtNumber'),
            'substitute': p_entry.get('substitute'),
            'rating': stats.get('rating'),
            'minutes_played': stats.get('minutesPlayed'),
        }
        
        # Add all stats
        for k, v in stats.items():
            if isinstance(v, (int, float, str)):
                rec[f'stat_{k}'] = v
                
        records.append(rec)

df = pd.DataFrame(records)
print(df.columns.tolist())
print(df.head())
