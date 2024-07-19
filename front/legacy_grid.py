

class RowGridView:
    def __init__(self, cells_sizes: tuple):
        self.cells_sum = sum(cells_sizes)
        self.cells_count = len(cells_sizes)
        self.cells = cells_sizes

    def calc_grid(self, size: int, window_width: int) -> float:
        return (window_width/self.cells_sum)*size