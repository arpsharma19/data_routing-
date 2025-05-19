# Optimized Data Routing Using Dijkstra’s Algorithm 🚦📡

A network simulation project that visualizes data packet routing using **Dijkstra’s algorithm** with **IP addressing**, **hop tracking**, and **payload details**. The simulation demonstrates how a data packet travels optimally from a source to a destination through a network of routers and servers.

## 🧠 Objective

To simulate and visualize optimized data routing in a computer network using Dijkstra’s algorithm, highlighting real-time IP transitions, packet variables, and network structure.

## 🔧 Technologies Used

- Python 3
- [NetworkX](https://networkx.org/) – for graph modeling and shortest path calculation
- [Matplotlib](https://matplotlib.org/) – for real-time network visualization and animation
- IP Address module (`ipaddress`) – for IP assignment

## 📌 Features

- Constructs a network topology with routers and servers
- Calculates the **shortest path** using Dijkstra’s algorithm
- Assigns **unique IPv4 addresses** to each node
- Simulates a data packet containing dynamic variables (`x`, `y`, `z`)
- Real-time packet **movement animation** across nodes
- Displays packet header, current IP, and payload at each step
- Highlights source (`lime`), destination (`red`), and current location (`yellow`) visually
- Annotates each node with its IP and each link with its weight (distance/cost)

## 🔄 How It Works

1. The network graph is constructed with weighted edges representing link costs.
2. A data packet is created with:
   - Source and destination IPs
   - Random payload variables
   - Current location and hop index
3. The shortest path is calculated using `networkx.dijkstra_path`.
4. An animated visualization shows the packet traveling node by node:
   - Updating current location and IP
   - Displaying packet details in a side panel
   - Highlighting active path and current node

## 📽️ Demo Preview

![Demo Preview](ip_packet_routing.gif)  
*(You can uncomment the saving function in the script to export the animation)*

## 📁 Project Structure

