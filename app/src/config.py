import json
import core_classes as core

id_config = {"pole_id_length": 2,
             "armoire_id_length": 2,
             "drawer_id_length": 2}

pole_id_counter = 1
armoire_id_counter = 1
drawer_id_counter = 1

def format_id(id: int, id_type: str):
    if id_type == "pole":
        return str(id).zfill(id_config["pole_id_length"])
    elif id_type == "armoire":
        return str(id).zfill(id_config["armoire_id_length"])
    elif id_type == "drawer":
        return str(id).zfill(id_config["drawer_id_length"])


def load_config_from_file(json_config_link, pole_id_counter=1, armoire_id_counter=1, drawer_id_counter=1):
    with open(json_config_link, "r") as json_file:
        config = json.load(json_file)
        poles = []
        invalid_config = False

        if config.get("version") == 1.0:
            # pole
            if config.get("poles") is not None and config["poles"].keys() != []:
                for pole in config["poles"].keys():
                    if check_valid_id(pole, "pole"):
                        poles.append(core.Pole(pole, config["poles"][pole].get("async_work", True)))
                        pole_id_counter += 1 # idk why I was forced to add it as parameter, might be because of "with" keyword

                        # armoire
                        dict_path_pole_as_root = config["poles"][pole]
                        if dict_path_pole_as_root.get("armoires") is not None and dict_path_pole_as_root["armoires"].keys() != []:
                            for armoire in dict_path_pole_as_root["armoires"].keys():
                                if check_valid_id(armoire, "armoire") and dict_path_pole_as_root["armoires"][armoire].get("capacity", None) is not None:
                                    poles[pole_id_counter - 1].add_armoire(core.Armoire(armoire, dict_path_pole_as_root["armoires"][armoire]["capacity"]))
                                    armoire_id_counter += 1

                                # drawer
                                dict_path_armoire_as_root = dict_path_pole_as_root["armoires"][armoire]
                                if dict_path_armoire_as_root.get("drawers") is not None and dict_path_armoire_as_root["drawers"].keys() != []:
                                    for drawer in dict_path_armoire_as_root["drawers"].keys():
                                        if check_valid_id(drawer, "drawer") and dict_path_armoire_as_root["drawers"][drawer].get("capacity", None) is not None:
                                            poles[pole_id_counter - 1].armoires[armoire_id_counter - 1].add_drawer(core.Drawer(drawer, dict_path_armoire_as_root["drawers"][drawer]["capacity"]))
                                            drawer_id_counter += 1
                                        else:
                                            invalid_config = True
                                            break
                                else:
                                    invalid_config = True
                                    break
                                drawer_id_counter = 1
                    else:
                        invalid_config = True
                        break
                    armoire_id_counter = 1

    if not invalid_config:
        return poles
    else:
        return None


def check_valid_id(id: str, id_type: str) -> True | False: # check for valid length and value of id depending on id_type
    if id_type == "pole" and len(id) == id_config["pole_id_length"] and id == format_id(pole_id_counter, "pole"):
        return True
    elif id_type == "armoire" and len(id) == id_config["armoire_id_length"] and id == format_id(armoire_id_counter, "armoire"):
        return True
    elif id_type == "drawer" and len(id) == id_config["drawer_id_length"] and id == format_id(drawer_id_counter, "drawer"):
        return True
    return False


def display_config(): # will print current config in the console
    return