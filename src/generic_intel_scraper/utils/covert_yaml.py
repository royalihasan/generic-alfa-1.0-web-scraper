import yaml


def yaml_to_selector(selectors):

    with open(f"./generic_intel_scraper/selectors\\{selectors}.yaml") as file:
        sel = yaml.load(file, Loader=yaml.SafeLoader)
        return sel

