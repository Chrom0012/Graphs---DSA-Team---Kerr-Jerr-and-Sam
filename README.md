## Table of Contents

1. [Introduction](#introduction)  
2. [Installation & Launch](#installation--launch)  
3. [Quick Start Guide](#quick-start-guide)  
4. [User Interface Overview](#user-interface-overview)  
   - [Left Sidebar (Tools & Settings)](#left-sidebar-tools--settings)  
   - [Central Canvas (Graph Workspace)](#central-canvas-graph-workspace)  
   - [Right Sidebar (Diagnostics & Playback)](#right-sidebar-diagnostics--playback)  
5. [Building Graphs](#building-graphs)  
   - [Adding Vertices (Nodes)](#adding-vertices-nodes)  
   - [Adding Edges (Connections)](#adding-edges-connections)  
   - [Moving and Deleting Vertices](#moving-and-deleting-vertices)  
   - [Deleting Edges](#deleting-edges)  
   - [Using Graph Examples](#using-graph-examples)  
   - [Random Graph Generator](#random-graph-generator)  
6. [Graph Type & Appearance](#graph-type--appearance)  
   - [Undirected vs Directed](#undirected-vs-directed)  
   - [Vertex Color & Size](#vertex-color--size)  
   - [Edge Width](#edge-width)  
   - [Canvas Background](#canvas-background)  
7. [Graph Traversal (BFS/DFS)](#graph-traversal-bfsdfs)  
   - [Starting a Traversal](#starting-a-traversal)  
   - [Animation & Step by Step Playback](#animation--step-by-step-playback)  
   - [Target Stop Vertex](#target-stop-vertex)  
   - [Understanding the Diagnostic Panel](#understanding-the-diagnostic-panel)  
8. [Advanced Features](#advanced-features)  
   - [Zoom & Pan](#zoom--pan)  
   - [Animation Speed Control](#animation-speed-control)  
   - [Auto open Drawers](#auto-open-drawers)

---
Created by: Kerr, Jerr, and Sam
---

## Introduction

This app was developed to make a visualizer for Breadth First Search (BFS), and Depth First Search (DFS) to serve as interactive application that will help understand how these two works on graphs. It also allows you to create your own graph either a directed, or undirected. 

---

## Installation & Launch

### Requirements

- Python 3.7+ 

### Steps

1. Install the folder entilted "Official Code"
2. Run any IDE compiler, and open that folder
3. Make sure that the main.py is open
4. Run the main.py, and enjoy!


## Quick Start Guide

1. **Add vertices** – Click the `⬢ Add Vertex Node` button, then click anywhere on the canvas.  
   Choose naming mode: `Integer`, `Letter`, or `Custom`.
2. **Add edges** – Click `➔ Connect Edge Link`, then click on two vertices in order.
3. **Run BFS** – Click `▶ Run Active Search...` → **Breadth‑First Search** → click a root vertex.  
   Watch the animation.
4. **Run DFS** – Same button → **Depth‑First Search**.
5. **Reset** – Use `⚠ Reset Graph Canvas` or the restart button in the right sidebar.


## User Interface Overview

### Left Sidebar (Tools & Settings)

The left sidebar has dropdown (click the `◀` handle). It contains the following:

- **NAMING MODE** – You can customize the name or ID of the vertex: `Integer` (1,2,3…), `Letter` (A,B,C…), or `Custom` (free text with dialog).
- **OPERATIONAL ENGINE** – Large `▶ Run Active Search...` button for BFS/DFS.
- **TOPOLOGY BUILDER TOOLS** – Five mode buttons:
  - `⬢ Add Vertex Node`
  - `➔ Connect Edge Link`
  - `✛ Move Coordinates`
  - `❌ Delete Vertex Node`
  - `✂ Trim Edge Link`
- **QUICK GRAPH EXAMPLES** – Predefined graphs: `Undirected Triangle`, `Bidirectional Directed`, `🎲 Random Graph...` (dialog for vertex/edge count and directed option).
- **VERTEX APPEARANCE** – Pick vertex fill colour, adjust radius/diameter with slider or entry.
- **CANVAS BACKGROUND** – Pick background colour or preset (White, Dark, Navy, Slate, Cream, Mint).
- **EDGE APPEARANCE** – Set edge line width (1–10).
- **TARGET STOP VERTEX** – Enter a vertex ID; traversal stops early when this node is visited.
- **GRAPH TYPE** – Switch between `Undirected` and `Directed`. Changing clears the graph.
- **SPEED CONTROL** – Set animation step delay in milliseconds (default 650 ms).
- **RESET** – `⚠ Reset Graph Canvas` clears everything.

### Central Canvas (Graph Workspace)

- Displays the graph.
- **Left‑click** – Depends on active mode (add, select edge source/target, delete, etc.).
- **Right‑click + drag** – Pan the canvas.
- **Mouse wheel** – Zoom in/out (centered on mouse position).
- Top‑left controls: `Zoom [+]` and `Zoom [-]` buttons, plus a pan tip label.


### Right Sidebar (Diagnostics & Playback)

Also collapsible with a `◀` handle. It shows:

- **Status** – Current mode or animation state.
- **Hint** – Contextual guidance.
- **Playback controls** – ⏮ (step back), ⏸ (pause), ⏭ (step forward), 🔄 (restart traversal).
- **Step Index** – Current step number.
- **DATA STRUCTURE FRONTIER** – Live display of BFS queue or DFS stack.
- **TRACE ROADMAP PROGRESS** – The order of visited vertices as a sequence.
- **LIVE ADJACENCY LIST VIEW** – The graph’s adjacency list, with the current node highlighted.
- **PERFORMANCE STATISTICS** – Time elapsed (ms), visited nodes count, step counter.

## Building Graphs

### Adding Vertices (Nodes)

1. Click `⬢ Add Vertex Node` (the button turns cyan).  
2. Click anywhere on the canvas.  
3. If naming mode is **Custom**, a dialog appears:  
   - Enter a unique Vertex ID (e.g., `"A1"`, `"Router3"`).  
   - Optionally add custom data (appears below the vertex label).  
4. The vertex bounces with an animation and appears.

### Adding Edges (Connections)

1. Click `➔ Connect Edge Link`.  
2. Click on the **source** vertex (it turns cyan).  
3. Click on the **destination** vertex.  
   - For undirected graphs, direction is irrelevant; for directed graphs, arrow points from first to second.  
   - Self‑loops are disallowed.  
   - Duplicate edges are prevented.  
4. The edge grows with an animation.

### Moving and Deleting Vertices

- **Move** – Click `✛ Move Coordinates`, then click and drag any vertex.  
- **Delete vertex** – Click `❌ Delete Vertex Node`, then click inside a vertex. All incident edges are removed automatically.

### Deleting Edges

- Click `✂ Trim Edge Link`, then click near the **middle** of an edge (it highlights red). Click to delete.

### Using Graph Examples

- `Undirected Triangle` – 3 vertices fully connected.  
- `Bidirectional Directed` – Two vertices with arrows in both directions.  
- `🎲 Random Graph...` – Opens a dialog:  
  - Enter number of vertices and edges.  
  - Check `Directed` if needed.  
  - Click `Generate`. Vertices are placed on a circle; edges are random (no duplicates, no self‑loops).

### Random Graph Generator

- Automatically respects graph type (undirected/directed).  
- If too many edges requested, a warning appears.  
- After generation, the graph is ready for traversal.

## Graph Type & Appearance

### Undirected vs Directed

- Use the **GRAPH TYPE** radio buttons. Changing type **clears the current graph** (confirmation dialog).  
- Undirected edges have no arrow, adjacency is symmetric.  
- Directed edges show an arrowhead at the destination. Bidirectional edges show two separate arrows.

### Vertex Color & Size

- **Pick Vertex Color** – Opens a colour chooser; updates all vertices.  
- **Size** – Switch between Radius (R) and Diameter (D) modes.  
  - Use the entry field or slider to adjust.  
  - Click `Set` to apply; a temporary preview popup shows the new size.  
- Size changes affect all vertices uniformly.

### Edge Width

- Set integer from 1 to 10 via entry or slider, then `Set`. Redraws graph.

### Canvas Background

- Pick any colour or use one of six presets. The pan tip label and canvas background update immediately.

## Graph Traversal (BFS/DFS)

### Starting a Traversal

1. Ensure the graph is non‑empty.  
2. Click the large `▶ Run Active Search...` button in the left sidebar.  
3. Choose **Breadth‑First Search (BFS)** (yellow theme) or **Depth‑First Search (DFS)** (cyan theme).  
4. Click on any vertex as the **root**. The traversal starts immediately.  
   - The right sidebar auto‑opens (if closed) and the left sidebar auto‑closes to focus on diagnostics.

### Animation & Step by Step Playback

- The traversal advances automatically at the speed set in **SPEED CONTROL**.  
- **Control buttons** (right sidebar):  
  - `⏸` Pause – freezes animation. Click again (now `▶`) to resume.  
  - `⏮` Step back – move one step backward in the history.  
  - `⏭` Step forward – move one step forward (when paused).  
  - `🔄` Restart – reset to step 0 and pause.  
- While paused, you can inspect the frontier, roadmap, adjacency list, and vertex colours.  
- Active node is highlighted in the algorithm’s colour; visited nodes turn a variant colour; frontier nodes are dark with neon outline.

### Target Stop Vertex

- In the left sidebar **TARGET STOP VERTEX**, enter a vertex ID and click `Lock`.  
- During BFS or DFS, if that vertex is visited, the traversal stops immediately (even if more nodes remain).  
- Useful for debugging or finding a path to a specific node.

### Understanding the Diagnostic Panel

- **Frontier** – For BFS: shows queue order (left = next to process). For DFS: shows stack (top = next).  
- **Roadmap** – The exact order vertices were visited.  
- **Adjacency List** – Updates live; the current node is highlighted in gold.  
- **Statistics** – Elapsed time, visited count (out of total vertices), step index.  
- **Process Label** – Displays current step number.  
- **Status/Hint** – Informative messages (e.g., “Discovered adjacent node X”).


## Advanced Features

### Zoom & Pan

- **Zoom** – Mouse wheel; also `Zoom [+]` / `Zoom [-]` buttons.  
- **Pan** – Right‑click and drag anywhere on the canvas.  
- Zoom preserves relative vertex positions and edge connections.

### Animation Speed Control

- **SPEED CONTROL** – Set delay (ms) between steps. Minimum 50 ms.  
- Faster speeds are good for overview, slower for detailed observation.

### Auto open Drawers

- When a traversal starts, the right sidebar **automatically opens** (if closed) and the left sidebar **automatically closes** to maximise diagnostic space.  
- After traversal finishes, the left sidebar re‑opens (via `auto_open_left_drawer`). You can also manually toggle drawers with their handle buttons.




