mutation:
	uses_water: bool
	tier: str
	total_growth_stages: int
	applies_effects: list[str]
	collection_yield: dict{str: int}
	mutation_item_yield: int
Tile:
	 mutation: str | None
water_level: float between [-100, 100]
flooring_material: str 
active_effects: list[str]
grid: list[list[tile]]
active_grids: list[grid], maximum length of 3


Effect Types:
	Bonus Drops
Yield modifiers
XP modifiers
Water modifiers
Special effects (IMMUNITY, EFFECT_SPREAD)

Simulation Tick Order:
1)	Update tile state (water level, growth stage, interaction timers)
2)	Handle growth completion / harvesting
3)	Clear all active_effects on non-harvestable tiles
4)	Each tile emits effects to adjacent tiles
5)	Apply and resolve effects (stacking, immunity, etc.)

Notes/design decisions:
Adjacent tiles includes diagonally touching tiles. 
Mutations are data-driven (dicts) to allow easy balancing and extension
	Tile is a class to encapsulate state and behavior
Effects are string identifiers to keep the system flexible
