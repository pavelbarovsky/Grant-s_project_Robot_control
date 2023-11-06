import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation


class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("График")
        self.geometry("500x610")
        self.fig = plt.figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111)


        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Подписи для места ввода координат
        x_label = tk.Label(self, text="X координата:")
        x_label.pack()
        self.x_entry = tk.Entry(self)
        self.x_entry.pack()

        y_label = tk.Label(self, text="Y координата:")
        y_label.pack()
        self.y_entry = tk.Entry(self)
        self.y_entry.pack()

        self.button = tk.Button(self, text="Отрисовать график", command=self.update_graph)
        self.button.pack()

        # Изначальные значения координат точки и прямой
        self.line_x = 0
        self.point_y = 5

        # Отрисовка графика при запуске приложения
        self.draw_axes()

    def draw_axes(self):
        self.ax.clear()

        # Рисуем горизонтальные прямые сверху и снизу
        x = [0, 9.99]
        y = [0, 0]
        self.ax.plot(x, y, color='blue')

        y = [9.98, 9.98]
        self.ax.plot(x, y, color='blue')

        # Рисуем вертикальную прямую на оси x
        x = [self.line_x, self.line_x]
        y = [0, 10]
        self.line = self.ax.plot(x, y, color='red')[0]

        # Рисуем точку на вертикальной прямой
        x = [self.line_x]
        y = [self.point_y]
        self.point = self.ax.scatter(x, y, color='red')

        self.ax.grid(True)

        # Устанавливаем пределы для осей
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])

        # Добавляем подписи к осям
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")

        self.canvas.draw()

    def update_graph(self):
        # Обновляем координаты прямой на оси ординат и точки на прямой
        new_line_x = float(self.x_entry.get())
        new_point_y = float(self.y_entry.get())

        # Вычисляем промежуточные координаты для анимации
        frames = 60
        line_x_increment = (new_line_x - self.line_x) / frames
        point_y_increment = (new_point_y - self.point_y) / frames

        def animate(frame):
            # Обновляем координаты прямой и точки
            self.line_x += line_x_increment
            self.point_y += point_y_increment

            x = [self.line_x]
            y = [self.point_y]
            self.point.set_offsets([x[0], y[0]])

            x = [self.line_x, self.line_x]
            y = [0, 10]
            self.line.set_data(x, y)

        # Создаем анимацию
        anim = animation.FuncAnimation(
            self.fig, animate, frames=frames, interval=20, repeat=False
        )

        self.canvas.draw()


if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()