import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import random
from ipaddress import IPv4Address

# Create a network with routers and servers
G = nx.Graph()
edges = [
    ("Router A", "Router B", 4), ("Router A", "Router C", 2),
    ("Router B", "Router C", 1), ("Router B", "Router D", 5),
    ("Router C", "Router D", 8), ("Router C", "Router E", 10),
    ("Router D", "Router E", 2), ("Router D", "Router F", 6),
    ("Router E", "Router F", 3), ("Router F", "Server 1", 1),
    ("Router D", "Server 2", 3)
]
G.add_weighted_edges_from(edges)

# Assign IP addresses to each node
base_ip = IPv4Address('192.168.0.0')
ip_addresses = {}
for i, node in enumerate(G.nodes()):
    ip_addresses[node] = str(base_ip + i + 1)  # Skip network address

# Position nodes with space for IP display
pos = {
    "Router A": (0, 1), "Router B": (1, 2), "Router C": (1, 0),
    "Router D": (2, 1), "Router E": (3, 0), "Router F": (3, 2),
    "Server 1": (4, 2), "Server 2": (2.5, 1.5)
}

# Calculate shortest path
source = "Router A"
target = "Server 1"
shortest_path = nx.dijkstra_path(G, source, target)
path_edges = list(zip(shortest_path, shortest_path[1:]))

# Create data packet with variables and IP addressing
class DataPacket:
    def __init__(self, source, destination):
        self.source_ip = ip_addresses[source]
        self.dest_ip = ip_addresses[destination]
        self.x = random.randint(1, 100)
        self.y = random.randint(1, 100)
        self.z = random.randint(1, 100)
        self.current_ip = self.source_ip
        self.current_location = source
        self.path = shortest_path
        self.hop_index = 0
        
    def move(self):
        if self.hop_index < len(self.path) - 1:
            self.hop_index += 1
            self.current_location = self.path[self.hop_index]
            self.current_ip = ip_addresses[self.current_location]
        return self.current_location
    
    def get_variables(self):
        return f"Payload:\nx={self.x}\ny={self.y}\nz={self.z}"
    
    def get_header(self):
        return (f"Source IP: {self.source_ip}\n"
                f"Dest IP: {self.dest_ip}\n"
                f"Current IP: {self.current_ip}\n"
                f"At Node: {self.current_location}")

packet = DataPacket(source, target)

# Set up visualization
fig, ax = plt.subplots(figsize=(16, 10))
plt.title("Network Routing with IP Addressing and Data Packet Variables")

# Initial styles
node_colors = {node: "lightblue" for node in G.nodes()}
edge_colors = {edge: "gray" for edge in G.edges()}
node_sizes = {node: 1000 for node in G.nodes()}
edge_widths = {edge: 1 for edge in G.edges()}

# Highlight source and target
node_colors[source] = "lime"
node_colors[target] = "red"
node_sizes[source] = 1500
node_sizes[target] = 1500

# Draw the network with IP addresses and packet info
def draw_network(packet_info=""):
    ax.clear()
    
    # Draw nodes and edges first
    nx.draw_networkx_nodes(
        G, pos,
        node_color=[node_colors[node] for node in G.nodes()],
        node_size=[node_sizes[node] for node in G.nodes()],
        edgecolors="black",
        ax=ax
    )
    nx.draw_networkx_edges(
        G, pos,
        edge_color=[edge_colors[edge] for edge in G.edges()],
        width=[edge_widths[edge] for edge in G.edges()],
        ax=ax
    )
    
    # Draw node labels (names)
    nx.draw_networkx_labels(
        G, {k: (v[0], v[1]-0.15) for k,v in pos.items()},  # Offset names downward
        font_size=10,
        font_weight="bold",
        ax=ax
    )
    
    # Draw IP addresses above nodes
    for node, (x, y) in pos.items():
        ax.text(
            x, y+0.15,  # Position IP above node
            ip_addresses[node],
            ha='center',
            va='center',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1),
            fontsize=8,
            fontfamily='monospace'
        )
    
    # Draw edge weights
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=nx.get_edge_attributes(G, "weight"),
        font_size=8,
        ax=ax
    )
    
    # Add packet information box
    ax.text(
        0.02, 0.90, packet_info,
        transform=ax.transAxes,
        bbox=dict(facecolor='white', alpha=0.9, pad=10),
        fontfamily='monospace',
        fontsize=10,
        linespacing=1.5
    )
    
    # Add legend
    legend_text = (
        "Legend:\n"
        "Source: lime\n"
        "Target: red\n"
        "Packet Route: orange\n"
        "Current Location: yellow\n"
        "IP Addresses shown above nodes"
    )
    ax.text(
        0.02, 0.70, legend_text,
        transform=ax.transAxes,
        bbox=dict(facecolor='white', alpha=0.7, pad=5),
        fontsize=9
    )
    
    ax.set_title(f"Network Routing Simulation | Source: {source} ({packet.source_ip}) → Destination: {target} ({packet.dest_ip})", pad=20)

# Animation function
def update(frame):
    if frame == 0:
        # Initial state
        for edge in edge_colors:
            edge_colors[edge] = "gray"
        for node in node_colors:
            if node not in [source, target]:
                node_colors[node] = "lightblue"
        draw_network(packet.get_header() + "\n\n" + packet.get_variables())
        return
    
    if packet.hop_index < len(packet.path) - 1:
        # Highlight the path being taken
        current_edge = (packet.path[packet.hop_index], packet.path[packet.hop_index+1])
        edge_colors[current_edge] = "orange"
        
        # Move the packet
        prev_location = packet.current_location
        new_location = packet.move()
        
        # Update node colors
        node_colors[prev_location] = "lightblue"
        node_colors[new_location] = "yellow"
    
    # Display packet info
    packet_info = packet.get_header() + "\n\n" + packet.get_variables()
    draw_network(packet_info)

# Create animation
ani = FuncAnimation(
    fig, update,
    frames=len(shortest_path)*2,  # Extra frames for pauses
    interval=1000,  # 1 second per hop
    repeat=False
)

plt.tight_layout()
plt.show()

# To save the animation (uncomment to use)
# ani.save("ip_packet_routing.gif", writer="pillow", fps=1, dpi=100)