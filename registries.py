import json
import os

PATH = "resources/jars/generated/data/minecraft"
REGISTRIES = (
    "banner_pattern",
    "chat_type",
    "damage_type",
    "dimension_type",
    "painting_variant",
    "trim_material",
    "trim_pattern",
    "wolf_variant",
    "worldgen/biome"
)

registries = dict()
for registry in REGISTRIES:
    registries[registry] = dict()
    for child in os.listdir(f"{PATH}/{registry}"):
        with open(f"{PATH}/{registry}/{child}") as f:
            registries[registry][f"minecraft:{child.removesuffix(".json")}"] = json.load(f)

with open("resources/registries-1.21.4.json", "w") as f:
    json.dump(registries, f, indent=4)
