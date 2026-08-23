-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">00 - Foundations</span>
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
-- MAGIC # Lakehouse Federation
-- MAGIC
-- MAGIC During migration, **Oracle** and **Databricks** often need to run in parallel. This module introduces Lakehouse Federation, a data interoperability pattern that enables safe coexistence, leveraging Unity Catalog's capabilities to minimize risk and duplication.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC - Define data interoperability and understand its business value
-- MAGIC - Identify common interoperability challenges
-- MAGIC - Understand how to use Lakehouse Federation to query external catalogs from Databricks

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Coexistence may not be required</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC                 For smaller or less complex migrations, coexistence can often be bypassed. If your organization can execute a rapid cutover with acceptable risk, consider moving directly to migration execution.
-- MAGIC             </p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Why Coexistence is Often Necessary
-- MAGIC
-- MAGIC Most enterprise migrations cannot happen overnight. Understanding the factors that drive coexistence helps you plan appropriately.
-- MAGIC
-- MAGIC | Factor | Implication |
-- MAGIC |--------|-------------|
-- MAGIC | **Complex Dependencies** | Workloads with upstream/downstream relationships must migrate in sequence |
-- MAGIC | **Validation Requirements** | Business-critical data needs parallel validation before cutover |
-- MAGIC | **Business Continuity** | Production systems cannot tolerate disruption |
-- MAGIC | **Team Capacity** | Phased approach spreads work and builds expertise |
-- MAGIC | **Risk Management** | Rollback capability needed until confidence is established |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Typical Coexistence Duration
-- MAGIC
-- MAGIC The length of coexistence depends on migration scope and complexity:
-- MAGIC
-- MAGIC | Migration Size | Object Count | Typical Duration | Recommended Approach |
-- MAGIC |----------------|--------------|------------------|----------------------|
-- MAGIC | **Small** | < 50 objects | 1-2 months | Consider skipping coexist |
-- MAGIC | **Medium** | 50-500 objects | 3-6 months | Targeted coexistence |
-- MAGIC | **Large** | 500+ objects | 6-12+ months | Full coexistence patterns |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Common Interoperability Challenges
-- MAGIC
-- MAGIC Cross-platform data access might face significant obstacles.
-- MAGIC
-- MAGIC | Challenge | Impact | Traditional Workaround |
-- MAGIC |-----------|--------|------------------------|
-- MAGIC | **Format Incompatibility** | Proprietary formats create vendor lock-in | Export/import with data loss |
-- MAGIC | **Schema Evolution** | Different platforms handle schema changes differently | Manual reconciliation |
-- MAGIC | **Access Barriers** | Authentication complexity across systems | Multiple credentials, security gaps |
-- MAGIC | **Governance Fragmentation** | Policies don't cross platform boundaries | Duplicate policy management |
-- MAGIC | **Performance Bottlenecks** | Cross-platform queries are slow | Data duplication |
-- MAGIC
-- MAGIC Lakehouse Federation enables us to access Oracle data from Databricks in a secure, governed, and easy-to-use way. This directly addresses the **Access Barriers** and **Governance Fragmentation** challenges. The remaining challenges - format incompatibility, schema evolution, and performance bottlenecks - are addressed through the broader migration process covered in later modules.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## Lakehouse Federation Overview
-- MAGIC
-- MAGIC <a href="https://docs.databricks.com/aws/en/query-federation/" target="_blank">Lakehouse Federation</a> provides a set of features that enable users and systems to run queries against multiple data sources without needing to migrate all data to a unified system. 
-- MAGIC
-- MAGIC This pattern enables Databricks to query external catalogs like **Oracle**, Hive Metastore, or AWS Glue without moving data.
-- MAGIC
-- MAGIC <br />
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     subgraph P2["Lakehouse Federation"]
-- MAGIC         direction LR
-- MAGIC         A2["Databricks"] -->|Federation| B2["External Catalog<br/>(Oracle, Glue)"]
-- MAGIC         B2 --> C2["External Storage"]
-- MAGIC     end
-- MAGIC     style P2 fill:#e3f2fd,stroke:#1976d2
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC There are two types of federation: query federation and catalog federation. Both allow you to query data without a full migration, meaning that the data remains in the original source system. Still, they differ significantly in how they handle compute and access.
-- MAGIC
-- MAGIC | Attribute | Query Federation | Catalog Federation |
-- MAGIC | :--- | :--- | :--- |
-- MAGIC | **Query Path** | Uses **JDBC push-down**. Queries run on both Databricks and the remote database compute. | **Direct access** to object storage. Queries run exclusively on Databricks compute. |
-- MAGIC | **Performance** | Best for small datasets or ad hoc needs; limited by external database compute. | **Highly optimized** and cost-effective; leverages Databricks' distributed processing. |
-- MAGIC | **Best For** | Ad hoc reporting, PoCs, and operational data access. | High-volume data, migration phasing, and long-term hybrid models. |
-- MAGIC | **Some supported data sources** | **Oracle**, PostgreSQL, MySQL, Microsoft SQL Server, Snowflake | AWS Glue, Apache Iceberg catalogs | 
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### How It Works With Oracle
-- MAGIC
-- MAGIC Oracle connects via query federation (JDBC push-down). The steps are the following:
-- MAGIC
-- MAGIC 1. **Connection** Create a connection object in Unity Catalog with your access credentials and JDBC URL.
-- MAGIC 2. **Catalog** Create a foreign catalog using the connection. The schemas and tables from Oracle will show up in this catalog.
-- MAGIC 3. **Privileges** Grant privileges to users on tables in the foreign catalog.
-- MAGIC 4. **Usage** Run queries. These are pushed down to the external database.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Use Cases
-- MAGIC
-- MAGIC | Use Case | Description |
-- MAGIC |----------|-------------|
-- MAGIC | **Query Before Migration** | Access Oracle data from Databricks without moving it |
-- MAGIC | **Cross-Platform Joins** | Join Oracle tables with UC tables in a single query |
-- MAGIC | **Gradual Data Migration** | Query federated data while migrating incrementally |
-- MAGIC | **Validation During Migration** | Compare source and target data using federated queries |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Key Takeaways
-- MAGIC
-- MAGIC - **Query Federation** uses JDBC push-down to run queries against Oracle (and other external databases) without moving data - best for ad hoc access and validation during migration
-- MAGIC - **Catalog Federation** provides direct object storage access running entirely on Databricks compute - better suited to high-volume or long-term hybrid workloads
-- MAGIC - For Oracle specifically, query federation via a Unity Catalog connection object is the supported path
-- MAGIC
-- MAGIC **Next Steps**
-- MAGIC
-- MAGIC - Proceed to [**Module 01 - Discover**]($../01 - Discover/1.0 - Overview) to begin your migration journey

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
