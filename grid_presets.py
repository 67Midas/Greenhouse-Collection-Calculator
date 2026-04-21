"""
grid_presets.py
Preset grid generators for testing greenhouse mutation grids.
"""

from mutation_collection_processing import Grid

def full_grid(mutation_name: str) -> Grid:
    """Fill the entire grid with the same mutation."""
    grid = Grid()
    for row in range(grid.GRID_SIZE):
        for col in range(grid.GRID_SIZE):
            grid.set_mutation(row, col, mutation_name)
    return grid

def alternating_rows(mutation1: str, mutation2: str) -> Grid:
    """Alternate two mutations by row."""
    grid = Grid()
    for row in range(grid.GRID_SIZE):
        mut = mutation1 if row % 2 == 0 else mutation2
        for col in range(grid.GRID_SIZE):
            grid.set_mutation(row, col, mut)
    return grid

def every_other_column(mutation_name: str) -> Grid:
    """Fill every other column with the mutation, leave the rest empty."""
    grid = Grid()
    for row in range(grid.GRID_SIZE):
        for col in range(grid.GRID_SIZE):
            if col % 2 == 0:
                grid.set_mutation(row, col, mutation_name)
    return grid

def checkerboard(mutation1: str, mutation2: str) -> Grid:
    """Checkerboard pattern of two mutations."""
    grid = Grid()
    for row in range(grid.GRID_SIZE):
        for col in range(grid.GRID_SIZE):
            mut = mutation1 if (row + col) % 2 == 0 else mutation2
            grid.set_mutation(row, col, mut)
    return grid

def empty_grid() -> Grid:
    """Return an empty grid (no mutations)."""
    return Grid()
