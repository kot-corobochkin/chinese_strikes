
---

## Data

### `chinese_strikes.json`

The dataset is based on publicly available strike and protest records collected by **China Labor Bulletin (CLB)**.  
The version used in this project reflects the state of the CLB database as of **May 2025**.

China Labor Bulletin ceased its operations in **June 2025**, which means that the dataset includes the most recent publicly available records produced by the organization.

Event-level dataset of labor conflicts in China, including:
- date and location,
- industry and enterprise size,
- type of action (strike, protest, etc.),
- worker demands,
- government or employer responses.

One event may include **multiple demands and action types**.

---

## Code Architecture (for developers)

The project follows a **modular design**:

- `data_loading.py`  
  Functions for loading and preprocessing raw data (JSON → DataFrame).

- `analysis.py`  
  Analytical logic: transformations, indicators, composite indices.

- `plots.py`  
  All visualization logic (Plotly-based), separated from analysis.

Notebooks act as **orchestration layers**, combining these components for specific research questions.

For rendered figures and interactive visualizations, see VIEW_FIGURES.md.

---

## Notebooks Overview (for researchers)

### 01 — General Strike Dynamics
**`01_strikes.ipynb`**  
Time-series overview of labor conflicts: volume, trends, and temporal concentration.

**Main charts**:  
- Line charts (strikes over time)

---

### 02 — Urban Distribution
**`02_strikes_by_cities.ipynb`**  
Spatial concentration of strikes across cities.

**Main charts**:  
- Bar charts (cities by number of strikes)

---

### 03 — Industry Distribution
**`03_strikes_by_industries.ipynb`**  
Strike distribution across industrial sectors.

**Main charts**:  
- Bar charts  
- Ranked industry comparisons

---

### 04 — Enterprise Size
**`04_strikes_by_size.ipynb`**  
Strikes by firm size (number of workers).

**Main charts**:  
- Grouped bar charts  
- Comparative regional views

---

### 05–07 — Economic Context
- **`05_economic_indicators.ipynb`** – macro indicators  
- **`06_gdp_composition.ipynb`** – sectoral GDP structure  
- **`07_wages.ipynb`** – wage dynamics  

Purpose: contextualize labor conflict within broader economic change.

---

### 08–09 — Worker Demands
- **`08_demands.ipynb`** – aggregate worker demands  
- **`09_strikes_by_state_and_demands.ipynb`** – regional patterns of demands  

**Main charts**:  
- Multi-colored bar charts (demands by category)  

Note: a single strike may include **multiple demands**, so counts reflect demand occurrences, not unique events.

---

### 10–12 — Forms of Action and Responses
- **`10_action_types_pie.ipynb`** – action type composition  
- **`11_action_by_state_and_type.ipynb`** – regional variation  
- **`12_strikes_by_state_and_response.ipynb`** – state/employer responses  

**Main charts**:  
- Pie charts  
- Grouped bar charts

---

### 13–14 — Industry × Region
- **`13_industries_sunbursts.ipynb`**  
- **`14_strikes_by_state_and_industry.ipynb`**

Hierarchical visualization of labor conflict by **region → industry**.

**Main charts**:  
- Sunburst diagrams

---

### 15 — Structural Labor Power
**`15_structural_labor_power.ipynb`**

This notebook operationalizes **structural working-class power** (Erik Olin Wright) using a composite **Structural Labor Power Index** (*strike leverage index*).

The index captures the **structural vulnerability of capital** based on:
- worker concentration,
- employment dynamics,
- profit per worker,
- profit per worker growth.

**Main charts**:  
- Bubble scatter plots  
  - x-axis: employment growth  
  - y-axis: profit per worker growth  
  - size: sectoral profit weight  
  - color: structural labor power index

---

## Intended Audience

- **Researchers & academics** studying labor, political economy, or China
- **Data analysts** interested in event data and composite indicators
- **Developers** working with reproducible notebook-based research pipelines

---

## Reproducibility

All figures can be reproduced by running notebooks sequentially.  
The project assumes a standard Python scientific stack (`pandas`, `numpy`, `plotly`).
