import zipfile
from dotenv import load_dotenv
import os
import time
import requests;
import pyautogui as g;

def CheckFile():
    with open('tokens.txt', 'r') as file:
        data = file.read()
        if len(data) == 0:
           return True
        else:
            return False
word = str;
word2 = str;
if CheckFile() == True:
    word = 'tokens2.txt'
    word2 = 'tokens.txt'
else:
    word = 'tokens.txt'
    word2 = 'tokens2.txt'

def remove_token():
    with open(word2, 'r+') as input_file, open(word, 'a') as output_file:
        lines = input_file.readlines()

        output_file.write(lines[0].strip() + '\n')

        input_file.seek(0)
        input_file.writelines(lines[1:])

        input_file.truncate()

def send_webhook_things(name, money, token, discord_webhook_url):

    embed = {
        "title": "A New bot has claimed the daily!",
        "description": "The data will be shown.",
        "color": 16711680, # Red color
        "author": {
            "name": name,
            "icon_url": 'https://cdn.discordapp.com/channel-icons/899730490532171827/9c0dbf36835a394aa3e04730c8c61de7.webp?size=32'
        },
        "fields": [
            {
                "name": "Cash",
                "value": f'`{money}`',
                "inline": False
            },
            {
                "name": "Token",
                "value": f'`{token}`',
                "inline": False
            }
        ],
        "thumbnail": {
            "url": 'https://cdn.discordapp.com/attachments/1083815711048208446/1083815711895474206/keemgnome.jpg'
        }
    }

    payload = {
        "embeds": [embed]
    }

    requests.post(discord_webhook_url, json=payload)



def checkToken(token):
    response = requests.get('https://discord.com/api/v9/auth/login', headers={"Authorization": token})
    return True if response.status_code == 200 else False


def failedToken():
    with open('tokens.txt', 'r+') as input_file, open('failedTokens.txt', 'a') as output_file:
        lines = input_file.readlines()

        output_file.write(lines[0].strip() + '\n')

        input_file.seek(0)
        input_file.writelines(lines[1:])

        input_file.truncate()


#1707, 243;
#1318, 1061
def changeVPN():
    g.click(1318, 1061)
    g.click(1707, 243)

