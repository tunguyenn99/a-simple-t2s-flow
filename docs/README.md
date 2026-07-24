# 🎨 Project Documentation & Visual Assets (`docs/`)

This directory contains architecture diagrams, Excalidraw design source files, and Python scripts for generating executive business analytics dashboard charts.

---

## 📁 Subdirectory Layout

| Directory / File | Description |
| :--- | :--- |
| **`chart_generation/`** | Python script (`generate_charts.py`) querying Gold models to generate charts saved in `chart_generation/charts/`. |
| **`excalidraw/`** | System architecture diagrams stored as `.png`, `.svg`, and `.excalidraw` vector formats. |

---

## 🛠️ How to Generate Dashboard Charts

From the project root:
```bash
python docs/chart_generation/generate_charts.py
# OR using Makefile shortcut:
make charts
```
