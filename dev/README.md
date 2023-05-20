
### Business Systems Quality and Integrity Management, Alert-Based Reporting

Konula services as a framework for data analysts, data scientists, software engineers, and stakeholders that control the data quality of the company. 

# Konula Core
## Tests
### Test Types
- **Remote Test** - a test that is run directly from the UI/API, based on a ready-made connector package and test configuration
- **Local Test** - a test that is run from another resource, such as Airflow, Prefect, or a local script, but is still tracked by the Konula API. 
- **Test Run** - a test that is run locally and does not store results on the api.
### Core Test Options
- **Aggregates**: sum, min, max, count, mean, median, mode, string_agg, distributions
- **Scans**: unique, null, duplicates
- **Comparisons**: joining 2 datasets, defining how they should compare

### Test Threshold Indicators
- **Time-driven** - defined minimum number (or percentage) of successful health checks in a given time period
- **Data-ratio** - defined minimum ratio of healthy data in a given dataset
- **Trends** - 

### Secrets - Cloud
- Secrets are tied to a single account
- Checks can only read secrets in the path of their account
- Secrets can be stored via the UI/API
- Secrets cannot be retrieved via the UI/API
- When runner picks up check, it creates a job
- Vault Agent Containers inject secrets into pod securely

### Secrets - On-prem or Local
- Follows same guidelines as cloud if the secrets are being stored in the cloud
- Client can handle secret injection any way they would like
- Docs will include steps for injecting your own secrets

### Logging (includes runtime, result, workflow logging)
- Cloud only
    - Logs are pushed to the api from the run and stored securely 
    - Incentive is to use logging for analysis and workflow triggers, whereas thats not available in hybrid
- On-prem
    - Securely store logs outside of the api
    - Logs are pushed to whatever destination connector the user would like
        - JSON, CSV, SQL, etc.
        - S3, Database, Sheets, etc.

### Checks
- Cloud only
    - Core Checks can be used to create checks straight from the API
- On-prem
    - Core checks can be called from python scripts, prefect flows, airflow, API’s, etc.
    - Custom checks, connectors can be created and stored in local buckets 
        - Custom checks go through a registration process so that the API knows what arguments it needs. 
	- Custom checks can also be run directly from a script or workflow manager Prefect or Airflow
    - API can still handle scheduling, logging, secrets, workflow distributions, notifications, state handling

### Product Offerings
- All tests will run on user resources
- API will manage scheduling, secrets (optional), logging (optional), state handling, workflow triggers
- **Free** - Managed orchestration - API 7 day history, 1000 check runs per month, 1000 workflow triggers per month, 100 secrets, 1 user
- **Team** $30/mo - Team - API 30-day history, 10k flow runs, 10k workflow triggers, 1k secrets, 3 users
- **Organization** - $450/mo - Organization - API 30+ day history, 500k runs, 50k workflows, unlimited secrets, 10 users
- **Premium** - $1000/mo - API 30+, 1m runs, 1m workflows, secrets, 100 users
- **Enterprise** - .001/run/workflow, api per GB, 5$ per user

### Hybrid Cloud structure
- Cloud represents everything that is done through the UI. 
- Offers a free trial of the product
- Free trial lets users run tests on their own infrastructure and utilize the cloud secrets, logging (30-day), and workflows
- Local or K8s runs
- Users can run on their infrastructure or ours, depending on the security needs

