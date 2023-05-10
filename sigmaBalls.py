import tkinter as tk
import math
import random
from PIL import Image, ImageTk
import time

class CircleButtonsGUI:
    def __init__(self):
        # Initialize GUI
        self.root = tk.Tk()
        self.root.title("Sigma balls")
        self.root.geometry("500x500")
        self.root.resizable(False,False)
        
        self.background_image = Image.open("arena.png")
        self.background_image = self.background_image.resize((500, 500), Image.LANCZOS)
        self.background_image_resized = ImageTk.PhotoImage(self.background_image)
        
        self.duration = 0

        self.midImg = tk.PhotoImage(file="mid.PNG")
        self.remoteimg = tk.PhotoImage(file="remote.PNG")
        
        # Resize and scale background image to new canvas size
        self.bg_label = tk.Label(self.root, image=self.background_image_resized)
        self.bg_label.pack()
        self.bg_label.place(x=0, y=0, width=500, height=500)
        
        # Create a frame on top of the background image
        self.frame = tk.Frame(self.bg_label, bg='black', bd=0, width=0)
        self.frame.pack()
        self.frame.place(relx=0.5, rely=0.5, anchor='center')
        self.front_label = tk.Label(self.frame)
        
        # Create canvas for circle
        self.canFrame = tk.Frame(self.bg_label, bg='black', bd=0, width=0)
        self.canFrame.pack()
        self.canFrame.place(relx=0.5, rely=0.7, anchor='center')
        self.canvas = tk.Canvas(self.canFrame, width=150, height=75, bg="#00a2e8",bd=0,highlightthickness=0)
        self.canvas.pack()
        
        self.newButton = tk.Button(self.bg_label, text="New Game", command=lambda: self.button_newGame())
        self.newButton.pack()
        self.newButton.place(x=0, y=0)
        # Bind canvas resizing to update button positions and grid size
        
        self.timeBox = tk.Text(self.bg_label, bg="dark blue", fg="white", bd=1, height=1, width=10)
        self.timeBox.pack()
        self.timeBox.place(relx=1, rely=0, anchor='ne')
            
    def update_canvas(self):
        self.canvas.destroy()
        self.front_label.destroy()
        self.timeBox.destroy()
    
        self.correct = -1
        mid = bool(random.getrandbits(1))
        position = random.randint(0, 7)
        unmarked = random.sample(range(4, 8), 2)
        top_row = [0,1,2,3]
        bot_row = [4,5,6,7]
        marked_bot = list(set(bot_row) - set(unmarked))
        
        #find the correct answer
        if(position>3):
            if position in unmarked:
                if position >= unmarked[0] and position >= unmarked[1]:
                    self.correct = 6
                else:
                    self.correct = 5
            else:
                if position >= marked_bot[0] and position >= marked_bot[1]:
                    self.correct = 0
                else:
                    self.correct = 3
        else:
            partner = position+4
            if partner in unmarked:
                if partner >= unmarked[0] and partner >= unmarked[1]:
                    if mid:
                        self.correct = 4
                    else:
                        self.correct = 2
                else:
                    if mid:
                        self.correct = 7
                    else:
                        self.correct = 1
            else:
                if partner >= marked_bot[0] and partner >= marked_bot[1]:
                    if mid:
                        self.correct = 2
                    else:
                        self.correct = 4
                else:
                    if mid:
                        self.correct = 1
                    else:
                        self.correct = 7
                
        # Set the front image inside the frame
        if(mid):
            self.front_label = tk.Label(self.frame, image=self.midImg)
        else:
            self.front_label = tk.Label(self.frame, image=self.remoteimg)
        self.front_label.pack()
        
        self.canvas = tk.Canvas(self.canFrame, width=150, height=75, bg="#00a2e8",bd=0,highlightthickness=0)
        self.canvas.pack()
        
        self.timeBox = tk.Text(self.bg_label, bg="dark blue", fg="white", bd=1, height=1, width=10)
        self.timeBox.pack()
        self.timeBox.place(relx=1, rely=0, anchor='ne')
        
        self.num_buttons = 8
        self.buttons = []
        
        # Calculate button positions on circle relative to canvas size
        self.button_radius = 0.4 * min(500, 500)
        self.center_x = 500 / 2 - 15
        self.center_y = 500 / 2 - 15
        self.button_positions = []
        for i in range(self.num_buttons):
            angle = 2 * math.pi * -i / self.num_buttons - math.pi/8
            x = self.center_x + self.button_radius * math.cos(angle)
            y = self.center_y + self.button_radius * math.sin(angle)
            self.button_positions.append((x, y))
        
        # Create buttons on canvas
        self.button_colors = ["lightgray"] * self.num_buttons
        for i in range(self.num_buttons):
            button = tk.Button(self.bg_label, text=f"{i}", command=lambda i=i: self.button_click(i), bg=self.button_colors[i], activebackground="dark blue", relief="raised", width=4, height=2, padx=2, pady=2)
            xPos, yPos = self.button_positions[i]
            self.buttons.append(button)
            button.place(x = xPos, y = yPos)
        
        # Create grid of colored squares in center of canvas
        self.grid_size = 8
        self.grid_square_size = 20
        self.grid_spacing = 10
        self.grid_x = self.canvas.winfo_height()/2 +20
        self.grid_y = self.canvas.winfo_height()/2 +20
        self.grid_squares = []
        for i in range(0,4):
            for j in range(0,2):
                x = self.grid_x + i * (self.grid_square_size + self.grid_spacing)
                y = self.grid_y + j * (self.grid_square_size + self.grid_spacing)
                playerOutline = ""
                if(position == i + j*4):
                    playerOutline = "purple"
                if(j == 1 and i+4 in unmarked):
                    player = self.canvas.create_rectangle(x, y, x + self.grid_square_size, y + self.grid_square_size, fill="white", outline=playerOutline, width=5)
                else:
                    player = self.canvas.create_rectangle(x, y, x + self.grid_square_size, y + self.grid_square_size, fill="dark orange", outline=playerOutline, width=5)
                self.grid_squares.append(player)
                
    def button_click(self, button_index):
        if button_index == self.correct:
            self.buttons[button_index].config(bg="green")
            self.duration = (time.time() - self.duration)
            self.timeBox.insert(tk.END, str(self.duration))
        else:
            self.buttons[button_index].config(bg="red")
                
    def button_newGame(self):
        self.update_canvas()
        self.duration = time.time()

                
    def run(self):
        self.root.mainloop()

# Create and run GUI
gui = CircleButtonsGUI()
gui.run()
