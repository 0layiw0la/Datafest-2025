# Data-Driven Solutions to Post-Harvest Losses in Nigeria

### Team: CyberFarm

**Team Members**
- Ibrahim Abdulrahim – Data Analysis & Fullstack (Web App)
- Chi-Ife Ileka – Data Engineering
- Toluwase Shoniran – Backend / USSD Integration  



## Table of Contents
1. [About Our Project](#about-our-project)

2. [Distribution Solution](#distribution-solution)

3. [Post Harvest Loss Report (Risk Analysis)](#read-the-full-report)

4. [Summary of Report]()

5. [Data & Methodology](#data--methodology)

    - [Datasets Used](#datasets-used)
    - [Transformations & Tasks](#transformations--tasks)
    - [Environmental Variables Chosen](#environmental-variables-chosen)
    - [Transformations & Index Logic](#transformations--index-logic)
    - [Why Separate Climate Risk?](#why-separate-climate-risk)
---

## About Our Project

CyberFarm combines data analysis and digital tools to tackle post-harvest losses (PHL) in Nigeria.

We focus on two core deliverables:
1. A **Hybrid Distribution Solution** (Web + USSD) for farmers and distributors alike, meant to connect them to the nearest service they need.

2. A **PHL Feasibility Report** exploring market risks, designed to help **young investors** and **agripreneurs** understand:
    - What causes PHL and where the risks lie,
    - How to interpret state-level data to minimize those risks,
    - And where opportunities exist for safe, profitable investment in Nigeria’s agricultural value chain.

---

## Distribution Solution  
**Connecting Farmers to Storage, Transport & Opportunity**

From our analysis, one of the biggest contributors to post-harvest loss (PHL) in Nigeria is the lack of access to affordable storage, reliable transport, and nearby markets, especially for rural and smallholder farmers.

### What We're Building  
We developed a smart digital platform that connects farmers with key post-harvest services: cold truck operators, storage providers, and nearby markets. The goal is to bridge infrastructure gaps and reduce losses that occur between harvest and sale.


### How It Works  
- **Role-Based Sign Up**: Users register as a farmer, storage provider, or cold truck operator  
- **Automatic Geolocation**: Farmers are matched with the 10 nearest providers within a 30km radius, first doing a search within our userbase then expanding using Google Maps API to find more if needed.  
- **Request or Offer Services**: Farmers request transport or storage, while providers find clients  
- **Offline USSD Support**: Ensures farmers without internet can still access nearby storage services

**Web App:**  [Try the Web App](https://cyberfarmdf.netlify.app)

> Note: we've created a test user for quick review. (username = testuser,password = password)

**Web App Demo :**

![Web App Demo](cyberfarmweb.gif)

**USSD Demo :**

![USSD Demo](cyberfarmussd.gif) 


### Built for Every Farmer, Even Without the Internet  
To ensure wider access, the system works in two ways:
- **Web App**: For farmers, transporters, and storage providers with smartphones or internet access  

- **USSD Access**: Designed for smallholder, rural, and illiterate farmers using basic phones.  
  Through USSD, users can input their location and receive SMS-based contact details of nearby storage providers.

> Note: The USSD version offers limited functionality, it's focused on helping farmers **locate the nearest storage** via SMS. Full service requests and role-based features are only available through the web app.

For example, a farmer in Nasarawa can dial a code, input their location, and receive a list of nearby storage providers, no smartphone required.

### Unlocking Opportunity for Youth Entrepreneurs  
This system doesn’t only serve farmers, it also enables youth to participate in agriculture through service delivery:
- Young people can register as cold chain or storage providers.
- They get matched with farmers in need of services.
- This unlocks micro-business opportunities in transport, warehousing, and aggregation, without needing farmland.

### Why This Matters  
The Federal Ministry of Agriculture and Rural Development estimates that Nigeria loses **30–50% of its perishable crops annually**, costing nearly **$9 billion**. These losses threaten food security, farmer income, and youth employment.

By connecting farmers to the support they need, our platform helps:
- Reduce preventable food losses  
- Improve farmer profitability  
- Create youth-led agri-business opportunities   

---

## Read the Full Report

👉 **[Open the PHL Analysis Report](https://cyberfarm.streamlit.app/)**

Includes:
- Key risk drivers by state 
- Market access and transport analysis
- Storage and processing analysis
- Climate risk heatmaps by crop & month   
- Opportunity mapping for youth agripreneurs

---

## 🧪 Data & Methodology

### **Datasets Used**
- Nigerian **State-level Climate Data (2022)** – Scraped from [FAO's Climate Information Tool](https://aquastat.fao.org/climate-information-tool/) for all 36 states.
- **Flood Incidence Reports** – Extracted from [NEMA](https://data.humdata.org/dataset/nigeria-nema-flood-affected-geographical-areasnorth-east-nigeria-flood-affected-geographical-areas/resource/833fe41d-1b92-4ca8-bfa0-8b483ed81690) for flood occurrences in 2022.
- [**National Agricultural Sample Census (2022)**](https://microdata.nigerianstat.gov.ng/index.php/catalog/80/get-microdata) – Community-level data on agro-processing, storage, transportation, and land degradation, disasters, and market access.


### Note: You can review the transformations and anlysis jupyter notebooks [here instead](https://github.com/0layiw0la/Datafest-2025/tree/main/Data%20Analysis/jupyter_notebooks).
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


