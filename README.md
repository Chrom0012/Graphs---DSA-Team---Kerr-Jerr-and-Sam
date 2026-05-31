# Graphs---DSA-Team---Kerr-Jerr-and-Sam
DSA all about graphs

This project is intended to make a visualizations all about graphs. Including directed, and undirected graphs. It visualizes how the Breadth First Search (BFS), and Depth First Search (DFS) works. Traversing each vertex from any starting point.

---

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
9. [Troubleshooting & Tips](#troubleshooting--tips)  
10. [Appendix: File Structure & Key Modules](#appendix-file-structure--key-modules)

---

## Introduction

The **Graph Topology Engine Dashboard** lets you build undirected or directed graphs, edit them with drag‑and‑drop, and run animated **Breadth‑First Search (BFS)** or **Depth‑First Search (DFS)** traversals. It provides:

- Step‑by‑step playback with pause, step‑forward/backward, and restart.
- Real‑time display of the frontier (queue/stack), visited roadmap, and adjacency list.
- Fully customisable vertex colours, sizes, edge widths, and canvas background.
- Zoom, pan, random graph generator, and early‑stop target vertex.


---

## Installation & Launch

### Requirements

- Python 3.7+ (only the standard library: `tkinter`, `math`, `collections`, `random`, `time` – no external packages).

### Steps

1. Save all provided `.py` files into one folder (e.g., `graph_engine/`).  
2. Make sure `main.py` is the entry point.  
3. Run from terminal:
4. The window opens with an empty canvas.


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

The left sidebar is collapsible (click the `◀` handle). It contains these expandable categories:

- **NAMING MODE** – Choose how new vertices are named: `Integer` (1,2,3…), `Letter` (A,B,C…), or `Custom` (free text with dialog).
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


## Troubleshooting & Tips

| Issue | Likely cause | Solution |
|-------|--------------|----------|
| Cannot add vertex | Graph type change pending? | Ensure no animation is running (press reset if needed). |
| Edge does not appear | Forgot to click two vertices | Click source, then destination. Edge grows after second click. |
| Traversal won’t start | Graph is empty | Add at least one vertex. |
| Animation stops early | Target vertex set and reached | Clear target by leaving empty and clicking `Lock`. |
| Zoom too sensitive | – | Use the buttons for precise steps. |
| Canvas pan not working | Right‑click used elsewhere | Ensure you right‑click on the canvas, not on a control. |
| Vertex ID already exists | Duplicate custom name | Choose another ID. |
| Graph type switch clears my work | Intended behaviour | Save your graph (manually note vertices/edges) before switching. |
| Step backward not available | At first step | Press restart first to enable stepping back. |

**Tip:** Use **quick examples** to familiarise yourself with traversal animations before building complex graphs.

## Appendix: File Structure & Key Modules

The application is modular. Here are the core files and their responsibilities:

| File | Purpose |
|------|---------|
| `main.py` | Entry point; sets up window, top bar, coordinates UI construction. |
| `state.py` | Global variables (vertices, adjacency, mode, colours, etc.). |
| `graph_core.py` | Geometry helpers, contrast colour, edge endpoint calculation, full redraw, zoom/pan handlers. |
| `graph_interaction.py` | Facade for split graph interaction modules. |
| `mode_management.py` | Mode switching (vertex, edge, move, delete, etc.). |
| `vertex_dialog.py` | Custom vertex naming dialog. |
| `graph_handlers.py` | Mouse click/move handlers for each mode. |
| `graph_drag_reset.py` | Drag‑to‑move vertex, graph reset. |
| `traversal_engine.py` | BFS/DFS history builders, spark effects, edge travel animation. |
| `traversal_playback.py` | Step rendering, animation loop, pause/step/restart. |
| `traversal.py` | Public API shim for traversal modules. |
| `animation.py` | Vertex bounce, edge growth, radar pulse, travelling photon pulse. |
| `graph_examples.py` | Predefined and random graph generators. |
| `ui_canvas.py` | Builds the central canvas with zoom buttons. |
| `ui_left_sidebar.py` | Assembles left sidebar from top/bottom sections. |
| `ui_left_sidebar_top.py` | Naming, engine, builder tools, examples sections. |
| `ui_left_sidebar_bottom.py` | Vertex appearance, canvas bg, edge, target, graph type, speed, reset. |
| `ui_right_sidebar.py` | Builds scrollable diagnostic panel and playback controls. |
| `ui_sidebar_widgets.py` | ToolTip and CollapsibleCategory classes. |
| `ui_theme.py` | Colour pickers, hover effects, zoom helpers, drawer toggles, animation state button logic. |
| `ui_controls.py` | Vertex/edge size controls, speed, target assignment. |
| `ui_helpers.py` | Public API shim for theme and controls. |
| `graph.py` | Public API shim for graph_core + graph_interaction. |


---

Enjoy building and traversing graphs with the **Graph Topology Engine Dashboard**!  
For further assistance, refer to the source code comments or the troubleshooting section above.

```bash
python main.py

