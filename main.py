"""
main.py
Entry point for testing grid presets and yield calculations.
"""

from mutation_collection_processing import CROP_NICKNAMES
import grid_presets


def print_grid_and_yield(grid, farming_fortune=2000, evergreen_bonus=1.6, additive_yield_total=1.0):
    print("Grid layout:")
    print(grid.display())
    print("\nCalculating yield with:")
    print(f"  farming_fortune = {farming_fortune}")
    print(f"  evergreen_bonus = {evergreen_bonus}")
    print(f"  additive_yield_total = {additive_yield_total}")
    total_yield = grid.calculate_total_yield(
        farming_fortune=farming_fortune,
        evergreen_bonus=evergreen_bonus,
        additive_yield_total=additive_yield_total
    )
    print("\nTotal yield from grid:")
    for crop, amount in sorted(total_yield.items()):
        crop_name = CROP_NICKNAMES.get(crop, crop)
        print(f"  {crop_name}: {amount:,.0f}")
    print("\n" + "="*50 + "\n")


def main():
    # Test 1: Full grid of GLOOMGOURD
    print("Test 1: Full grid of GLOOMGOURD")
    grid1 = grid_presets.full_grid("GLOOMGOURD")
    print_grid_and_yield(grid1)

    # Test 2: Alternating rows of GLOOMGOURD and CHOCONUT
    print("Test 2: Alternating rows of GLOOMGOURD and CHOCONUT")
    grid2 = grid_presets.alternating_rows("GLOOMGOURD", "CHOCONUT")
    print_grid_and_yield(grid2)

    # Test 3: Every other column GLOOMGOURD
    print("Test 3: Every other column GLOOMGOURD")
    grid3 = grid_presets.every_other_column("GLOOMGOURD")
    print_grid_and_yield(grid3)

    # Test 4: Checkerboard GLOOMGOURD/CHOCONUT
    print("Test 4: Checkerboard GLOOMGOURD/CHOCONUT")
    grid4 = grid_presets.checkerboard("GLOOMGOURD", "CHOCONUT")
    print_grid_and_yield(grid4)

    # Test 5: Empty grid
    print("Test 5: Empty grid")
    grid5 = grid_presets.empty_grid()
    print_grid_and_yield(grid5)


if __name__ == "__main__":
    main()
