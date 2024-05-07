import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class GameVisualizer(tk.Tk):
    def __init__(self, grid_size, cell_size,initial_state):
        super().__init__()
        self.title("Spiders and Flies")


        self.grid_size = grid_size
        self.cell_size = cell_size
        self.initial_state = initial_state

        self.timeelapsed_label = tk.Label(self, text="Total time elapsed: 0 ms")
        self.timeelapsed_label.pack(pady=7)

        # Creating the canvas
        self.canvas = tk.Canvas(self, width=grid_size * self.cell_size, height=grid_size * self.cell_size)
        self.canvas.pack(padx=5,pady=5)

        # Load gif Sequence for spiders and flies
        self.spider_images = self._load_and_resize_gif("spider_image.gif")
        self.fly_images = self._load_and_resize_gif("fly_image.gif")

        self.timestep_label = tk.Label(self, text="Timestep: 0")
        self.timestep_label.pack(pady=8)


        self.draw_grid()
        self.draw_state(initial_state,0,0)


    def _load_and_resize_gif(self, file_path):
        gif = Image.open(file_path)
        gif_frames = [ImageTk.PhotoImage(frame.resize((int(self.cell_size), int(self.cell_size)))) for frame in ImageSequence.Iterator(gif)]
        return gif_frames

    def draw_grid(self):
        offset = 3
        for i in range(offset, (self.grid_size) * self.cell_size + 1, self.cell_size):
            self.canvas.create_line(i, 0, i, self.grid_size * self.cell_size, fill="gray")
            self.canvas.create_line(0, i, self.grid_size * self.cell_size, i, fill="gray")
        self.canvas.create_rectangle(offset, offset, self.grid_size * self.cell_size, self.grid_size * self.cell_size, outline="gray")

    def draw_state(self, state, time_step,time_elapsed):
        for row_index, row in enumerate(state):
            for col_index, cell in enumerate(row):
                x1, y1 = col_index * self.cell_size, row_index * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                if cell == 'S':
                    image_index = (time_step // 2) % len(self.spider_images)
                    self.canvas.create_image((x1 + x2) // 2, (y1 + y2) // 2, image=self.spider_images[image_index])
                elif cell == 'F':
                    image_index = (time_step // 1) % len(self.fly_images)
                    self.canvas.create_image((x1 + x2) // 2, (y1 + y2) // 2, image=self.fly_images[image_index])

        self.timestep_label.config(text=f"Timestep: {time_step}")
        self.timeelapsed_label.config(text=f"Total time elapsed : {time_elapsed} ms")

    def update_state(self, new_state, time_step,time_elapsed):
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_state(new_state, time_step,time_elapsed)

