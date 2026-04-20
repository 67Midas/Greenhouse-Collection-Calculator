"""
WIP: Estimate the amount of collection crops generated from a given list of mutations and active effects
"note that the yield upgrade from desk is currently just broken and does nothing" - qtLuna
"all the yield %s are additive except for evergreen chip which is multiplicative 
and then multiplied by farming fortune too" - qtLuna

"""


from typing import Final
import logging


CROP_NICKNAMES: Final[dict[str, str]] = {
    "MELON": "Melon",
    "PUMPKIN": "Pumpkin",
    "CACTUS": "Cactus",
    "INK_SACK:3": "Cocoa Beans",   # Cocoa Beans
    "CARROT_ITEM": "Carrot",
    "WHEAT": "Wheat",
    "SUGAR_CANE": "Sugar Cane",
    "NETHER_STALK": "Netherwart",
    "POTATO_ITEM": "Potato",
    "RED_MUSHROOM": "Mushroom",
    "MOONFLOWER": "Moonflower",
    "WILD_ROSE": "Wild Rose",
    "DOUBLE_PLANT": "Sunflower",  # Sunflower
}

NPC_SELL_PRICES: Final[dict[str, float]] = {
    "MELON": 2,
    "PUMPKIN": 10,
    "CACTUS": 4,
    "INK_SACK:3": 3,   # Cocoa Beans
    "CARROT_ITEM": 3,
    "WHEAT": 6,
    "SUGAR_CANE": 4,
    "NETHER_STALK": 4,
    "POTATO_ITEM": 3,
    "RED_MUSHROOM": 10,
    "MOONFLOWER": 4,
    "WILD_ROSE": 4,
    "DOUBLE_PLANT": 4,  # Sunflower
}

# Ok I really need to just make a tile class, and make a design doc before I keep doing this
"""
base_crops = {
    "MELON": {"MELON": 320, "APPLIES"},
    "PUMPKIN": 10,
    "CACTUS": 4,
    "INK_SACK:3": 3,   # Cocoa Beans
    "CARROT_ITEM": 3,
    "WHEAT": 6,
    "SUGAR_CANE": 4,
    "NETHER_STALK": 4,
    "POTATO_ITEM": 3,
    "RED_MUSHROOM": 10,
    "MOONFLOWER": 4,
    "WILD_ROSE": 4,
    "DOUBLE_PLANT": 4,  # Sunflower
}
"""

common_mutations = {
    "ASHWREATH": {"NETHER_STALK": 360},
    "CHOCONUT": {"INK_SACK:3": 200},
    "DUSTGRAIN": {"WHEAT": 100},
    "GLOOMGOURD": {"PUMPKIN": 30, "MELON": 140},
    "LONELILY": {"POTATO_ITEM": 600, "CARROT_ITEM": 700, "PUMPKIN": 340},
    "SCOURROOT": {"POTATO_ITEM": 105, "CARROT_ITEM": 122},
    "SHADEVINE": {"CACTUS": 68, "SUGAR_CANE": 90},
    "VEILSHROOM": {"RED_MUSHROOM": 33*2},   # I'm not going to bother differentiating red and brown mushrooms
    "WITHERBLOOM": {"WILD_ROSE": 300}
}



# TODO: Eventually additive_yield_bonus should be calculated based on the effects of the given mutation
# For testing purposes it's not but once the effects parsing is added, update this method
# Also mutation's type probably shouldn't be str, I should make a custom class for it to hold the active effects it has
# I really should've made a design doc - make a design doc before spending too much more time on this
def mutation_to_collection(mutation: str, farming_fortune: int, evergreen_bonus: float, additive_yield_total: float):
    temp_dict = {}
    for key, value in common_mutations[mutation].items():
        temp_dict[key] = value*farming_fortune*additive_yield_total*evergreen_bonus # Note: ask Luna how Hypixel handles rounding with the greenhouse
    return temp_dict

# Test it:
print(mutation_to_collection(mutation = "GLOOMGOURD", farming_fortune=2000, evergreen_bonus=1.6, additive_yield_total=1.0))