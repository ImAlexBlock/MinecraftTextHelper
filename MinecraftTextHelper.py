# coding:UTF-8
import requests
import os
import random
import time
import pyperclip
import keyboard
import string
from tkinter import simpledialog, messagebox

os.system("title MinecraftTextHelper 1.0")
print('MinecraftTextHelper 1.0 Beta Version')
print(f'by AlexBlock Build:0125')
print('===============================================')
print('''功能列表：
1.一言[H]
2.刷屏[J]
3.查询玩家信息[K]''')
print('===============================================')


def get_time():
    time_is = "[" + time.strftime("%H:%M:%S", time.localtime()) + "]"
    return time_is


def typing(text):
    pyperclip.copy(text)
    keyboard.press_and_release('t')
    time.sleep(0.1)
    keyboard.press('ctrl+v')
    time.sleep(0.1)
    keyboard.release('ctrl+v')
    keyboard.press_and_release('enter')


def read_key():
    key = keyboard.read_key()
    return key


def get_hitokoto():
    hitokoto = requests.get("https://v1.hitokoto.cn").json()
    hitokoto_back = f'“{hitokoto["hitokoto"]}”' + f' ———— {hitokoto["from"]}'
    return hitokoto_back


def spam(length):
    text = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(text) for _ in range(length))
    return random_string


# APIload
api_key = 'none'
if os.path.isfile('key.config'):
    print(f"{get_time()}检测到APIkey配置文件")
    with open('key.config', 'r') as file:
        api_key = file.read()
    print(f"{get_time()}识别到APIkey:{api_key}")
else:
    with open('key.config', 'w') as file:
        print(f"{get_time()}没有找到配置文件，正在帮您创建")
        file.write(input(f"{get_time()}请输入你的API-KEY: "))
    with open('key.config', 'r') as file:
        api_key = file.read()
        print(f"{get_time()}识别到APIkey:{api_key}")

while True:
    if read_key() == 'f12':
        print(f"{get_time()}End.")
        break
    elif read_key() == 'h':
        print(f"{get_time()}一言")
        typing(get_hitokoto())
    elif read_key() == 'j':
        print(f"{get_time()}刷屏")
        typing(spam(20) + '| by MinecraftTextHelper')
    elif read_key() == 'k':
        print(f"{get_time()}查询玩家信息")
        game_name = simpledialog.askstring("MTH", "请输入玩家名：")
        if game_name is not None:
            # Get uuid
            back_uuid_data = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{game_name}")
            back_uuid = back_uuid_data.json()
            player_uuid = back_uuid["id"]
            print(f"{get_time()}BackPlayerUUID：" + player_uuid)
            # 接口
            api_url = "https://api.hypixel.net/player"
            api_url2 = "https://api.hypixel.net/status"
            api_url3 = "https://api.hypixel.net/recentgames"
            # 请求参数
            request = {
                "key": api_key,
                "uuid": player_uuid
            }
            response = requests.get(api_url, params=request)
            back_data = response.json()
            if back_data["success"]:
                if "newPackageRank" in back_data["player"]:
                    a = back_data["player"]["newPackageRank"]
                else:
                    a = "Normal"
                data = f'''玩家名:{back_data["player"]["displayname"]}
Rank:{a}
BWLeave:{back_data["player"]["achievements"]["bedwars_level"]}
WLR:{back_data["player"]["stats"]["Bedwars"]["wins_bedwars"] / back_data["player"]["stats"]["Bedwars"]["losses_bedwars"]:.2f}   W:{back_data["player"]["stats"]["Bedwars"]["wins_bedwars"]}  L:{back_data["player"]["stats"]["Bedwars"]["losses_bedwars"]}
KD:{back_data["player"]["stats"]["Bedwars"]["kills_bedwars"] / back_data["player"]["stats"]["Bedwars"]["deaths_bedwars"]:.2f}   K:{back_data["player"]["stats"]["Bedwars"]["kills_bedwars"]}  D:{back_data["player"]["stats"]["Bedwars"]["deaths_bedwars"]}
FKDR:{back_data["player"]["stats"]["Bedwars"]["final_kills_bedwars"] / back_data["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]:.2f} FK:{back_data["player"]["stats"]["Bedwars"]["final_kills_bedwars"]} FD:{back_data["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]}
            '''
                result = messagebox.askquestion("玩家信息(选是复制到剪贴板):", data, icon="info")
                if result:
                    pyperclip.copy(data)
                    print(f"{get_time()}将查询数据复制到剪贴板")

            else:
                print(f'{get_time()}查询失败！请检查用户名是否正确、api是否异常')
                messagebox.showerror("API请求失败", "请检查用户名是否正确、api是否异常")
        else:
            print("玩家名未输入!")
