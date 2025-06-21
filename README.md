# 🏪 Olist E-commerce Data Warehouse

A production-grade, multi-source data warehouse built with modern data engineering tools. This project demonstrates real-time streaming, batch processing, and end-to-end data pipeline orchestration.

## 🏗️ Architecture

**Multi-Source Data Pipeline:**
- **ERP System** (CSV) → PostgreSQL
- **CRM System** (Mock API) → PostgreSQL  
- **Product Catalog** (Mock Database) → PostgreSQL
- **Review System** (Flask REST API) → PostgreSQL
- **Payment Stream** (Kafka) → PostgreSQL

**Transformation & Orchestration:**
- **dbt** for data modeling (Star Schema)
- **Dagster** for workflow orchestration (8 different jobs)
- **PostgreSQL** as data warehouse
- **Apache Superset** for BI dashboards

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Orchestration** | Dagster | Workflow management & scheduling |
| **Transformation** | dbt | Data modeling & testing |
| **Streaming** | Apache Kafka | Real-time data ingestion |
| **Database** | PostgreSQL | Data warehouse |
| **API** | Flask | Mock external services |
| **BI** | Apache Superset | Dashboards & visualization |
| **Infrastructure** | Docker Compose | Containerized deployment |

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Setup & Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/olist-datawarehouse.git
   cd olist-datawarehouse
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials (optional - defaults work for local development)
   ```

3. **Start the entire pipeline:**
   ```bash
   docker-compose up -d
   ```

   **Note:** The project includes sensible defaults and will work out-of-the-box for local development.

4. **Access services:**
   - **Dagster UI:** http://localhost:3000
   - **Superset:** http://localhost:8088 (admin/admin)
   - **Review API:** http://localhost:5001

## 📊 Data Pipeline Jobs

**Available Dagster Jobs:**
1. `master_pipeline` - Orchestrates all data sources → dbt transformations
2. `olist_pipeline` - Basic CSV ingestion → transformations
3. `erp_pipeline` - ERP data ingestion
4. `crm_pipeline` - Customer data from CRM
5. `catalog_pipeline` - Product & seller data
6. `review_pipeline` - Reviews from REST API
7. `streaming_pipeline` - Real-time payment processing
8. `incremental_analytics` - Scheduled incremental updates (every 5 minutes)

## 🗂️ Data Model

**Star Schema Implementation:**
- `fct_orders` - Orders fact table with metrics
- `dim_customers` - Customer dimension
- Raw staging tables from all sources

## 🔧 Development

**Run dbt transformations:**
```bash
docker-compose exec dbt dbt run
docker-compose exec dbt dbt test
```

**Monitor Kafka streams:**
```bash
docker-compose exec kafka kafka-console-consumer --topic order-payments --bootstrap-server localhost:9092
```

**Access database:**
```bash
docker-compose exec postgres psql -U olist -d olist_dw
```

## 📈 Business Metrics

The warehouse supports analytics for:
- Sales performance by region/category
- Customer behavior analysis  
- Real-time payment processing
- Order fulfillment tracking
- Product performance metrics

## 🎯 Project Highlights

- **Multi-source ingestion** from 5 different systems
- **Real-time streaming** with Kafka + batch processing
- **Modern orchestration** with dependency management
- **Data quality testing** with dbt
- **Containerized deployment** for easy reproduction
- **Production patterns** with proper error handling

## 🤝 Contributing

This is a portfolio project demonstrating data engineering skills. Feel free to explore the code and reach out with questions!


