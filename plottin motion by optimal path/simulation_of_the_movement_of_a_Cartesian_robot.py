import tkinter as tk
from mpl_toolkits.mplot3d import axes3d
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import ast
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Движение робота")
        self.geometry("500x790")
        self.fig = plt.figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Метка для ввода координат
        coords_label = tk.Label(self, text="Путь. Координаты (в формате [(0, 2), (1, 2), ...]):")
        coords_label.pack()
        self.coords_entry = tk.Entry(self)
        self.coords_entry.pack()

        self.paste_button = tk.Button(self, text="Вставить", command=self.paste_coords)
        self.paste_button.pack()

        self.button = tk.Button(self, text="Обновить", command=self.update_graph)
        self.button.pack()

        # Метка для ввода координат предмета
        obj_label = tk.Label(self, text="Координаты предмета (в формате (2.5, 3.5, 0.5)):")
        obj_label.pack()
        self.obj_entry = tk.Entry(self)
        self.obj_entry.pack()

        self.add_obj_button = tk.Button(self, text="Добавить предмет", command=self.add_object_coordinates)
        self.add_obj_button.pack()

        self.take_obj_button = tk.Button(self, text="Выдвинуть хваталку", command=self.take_object)
        self.take_obj_button.pack()

        self.release_obj_button = tk.Button(self, text="Забрать предмет", command=self.release_object)
        self.release_obj_button.pack()

        self.place_obj_button = tk.Button(self, text="Положить предмет", command=self.place_object)
        self.place_obj_button.pack()

        self.place_obj_button = tk.Button(self, text="Убрать хваталку", command=self.delete_gripper)
        self.place_obj_button.pack()

        # Начальные значения координат точки и линии
        self.line_x = 0.5
        self.point_y = 0.5

        self.gripper = None

        # Рисуем график при запуске приложения
        self.draw_axes()

    def draw_axes(self):
        self.ax.clear()

        # Нарисуем вертикальные линии сетки
        for i in range(5):
            x = [i, i]
            y = [0, 4]
            z = [0, 0]
            self.ax.plot(x, y, z, color='gray')

        # Нарисуем горизонтальные линии сетки
        for i in range(5):
            x = [0, 4]
            y = [i, i]
            z = [0, 0]
            self.ax.plot(x, y, z, color='gray')

        # Закрасим рабочую плоскость
        x = range(5)
        y = range(5)
        X, Y = np.meshgrid(x, y)
        Z = X * 0
        self.ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.25)

        # Нарисуем две параллельные линии по оси X
        x = [0, 4]
        y = [0, 0]
        z = [0, 0]
        self.ax.plot(x, y, z, color='blue', linewidth=4)

        y = [4, 4]
        self.ax.plot(x, y, z, color='blue', linewidth=4)

        # Нарисуем вертикальную линию по оси Y
        x = [self.line_x, self.line_x]
        y = [0, 4]
        self.line = self.ax.plot(x, y, z, color='purple', linewidth=4)[0]

        # Нарисуем точку на вертикальной линии
        x = [self.line_x]
        y = [self.point_y]
        z = [0]
        self.point = self.ax.scatter(x, y, z, color='orange', linewidth=6)

        # Установим пределы для осей
        self.ax.set_xlim([0, 4])
        self.ax.set_ylim([0, 4])
        self.ax.set_zlim([0, 1])

        # Добавим метки к осям
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.canvas.draw()

    def paste_coords(self):
        coords_str = self.clipboard_get()
        self.coords_entry.delete(0, tk.END)
        self.coords_entry.insert(0, coords_str)

    def add_object_coordinates(self):
        obj_coords = self.obj_entry.get()
        try:
            obj_coords = ast.literal_eval(obj_coords)
            if isinstance(obj_coords, tuple) and len(obj_coords) == 3:
                x, y, z = obj_coords

                # Сохраняем координаты в переменные
                self.object_x = x
                self.object_y = y
                self.object_z = z

                # Отрисовка красной точки на рисунке
                self.object_point = self.ax.scatter(x, y, z, color='red', s=100)
                self.canvas.draw()
            else:
                messagebox.showerror("Ошибка", "Неверный формат координат предмета")
        except (ValueError, SyntaxError):
            messagebox.showerror("Ошибка", "Неверный формат координат предмета")

    def update_graph(self):
        # Получаем введенную строку координат и преобразуем её в список координат
        coords_str = self.coords_entry.get()
        try:
            coords = ast.literal_eval(coords_str)
        except (SyntaxError, ValueError):
            # Если произошла ошибка при разборе строки, выводим сообщение об ошибке
            messagebox.showerror("Ошибка", "Некорректный формат ввода координат")
            return

        if not isinstance(coords, list):
            messagebox.showerror("Ошибка", "Некорректный формат ввода координат")
            return

        # Вычисляем промежуточные координаты для анимации
        frames_per_coord = 10  # количество кадров на каждую координату
        frames = (len(coords) - 1) * frames_per_coord + 1

        # Создаем массив равномерно распределенных промежуточных значений для каждой координаты
        x_interp = []
        y_interp = []

        for i in range(len(coords) - 1):
            x_start, y_start = coords[i]
            x_end, y_end = coords[i + 1]
            x_interp.extend(np.linspace(x_start, x_end, frames_per_coord, endpoint=False))
            y_interp.extend(np.linspace(y_start, y_end, frames_per_coord, endpoint=False))

        x_interp.append(coords[-1][0])
        y_interp.append(coords[-1][1])

        def animate(frame):
            # Получаем текущие промежуточные координаты
            current_x = x_interp[frame]
            current_y = y_interp[frame]

            # Обновляем координаты линии и точки
            self.line_x = current_x
            self.point_y = current_y

            x = [self.line_x]
            y = [self.point_y]
            z = [0]
            self.point._offsets3d = (x, y, z)  # Обновляем координаты диаграммы рассеяния

            x = [self.line_x, self.line_x]
            y = [0, 4]
            z = [0, 0]
            self.line.set_data(x, y)
            self.line.set_3d_properties(z)

        # Создаем анимацию
        anim = animation.FuncAnimation(
            self.fig, animate, frames=frames, interval=100, repeat=False
        )

        self.canvas.draw()

    def take_object(self):
        if self.object_x is not None and self.object_y is not None and self.object_z is not None:
            # Создаем линию "gripper" из точки orange до точки с сохраненными координатами
            x = [self.line_x, self.object_x]
            y = [self.point_y, self.object_y]
            z = [0, self.object_z]
            self.gripper = self.ax.plot(x, y, z, color='green', linewidth=2)
            self.canvas.draw()

    def release_object(self):
        if self.object_x is not None and self.object_y is not None and self.object_z is not None:
            # Удаляем линию "gripper" с рисунка
            if self.gripper is not None:
                self.gripper.pop(0).remove()
                self.gripper = None

            # Сохраняем координату Z перед удалением точки
            z_before_removal = self.object_z

            # Удаляем красную точку с рисунка
            if self.object_point is not None:
                self.object_point.remove()
                self.object_x = None
                self.object_y = None
                self.object_z = None
                self.object_point = None

            self.canvas.draw()

            # Используйте переменную z_before_removal для необходимых дальнейших действий
            print("Координата Z перед удалением точки:", z_before_removal)

    def place_object(self):
        coords = self.obj_entry.get()

        if coords:
            try:
                x, y, z = ast.literal_eval(coords)

                x = self.line_x
                y = self.point_y

                self.ax.scatter(x, y, z, color='blue', s=100)
                self.ax.plot([x], [y], [z], color='blue', linewidth=4)

                # Создаем линию "gripper" из точки orange до точки с сохраненными координатами
                x_gripper = [self.line_x, self.line_x]
                y_gripper = [self.point_y, self.point_y]
                z_gripper = [0, z]
                self.gripper = self.ax.plot(x_gripper, y_gripper, z_gripper, color='green', linewidth=2)

                self.canvas.draw()
            except (ValueError, SyntaxError):
                messagebox.showerror("Ошибка", "Неверный формат координат")
        else:
            messagebox.showerror("Ошибка", "Координаты не указаны")

    def delete_gripper(self):
        if self.gripper:
            self.gripper.pop(0).remove()  # Удаляем линию gripper из графического контекста
            self.canvas.draw()


def main():
    # Создаем экземпляр приложения и запускаем основной цикл
    app = GraphApp()
    app.mainloop()


if __name__ == "__main__":
    main()