home task 1.0.0.0 (08/06/2025)
==============================

Features
--------
- Adds models for all database tables (SQLite).
- Factories for each model to enable test data generation.
- Tests covering all models.
- Two new API endpoints:
  - **Top sales representative by year**  
    `GET api/v1/sellers/<year>/top`  
    Returns a JSON response with the top Sales Rep (Employee) (the one with most sales) & their total sales for year X.
  - **Top sales representative for each available year**  
    `GET api/v1/sellers/top`  
    Returns a JSON response with all top Sales Rep (Employee) with their respective total sales and the year.
- Tests to these two Endpoints to verify correct behavior.