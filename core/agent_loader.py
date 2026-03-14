import os
import importlib


AGENTS_FOLDER = "agents"


def load_agents():

    agents = {}

    for file in os.listdir(AGENTS_FOLDER):

        if file.endswith(".py") and not file.startswith("_"):

            module_name = file[:-3]

            module = importlib.import_module(f"agents.{module_name}")

            for attr in dir(module):

                obj = getattr(module, attr)

                if isinstance(obj, type):

                    if attr.endswith("Agent"):

                        agents[module_name] = obj()

    return agents
