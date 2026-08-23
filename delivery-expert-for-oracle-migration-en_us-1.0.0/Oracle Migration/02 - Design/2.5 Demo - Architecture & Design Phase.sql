-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">02 - Design</span>
-- MAGIC     </div>
-- MAGIC     <div style="display: flex; align-items: center; gap: 8px;">
-- MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" />
-- MAGIC         <span style="color: #999; font-size: 16px;">-></span>
-- MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="24" height="24"/>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img
-- MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
-- MAGIC     alt="Databricks Learning"
-- MAGIC   >
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #f44336;
-- MAGIC   background: #ffebee;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Important Prerequisites</strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC This notebook is not supported for execution on Databricks Academy provided Vocareum workspaces.
-- MAGIC
-- MAGIC Please go through this guided notebook as a study guide and lecture for Oracle Migration.
-- MAGIC
-- MAGIC The material is intended to be run in your own sandbox environments if you would like. Databricks Academy does not provide Oracle access (on-prem, cloud-hosted, or OCI), a Databricks account with admin level access, or an AWS account for this notebook.
-- MAGIC
-- MAGIC Please view the PREREQUISITES file for more information.
-- MAGIC
-- MAGIC **However, the provided LAB notebooks at the end of each section can be run in a Databricks Academy provided Vocareum workspace and allow you to practice the concepts.**
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC # Demo: Architecture & Design Phase

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this demo, you will be able to:
-- MAGIC - Configure Unity Catalog metastores, catalogs, and schemas for migration environments
-- MAGIC - Establish secure cloud storage access using Storage Credentials and External Locations
-- MAGIC - Use Unity Catalog Volumes for governed file access

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## Compute Requirements
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC   <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC     <span style="font-size: 24px;">🚨</span>
-- MAGIC     <div>
-- MAGIC       <strong style="color: #1565c0; font-size: 1.1em;">REQUIRED – SQL WAREHOUSE OR SERVERLESS COMPUTE</strong>
-- MAGIC       <p style="margin: 8px 0 0 0; color: #333;">This notebook runs on both <strong>SQL Warehouse</strong> and <strong>Serverless compute</strong>. Select your preferred compute resource before executing any cells.</p>
-- MAGIC       <p style="margin: 8px 0 0 0; color: #333;"><strong>Testing configuration:</strong> This demo was tested using SQL Warehouse</strong> and Serverless compute <strong>version 4</strong>. For more details on Serverless versions, see the <a href="https://docs.databricks.com/aws/en/compute/serverless/dependencies" style="color: #1565c0; text-decoration: none; font-weight: 500;">Databricks documentation</a>.</p>
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Platform Setup and Environment
-- MAGIC
-- MAGIC Verify the environment and establish the core storage and catalog structure for the migration.
-- MAGIC Start by inspecting the available metastores in the system information schema to confirm your environment's governance foundation.

-- COMMAND ----------

-- DBTITLE 1,Inspect Metastore(s) (SQL)
-- View existing metastore (requires account admin)
SELECT * FROM system.information_schema.metastores;

-- Metastore creation is done via Account Console UI or CLI
-- The managed storage location should be pre-configured in your cloud provider

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Establish the catalog and schema hierarchy, utilizing development and production stages.

-- COMMAND ----------

-- DBTITLE 1,Create Target Catalogs and Schemas (SQL)
-- Create catalogs for migration
-- Run as catalog owner or metastore admin

CREATE CATALOG IF NOT EXISTS migration_dev
COMMENT 'Development catalog for Oracle migration';

CREATE CATALOG IF NOT EXISTS migration_prod
COMMENT 'Production catalog for Oracle migration';

-- Create schemas mirroring Oracle structure
USE CATALOG migration_dev;

CREATE SCHEMA IF NOT EXISTS hr_raw
COMMENT 'Bronze layer - raw ingested data from Oracle';

CREATE SCHEMA IF NOT EXISTS hr_harmonized
COMMENT 'Silver layer - cleansed and conformed data';

CREATE SCHEMA IF NOT EXISTS hr_analytics
COMMENT 'Gold layer - business-ready aggregates';

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Configure Cloud Storage

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 AWS Setup: Create S3 Bucket, IAM Role, and Trust Policy for Databricks</summary>
-- MAGIC
-- MAGIC Before creating a storage credential in Databricks, you must configure the required cloud resources.
-- MAGIC
-- MAGIC <a href="https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/s3/s3-external-location-manual" target="_blank">For more details, read the documentation here.</a>
-- MAGIC
-- MAGIC <div class="code-block" data-language="bash">
-- MAGIC # Variables - customize these for your environment
-- MAGIC BUCKET_NAME="databricks-oracle-migration"
-- MAGIC ROLE_NAME="databricks-migration-role"
-- MAGIC DATABRICKS_ACCOUNT_ID="your-databricks-account-id"
-- MAGIC AWS_ACCOUNT_ID="your-aws-account-id"
-- MAGIC
-- MAGIC # 1. Create S3 bucket
-- MAGIC aws s3 mb s3://${BUCKET_NAME} --region eu-central-1
-- MAGIC
-- MAGIC # 2. Create the trust policy for Databricks Unity Catalog
-- MAGIC cat > trust-policy.json << EOF
-- MAGIC {
-- MAGIC   "Version": "2012-10-17",
-- MAGIC   "Statement": [
-- MAGIC     {
-- MAGIC       "Effect": "Allow",
-- MAGIC       "Principal": {
-- MAGIC         "AWS": [
-- MAGIC           "arn:aws:iam::414351767826:role/unity-catalog-prod-UCMasterRole-14S5ZJVKOTYTL"
-- MAGIC         ]
-- MAGIC       },
-- MAGIC       "Action": "sts:AssumeRole",
-- MAGIC       "Condition": {
-- MAGIC         "StringEquals": {
-- MAGIC           "sts:ExternalId": "${DATABRICKS_ACCOUNT_ID}"
-- MAGIC         }
-- MAGIC       }
-- MAGIC     }
-- MAGIC   ]
-- MAGIC }
-- MAGIC EOF
-- MAGIC
-- MAGIC # 3. Create the IAM policy for S3 access
-- MAGIC cat > s3-access-policy.json << EOF
-- MAGIC {
-- MAGIC   "Version": "2012-10-17",
-- MAGIC   "Statement": [
-- MAGIC     {
-- MAGIC       "Effect": "Allow",
-- MAGIC       "Action": [
-- MAGIC         "s3:GetObject",
-- MAGIC         "s3:PutObject",
-- MAGIC         "s3:DeleteObject",
-- MAGIC         "s3:ListBucket",
-- MAGIC         "s3:GetBucketLocation"
-- MAGIC       ],
-- MAGIC       "Resource": [
-- MAGIC         "arn:aws:s3:::${BUCKET_NAME}",
-- MAGIC         "arn:aws:s3:::${BUCKET_NAME}/*"
-- MAGIC       ]
-- MAGIC     },
-- MAGIC     {
-- MAGIC       "Action": ["sts:AssumeRole"],
-- MAGIC       "Resource": ["arn:aws:iam::${AWS_ACCOUNT_ID}:role/${ROLE_NAME}"],
-- MAGIC       "Effect": "Allow"
-- MAGIC     }
-- MAGIC   ]
-- MAGIC }
-- MAGIC EOF
-- MAGIC
-- MAGIC # 4. Create the IAM role
-- MAGIC aws iam create-role \
-- MAGIC   --role-name ${ROLE_NAME} \
-- MAGIC   --assume-role-policy-document file://trust-policy.json
-- MAGIC
-- MAGIC # 5. Attach the S3 access policy to the role
-- MAGIC aws iam put-role-policy \
-- MAGIC   --role-name ${ROLE_NAME} \
-- MAGIC   --policy-name databricks-migration-s3-access \
-- MAGIC   --policy-document file://s3-access-policy.json
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Create Storage Credential using Databricks CLI</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="bash">
-- MAGIC # Create storage credential using Databricks CLI
-- MAGIC databricks storage-credentials create --json '{
-- MAGIC   "name": "oracle_migration_cred",
-- MAGIC   "comment": "Credential for Oracle export landing bucket",
-- MAGIC   "aws_iam_role": {
-- MAGIC     "role_arn": "arn:aws:iam::your-aws-id:role/databricks-migration-role"
-- MAGIC   }
-- MAGIC }'
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
-- MAGIC
-- MAGIC <script>
-- MAGIC (function() {
-- MAGIC     function processCodeBlocks() {
-- MAGIC         document.querySelectorAll('.code-block').forEach(function(block) {
-- MAGIC             if (block.getAttribute('data-processed')) return;
-- MAGIC             block.setAttribute('data-processed', 'true');
-- MAGIC             var lang = block.getAttribute('data-language') || 'sql';
-- MAGIC             var code = block.textContent.trim();
-- MAGIC             var id = 'code-' + Math.random().toString(36).substr(2, 9);
-- MAGIC             block.innerHTML = 
-- MAGIC                 '<div style="position:relative;margin:16px 0;">' +
-- MAGIC                     '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
-- MAGIC                     '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:40px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:14px;"></code></pre>' +
-- MAGIC                 '</div>';
-- MAGIC             var codeEl = document.getElementById(id);
-- MAGIC             codeEl.textContent = code;
-- MAGIC             Prism.highlightElement(codeEl);
-- MAGIC             block.querySelector('.copy-btn').onclick = function() {
-- MAGIC                 var t = document.createElement('textarea');
-- MAGIC                 t.value = code;
-- MAGIC                 document.body.appendChild(t);
-- MAGIC                 t.select();
-- MAGIC                 document.execCommand('copy');
-- MAGIC                 document.body.removeChild(t);
-- MAGIC                 this.textContent = '✓ Copied!';
-- MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC             };
-- MAGIC         });
-- MAGIC     }
-- MAGIC     processCodeBlocks();
-- MAGIC     document.querySelectorAll('details').forEach(function(details) {
-- MAGIC         details.addEventListener('toggle', processCodeBlocks);
-- MAGIC     });
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Verify that the storage credentials have been successfully created and linked to your cloud provider roles.

-- COMMAND ----------

-- DBTITLE 1,List and Describe Storage Credentials (SQL)
-- Verify storage credentials (requires metastore admin)
SHOW STORAGE CREDENTIALS;

-- Describe a specific storage credential
DESCRIBE STORAGE CREDENTIAL oracle_migration_cred;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Now you can upload all exported data into the bucket. In the next step, an external volume will be created in Unity Catalog to make this data accessible and governed from the Databricks side.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Storage and Governance Design

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### External Location Design
-- MAGIC
-- MAGIC Map specific cloud storage paths to Unity Catalog by creating external locations for your data landing zones. A Unity Catalog external volume is created to govern the files in the landing zone.

-- COMMAND ----------

-- DBTITLE 1,Create External Location (SQL)
-- Create external locations for migration zones
-- Requires: Metastore Admin or CREATE EXTERNAL LOCATION privilege

-- Landing zone for Oracle exports
CREATE EXTERNAL LOCATION IF NOT EXISTS oracle_landing
URL 's3://databricks-oracle-migration-1234/landing/'
WITH (STORAGE CREDENTIAL oracle_migration_cred)
COMMENT 'Landing zone for raw Oracle exports';

-- Create additional external locations for Staging and Archive zones

-- Verify locations
DESCRIBE EXTERNAL LOCATION oracle_landing;

-- External volume pointing to Oracle landing zone
CREATE EXTERNAL VOLUME IF NOT EXISTS migration_dev.hr_raw.oracle_exports
LOCATION 's3://databricks-oracle-migration-1234/landing/hr/'
COMMENT 'Oracle exports for HR domain';

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Create volumes to provide governed file access. Managed volumes store data that is created and used in Databricks.

-- COMMAND ----------

-- DBTITLE 1,Create Volumes for Migration File Access (SQL)
-- Create volumes for migration file access
USE CATALOG migration_dev;
USE SCHEMA hr_raw;

-- Managed volume for intermediate processing
CREATE VOLUME IF NOT EXISTS processing
COMMENT 'Temporary files during migration processing';

-- Create the analytics schema reports volume (for analysts)
CREATE SCHEMA IF NOT EXISTS hr_analytics
COMMENT 'Schema for analysts';

USE SCHEMA hr_analytics;

CREATE VOLUME IF NOT EXISTS reports
COMMENT 'Reports and exports for analysts';

-- Verify volumes
SHOW VOLUMES IN migration_dev.hr_raw;
SHOW VOLUMES IN migration_dev.hr_analytics;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Storage Access Patterns
-- MAGIC
-- MAGIC Set permissions on Unity Catalog securables applying the principle of least privilege.
-- MAGIC Assign specific privileges to engineers, analysts, and service principals to ensure secure and controlled access to storage resources.

-- COMMAND ----------

-- DBTITLE 1,Grant Access to Storage (SQL)
--
-- External Location Grants
--

-- Migration service principal: Full access to landing zone
GRANT READ FILES, WRITE FILES
ON EXTERNAL LOCATION oracle_landing
TO `9e73900c-0cd8-43be-8651-ed2b401e7ec0`; --uuid for service principal

-- Data engineers: Read/write to staging, read from landing
GRANT READ FILES ON EXTERNAL LOCATION oracle_landing TO `data-engineers`;

-- additional grants for staging locations...

--
-- Volume Grants
--

-- Landing volume: engineers read/write for exported files
GRANT READ VOLUME, WRITE VOLUME 
ON VOLUME migration_dev.hr_raw.oracle_exports 
TO `data-engineers`;

-- Processing volume: engineers read/write for intermediate files
GRANT READ VOLUME ON VOLUME migration_dev.hr_raw.processing TO `data-engineers`;
GRANT WRITE VOLUME ON VOLUME migration_dev.hr_raw.processing TO `data-engineers`;

-- Reports volume: read-only access to gold layer volumes for analysts
GRANT READ VOLUME 
ON VOLUME migration_dev.hr_analytics.reports 
TO `data-analysts`;

-- additional grants for staging volume access...

-- Verify grants
SHOW GRANTS ON EXTERNAL LOCATION oracle_landing;
SHOW GRANTS ON VOLUME migration_dev.hr_raw.oracle_exports;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Ownership conventions
-- MAGIC
-- MAGIC Transfer ownership of the migration assets to the relevant administrative and domain teams to establish long-term governance.

-- COMMAND ----------

-- DBTITLE 1,Set Ownership for Migration Assets (SQL)
-- Transfer catalog ownership to platform team
ALTER CATALOG migration_dev OWNER TO `platform-team`;
ALTER CATALOG migration_prod OWNER TO `platform-team`;

-- Transfer schema ownership to domain teams
ALTER SCHEMA migration_dev.hr_raw OWNER TO `data-engineers`;
ALTER SCHEMA migration_dev.hr_harmonized OWNER TO `data-engineers`;
ALTER SCHEMA migration_dev.hr_analytics OWNER TO `data-analysts`;

-- Transfer external location ownership
ALTER EXTERNAL LOCATION oracle_landing OWNER TO `platform-team`;
-- ... transfer volume ownership for staging and archive zones

-- Verify ownership
DESCRIBE CATALOG EXTENDED migration_dev;
DESCRIBE SCHEMA EXTENDED migration_dev.hr_raw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Security and Access Design

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Implementing Role-Based Access Control (RBAC)
-- MAGIC
-- MAGIC Configure Role-Based Access Control by granting the necessary catalog and schema privileges to your functional user groups.

-- COMMAND ----------

-- DBTITLE 1,Grant Catalog-Level Access (SQL)
-- Run as catalog owner or metastore admin
GRANT USE CATALOG ON CATALOG migration_dev TO `data-engineers`;
GRANT USE CATALOG ON CATALOG migration_dev TO `data-analysts`;

-- Schema-level grants mirroring Oracle owner logic
USE CATALOG migration_dev;

GRANT USE SCHEMA ON SCHEMA hr_raw TO `data-engineers`;
GRANT CREATE TABLE ON SCHEMA hr_raw TO `data-engineers`;
GRANT MODIFY ON SCHEMA hr_raw TO `data-engineers`;

GRANT USE SCHEMA ON SCHEMA hr_analytics TO `data-analysts`;
GRANT SELECT ON SCHEMA hr_analytics TO `data-analysts`;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Audit and Compliance Framework
-- MAGIC
-- MAGIC Query the system audit logs to monitor recent administrative actions and permission updates, ensuring a clear trail of governance changes.

-- COMMAND ----------

-- DBTITLE 1,Query Audit Logs for Security Monitoring (SQL)
-- Requires system table access (granted to metastore admins by default)
-- Recent privilege changes

SELECT
  event_time,
  user_identity.email AS actor,
  action_name,
  request_params.securable_type,
  request_params.securable_full_name,
  request_params.changes
FROM system.access.audit
WHERE action_name = 'updatePermissions'
  AND event_date >= current_date() - INTERVAL 7 DAYS
ORDER BY event_time DESC
LIMIT 50;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Analyze table access patterns over the last 30 days to identify high-usage datasets and potential security anomalies.

-- COMMAND ----------

-- DBTITLE 1,Monitor Table Access (SQL)
-- Monitor table access patterns for compliance reporting

SELECT
  event_date,
  user_identity.email AS user_email,
  request_params.full_name_arg AS table_name,
  action_name,
  COUNT(*) AS access_count
FROM system.access.audit
WHERE action_name IN ('getTable', 'commandSubmit')
  AND event_date >= current_date() - INTERVAL 30 DAYS
GROUP BY 1, 2, 3, 4
ORDER BY access_count DESC
LIMIT 100;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Develop a specialized audit view that uses governed tags to dynamically track and report all access events involving PII-classified tables.

-- COMMAND ----------

-- DBTITLE 1,Track Access to PII (SQL)
-- Track access to tables with PII (compliance requirement)
-- Uses governed tags to dynamically identify tables containing PII columns

-- Create a view for ongoing monitoring
CREATE OR REPLACE VIEW migration_dev.hr_analytics.pii_access_audit AS
WITH pii_tables AS (
  -- Find all tables that have columns tagged with 'class.us_ssn' governed tag
  SELECT DISTINCT 
    CONCAT(catalog_name, '.', schema_name, '.', table_name) AS full_table_name
  FROM system.information_schema.column_tags
  -- WHERE tag_name = 'class.us_ssn' -- not applied in this demo
)
SELECT
  a.event_time,
  a.event_date,
  a.user_identity.email AS user_email,
  a.request_params.full_name_arg AS table_accessed,
  a.source_ip_address,
  a.user_agent
FROM system.access.audit a
INNER JOIN pii_tables p 
  ON a.request_params.full_name_arg = p.full_table_name
WHERE a.event_date >= current_date() - INTERVAL 90 DAYS;

-- Query the audit view
SELECT * FROM migration_dev.hr_analytics.pii_access_audit
ORDER BY event_time DESC
LIMIT 20;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Service Principal Security
-- MAGIC
-- MAGIC Before migration, document the grants assigned to Oracle service accounts and technical users, then recreate them in Unity Catalog.

-- COMMAND ----------

-- DBTITLE 1,Grant Privileges to Service Principal (SQL)
-- Service principals are created via Account Console or Workspace admin UI
-- Ingestion service principal: read from landing, write to bronze

GRANT USE CATALOG ON CATALOG migration_dev TO `9e73900c-0cd8-43be-8651-ed2b401e7ec0`; --uuid for service principal
GRANT USE SCHEMA ON SCHEMA migration_dev.hr_raw TO `9e73900c-0cd8-43be-8651-ed2b401e7ec0`;
GRANT READ VOLUME ON VOLUME migration_dev.hr_raw.oracle_exports TO `9e73900c-0cd8-43be-8651-ed2b401e7ec0`;
GRANT CREATE TABLE ON SCHEMA migration_dev.hr_raw TO `9e73900c-0cd8-43be-8651-ed2b401e7ec0`;
GRANT MODIFY ON SCHEMA migration_dev.hr_raw TO `9e73900c-0cd8-43be-8651-ed2b401e7ec0`;

-- Additional grants for other catalogs/tiers

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
