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

-- MAGIC %md
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img
-- MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
-- MAGIC     alt="Databricks Learning"
-- MAGIC   >
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Security and Access Design
-- MAGIC
-- MAGIC This lesson guides you through designing and implementing security controls for your migrated Databricks environment. You will map Oracle's user and role-based access patterns to Unity Catalog privileges and establish audit and compliance frameworks.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC
-- MAGIC - Map Oracle users and roles to Unity Catalog principals and groups
-- MAGIC - Implement role-based access control (RBAC) for catalogs, schemas, and tables
-- MAGIC - Plan the ABAC strategy: map Oracle VPD and Data Redaction to Unity Catalog row filters and column masks
-- MAGIC - Design an audit and compliance framework using `system.access.audit` to replace Oracle's unified audit trail
-- MAGIC - Establish security patterns for migration and production operations

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 1. Security Model Overview
-- MAGIC
-- MAGIC Understanding the fundamental differences between Oracle and Databricks security models is critical for a successful migration.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC flowchart TB
-- MAGIC     subgraph ORA["Oracle Security Model"]
-- MAGIC         direction TB
-- MAGIC         ORAR["<b>Roles</b><br/><i>Hierarchical inheritance</i>"]
-- MAGIC         ORAU["<b>Users</b>"]
-- MAGIC         ORAP["<b>Privileges</b><br/><i>Object level grants</i>"]
-- MAGIC         ORAU --> ORAR
-- MAGIC         ORAR --> ORAP
-- MAGIC     end
-- MAGIC     subgraph DB["Databricks Security Model"]
-- MAGIC         direction TB
-- MAGIC         DBP["<b>Principals</b><br/><i>Users, Groups, Service Principals</i>"]
-- MAGIC         DBG["<b>Groups</b><br/><i>Nested hierarchy</i>"]
-- MAGIC         DBPriv["<b>Privileges</b><br/><i>Unity Catalog grants</i>"]
-- MAGIC         DBP --> DBG
-- MAGIC         DBG --> DBPriv
-- MAGIC     end
-- MAGIC     style ORA fill:#fff,stroke:#F80102,stroke-width:2px
-- MAGIC     style DB fill:#fff,stroke:#FF3621,stroke-width:2px
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "neutral" }); </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC | Concept | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Migration Notes |
-- MAGIC |---------|-----------|------------|-----------------|
-- MAGIC | **Identity** | User / schema | User (synced from IdP) | Map via SCIM provisioning |
-- MAGIC | **Role** | Role | Group (nested)| Flatten complex hierarchies |
-- MAGIC | **Service Identity** | Tech User / Service Account | Service Principal | Use for automation and pipelines |
-- MAGIC | **Privilege Grant** | `GRANT privilege ON object TO role` | `GRANT privilege ON object TO principal` | Similar syntax, different objects |
-- MAGIC | **Ownership** | Object owner (user/role) | Object owner (user/group) | Transfer during migration |
-- MAGIC | **Future Grants** | N/A (explicit per object) | Inherited via schema/catalog | Use inheritance model |
-- MAGIC | **Row-Level Security** | VPD / Row Level Security | Row Filters (ABAC) | Defined per table |
-- MAGIC | **Column Masking** | Data Redaction | Column Masks (ABAC) | Function-based masking |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 2. Unity Catalog Privilege Model
-- MAGIC
-- MAGIC Unity Catalog uses a hierarchical privilege model where permissions can be granted at any level and inherited by child objects.
-- MAGIC <br/><br/>
-- MAGIC <div class="mermaid">
-- MAGIC flowchart TD
-- MAGIC     META["<b>Metastore</b><br/>CREATE CATALOG, USE CATALOG"]
-- MAGIC     CAT["<b>Catalog</b><br/>USE CATALOG, CREATE SCHEMA"]
-- MAGIC     SCH["<b>Schema</b><br/>USE SCHEMA, CREATE TABLE/VOLUME/FUNCTION"]
-- MAGIC     TBL["<b>Table/View</b><br/>SELECT, MODIFY"]
-- MAGIC     VOL["<b>Volume</b><br/>READ VOLUME, WRITE VOLUME"]
-- MAGIC     FN["<b>Function</b><br/>EXECUTE"]
-- MAGIC     META --> CAT
-- MAGIC     CAT --> SCH
-- MAGIC     SCH --> TBL
-- MAGIC     SCH --> VOL
-- MAGIC     SCH --> FN
-- MAGIC     style META fill:#4A8090,stroke:#6AB0C0,color:#fff
-- MAGIC     style CAT fill:#5A90A0,stroke:#7AC0D0,color:#fff
-- MAGIC     style SCH fill:#6AA0B0,stroke:#8AD0E0,color:#000
-- MAGIC     style TBL fill:#7AB0C0,stroke:#9AE0F0,color:#000
-- MAGIC     style VOL fill:#7AB0C0,stroke:#9AE0F0,color:#000
-- MAGIC     style FN fill:#7AB0C0,stroke:#9AE0F0,color:#000
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "neutral" }); </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Oracle to Databricks Privilege Mapping
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle Privilege</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks Equivalent</span> | Scope |
-- MAGIC |-----------|------------|-------|
-- MAGIC | `CREATE SESSION` | `USE CATALOG` | Catalog |
-- MAGIC | `SELECT` on Table | `SELECT` | Table/View |
-- MAGIC | `INSERT`, `UPDATE`, `DELETE` | `MODIFY` | Table |
-- MAGIC | `CREATE TABLE` | `CREATE TABLE` | Schema |
-- MAGIC | `READ ON DIRECTORY` | `READ VOLUME` | Volume |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. Implementing Role-Based Access Control (RBAC)
-- MAGIC
-- MAGIC Design your access control around functional roles that mirror your organization's data access patterns. Start by identifying the personas who need access and their required privilege levels.
-- MAGIC
-- MAGIC | Persona | Access Pattern | Recommended Privileges |
-- MAGIC |---------|----------------|----------------------|
-- MAGIC | **Data Engineer** | Build and maintain pipelines | `USE CATALOG`, `USE SCHEMA`, `CREATE TABLE`, `MODIFY` on bronze/silver |
-- MAGIC | **Data Analyst** | Query curated data | `USE CATALOG`, `USE SCHEMA`, `SELECT` on silver/gold |
-- MAGIC | **Data Scientist** | Explore and model | `USE CATALOG`, `USE SCHEMA`, `SELECT` on all, `CREATE TABLE` on sandbox |
-- MAGIC | **BI Developer** | Build dashboards | `USE CATALOG`, `USE SCHEMA`, `SELECT` on gold |
-- MAGIC | **Platform Admin** | Manage infrastructure | Metastore admin, workspace admin |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #607d8b; background: #eceff1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚙️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #37474f; font-size: 1.1em;">Account-Level Group Management</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Groups in Databricks should be created at the <strong>account level</strong>, not the workspace level, to enable consistent identity management across workspaces. To create and manage groups, use the <a href="https://accounts.cloud.databricks.com" target="_blank">Account Console</a> (<strong>User management -> Groups</strong>), the <a href="https://docs.databricks.com/api/account/groups" target="_blank">Account-level REST API</a>, the <a href="https://docs.databricks.com/en/dev-tools/cli/account-commands.html" target="_blank">Databricks CLI</a>, the <a href="https://docs.databricks.com/en/dev-tools/sdk-python.html" target="_blank">Python SDK</a>, or Infrastructure-as-Code tooling.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 4. Attribute-Based Access Control (ABAC)
-- MAGIC
-- MAGIC Unity Catalog supports fine-grained access control through row filters and column masks. These allow you to restrict data access based on user attributes, data values, or governed tags.
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">ABAC Policies vs Local Definitions</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Unity Catalog uses <b>Row Filters</b> and <b>Column Masks</b>, which can be defined as SQL functions on a column/table level, or as <b>Policies</b> using governed tags for scalable, tag-based security.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Unity Catalog supports row filters and column masks, replacing Oracle's VPD and Data Redaction features.
-- MAGIC
-- MAGIC | Feature | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks (Unity Catalog)</span> |
-- MAGIC |:---|:---|:---|
-- MAGIC | **Row-level filtering** | **VPD** (Dynamic predicates) or **OLS** (Data Labels) | **Row Filters** (SQL functions or Policy with governed tags) |
-- MAGIC | **Column masking** | **Data Redaction** (Full/Partial/Regexp) | **Column Masks** (SQL functions or Policy with governed tags) |
-- MAGIC | **Policy Binding** | `DBMS_RLS.ADD_POLICY` or `DBMS_REDACT.ADD_POLICY` | `ALTER TABLE ... SET ROW FILTER` or **Governed Tags** |
-- MAGIC | **Context Functions** | `SYS_CONTEXT('USERENV', 'SESSION_USER')` | `current_user()`, `is_account_group_member()` |
-- MAGIC | **ABAC Strategy** | **OLS Labels:** (Sensitivity, Compartments, Groups) | **Governed Tags:** (Tag-to-Policy inheritance) |
-- MAGIC | **Management** | Manual application to every table/view | Automatic "Tag-and-Protect" across the Catalog |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #607d8b; background: #eceff1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" /></span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #37474f; font-size: 1.1em;">Oracle Database Vault</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC                 Oracle Database Vault enforces <b>separation of duties at the kernel level</b> — preventing even highly privileged DBAs from accessing application data. It is common in regulated industries (financial services, healthcare) where privileged-user access must be audited and restricted.
-- MAGIC             </p>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC                 The closest mapping in Databricks Unity Catalog is the separation between:
-- MAGIC             </p>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li><b>Metastore admin</b> — manages governance objects (catalogs, schemas, external locations) but does not automatically have <code>SELECT</code> on data.</li>
-- MAGIC                 <li><b>Data owner / catalog owner</b> — controls data-level grants.</li>
-- MAGIC                 <li><b>Unity Catalog audit logs</b> (<code>system.access.audit</code>) — provide a tamper-evident trail for all data access, equivalent to Oracle Database Vault's mandatory auditing.</li>
-- MAGIC             </ul>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC                 Document which Database Vault realms and command rules are in use and map each to an explicit Unity Catalog grant matrix before migration. Engage your security and compliance teams early if Database Vault policies are a compliance requirement.
-- MAGIC             </p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #009688; background: #e0f2f1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">💡</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #00695c; font-size: 1.1em;">Implementation covered in Module 5</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Step-by-step implementation of governed tags, ABAC policy creation, and policy binding — including runtime requirements and the constraint that manual row filters and ABAC policies cannot coexist on the same table — is covered in <b>5.2 Lecture — Security and Fine-Grained Access</b>.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 5. Audit and Compliance Framework
-- MAGIC
-- MAGIC Unity Catalog provides comprehensive audit logging through system tables, replacing Oracle's `AUDIT_TRAIL` or unified audit views.
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle View</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks System Table</span> | Purpose |
-- MAGIC |------------------|--------------------------|---------|
-- MAGIC | `DBA_AUDIT_TRAIL`, `UNIFIED_AUDIT_TRAIL` | `system.access.audit` | All administrative/access events |
-- MAGIC | `DBA_USERS` | `system.access.users` | Identity inventory |
-- MAGIC | `V$SQL` | `system.query.history` | Query execution logs |
-- MAGIC | `ALL_DEPENDENCIES` | `system.access.table_lineage` | Table-level data lineage |
-- MAGIC | SQL Developer Data Modeler (SDDM) | `system.access.column_lineage` | Column-level data lineage |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #4caf50; background: #e8f5e9; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">✅</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #2e7d32; font-size: 1.1em;">Recommendation: Build Compliance Dashboards</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Use AI/BI Dashboards to create real-time compliance monitoring:</p>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li><b>Access patterns</b>: Who accessed what, when, and from where</li>
-- MAGIC                 <li><b>Privilege changes</b>: Track grants/revokes over time</li>
-- MAGIC                 <li><b>Failed access attempts</b>: Identify potential security issues</li>
-- MAGIC                 <li><b>Data lineage</b>: Trace data flow for regulatory requirements</li>
-- MAGIC             </ul>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 6. Service Principal Security
-- MAGIC
-- MAGIC For automated pipelines, migrations, and integrations, use service principals instead of personal user credentials. This provides better auditability and follows the principle of least privilege.
-- MAGIC
-- MAGIC | Use Case | Identity Type | Recommended Scope |
-- MAGIC |----------|---------------|-------------------|
-- MAGIC | Migration scripts | Service Principal | Read on source, Write on target schemas |
-- MAGIC | Lakeflow Spark Declarative Pipelines | Service Principal | Catalog/schema ownership or `MODIFY` grants |
-- MAGIC | BI tool connections | Service Principal | `SELECT` on gold layer only |
-- MAGIC | CI/CD deployments | Service Principal | Workspace admin or limited grants |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Export Oracle Service Account Grants
-- MAGIC
-- MAGIC Before migration, document the grants assigned to Oracle service accounts and technical users.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Warning: Avoid Over-Privileging Service Principals</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">A common anti-pattern is granting service principals broad access (like <code>ALL PRIVILEGES</code> on catalogs) for convenience. This creates security risks:</p>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li>Compromised credentials expose more data</li>
-- MAGIC                 <li>Audit trails become less meaningful</li>
-- MAGIC                 <li>Violates principle of least privilege</li>
-- MAGIC             </ul>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Always scope service principal access to the minimum required for their function.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 7. Security Migration Checklist
-- MAGIC
-- MAGIC Use this checklist to ensure all security aspects are addressed during migration.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Pre-Migration
-- MAGIC
-- MAGIC ✅ Document all Oracle roles and their privilege assignments  
-- MAGIC ✅ Identify service users and their access patterns  
-- MAGIC ✅ Map Oracle roles to Databricks groups  
-- MAGIC ✅ Document VPD / RLS policies and data redaction rules  
-- MAGIC ✅ Export audit log samples for compliance baseline  

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### During Migration
-- MAGIC
-- MAGIC ✅ Create groups in Databricks (via SCIM or manually)  
-- MAGIC ✅ Establish privilege grants at catalog/schema level  
-- MAGIC ✅ Implement row filters for tables with Row Access Policies  
-- MAGIC ✅ Implement column masks for PII columns  
-- MAGIC ✅ Create service principals for automated processes  
-- MAGIC ✅ Test access with different user personas  

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Post-Migration
-- MAGIC
-- MAGIC ✅ Verify privilege equivalence with Oracle  
-- MAGIC ✅ Enable audit log monitoring and alerting  
-- MAGIC ✅ Create compliance dashboards  
-- MAGIC ✅ Document security model for operations team  
-- MAGIC ✅ Schedule periodic access reviews  

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Summary

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Key Takeaways
-- MAGIC
-- MAGIC | Aspect | Approach |
-- MAGIC |--------|----------|
-- MAGIC | **Identity mapping** | Oracle Users -> SCIM Users; Oracle Roles -> Groups |
-- MAGIC | **Privilege model** | Use hierarchical grants at Catalog/Schema level for inheritance |
-- MAGIC | **Fine-grained access** | Replace VPD and Data Redaction with Row Filters and Column Masks |
-- MAGIC | **Automation security** | Service Principals with scoped privileges for pipelines and integrations |
-- MAGIC | **Compliance** | System tables (`system.access.audit`) provide comprehensive audit trail |
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### What Maps Directly
-- MAGIC
-- MAGIC - `GRANT SELECT/MODIFY` syntax (minor adjustments)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### What Requires Redesign
-- MAGIC
-- MAGIC - Role hierarchies -> Group nesting with explicit grants
-- MAGIC - VPD -> SQL functions as row filters, ABAC policies
-- MAGIC - Data Redaction -> SQL functions as column masks, ABAC policies

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## References
-- MAGIC
-- MAGIC - [Unity Catalog Privileges](https://docs.databricks.com/en/data-governance/unity-catalog/manage-privileges/privileges.html)
-- MAGIC - [Row Filters and Column Masks](https://docs.databricks.com/en/data-governance/unity-catalog/row-and-column-filters.html)
-- MAGIC - [System Tables for Audit](https://docs.databricks.com/en/administration-guide/system-tables/audit-logs.html)
-- MAGIC - [Service Principals](https://docs.databricks.com/en/admin/users-groups/service-principals.html)

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
