---
name: rail-lidar-qa-mvp
description: Rail LiDAR QA MVP - Local LiDAR quality validation for railway infrastructure using drone simulation, point cloud metrics, and 3D visualization.
version: 1.0
created: 2026-05-30
updated: 2026-05-30
source: https://github.com/Ntizar/rail-lidar-qa-mvp
tags: [data-science, lidar, railway, QA]

---

# Rail LiDAR QA MVP

## Overview

A local tool for validating LiDAR quality on railway infrastructure. Simulates drone flights over a PNOA LiDAR point cloud to detect coverage gaps, low-density zones, and shadow areas.

## Workflow

1. User loads `.laz` point cloud file
2. System reads point cloud and calculates general metrics
3. User selects analysis zone (e.g., 20m track + embankment)
4. Tool divides zone into 2D grid
5. For each cell: calculates density, elevation range, coverage
6. Simulates multiple drone passes from different positions
7. Generates QA map with color coding
8. Demo shows if capture is acceptable or needs repetition

## Drone Pass Strategy

| Pass | Coverage | Purpose |
|------|----------|---------|
| P1 | Track axis | Global view of platform, track, ballast, embankment |
| P2 | Right flank | Reduce shadows on embankment face, ditch, ballast edge |
| P3 | Left flank | Confirm doubtful zones, improve density continuity |
| P4 | Adaptive (optional) | Target red cells after P1-P3 |

## QA Traffic Light

- **Green**: Sufficient density and continuous coverage
- **Yellow**: Partial coverage, irregular density, needs review
- **Red**: Gap, shadow, low density, insufficient capture

## Minimum Metrics

- Total point count
- Bounding box X/Y/Z
- Elevation range
- Mean points per square meter
- Green cell percentage
- Yellow cell percentage
- Red cell percentage
- QA score 0-100

## Math Model

```
eje_via = principal_eigenvector(covariance(X, Y))
s = longitudinal projection on eje_via
d = transverse projection on normal_via
```

Error reduction per pass:
```
e_i,k+1 = max(e_floor, e_i,k * (1 - g_k * visibility_i,k)) + anomaly_i
```

Planner prioritizes cells with highest residual error for adaptive P4.

## Tech Stack

- Python: `laspy`, `lazrs` (LAZ reading), `numpy` (grid metrics)
- Three.js: 3D point cloud visualization
- Local HTTP server (Python stdlib)
- Windows launcher (`run_mvp.bat`)

## Color Classification

Points are classified visually:
- Green: Vegetation (high NIR response)
- Dark gray: Track/platform
- Ochre: Ballast/substructure
- Brown: Natural terrain/embankment
- Dark blue: Shadow/occlusion/water

## European Sovereignty Narrative

- Galileo Open Service as GNSS base
- Galileo HAS for PPP high-precision corrections
- EGNOS for operational integrity layer
- Local processing, no external cloud
- PNOA LiDAR (CNIG) as free base data

## Static Demo Generation

```bat
python src\build_static.py
```
Creates `docs/` with Three.js viewer, preprocessed `sample_analysis.json`, and HTML report. Publishable to GitHub Pages or Vercel without uploading the `.laz` file.

## Pitfalls
- MVP uses heuristic rules, not real AI
- Track detection may be manual or configurable in v1
- Precision depends on sensor, GNSS, IMU, calibration, and pass geometry
- Tool does NOT certify railway safety
