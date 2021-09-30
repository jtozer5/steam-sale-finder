import steamapi
import json
import requests
from datetime import datetime
from datetime import timedelta
import threading
import smtplib

# Scheduling code
now = datetime.now()
run_at = now + timedelta(weeks=1)
delay = (run_at - now).total_seconds()
# User info pulled from server
user_url = 'karcosa'
user_email ='joshiantozer@gmail.com'

def get_game_list(user_url):

    sale_list = []
    response = requests.get("https://store.steampowered.com/api/featuredcategories/")
    sale_info = json.loads(response.text)

    for game in sale_info['4']['items']:
        sale_list.append(game['id'])

    for game in sale_info['specials']['items']:
        sale_list.append(game['id'])

    steamapi.core.APIConnection(api_key="C9F701E18E7A7D170F03F539BFA8B87F", validate_key=True)
    user = steamapi.user.SteamUser(userurl=user_url)
    game_list = user.recently_played
    tag_list = []
    for game in game_list:
        response = requests.get("https://store.steampowered.com/api/appdetails?appids=" + str(game.appid))
        game_info = json.loads(response.text)
    
        for item in game_info[str(game.appid)]["data"]["genres"]:
            if item["description"] in tag_list:
                pass
            else:
                tag_list.append(item["description"])

    rec_list = []
    for game_id in sale_list:
        response = requests.get("https://store.steampowered.com/api/appdetails?appids=" + str(game_id))
        game_info = json.loads(response.text)
        if game_info[str(game_id)]["success"] is False:
            pass
        else:
            for item in game_info[str(game_id)]["data"]["genres"]:
                if item["description"] in tag_list:
                    if game_id in rec_list:
                        pass
                    else:
                        rec_list.append(game_id)

    def game_list_printer(id_list):
        message = f'Your curated game list:\n'

        for game_id in id_list:
            response = requests.get("https://store.steampowered.com/api/appdetails?appids=" + str(game_id))
            game_info = json.loads(response.text)
            name = str(game_info[str(game_id)]["data"]["name"]).encode('utf-8').strip()
            name = name.decode()
            percent_discount = str(game_info[str(game_id)]["data"]["price_overview"]["discount_percent"]) + '%'
            final_price = str(game_info[str(game_id)]["data"]["price_overview"]["final_formatted"])


            message = message + f'{name} is {final_price} and {percent_discount} off.\n Link: https://store.steampowered.com/app/{game_id}/\n\n'
        
        return message

    def emailer():
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        print(smtpObj.ehlo())
        print(smtpObj.starttls())
        print(smtpObj.login('gamereccs@gmail.com', 'PythonIsCool123'))
        msg = game_list_printer(rec_list)
        print(smtpObj.sendmail('gamereccs@gmail.com', user_email, msg))

    return emailer()

# while True:
#  threadObj = threading.Timer(delay, get_game_list(user_url))
#  threadObj.start()

get_game_list(user_url)
