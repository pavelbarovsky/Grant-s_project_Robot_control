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
        self.geometry("500x610")
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

        # Начальные значения координат точки и линии
        self.line_x = 0.5
        self.point_y = 0.5

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
        self.ax.plot(x, y, z, color='blue')

        y = [4, 4]
        self.ax.plot(x, y, z, color='blue')

        # Нарисуем вертикальную линию по оси Y
        x = [self.line_x, self.line_x]
        y = [0, 4]
        self.line = self.ax.plot(x, y, z, color='purple')[0]

        # Нарисуем точку на вертикальной линии
        x = [self.line_x]
        y = [self.point_y]
        z = [0]
        self.point = self.ax.scatter(x, y, z, color='orange')

        # Установим пределы для осей
        self.ax.set_xlim([0, 4])
        self.ax.set_ylim([0, 4])
        self.ax.set_zlim([0, 4])

        # Добавим метки к осям
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.canvas.draw()

    def paste_coords(self):
        coords_str = self.clipboard_get()
        self.coords_entry.delete(0, tk.END)
        self.coords_entry.insert(0, coords_str)


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
        frames = len(coords) * 10  # увеличиваем количество кадров в 10 раз

        # Создаем массив равномерно распределенных промежуточных значений для каждой координаты
        x_interp = np.linspace(self.line_x, coords[-1][0], frames)
        y_interp = np.linspace(self.point_y, coords[-1][1], frames)

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


def main():
    # Создаем экземпляр приложения и запускаем основной цикл
    app = GraphApp()
    app.mainloop()


if __name__ == "__main__":
    main()