import tkinter as tk
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import ast
import tkinter.messagebox as messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Движение робота")
        self.geometry("500x790")
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.create_widgets()

        self.line_x, self.point_y, self.gripper = 0.5, 0.5, None
        self.draw_axes()

    def create_widgets(self):
        tk.Label(self, text="Путь. Координаты (в формате [(0, 2), (1, 2), ...]):").pack()
        self.coords_entry = tk.Entry(self)
        self.coords_entry.pack()
        tk.Button(self, text="Вставить путь", command=self.paste_coords).pack()
        tk.Button(self, text="Выполнить движение", command=self.update_graph).pack()
        tk.Button(self, text="Выдвинуть хваталку", command=self.take_object).pack()
        tk.Button(self, text="Забрать предмет", command=self.release_object).pack()
        tk.Button(self, text="Положить предмет", command=self.place_object).pack()
        tk.Button(self, text="Убрать хваталку", command=self.delete_gripper).pack()

        tk.Label(self, text="Координаты предмета (в формате (2.5, 3.5, 0.5)):").pack()
        self.obj_entry = tk.Entry(self)
        self.obj_entry.pack()
        tk.Button(self, text="Добавить предмет", command=self.add_object_coordinates).pack()

    def draw_axes(self):
        self.ax.clear()

        for i in range(5):
            self.ax.plot([i, i], [0, 4], [0, 0], color='gray')
            self.ax.plot([0, 4], [i, i], [0, 0], color='gray')

        x, y = np.meshgrid(range(5), range(5))
        self.ax.plot_surface(x, y, x * 0, color='lightblue', alpha=0.25)

        x, y, z = [0, 4], [0, 0], [0, 0]
        self.ax.plot(x, y, z, color='mediumblue', linewidth=4)
        y = [4, 4]
        self.ax.plot(x, y, z, color='mediumblue', linewidth=4)

        x, y = [self.line_x, self.line_x], [0, 4]
        self.line = self.ax.plot(x, y, z, color='hotpink', linewidth=4)[0]

        x, y, z = [self.line_x], [self.point_y], [0]
        self.point = self.ax.scatter(x, y, z, color='navy', linewidth=6)

        self.ax.set(xlim=[0, 4], ylim=[0, 4], zlim=[0, 1], xlabel="X", ylabel="Y", zlabel="Z")

        self.canvas.draw()

    def paste_coords(self):
        coords_str = self.clipboard_get()
        self.coords_entry.delete(0, tk.END)
        self.coords_entry.insert(0, coords_str)

    def add_object_coordinates(self):
        obj_coords = self.obj_entry.get()
        try:
            x, y, z = ast.literal_eval(obj_coords)
            self.object_x, self.object_y, self.object_z = x, y, z
            self.object_point = self.ax.scatter(x, y, z, color='mediumvioletred', s=100)
            self.canvas.draw()
        except (ValueError, SyntaxError, TypeError):
            messagebox.showerror("Ошибка", "Неверный формат координат предмета")

    def update_graph(self):
        coords_str = self.coords_entry.get()
        try:
            coords = ast.literal_eval(coords_str)
        except (SyntaxError, ValueError):
            messagebox.showerror("Ошибка", "Некорректный формат ввода координат")
            return

        if not isinstance(coords, list):
            messagebox.showerror("Ошибка", "Некорректный формат ввода координат")
            return

        frames_per_coord = 10
        frames = (len(coords) - 1) * frames_per_coord + 1

        x_interp, y_interp = [], []

        for i in range(len(coords) - 1):
            x_start, y_start = coords[i]
            x_end, y_end = coords[i + 1]
            x_interp.extend(np.linspace(x_start, x_end, frames_per_coord, endpoint=False))
            y_interp.extend(np.linspace(y_start, y_end, frames_per_coord, endpoint=False))

        x_interp.append(coords[-1][0])
        y_interp.append(coords[-1][1])

        def animate(frame):
            current_x, current_y = x_interp[frame], y_interp[frame]
            self.line_x, self.point_y = current_x, current_y
            self.point._offsets3d = ([self.line_x], [self.point_y], [0])
            self.line.set_data([self.line_x, self.line_x], [0, 4])
            self.line.set_3d_properties([0, 0])

        anim = animation.FuncAnimation(self.fig, animate, frames=frames, interval=100, repeat=False)
        self.canvas.draw()

    def take_object(self):
        if None not in (self.object_x, self.object_y, self.object_z):
            x, y, z = [self.line_x, self.object_x], [self.point_y, self.object_y], [0, self.object_z]
            self.gripper = self.ax.plot(x, y, z, color='cornflowerblue', linewidth=4)
            self.canvas.draw()

    def release_object(self):
        if None not in (self.object_x, self.object_y, self.object_z):
            if self.gripper:
                self.gripper.pop(0).remove()
                self.gripper = None
            if self.object_point:
                self.object_point.remove()
                self.object_x = self.object_y = self.object_z = self.object_point = None
            self.canvas.draw()

    def place_object(self):
        coords = self.obj_entry.get()
        if coords:
            try:
                x, y, z = ast.literal_eval(coords)
                x, y = self.line_x, self.point_y
                self.ax.scatter(x, y, z, color='mediumvioletred', s=100)
                self.ax.plot([x], [y], [z], color='mediumvioletred', linewidth=4)
                x_gripper = [
                    self.line_x, self.line_x]
                y_gripper = [self.point_y, self.point_y]
                z_gripper = [0, z]
                self.gripper = self.ax.plot(x_gripper, y_gripper, z_gripper, color='cornflowerblue', linewidth=4)
                self.canvas.draw()
            except (ValueError, SyntaxError):
                messagebox.showerror("Ошибка", "Неверный формат координат")
        else:
            messagebox.showerror("Ошибка", "Координаты не указаны")

    def delete_gripper(self):
        if self.gripper:
            self.gripper.pop(0).remove()
            self.canvas.draw()


def main():
    app = GraphApp()
    app.mainloop()


if __name__ == "__main__":
    main()