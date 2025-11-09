# Drifting Realms – Agents & Architecture Guide

## Overview
**Drifting Realms** is an open-world survival exploration game built in **Python** using the **Ursina Engine**.  
Players explore procedurally generated **planets**, each with unique gravity, biomes, and environmental conditions. The player can build bases, gather resources, fight enemies, and travel between worlds using an upgradeable ship.

---

## Game Engine: Ursina
**Ursina** is a lightweight Python 3D engine built on top of **Panda3D**.  
It is chosen for its:
- Pythonic syntax and OOP-friendly architecture  
- Real-time entity management (`Entity`, `Button`, `Text`, etc.)  
- Built-in support for lighting, collisions, physics, and input handling  
- Simple update loop (`update()` and `input()` hooks)  
- Rapid prototyping abilities

---

## File Structure

Recommended directory layout:

```
drifting_realms/
│
├── main.py                  # Entry point - loads engine, main loop, and active world
│
├── core/
│   ├── player.py             # Player class & movement logic
│   ├── ship.py               # Ship class (for interplanetary travel)
│   ├── camera_controller.py  # Handles camera behavior and switching
│   ├── physics.py            # Gravity and physics helpers
│   ├── ui_manager.py         # HUD, popup text, and interface logic
│   └── utils.py              # Common utility functions
│
├── worlds/
│   ├── base_world.py         # Starting planet
│   ├── lava_world.py         # Example of a different biome
│   ├── ice_world.py          # Example of a frozen planet
│   └── __init__.py
│
└── assets/
    ├── models/
    ├── textures/
    └── sounds/

```

---

## OOP Structure and Class Responsibilities

### `Player` Class (`core/player.py`)
Handles all player-related functionality:
- Movement, jump, gravity, and collision detection  
- Health, stamina, and inventory  
- Interaction with environment and entities  

---

### `World` / `Planet` Classes (`worlds/*.py`)
Each planet inherits from a base `World` or `Planet` class.  
Responsible for:
- Setting up terrain, gravity direction, and atmosphere  
- Spawning enemies, resources, and interactables  
- Managing transitions between worlds  

---

### `Ship` Class (`core/ship.py`)
Handles interplanetary travel:
- Ship control and fuel usage  
- World switching logic  
- Upgrade system and docking

---

### `Game Manager` (`main.py`)
- Initializes the engine  
- Loads or transitions between planets  
- Controls saving/loading state  

---

## ⚙️ Development Standards

### 1. Object-Oriented Design
- Each system should be encapsulated in its own class or module  
- Avoid global variables  
- Use inheritance where logical (e.g. all planets inherit from `BasePlanet`)  
- Use composition for modularity (e.g. `Player` has an `Inventory` instance)

### 2. Consistent Naming
- Classes: `PascalCase`
- Functions & variables: `snake_case`
- Files: lowercase with underscores

### 3. Separation of Concerns
- UI, physics, rendering, and input must be in separate modules  
- Keep world data (terrain, assets) isolated from logic

### 4. Version Control Practices
- Use Git branches for new features  
- Commit messages should describe **what** and **why**, not just “fix”  

---

## 🚀 Development Process

1. **Setup Engine**
   - Install Ursina: `pip install ursina`
   - Create entry file `main.py` and test rendering

2. **Core Systems**
   - Implement `Player` class  
   - Implement `BaseWorld`  
   - Add gravity and collision logic  

3. **Expansion**
   - Create new `World` subclasses  
   - Add ships, inventory, crafting, and survival mechanics  

4. **Polish**
   - Add audio, post-processing, and GUI elements  
   - Optimize scene loading  

5. **Testing & Scaling**
   - Use modular loading for planets  
   - Add save/load system  
   - Eventually migrate physics or rendering-heavy parts to Panda3D directly if needed  

---

## 🧠 Future Agents
As the game grows, new “agents” (AI or system modules) can be added:
| Agent | Responsibility |
|-------|----------------|
| `AIController` | Governs NPC and enemy behaviors |
| `ResourceManager` | Handles item drops, materials, and inventory syncing |
| `DialogueAgent` | Manages NPC interactions and quest dialogue |
| `WeatherAgent` | Controls planet-specific effects like storms or day-night cycles |
| `EventAgent` | Triggers story or environmental events dynamically |

---

## ✅ Summary
This document defines the **foundation** for Drifting Realms’ architecture — keeping the game modular, scalable, and OOP-compliant.  
Future developers should follow this structure to ensure clean maintainability and consistent gameplay logic.
