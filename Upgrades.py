
import random
import json


class Upgrades:
    def __init__(self):
        with open('configs/upgrades.json') as fp:
            data = json.load(fp)
        self.upgrade_list = data.get("upgrades")

    def random_upgrade(self):
        random_index = random.randint(0, len(self.upgrade_list)-1)
        return self.upgrade_list[random_index]

    def apply_upgrade(self, player, upgrade):
        if upgrade.get("effect_operation") == "multiply":
            player.stats_dict[upgrade.get(
                "effected_variable")] *= upgrade.get("upgrade_amount")

        elif upgrade.get("effect_operation") == "addition":
            player.stats_dict[upgrade.get(
                "effected_variable")] += upgrade.get("upgrade_amount")
