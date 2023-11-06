import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("График")
        self.geometry("500x610")
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')

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

        # Рисуем две параллельные прямые на оси x
        x = [0, 10]
        y = [0, 0]
        z = [0, 0]
        self.ax.plot(x, y, z)

        y = [10, 10]
        self.ax.plot(x, y, z)

        # Рисуем вертикальную прямую на оси y
        x = [self.line_x, self.line_x]
        y = [0, 10]
        self.line = self.ax.plot(x, y, z)[0]

        # Рисуем точку на вертикальной прямой
        x = [self.line_x]
        y = [self.point_y]
        z = [0]
        self.point = self.ax.scatter(x, y, z, color='red')

        # Устанавливаем пределы для осей
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])
        self.ax.set_zlim([0, 10])

        # Добавляем подписи к осям
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.canvas.draw()

    def update_graph(self):
        # Обновляем координаты прямой на оси ординат и точки на прямой
        new_line_x = float(self.x_entry.get())
        new_point_y = float(self.y_entry.get())

        # Перерисовываем график с новыми координатами
        self.line_x = new_line_x
        self.point_y = new_point_y
        self.draw_axes()


if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()