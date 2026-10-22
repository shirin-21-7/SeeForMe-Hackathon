# Graph Report - SeeForMe-Hackathon  (2026-10-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 19 nodes · 22 edges · 4 communities (0 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- logging
- get
- analyse

## God Nodes (most connected - your core abstractions)
1. `analyse()` - 4 edges
2. `lifespan()` - 3 edges
3. `health()` - 2 edges
4. `home()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `analyse()` --calls--> `logging`  [EXTRACTED]
  main.py →   _Bridges community 3 → community 1_

## Import Cycles
- None detected.

## Communities (4 total, 4 thin omitted)

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `analyse()` connect `analyse` to `main.py`, `logging`?**
  _High betweenness centrality (0.216) - this node is a cross-community bridge._
- **Why does `health()` connect `get` to `main.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `home()` connect `get` to `main.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._