"""
Used to generate minecraft registries packet data for every version
"""
import json
import os

PATH = "resources/jars/generated/data/minecraft"
REGISTRIES = (
    "banner_pattern",
    "cat_variant",
    "chicken_variant",
    "cow_variant",
    "frog_variant",
    "pig_variant",
    "wolf_sound_variant",
    "chat_type",
    "damage_type",
    "dimension_type",
    "painting_variant",
    "trim_material",
    "trim_pattern",
    "wolf_variant",
    "worldgen/biome"
)

registries = {}
for registry in REGISTRIES:
    registries[registry] = {}
    for child in os.listdir(f"{PATH}/{registry}"):
        with open(f"{PATH}/{registry}/{child}", encoding="utf-8") as f:
            registries[registry][f"minecraft:{child.removesuffix(".json")}"] = json.load(f)

with open("resources/registries-1.21.8.json", "w", encoding="utf-8") as f:
    json.dump(registries, f, indent=4)
