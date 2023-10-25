import random
import json


class Upgrades:
    def __init__(self, upgrade_data_file):
        with open(upgrade_data_file, 'r') as fp:
            self.upgrade_data = json.load(fp).get("upgrades")

    def get_upgrade(self, upgrade_name):
        upgrade = self.upgrade_data.get(upgrade_name)
        if upgrade:
            return upgrade_name, upgrade  # Return both the name and the upgrade data
        else:
            return None

    def random_upgrade(self):
        upgrade_names = list(self.upgrade_data.keys())
        random_upgrade_name = random.choice(upgrade_names)
        return random_upgrade_name, self.upgrade_data[random_upgrade_name]

    def apply_upgrade(self, player, upgrade_name):
        upgrade_data = self.get_upgrade(upgrade_name)
        
        if upgrade_data:
            upgrade_name, upgrade = upgrade_data  # Unpack the values if the data is not None

            effect_operation = upgrade.get("effect_operation")
            effected_variable = upgrade.get("effected_variable")
            upgrade_amount = upgrade.get("upgrade_amount")

            if effect_operation == "multiply":
                player.stats_dict[effected_variable] *= upgrade_amount

            elif effect_operation == "divide":
                player.stats_dict[effected_variable] /= upgrade_amount

            elif effect_operation == "addition":
                player.stats_dict[effected_variable] += upgrade_amount

            elif effect_operation == "subtract":
                player.stats_dict[effected_variable] -= upgrade_amount

            else:
                print("Unknown upgrade operation")
        else:
            print(f"Upgrade '{upgrade_name}' not found in the JSON data")

    def display_all_upgrades(self):
        print("Available Upgrades:")
        for upgrade_name, upgrade_data in self.upgrade_data.items():
            print(f"Upgrade Name: {upgrade_name}")
            print(f"Upgrade Amount: {upgrade_data['upgrade_amount']}")
            print(f"Effected Variable: {upgrade_data['effected_variable']}")
            print(f"Effect Operation: {upgrade_data['effect_operation']}")
            print("-" * 30)