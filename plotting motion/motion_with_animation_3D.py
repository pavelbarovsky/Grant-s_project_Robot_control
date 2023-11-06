import tkinter as tk
from mpl_toolkits.mplot3d import axes3d
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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

        # Labels for coordinate input
        x_label = tk.Label(self, text="Координата X:")
        x_label.pack()
        self.x_entry = tk.Entry(self)
        self.x_entry.pack()

        y_label = tk.Label(self, text="Координата Y:")
        y_label.pack()
        self.y_entry = tk.Entry(self)
        self.y_entry.pack()

        self.button = tk.Button(self, text="Обновить", command=self.update_graph)
        self.button.pack()

        # Начальные значения координат точки и линии
        self.line_x = 0
        self.point_y = 5

        # Рисуем график при запуске приложения
        self.draw_axes()

    def draw_axes(self):
        self.ax.clear()

        # Нарисуйте две параллельные линии по оси X
        x = [0, 10]
        y = [0, 0]
        z = [0, 0]
        self.ax.plot(x, y, z)

        y = [10, 10]
        self.ax.plot(x, y, z)

        # Draw a vertical line on the y-axis
        x = [self.line_x, self.line_x]
        y = [0, 10]
        self.line = self.ax.plot(x, y, z)[0]

        # Нарисуйте точку на вертикальной линии
        x = [self.line_x]
        y = [self.point_y]
        z = [0]
        self.point = self.ax.scatter(x, y, z, color='red')

        # Установите пределы для осей
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])
        self.ax.set_zlim([0, 10])

        # Добавляем метки к осям
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.canvas.draw()

    def update_graph(self):
        # Обновляем координаты линии по оси Y и точки на линии
        new_line_x = float(self.x_entry.get())
        new_point_y = float(self.y_entry.get())

        # Вычисляем промежуточные координаты для анимации
        frames = 60  # количество кадров
        line_x_increment = (new_line_x - self.line_x) / frames
        point_y_increment = (new_point_y - self.point_y) / frames

        def animate(frame):
            # Обновляем координаты линии и точки
            self.line_x += line_x_increment
            self.point_y += point_y_increment

            x = [self.line_x]
            y = [self.point_y]
            z = [0]
            self.point._offsets3d = (x, y, z)  # Обновляем координаты диаграммы рассеяния

            x = [self.line_x, self.line_x]
            y = [0, 10]
            z = [0, 0]
            self.line.set_data(x, y)
            self.line.set_3d_properties(z)

        # Create the animation
        anim = animation.FuncAnimation(
            self.fig, animate, frames=frames, interval=1, repeat=False  # Уменьшен интервал для более быстрой анимации.
        )

        self.canvas.draw()


# Создаем экземпляр приложения и запускаем основной цикл
app = GraphApp()
app.mainloop()