from queue import PriorityQueue

class Cell:
    def __init__(self, x, y, has_item):
        self.x, self.y, self.has_item = x, y, has_item

    def get_neighbors(self):
        return [Cell(self.x + i, self.y + j, self.has_item) for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]]

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, Cell) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def toggle_item(self):
        self.has_item = not self.has_item

def heuristic(cell1, cell2):
    return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

def find_path(start, goal, non_existent_cells, flag):
    if flag == 0 and goal.has_item == False and start.has_item == True:
        print("Путь может быть найден, можно положить предмет в эту ячейку")
    elif flag == 1 and goal.has_item == True and start.has_item == False:
        print("Путь может быть найден, можно забрать предмет из ячейки")
    else:
        print("Ошибка, нельзя выполнить действие")
        return None

    if start in non_existent_cells or goal in non_existent_cells:
        return None

    open_set, came_from, g_score, closed_set = PriorityQueue(), {}, {start: 0}, set()

    open_set.put((0, start))

    while not open_set.empty():
        current = open_set.get()[1]
        if current == goal:
            break

        closed_set.add(current)

        neighbors = [neighbor for neighbor in current.get_neighbors() if neighbor not in non_existent_cells and neighbor not in closed_set]

        for neighbor in neighbors:
            new_g_score = g_score[current] + 1
            if neighbor not in g_score or new_g_score < g_score[neighbor]:
                g_score[neighbor] = new_g_score
                f_score = new_g_score + heuristic(neighbor, goal)
                open_set.put((f_score, neighbor))
                came_from[neighbor] = current

    if goal not in came_from:
        return None

    path, current = [], goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path

# все ячейки шкафа
cell_list = [
    Cell(0.5, 0.5, False), Cell(0.5, 1.5, False), Cell(0.5, 2.5, True), Cell(0.5, 3.5, False),
    Cell(1.5, 0.5, False), Cell(1.5, 1.5, False), Cell(1.5, 2.5, False), Cell(1.5, 3.5, False),
    Cell(2.5, 0.5, False), Cell(2.5, 1.5, False), Cell(2.5, 2.5, False), Cell(2.5, 3.5, False),
    Cell(3.5, 0.5, False), Cell(3.5, 1.5, False), Cell(3.5, 2.5, False), Cell(3.5, 3.5, True),
]

non_existent_cells = []

try:
    start, goal = cell_list[0], cell_list[15]
    print(f"Приёмка: {start.x}, {start.y}, {start.has_item}\nЦелевая точка: {goal.x}, {goal.y}, {goal.has_item}")

    # флаг 0 - положить предмет в ячейку; флаг 1 - надо взять предмет из ячейки
    path = find_path(start, goal, non_existent_cells, 1)

    if path is None:
        print("Путь не может быть найден.")
    else:
        pathway = [(cell.x, cell.y) for cell in path]
        print("Найденный путь:", pathway)

    # пример смены флага наличия
    # cell_list[0].toggle_item()
    # print(cell_list[0].has_item)
    # cell_list[0].toggle_item()
    # print(cell_list[0].has_item)
except IndexError:
    print("Ошибка, не существует заданной ячейки")
