from queue import PriorityQueue


class Cell:
    def __init__(self, x, y, has_item):
        self.x = x
        self.y = y
        self.has_item = has_item

    # определение соседей ячейки
    def get_neighbors(self):
        return [
            Cell(self.x + 1, self.y, self.has_item),
            Cell(self.x - 1, self.y, self.has_item),
            Cell(self.x, self.y + 1, self.has_item),
            Cell(self.x, self.y - 1, self.has_item)
        ]

    # перегрузка оператора < (меньше)
    def __lt__(self, other):
        return False

    # перегрузка оператора == (равно)
    def __eq__(self, other):
        return isinstance(other, Cell) and self.x == other.x and self.y == other.y

    # хэширование значений объектов для оптимизации хранения и взаимодействия
    def __hash__(self):
        return hash((self.x, self.y))

    # функция смены флага наличия объекта в ячейке
    def toggle_item(self):
        self.has_item = not self.has_item


# Эвристика. Манхэттнское расстояние
def heuristic(cell1, cell2):
    return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)


def find_path(start, goal, non_existent_cells, flag):
    if flag == 0:
        if goal.has_item == False and start.has_item == True:
            print("Путь может быть найден, можно положить предмет в эту ячейку")

        else:
            print("Ошибка, нельзя положить предмет в ячейку")
            return None
    elif flag == 1:
        if goal.has_item == True and start.has_item == False:
            print("Путь может быть найден, можно забрать предмет из ячейки")
        else:
            print("Ошибка, нельзя забрать предмет из ячейки")
            return None

    if start in non_existent_cells or goal in non_existent_cells:
        return None

    open_set = PriorityQueue()  # открытый список узлов
    open_set.put((0, start))  # добавление начальной точки
    came_from = {}  # словарь ссылок на родственников
    g_score = {start: 0}  # расстояние от начальной ячейки до остальных
    closed_set = set()  # закрытый список узлов

    while not open_set.empty():
        current = open_set.get()[1]
        if current == goal:
            break

        closed_set.add(current)

        neighbors = current.get_neighbors()

        for neighbor in neighbors:
            if neighbor in non_existent_cells or neighbor in closed_set:
                continue

            new_g_score = g_score[current] + 1
            if neighbor not in g_score or new_g_score < g_score[neighbor]:
                g_score[neighbor] = new_g_score
                f_score = new_g_score + heuristic(neighbor, goal)
                open_set.put((f_score, neighbor))
                came_from[neighbor] = current

    if goal not in came_from:
        return None

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path


# все ячейки шкафа
cell_list = [
    Cell(0, 0, True), Cell(0, 1, False), Cell(0, 2, True), Cell(0, 3, False), Cell(0, 4, True),
    Cell(1, 0, False), Cell(1, 1, False), Cell(1, 2, False), Cell(1, 3, False), Cell(1, 4, False),
    Cell(2, 0, False), Cell(2, 1, False), Cell(2, 2, False), Cell(2, 3, False), Cell(2, 4, False),
    Cell(3, 0, False), Cell(3, 1, False), Cell(3, 2, False), Cell(3, 3, False), Cell(3, 4, False),
    Cell(4, 0, False), Cell(4, 1, False), Cell(4, 2, False), Cell(4, 3, False), Cell(4, 4, False)
]

# список несуществующих ячеек, чтобы выделить приёмку
non_existent_cells = [cell_list[0], cell_list[1], cell_list[3], cell_list[4]]

try:
    start = cell_list[2]
    goal = cell_list[24]

    print(f"Приёмка: {start.x}, {start.y}, {start.has_item}")
    print(f"Целевая точка: {goal.x}, {goal.y}, {goal.has_item}")

    # флаг 0 - положить предмет в ячейку
    # флаг 1 - надо взять предмет из ячейки
    path = find_path(start, goal, non_existent_cells, 0)

    if path is None:
        print("Путь не может быть найден.")
    else:
        pathway = [(cell.x, cell.y) for cell in path]
        print("Найденный путь:", pathway)

    # Пример смены флага has_item у ячейкм
    cell_list[0].toggle_item()
    print(cell_list[0].has_item)
    cell_list[0].toggle_item()
    print(cell_list[0].has_item)
except IndexError:
    print("Ошибка, не существует заданной ячейки")
