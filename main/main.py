import json
import os
import random
import sys

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox


class dice():
    def __init__(self, upper:int ,size_x: int, size_y: int):
        self.upper = upper
        self.size_x = size_x
        self.size_y = size_y

    def roll(self):
        val = random.randint(1, self.upper)
        x = random.uniform(0, self.size_x)
        y = random.uniform(0, self.size_y)
        return (val ,x ,y)
        
class dice_set():

    def __init__(self, name:str, color :str, size_x: int, size_y: int):
        self.name  = name
        self.dice: list[dice] = [
            dice(4, size_x, size_y),
            dice(6, size_x, size_y),
            dice(8, size_x, size_y),
            dice(10, size_x, size_y),
            dice(12, size_x, size_y),
            dice(20, size_x, size_y)
        ]
        self.color :str  = color
        self.count = 1

    def roll(self):
        tmp :list[tuple[int, float, float]] = []
        for d in self.dice:
            tmp.append(d.roll())

        return tmp
    
    def set_count(self, i):
        i = int(i)
        if i < 0 or i == self.count or i == None:
            return
        self.count = i

# vairabels
width = 1280
height= 720
sets : list[dice_set] = []

fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)

# Separate figure for text boxes
fig_textboxes = plt.figure(figsize=(4, 6))

def generate_map ():
     
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('lightgray')
    
    for item in sets:
        
        for i in range(item.count):
            tmp = item.roll()

            for value, px, py in tmp:
                ax.text(px, py, str(value), fontsize=8, color='black', ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.1", facecolor=item.color, alpha=0.7))
            
def generate_event(event):
     if event.key != ' ':  # Spacebar pressed
         return
     ax.clear()
     generate_map()
     fig.canvas.draw()  # Refresh display

def update_count_event(text, index):
    sets[index].set_count(text)

def on_window_close_event(event):
    """Close ALL figures and exit program"""
    plt.close('all')  # Closes both windows
    plt.ioff()        # Disable interactive mode
    sys.exit(0)       # Exit Python process

def main():

    plt.ion()  # Enable interactive mode   
    generate_map()

    
    fig.canvas.mpl_connect('key_press_event', 
        lambda event: generate_event(event)
    )  # Bind spacebar
    
    textboxes = []
    for i, set in enumerate(sets):
        y_pos = 0.85 - i*0.06
        ax_text = fig_textboxes.add_axes([0.1, y_pos, 0.6, 0.03])  # smaller width and height
        fig_textboxes.text(0, y_pos + 0.035, f'{set.name}', ha='left', fontsize=6)
        tb = TextBox(ax_text, '', initial='1')
        tb.label.set_fontsize(6)  # smaller font for label    
        textboxes.append(tb)
        tb.on_submit(lambda val, idx=i: update_count_event(val, idx))

    fig.canvas.mpl_connect('close_event', on_window_close_event)
    fig_textboxes.canvas.mpl_connect('close_event', on_window_close_event)


    plt.show(block=True)
    

if __name__ == "__main__":

    # Load configuration JSON
    json_path = 'config.json'
    if os.path.exists(json_path):
        
        with open(json_path, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "size": {"width": 1280, "height": 720},
            "dice_sets": []
        }

    width = config["size"]["width"]
    height = config["size"]["height"]

    dice_sets = config["dice_sets"]
    for d in dice_sets:
        tmp = dice_set(name=d["name"],color=d["color"], size_x= width, size_y= height)
        sets.append(tmp)
    

    main()
