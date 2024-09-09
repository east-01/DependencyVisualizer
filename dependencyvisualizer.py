import json
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import argparse

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
    def __init__(self, root_path, namespace_blacklist=[]):
        self.root_dir = Path(root_path)
        self.asmdef_files = []
        self.graph = nx.DiGraph()
        self.namespace_whitelist = namespace_blacklist

    def is_whitelisted(self, namespace):
        if(self.namespace_whitelist is None or len(self.namespace_whitelist) == 0):
            return True
        return any(namespace.startswith(prefix) for prefix in self.namespace_whitelist)

    def find_asmdef_files(self):
        self.asmdef_files = []
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix == ".asmdef":
                self.asmdef_files.append(file_path)

    def generate_edges(self):
        self.graph.clear_edges()
        for asmdef_file_path in self.asmdef_files:
            json = read_json(asmdef_file_path.resolve())
            if(json is None or json["references"] is None):
                continue

            name = json["name"]

            if(not self.is_whitelisted(name)):
                print("Blocked namespace:",name)
                continue

            for reference in json["references"]:
                if(not self.is_whitelisted(reference)):
                    continue
                self.graph.add_edge(json["name"], reference)

parser = argparse.ArgumentParser(description="Visualize .asmdef dependencies")
parser.add_argument('root_path', type=str, help="The root filepath that .asmdef files will be searched for")
parser.add_argument('--ns_whitelist', type=str, help="Optional, a list of namespaces that are whitelisted. All other namespaces will be ignored. (SEPARATE VALUES WITH COMMAS AND NO SPACES)")
args = parser.parse_args()

ns_whitelist = []
if(args.ns_whitelist is not None):
    ns_whitelist = args.ns_whitelist.split(",")

vis = DependencyVisualizer(args.root_path, ns_whitelist)
vis.find_asmdef_files()
vis.generate_edges()

print(f"Cycles: {list(nx.simple_cycles(vis.graph))}")

nx.draw(vis.graph, nx.circular_layout(vis.graph), with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
plt.show()
