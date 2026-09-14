
# Lure_data_processing_project/ <br>
The modularize project is to aim to check the deviation of mysql legacy data to track every days change....

├── config/  <br>
│   └── config.yaml          # Single source of truth for all   <br>environments <br>
├── src/ <br>
│   ├── base/ <br>
│       ├──__init__.py<br>
│   │   ├── job_interface.py      # Abstract base class for PySpark jobs  <br>
│   │   └── schemas_defn.py       # StructType definitions for data validation  <br>
│   ├── jobs/  <br>
│       ├──__init__.py<br>
│   │   └── pipeline.py          # Concrete implementation of transformation logic  <br>
│   └── utils/  <br>
│       ├──__init__.py<br>
│       ├── logger_utils.py      # Environment-aware logging utility  <br>
│       └── config_loader.py     # YAML configuration parser  <br>
├── notebooks/  <br>
│   └── app.py                   # Entry point notebook for Databricks Jobs  <br>
├── tests/  <br>
│   └── test_pipeline.py         # Pytest suite for business logic  <br>
├── requirements.txt             # Project dependencies (PyYAML, etc.)  <br>
└── README.md                    # Project documentation  <br>

## one time insert
```
%sql
Create or replace table Movie_Demo.Movie_Schema.Movie_job_control_table
(ID BIGINT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
 job_run_id string,
 job_name string,
 job_status string,
 job_start_time timestamp,
 job_end_time timestamp
)
```

The updated job is 

```
resources:
  jobs:
    LURE_ORACLE_DATA_DEVIATION_ANALYSIS:
      name: LURE_ORACLE_DATA_DEVIATION_ANALYSIS
      tasks:
        - task_key: Starting_app
          spark_python_task:
            python_file: /Workspace/Users/sandutta2020@gmail.com/DataBricks_all/Movie_Review_System/notebooks/app.py
            parameters:
              - --run_id
              - "{{job.run_id}}"
              - --job_id
              - "{{job.id}}"
          min_retry_interval_millis: 900000
          disable_auto_optimization: true
          environment_key: Default
      queue:
        enabled: true
      parameters:
        - name: RUN_ID
          default: "{{job.run_id}}"
        - name: RUN_NAME
          default: "{{job.name}}"
        - name: TASK_ID
          default: "{{job.run_id}}{{job.start_time.is_weekday}}"
      environments:
        - environment_key: Default
          spec:
            environment_version: "5"
      performance_target: PERFORMANCE_OPTIMIZED
```

## I.  Contributors, Reviewers, and Approvers
## II.  Related Reference
## III. Related Documents
## IV. Summarize Functional Requirements / Functional Overview
### A.    Definitions
### B.    Scope
1.     Items In Scope
2.     Items Out of Scope
## V.  Detailed Business Requirements/Features/Rules (Bullet Points or in Tables)
## VI. Technical Solution Overview
A.    Asset Name(s)
B.    Purpose
C.    Solution Overview
D.    Design Considerations
E.    Table/File Names:
1.     Source
2.     Target
3.     Lookups
4.     APIs
F.   Exception Handling
1.     Error Handling Details
G.   Auditing
H.   Recovery Procedure
I.     Archiving
J.     Dependencies
1.     Design Dependencies
2.     Design Constraints
3.     Design Assumptions
4.     Pre-Conditions
5.     Post-Conditions
6.     Pre-Existing Mappings
7.     Pre-Existing Mapplets
8.     Pre-Existing Stored Procedures
9.     Pre-Existing Custom Functions
## VII.   Processing Logic
A.    CRUD Matrix
B.    Data Quality Rules
C.    Data Source Flow
D.    Detailed Processing Logic / Design Pattern
1.     Process Specific Transformation/Validation Rules
1. Source Data Extraction
2. Transaction Type Derivation
3. Fulfillment Type Derivation
4. Business Validations
Common Validation

5. Batch ID Generation
Activation Processing
Dropout Processing
6. Target Table Routing
Provision
Activation
Dropout
7. Exception Handling
8. Subscription End Date Derivation
2.     System Connectivity Details
## VIII. Field Source to Target Mapping
A.    Attributes
## VIIII. Execution Methods
A.    Scheduling Details
1.     Scheduling Parameters
2.     Scheduling Considerations
3.     Stop / Start Instructions
## X. Performance Considerations
A.    Volume
B.    Index Considerations
## XI. Open and Closed Issues
