# 🌾 Smart AgriLink: Data-Driven Solutions to Post-Harvest Losses in Nigeria

### 👥 Team: AgriNOVA

**Team Members**
- Member 1 – Data Science & Visualizations  
- Member 2 – Frontend Developer  
- Member 3 – Backend / USSD Integration  
- Member 4 – Project Manager & Research  
- Member 5 – Business Analyst  

---

## 📌 About Our Project

Smart AgriLink combines data analysis and digital tools to tackle post-harvest losses (PHL) in Nigeria.

We focus on two core deliverables:
1. A **PHL Feasibility Report** exploring climate and market risks  
2. A **Hybrid Distribution Solution** (Web + USSD) for farmers

---

## 📊 Read the Full Report

👉 **[Open the PHL Analysis Notebook](your_link_here)**

Includes:
- Climate risk heatmaps by crop & month  
- Key risk drivers by state  
- Opportunity mapping for youth agripreneurs

---

## 🧭 Introduction

Post-harvest losses cost Nigerian farmers up to **$9 billion annually**. This study identifies the most affected crops, states, and seasons — and proposes digital infrastructure to improve resilience.

---

## 🧪 Data & Methodology

### **Datasets Used**
- Nigerian **State-level Climate Data (2022)** – Scraped from [FAO's Climate Information Tool](https://aquastat.fao.org/climate-information-tool/) for all 36 states.
- **Flood Incidence Reports** – Extracted from [NEMA](https://data.humdata.org/dataset/nigeria-nema-flood-affected-geographical-areasnorth-east-nigeria-flood-affected-geographical-areas/resource/833fe41d-1b92-4ca8-bfa0-8b483ed81690) for flood occurrences in 2022.
- **National Agricultural Sample Census (2022)** – Community-level data on agro-processing, storage, transportation, and land degradation.
- **Market Access Data** – Includes market location, distance, and type for farmers across Nigeria.
- **Disaster Impact Data** – Reports on disaster frequency, crop losses, and economic impacts over the past three years.

---

### **Transformations & Tasks**

#### **1. Climate Data Collection**
- **Scraping**: Climate data for all 36 Nigerian states was scraped from [FAO's Climate Information Tool](https://aquastat.fao.org/climate-information-tool/) using Selenium.
  - Features collected include:
    - Precipitation (mm/m)
    - Temperature (min, max, mean in °C)
    - Relative Humidity (%)
    - Sunshine (J/m²/day)
    - Wind Speed (2m, m/s)
    - Evapotranspiration (mm/m)
  - Each state's data was saved as a CSV file.
- **Aggregation**: Individual state CSVs were combined into a single dataset (`all_states_climate_2022.csv`), with unnecessary rows (e.g., totals) removed.

#### **2. Flood Data Integration**
- **Flood Dataset**: Flood occurrence data from NEMA was cleaned and validated:
  - Invalid or blank dates were removed.
  - Dates were parsed into a standard format (`dd/mm/YYYY`).
  - Flood occurrences were mapped to states and months.
- **Flood Flag**: A binary flood flag (`flood = 1`) was added to the climate dataset for each state and month where a flood occurred, resulting in the augmented dataset `all_states_climate_2022_with_flood.csv`.

#### **3. Agricultural Census Data Processing**
- **Feature Selection**: Relevant features were extracted from the National Agricultural Sample Census dataset:
  - **Agro-processing facilities**: Milling, feed mills, rice huskers, etc.
  - **Storage availability**: Binary indicator for access to storage facilities.
  - **Land degradation**: Percentage of degraded land and abandoned farms.
  - **Transportation methods**: Modes of transport used by farmers.
  - **Challenges**: Crop diseases, animal damage, poor transport, and sales difficulties.
- **Renaming Columns**: Columns were renamed for clarity (e.g., `c2q5__1` → `milling_facility`).
- **Cleaning**: Missing values were identified and handled appropriately.

#### **4. Market Access Data Processing**
- **Feature Selection**: Key features extracted from the market access dataset:
  - **Market location**: Whether markets are within the same LGA or in another LGA/state.
  - **Market distance**: Distance to the nearest market.
  - **Market type**: Type of market (e.g., wholesale, retail).
- **Calculations**:
  - Percentage of farmers with markets outside their LGA or state.
  - Distribution of market types and distances.

#### **5. Disaster Impact Data Processing**
- **Feature Selection**: Key features extracted from the disaster dataset:
  - **Disaster type**: Floods, droughts, pests, etc.
  - **Frequency**: Number of disaster events in the past three years.
  - **Economic losses**: Severity of economic impacts (small, significant, total).
  - **Crop losses**: Percentage of farmers reporting crop losses.
  - **Abandoned farms**: Percentage of farms abandoned due to disasters.
- **Calculations**:
  - Average disaster frequency by state and disaster type.
  - Percentage of farmers reporting economic losses and crop losses.
  - Severity of economic impacts grouped by disaster type.

#### **6. Risk Index Calculation**
- **Normalization**: Climate variables were normalized to a [0, 1] scale for comparability.
- **Crop-Specific Weights**: Each crop (e.g., maize, rice, sorghum) was assigned weights for climate variables based on sensitivity thresholds:
  - Example: Maize is more sensitive to temperature and humidity, while rice is more sensitive to precipitation.
- **Distance-to-Threshold Scores**: For each crop, the deviation of actual climate conditions from ideal thresholds was calculated and inverted into a score (0 = far from ideal, 1 = ideal).
- **Flood Impact**: Flood occurrences were given the highest weight, adding 1 to the risk index for affected states and months.
- **Final Risk Index**: The weighted scores for each crop were averaged to compute a final risk index for each state and month.

#### **7. Outputs**
- **State-Level Risk Index**: The final dataset (`risk_index.csv`) contains the average risk index for each crop, state, and month.
- **Visualizations**: The risk index and processed datasets were used to generate:
  - Heatmaps of climate risk by crop and month.
  - Choropleth maps of flood-affected states.
  - Treemaps of crop loss percentages by state.
  - Bar charts for disaster frequency, economic losses, and transportation challenges.

---

### **Environmental Variables Chosen**
We focused on 5 key climate variables with direct post-harvest impact:
- **Temperature**
- **Relative Humidity**
- **Precipitation**
- **Wind Speed**
- **Evapotranspiration**

Plus:
- **Flood Events** (binary: 0/1)

---

### **Transformations & Index Logic**
- Raw variables normalized to [0, 1].
- Each crop is assigned custom weights per variable.
- We compute a **distance-to-threshold score** (how far current conditions deviate from ideal).
- Floods are weighted **most heavily** due to their destructive impact.
- Final crop risk index per state/month is an average of weighted scores.

---

### **Why Separate Climate Risk?**
We isolate **climate risk** because:
- It's **location and time-sensitive** (e.g., floods in July, heat in March).
- It varies **by crop**, requiring specific thresholds.
- It's measurable with available meteorological data.

This makes it ideal for monthly visualization and early-warning planning, especially for storage and processing logistics.

## ⚙️ Distribution Solution

### How It Works:
- **Web App:** Maps nearest markets, storage points, and transport options
- **USSD Interface:** Offline farmers can access services and report losses
- **Dashboard:** Tracks reports and helps decision-makers allocate support

🔗 [Try the Web App](your_link_here)  
📞 USSD Demo: `*123*456#` (via emulator or video)  
🎥 [Watch Demo Video](your_link_here)

---

## 📂 Repository Structure

```bash
├── data/
│   └── all_states_climate_2022_with_flood.csv
├── notebooks/
│   └── climate_risk_index.ipynb
├── app/
│   └── frontend/ (web)
│   └── ussd/ (backend logic)
├── static/
│   └── plots/
│   └── videos/
└── README.md
