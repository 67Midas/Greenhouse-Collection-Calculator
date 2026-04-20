"""
WIP: Estimate the amount of collection crops generated from a given list of mutations and active effects
"note that the yield upgrade from desk is currently just broken and does nothing" - qtLuna
"all the yield %s are additive except for evergreen chip which is multiplicative 
and then multiplied by farming fortune too" - qtLuna

Data stored in mutation_data.json following the format from planning.md
"""

from dataclasses import dataclass
from typing import Final
import json
import logging


# Load mutation data from JSON
def load_mutation_data() -> dict:
    with open("mutation_data.json", "r") as f:
        return json.load(f)

MUTATION_DATA = load_mutation_data()


@dataclass
class Mutation:
    """Represents a mutation following the planning.md format"""
    name: str
    uses_water: bool
    tier: str  # COMMON, UNCOMMON, RARE, EPIC, LEGENDARY
    total_growth_stages: int
    applies_effects: list[str]
    collection_yield: dict[str, int]
    mutation_item_yield: int
    growth_surface: str
    size: str
    spreading_conditions: dict


def get_mutation(name: str) -> Mutation | None:
    """Get a mutation by name, returns None if not found"""
    data = MUTATION_DATA["mutations"].get(name.upper())
    if data is None:
        return None
    return Mutation(name=name.upper(), **data)


def get_all_mutations() -> list[Mutation]:
    """Get all mutations as a list"""
    return [Mutation(name=name, **data) for name, data in MUTATION_DATA["mutations"].items()]


def get_mutations_by_tier(tier: str) -> list[Mutation]:
    """Get all mutations of a specific tier"""
    return [m for m in get_all_mutations() if m.tier == tier.upper()]


# Crop nickname mapping for display
CROP_NICKNAMES: Final[dict[str, str]] = {
    "MELON": "Melon",
    "PUMPKIN": "Pumpkin",
    "CACTUS": "Cactus",
    "INK_SACK:3": "Cocoa Beans",
    "CARROT_ITEM": "Carrot",
    "WHEAT": "Wheat",
    "SUGAR_CANE": "Sugar Cane",
    "NETHER_STALK": "Netherwart",
    "POTATO_ITEM": "Potato",
    "RED_MUSHROOM": "Mushroom",
    "BROWN_MUSHROOM": "Mushroom",
    "MOONFLOWER": "Moonflower",
    "WILD_ROSE": "Wild Rose",
    "DOUBLE_PLANT": "Sunflower",
}

NPC_SELL_PRICES: Final[dict[str, float]] = {
    "MELON": 2,
    "PUMPKIN": 10,
    "CACTUS": 4,
    "INK_SACK:3": 3,
    "CARROT_ITEM": 3,
    "WHEAT": 6,
    "SUGAR_CANE": 4,
    "NETHER_STALK": 4,
    "POTATO_ITEM": 3,
    "RED_MUSHROOM": 10,
    "BROWN_MUSHROOM": 10,
    "MOONFLOWER": 4,
    "WILD_ROSE": 4,
    "DOUBLE_PLANT": 4,
}


# =============================================================================
# Effect System
# =============================================================================

# Effect definitions: effect_name -> (yield_modifier, xp_modifier, water_modifier, description)
EFFECT_DEFINITIONS: Final[dict[str, tuple[float, float, float, str]]] = {
    "Harvest Boost": (0.2, 0.0, 0.0, "Increases Yield by +20%"),
    "Improved Harvest Boost": (0.3, 0.0, 0.0, "Increases Yield by +30%"),
    "XP Boost": (0.0, 0.2, 0.0, "Increases Farming XP of adjacent crops by +20%"),
    "Improved XP Boost": (0.0, 0.3, 0.0, "Increases Farming XP of adjacent crops by +30%"),
    "Water Retain": (0.0, 0.0, 0.5, "Retains watering status of adjacent crops by +50%"),
    "Improved Water Retain": (0.0, 0.0, 1.0, "Retains watering status of adjacent crops by +100%"),
    "Immunity": (0.0, 0.0, 0.0, "Provides Immunity to negative effects."),
    "Effect Spread": (0.0, 0.0, 0.0, "Spreads other buffs and debuffs on the current crop to adjacent crops."),
    "Bonus Drops": (0.0, 0.0, 0.0, "Harvested items additionally roll from an extra loot pool."),
    "Harvest Loss": (-0.2, 0.0, 0.0, "Decreases Yield by -20%"),
    "XP Loss": (0.0, -0.2, 0.0, "Reduces Farming XP of adjacent crops by -20%"),
    "Water Drain": (0.0, 0.0, -0.3, "Reduces watering status of nearby crops by -30%"),
}


def get_effect_modifiers(effect_name: str) -> tuple[float, float, float]:
    """Get (yield_mod, xp_mod, water_mod) for an effect. Returns (0,0,0) if effect not found."""
    if effect_name in EFFECT_DEFINITIONS:
        return EFFECT_DEFINITIONS[effect_name][:3]
    logging.warning(f"Unknown effect: {effect_name}")
    return (0.0, 0.0, 0.0)


def calculate_additive_yield_from_effects(effects: list[str]) -> float:
    """
    Calculate the additive yield modifier from a list of effects.
    All yield modifiers are additive.
    """
    total_yield_mod = 0.0
    for effect in effects:
        yield_mod, _, _ = get_effect_modifiers(effect)
        total_yield_mod += yield_mod
    return total_yield_mod


# TODO: Implement effect system and yield calculation
# For testing purposes using placeholder values
def mutation_to_collection(mutation_name: str, farming_fortune: int, evergreen_bonus: float, additive_yield_total: float):
    mutation = get_mutation(mutation_name)
    if mutation is None:
        logging.warning(f"Mutation '{mutation_name}' not found")
        return {}
    
    temp_dict = {}
    for key, value in mutation.collection_yield.items():
        temp_dict[key] = value * farming_fortune * additive_yield_total * evergreen_bonus
    return temp_dict


# =============================================================================
# Grid and Tile classes for greenhouse simulation
# =============================================================================

@dataclass
class Tile:
    """Represents a single tile in the greenhouse grid"""
    mutation: str | None  # Mutation name (e.g., "GLOOMGOURD") or None if empty
    water_level: float = 0.0  # Range: -100 to 100
    flooring_material: str = "Farmland"
    active_effects: list[str] = None
    
    def __post_init__(self):
        if self.active_effects is None:
            self.active_effects = []


class Grid:
    """10x10 grid of tiles for the greenhouse"""
    
    GRID_SIZE = 10
    
    def __init__(self):
        self.tiles: list[list[Tile]] = [
            [Tile(mutation=None) for _ in range(self.GRID_SIZE)]
            for _ in range(self.GRID_SIZE)
        ]
    
    def set_mutation(self, row: int, col: int, mutation_name: str | None) -> bool:
        """Set a mutation at a specific position. Returns True if successful."""
        if not self._is_valid_position(row, col):
            logging.warning(f"Invalid position: ({row}, {col})")
            return False
        
        if mutation_name is not None and get_mutation(mutation_name) is None:
            logging.warning(f"Unknown mutation: {mutation_name}")
            return False
        
        self.tiles[row][col].mutation = mutation_name
        return True
    
    def get_mutation(self, row: int, col: int) -> Mutation | None:
        """Get the mutation at a specific position"""
        if not self._is_valid_position(row, col):
            return None
        mutation_name = self.tiles[row][col].mutation
        return get_mutation(mutation_name) if mutation_name else None
    
    def get_tile(self, row: int, col: int) -> Tile | None:
        """Get the tile at a specific position"""
        if not self._is_valid_position(row, col):
            return None
        return self.tiles[row][col]
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within grid bounds"""
        return 0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE
    
    def get_adjacent_tiles(self, row: int, col: int) -> list[Tile]:
        """Get all adjacent tiles (including diagonals)"""
        adjacent = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if self._is_valid_position(new_row, new_col):
                    adjacent.append(self.tiles[new_row][new_col])
        return adjacent
    
    def get_all_mutations(self) -> list[tuple[int, int, Mutation]]:
        """Get all mutations in the grid with their positions"""
        mutations = []
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                mutation = self.get_mutation(row, col)
                if mutation:
                    mutations.append((row, col, mutation))
        return mutations
    
    def calculate_total_yield(
        self,
        farming_fortune: int,
        evergreen_bonus: float = 1.0,
        additive_yield_total: float = 1.0
    ) -> dict[str, float]:
        """
        Calculate total collection yield from all mutations in the grid.
        Returns a dict mapping crop type to total yield.
        
        Effects from adjacent tiles are collected and applied to each tile's yield.
        """
        total_yield: dict[str, float] = {}
        
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                mutation_name = self.tiles[row][col].mutation
                if mutation_name is None:
                    continue
                
                # Get the mutation object
                mutation = get_mutation(mutation_name)
                if mutation is None:
                    continue
                
                # Collect all effects: own effects + adjacent tiles' effects
                all_effects = list(mutation.applies_effects)  # Start with own effects
                
                # Add effects from adjacent tiles
                adjacent_tiles = self.get_adjacent_tiles(row, col)
                for tile in adjacent_tiles:
                    if tile.mutation:
                        adj_mutation = get_mutation(tile.mutation)
                        if adj_mutation:
                            all_effects.extend(adj_mutation.applies_effects)
                
                # Calculate additive yield from all effects
                effect_yield_mod = calculate_additive_yield_from_effects(all_effects)
                
                # Calculate yield for this mutation with effects applied
                yield_dict = mutation_to_collection(
                    mutation_name,
                    farming_fortune,
                    evergreen_bonus,
                    additive_yield_total + effect_yield_mod  # Add effect modifier
                )
                
                # Aggregate yields
                for crop, amount in yield_dict.items():
                    total_yield[crop] = total_yield.get(crop, 0) + amount
        
        return total_yield
    
    def display(self) -> str:
        """Display the grid as a string (for debugging)"""
        lines = []
        for row in range(self.GRID_SIZE):
            row_str = ""
            for col in range(self.GRID_SIZE):
                mut = self.tiles[row][col].mutation
                if mut:
                    # Abbreviate mutation name to 4 chars
                    row_str += f"{mut[:4]:<5} "
                else:
                    row_str += "----- "
            lines.append(row_str)
        return "\n".join(lines)


def create_example_grid() -> Grid:
    """Create an example 10x10 grid with some mutations"""
    grid = Grid()
    
    # Example: Fill some positions with mutations
    grid.set_mutation(0, 0, "GLOOMGOURD")
    grid.set_mutation(0, 1, "CHOCONUT")
    grid.set_mutation(1, 0, "DUSTGRAIN")
    grid.set_mutation(1, 1, "ASHWREATH")
    grid.set_mutation(2, 2, "LONELILY")
    grid.set_mutation(3, 3, "SCOURROOT")
    
    return grid


# Test loading mutations
if __name__ == "__main__":
    # Test getting a mutation
    gloomgourd = get_mutation("GLOOMGOURD")
    if gloomgourd:
        print(f"Loaded {gloomgourd.name} ({gloomgourd.tier})")
        print(f"  Effects: {gloomgourd.applies_effects}")
        print(f"  Yield: {gloomgourd.collection_yield}")
        print(f"  Uses water: {gloomgourd.uses_water}")
    
    # Test getting all tiers
    print("\nMutations by tier:")
    for tier in ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY"]:
        mutations = get_mutations_by_tier(tier)
        print(f"  {tier}: {len(mutations)} mutations")
    
    # Test Grid functionality
    print("\n" + "="*50)
    print("Testing Grid functionality")
    print("="*50)
    
    # Create a grid and set some mutations
    grid = Grid()
    grid.set_mutation(0, 0, "GLOOMGOURD")
    grid.set_mutation(0, 1, "CHOCONUT")
    grid.set_mutation(1, 0, "DUSTGRAIN")
    grid.set_mutation(1, 1, "ASHWREATH")
    grid.set_mutation(2, 2, "LONELILY")
    grid.set_mutation(3, 3, "SCOURROOT")
    grid.set_mutation(4, 4, "SHADEVINE")
    grid.set_mutation(5, 5, "VEILSHROOM")
    
    print("\nGrid layout:")
    print(grid.display())
    
    # Calculate total yield
    print("\nCalculating yield with:")
    print("  farming_fortune = 2000")
    print("  evergreen_bonus = 1.6")
    print("  additive_yield_total = 1.0")
    
    total_yield = grid.calculate_total_yield(
        farming_fortune=2000,
        evergreen_bonus=1.6,
        additive_yield_total=1.0
    )
    
    print("\nTotal yield from grid:")
    for crop, amount in sorted(total_yield.items()):
        crop_name = CROP_NICKNAMES.get(crop, crop)
        print(f"  {crop_name}: {amount:,.0f}")