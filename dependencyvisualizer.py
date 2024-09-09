import json
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx

def read_json(json_path):
    try:
        # Open the JSON file and load the data
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Failed to find json file in path {json_path}")
    except json.JSONDecodeError:
        print(f"Failed to decode json in file {json_path}")

class DependencyVisualizer:
    def __init__(self, root_path, namespace_blacklist):
        self.root_dir = Path(root_path)
        self.asmdef_files = []
        self.graph = nx.DiGraph()
        self.namespace_blacklist = namespace_blacklist

    def is_blacklisted(self, namespace):
        return not any(namespace.startswith(prefix) for prefix in self.namespace_blacklist)

    def find_asmdef_files(self):
        self.asmdef_files = []
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix == ".asmdef":  # Ensure it's a file
                self.asmdef_files.append(file_path)

    def generate_edges(self):
        self.graph.clear_edges()
        for asmdef_file_path in self.asmdef_files:
            json = read_json(asmdef_file_path.resolve())
            if(json is None or json["references"] is None):
                continue

            name = json["name"]

            if(self.is_blacklisted(name)):
                print("Blocked namespace:",name)
                continue

            for reference in json["references"]:
                if(self.is_blacklisted(reference)):
                    continue
                self.graph.add_edge(json["name"], reference)

vis = DependencyVisualizer("C:/East/Prog/Unity/PackDev", ["Core", "Bootstrapper", "Networking", "PlayerMgmt"])
vis.find_asmdef_files()
vis.generate_edges()

print(f"Cycles: {list(nx.simple_cycles(vis.graph))}")

nx.draw(vis.graph, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
plt.show()
