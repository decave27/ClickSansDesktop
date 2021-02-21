from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from pypresence import Presence
import sys, os
import time

os.system("pip install -r requirements.txt")
start_time=time.time()

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


app = Ursina()
window.color = color._20
window.title = "ClickSans"
window.borderless = False
window.fps_counter.enabled = False
window.icon = "images/sans.ico"

gold = int(os.environ.get('CLICKSANSDATA_CLICKS', 0))
title = Text(text="ClickSans", x=-0.1, y=0.3, scale=2)
gold_text = Text(text=str(gold) + " CLICKS", x=-0.1, y=-0.3, scale=2)
button = Button(
    color=color.white, x=-0, scale=0.3, texture=resource_path("images/sans.png")
)

client_id = "812919380747747348"
RPC = Presence(client_id=client_id)
RPC.connect()

RPC.update(
    details="ClickSans Desktop",
    state="0 Clicks",
    large_image="sanslogo",
    large_text="ClickSans",
    buttons=[
        {
            "label": "Desktop Player",
            "url": "https://github.com/decave27/ClickSansDesktop",
        },
        {"label": "Web Player", "url": "https://clicksans.devkiki.xyz/"},
    ],
    start=start_time,
)

# DropdownMenu(
#    "Menu",
#    buttons=(
#        DropdownMenuButton("Game"),
#        DropdownMenuButton("Shop"),
#    ),
# )


def button_click():
    global gold
    gold += 1


button.on_click = button_click


def auto_plus_gold(plus=1, interval=1):
    global gold
    gold += plus

    invoke(auto_plus_gold, plus, delay=interval)


def get_auto_gold(button, plus=1):
    global gold

    if gold >= button.cost:
        gold -= button.cost

        button.cost = int(button.cost * 1.2)
        button.upgrade += 1

        invoke(auto_plus_gold, plus=plus, interval=1)


auto_settings = []

auto_buttons = []

for i, setting in enumerate(auto_settings):
    b = Button(
        x=(0.9),
        scale=0.2,
        disabled=True,
        cost=setting["cost"],
        earn=setting["earn"],
        upgrade=setting["upgrade"],
    )

    b.on_click = Func(get_auto_gold, b, b.earn)

    auto_buttons.append(b)


def update():
    global gold

    gold_text.text = str(gold) + " CLICKS"
    RPC.update(
        details="ClickSans Desktop",
        state=str(gold) + " CLICKS",
        large_image="sanslogo",
        large_text="ClickSans",
        buttons=[
        {
            "label": "Desktop Player",
            "url": "https://github.com/decave27/ClickSansDesktop",
        },
        {"label": "Web Player", "url": "https://clicksans.devkiki.xyz/"},
    ],
    start=start_time,
    )
    os.environ['CLICKSANSDATA_CLICKS'] = str(gold)

    for button in auto_buttons:
        if gold >= button.cost:
            button.disabled = False
            button.color = color.green
            button.text_color = color.black
        else:
            button.disabled = True
            button.color = color.gray
            button.text_color = color.white


app.run()
