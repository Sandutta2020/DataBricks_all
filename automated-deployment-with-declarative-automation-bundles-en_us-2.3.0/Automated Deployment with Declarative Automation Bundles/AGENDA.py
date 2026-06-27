# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](./Includes/images/common/db-academy.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Automated Deployment with Declarative Automation Bundles 
# MAGIC
# MAGIC This course provides a comprehensive review of DevOps principles and their application to Databricks projects. It begins with an overview of core DevOps, DataOps, continuous integration (CI), continuous deployment (CD), and testing, and explores how these principles can be applied to data engineering pipelines.
# MAGIC
# MAGIC
# MAGIC The course then focuses on continuous deployment within the CI/CD process, examining tools like the Databricks REST API, SDK, and CLI for project deployment. You will learn about Declarative Automation Bundles (DABs) and how they fit into the CI/CD process. 
# MAGIC
# MAGIC You’ll dive into their key components, folder structure, and how they streamline deployment across various target environments in Databricks. You will also learn how to add variables, modify, validate, deploy, and execute Declarative Automation Bundles for multiple environments with different configurations using the Databricks CLI.
# MAGIC
# MAGIC
# MAGIC Finally, the course introduces Visual Studio Code as an Integrated Development Environment (IDE) for building, testing, and deploying Declarative Automation Bundles locally, optimizing your development process. The course concludes with an introduction to automating deployment pipelines using GitHub Actions to enhance the CI/CD workflow with Declarative Automation Bundles.
# MAGIC
# MAGIC By the end of this course, you will be equipped to automate Databricks project deployments with Declarative Automation Bundles, improving
# MAGIC efficiency through DevOps practices.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Prerequisites
# MAGIC - Strong knowledge of the Databricks platform, including experience with Databricks Workspaces, Apache Spark, Delta Lake, the Medallion Architecture, Unity Catalog, Delta Live Tables, and Workflows. In particular, knowledge of leveraging Expectations with Lakeflow Spark Declarative Pipelines (SDP)
# MAGIC - Experience in data ingestion and transformation, with proficiency in PySpark for data processing and DataFrame manipulation. Candidates should also have experience writing intermediate-level SQL queries for data analysis and transformation
# MAGIC - Proficiency in Python programming, including the ability to design and implement functions and classes, and experience with creating, importing, and utilizing Python packages
# MAGIC - Familiarity with DevOps practices, particularly continuous integration and continuous delivery/deployment (CI/CD) principles
# MAGIC - A basic understanding of Git version control
# MAGIC - Prerequisite course: `DevOps Essentials for Data Engineering Course`

# COMMAND ----------

# MAGIC %md
# MAGIC ### Course Agenda
# MAGIC The following modules are part of the **Data Engineer Learning** Path by Databricks Academy.
# MAGIC | # | Module Name |
# MAGIC | --- | --- |
# MAGIC | 0 | [0 - REQUIRED - Course Setup and Authentication]($./0 - REQUIRED - Course Setup and Authentication) |
# MAGIC | 1 | [01 - Deploying a Simple DAB]($./01 - Deploying a Simple DAB) |
# MAGIC | 2 | [02L - Deploy a Simple DAB]($./02L - Deploy a Simple DAB) |
# MAGIC | 3 | [03 - Deploying a DAB to Multiple Environments]($./03 - Deploying a DAB to Multiple Environments) |
# MAGIC | 4 | [04L - Deploy a DAB to Multiple Environments]($./04L - Deploy a DAB to Multiple Environments) |
# MAGIC | 5 | [05L - Use a Databricks Default DAB Template]($./05L - Use a Databricks Default DAB Template) |
# MAGIC | 6 | [06 - Continuous Integration and Continuous Deployment with DABs]($./06 - Continuous Integration and Continuous Deployment with DABs) |
# MAGIC | 7 | [07L Bonus - Adding ML to Engineering Workflows with DABs]($./07L Bonus - Adding ML to Engineering Workflows with DABs) |
# MAGIC | 8 | [08 - Using VSCode with Databricks]($./08 - Using VSCode with Databricks) |
# MAGIC | 9 | [Summary and Next Steps]($./Summary and Next Steps) |
# MAGIC ---
# MAGIC ### Workspace Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC * To run demo and lab notebooks, you need to use the following Databricks runtime: **`17.3.x-scala2.13`**
# MAGIC
# MAGIC * Create catalog permissions

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
