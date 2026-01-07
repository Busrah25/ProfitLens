# ProfitLens

An end to end analytics and profitability intelligence system that simulates how organizations model, transform, and analyze transactional business data.

The project demonstrates a complete analytics workflow including data generation, ingestion, transformation, and an executive facing dashboard built with Streamlit.

## Overview
ProfitLens is designed to reflect real world analytics engineering and business intelligence practices. The repository is structured to mirror how production analytics systems separate raw data, analytics logic, and presentation layers.

The project emphasizes clarity, maintainability, and business relevance rather than simple visualization.

## Business Problem
Organizations need reliable and transparent profitability reporting across customers, products, and regions. This requires:
- Consistent business logic  
- Clean data models  
- Reproducible transformations  
- Executive friendly reporting  

ProfitLens addresses how transactional data can be transformed into trustworthy profitability insights for decision making.

## Solution Approach
The system follows a layered analytics architecture:

1. Generate realistic synthetic transactional data  
2. Load source aligned data into a raw schema  
3. Apply centralized SQL based business logic in analytics tables and views  
4. Validate data quality through automated checks  
5. Present insights through a multi page executive dashboard  

All transformations and calculations are reproducible and documented.

## Key Features
- Layered raw and analytics data models  
- Centralized SQL based profitability logic  
- Order and customer level margin analysis  
- Data quality validation checks  
- Global date filtering across dashboard pages  
- Executive focused KPI reporting  

## Technologies Used
- Python  
- PostgreSQL  
- SQL  
- Pandas  
- Streamlit  
- Docker  

## Data and Logic
All datasets are generated programmatically using Python and stored as CSV files. Data is ingested into PostgreSQL under a raw schema and transformed into analytics tables and views using SQL.

Profitability logic includes cost, revenue, discount, and shipping calculations. All business rules are documented and centralized to ensure consistency across reporting layers.

## Repository Structure

ProfitLens/
├── app/
│   ├── streamlit_app.py
│   └── pages/
├── pipeline/
│   ├── generate_data.py
│   ├── load_raw.py
│   ├── build_analytics.py
│   └── quality_checks.py
├── sql/
│   ├── 00_schemas.sql
│   ├── 01_raw_tables.sql
│   ├── 02_analytics_tables.sql
│   ├── 03_views.sql
│   └── 04_indexes.sql
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── products.csv
│   └── regions.csv
├── docs/
│   ├── assumptions.md
│   ├── data_dictionary.md
│   └── kpi_definitions.md
├── docker-compose.yml
├── requirements.txt
└── README.md

## How to Run Locally

1. Start PostgreSQL using Docker
2. Create schemas, tables, views, and indexes
3. Run the data pipeline
4. Launch the Streamlit dashboard

docker compose up -d

docker exec -i profitlens_postgres psql -U profitlens_user -d profitlens < sql/00_schemas.sql
docker exec -i profitlens_postgres psql -U profitlens_user -d profitlens < sql/01_raw_tables.sql
docker exec -i profitlens_postgres psql -U profitlens_user -d profitlens < sql/02_analytics_tables.sql
docker exec -i profitlens_postgres psql -U profitlens_user -d profitlens < sql/03_views.sql
docker exec -i profitlens_postgres psql -U profitlens_user -d profitlens < sql/04_indexes.sql

python pipeline/generate_data.py
python pipeline/load_raw.py
python pipeline/quality_checks.py
python pipeline/build_analytics.py

streamlit run app/streamlit_app.py

## Documentation

docs/assumptions.md — Business assumptions for cost and pricing logic

docs/data_dictionary.md — Field level definitions

docs/kpi_definitions.md — KPI calculations and dashboard met

## Future Improvements

Support for incremental data loads

Additional profitability breakdowns by channel

Role based dashboard access

Automated scheduling of pipeline execution