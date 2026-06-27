# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](../Includes/images/common/db-academy.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # 06 - Continuous Integration and Continuous Deployment (CI/CD) with Declarative Automation Bundles (DABs)
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC In this demonstration, you'll build on everything you've learned about DABs and apply it to a CI/CD workflow with three environments (`development`, `stage`, `production`). 
# MAGIC
# MAGIC The bundle deploys a workflow that runs **unit tests**, a **Lakeflow Spark Declarative Pipeline (SDP)** for ETL and integration tests, and a **visualization notebook**. Each target overrides the catalog, raw data path, and (for dev/stage) the compute, while production runs on Serverless.
# MAGIC
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this demonstration, you will be able to:
# MAGIC
# MAGIC 1. **Read and reason about a multi-file bundle** that splits resources into per-asset YAML files and uses a dedicated `variables.yml`.
# MAGIC 2. **Set bundle variables** (including a `lookup` variable that resolves a cluster name to a cluster ID).
# MAGIC 3. **Deploy and run unit tests, a Lakeflow Spark Declarative Pipeline, and a visualization** as a single workflow.
# MAGIC 4. **Promote the same bundle across `development`, `stage`, and `production` targets** with per-target overrides for catalog, raw data path, and compute.
# MAGIC 5. **Override variables from the CLI** with `databricks bundle <command> --var="<name>=<value>" -t <target>`.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - SELECT A COMPUTE ENVIRONMENT
# MAGIC <div style="
# MAGIC   border-left: 4px solid #f44336;
# MAGIC   background: #ffebee;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Select All-Purpose Compute</strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC This notebook requires **all-purpose compute** (Dedicated). Serverless is not supported for this notebook.
# MAGIC
# MAGIC Follow these steps to attach an all-purpose compute cluster:
# MAGIC
# MAGIC 1. Navigate to the top-right of this notebook and click the drop-down menu to select your `labuser_USERNAME` cluster.
# MAGIC     - By default, the notebook might use **Serverless**.
# MAGIC
# MAGIC 2. If your cluster is available, select it and continue to the next cell. If the cluster is not shown:
# MAGIC
# MAGIC     - In the drop-down, select **More**.
# MAGIC
# MAGIC     - In the **Attach to an existing compute resource** pop-up, select the first drop-down. You will see a unique cluster name in that drop-down. Please select that cluster.
# MAGIC
# MAGIC ⚠️ **NOTE:** If the cluster shows a **terminated** state (red dot in the cluster picker), it needs to be started before you can attach. Click the cluster, then **Start**, and wait a few minutes until you see a green dot.
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## REQUIRED - DATA SETUP
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #f44336;
# MAGIC   background: #ffebee;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Data Setup</strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC Recall that your environment was setup using the **0 - REQUIRED - Course Setup and Authentication**.
# MAGIC
# MAGIC If you end your lab or your lab session times out, your environment will be reset. You will need to rerun the **0 - REQUIRED - Course Setup and Authentication** notebook to recreate the catalogs and data for your environment.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Classroom Setup
# MAGIC
# MAGIC Run the following cell to configure your working environment for this course. 
# MAGIC
# MAGIC **NOTE:** The `DA` object is only used in Databricks Academy courses and is not available outside of these courses. It will dynamically reference the information needed to run the course.

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-06

# COMMAND ----------

# MAGIC %md
# MAGIC Run the cell below to confirm the Databricks CLI is working.

# COMMAND ----------

# MAGIC %sh
# MAGIC databricks catalogs list

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Inspect Pre-Configured YAML Files
# MAGIC
# MAGIC Our goal is to deploy our project to the `dev`, `stage`, and `prod` environments for our CI/CD pipeline. 
# MAGIC
# MAGIC In this example, the project is a simple workflow that contains unit tests, a Lakeflow Spark Declarative Pipeline, and a notebook visualization.
# MAGIC
# MAGIC ![Workflow](./images/06_Final_Workflow_Desc.png)
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Prerequisites
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC This advanced-level course assumes prerequisite knowledge of essential DevOps concepts such as code modularization, custom Python functions, unit testing with pytest, and integration tests with Spark Declarative Pipelines. 
# MAGIC
# MAGIC For a refresher on those topics, see the Databricks course **DevOps Essentials for Data Engineering**. We touch on each here, but the focus of this course is deployment with Declarative Automation Bundles.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Let's explore our project folder called **Full Project**. This folder contains all of our Databricks resources to deploy.
# MAGIC
# MAGIC You will find the following in the root folder:
# MAGIC
# MAGIC   - **src/**
# MAGIC   - **resources/**
# MAGIC   - **databricks.yml**
# MAGIC   - **tests/**
# MAGIC
# MAGIC 1. In a new tab, open the **databricks.yml** file.
# MAGIC
# MAGIC     - It begins by defining the bundle name under the `bundle` mapping.
# MAGIC         - **health_etl_bundle**
# MAGIC     
# MAGIC     - It defines the resources to include under the `include` mapping. 
# MAGIC         - All the YAML configuration resource files are in the **resources/** folder.
# MAGIC
# MAGIC     - Under the `targets` top-level mapping, you will see three defined targets and a variety of configuration specifics for each: `development`, `stage`, and `production`.
# MAGIC         - All three targets have a `root_path`.
# MAGIC         - All three targets have specific configurations.
# MAGIC         - The `stage` and `production` targets have additional variables we need to configure, such as `target_catalog` and `raw_data_path`, to specify the correct data.
# MAGIC
# MAGIC
# MAGIC 2. In the new tab, open **resources/**.
# MAGIC
# MAGIC     - Click on the YAML file named **variables.yml**. 
# MAGIC         - It contains pre-defined variables for the resources to be deployed when deploying the bundle. 
# MAGIC         - These include things like the job name, notebook paths, and parameters to pass to the notebooks.
# MAGIC
# MAGIC     - You will find two folders for a job and SDP resource: 
# MAGIC         - **job/**
# MAGIC            - The **dabs_workflow.job.yml** file (located in the **job/** folder) describes the tasks that will be created. 
# MAGIC            - Notice that there are 3 tasks: **Unit_Tests**, **Visualization**, and **Health_ETL**. 
# MAGIC            - While **Health_ETL** is listed after **Visualization**, it depends on **Unit_Tests**. 
# MAGIC            - The order of the tasks doesn't matter, since the `depends_on` key configures the dependencies.
# MAGIC
# MAGIC         - **pipeline/**
# MAGIC             - The **health_etl_pipeline.pipeline.yml** file (located in the **pipeline/** folder) describes the Spark Declarative Pipeline configuration.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC 3. In the new tab, navigate back to **src/** in the root folder. 
# MAGIC
# MAGIC     This folder contains other folders and notebooks that are called from the YAML files you inspected in the previous steps. These notebooks are chained together as part of the workflow we will deploy below.
# MAGIC
# MAGIC     - **dlt_pipelines/**: contains two Spark Declarative Pipeline notebooks:
# MAGIC       - **gold_tables_dlt**
# MAGIC       - **ingests-bronze-silver_dlt** 
# MAGIC       - You can inspect these notebooks to understand their role in the **Health_ETL** workflow.
# MAGIC     
# MAGIC     - **Final Visualization**: this notebook is the final task in our workflow. 
# MAGIC       - It creates a stacked bar chart of cholesterol distribution by age group.
# MAGIC
# MAGIC     - **helpers/**: contains a `.py` file with custom Python methods for the transformation of the data in the pipeline.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Explore and Update YAML Configuration Files
# MAGIC We will update our YAML files to better understand how to point to the assets and variables needed to configure the bundle before validation using the Databricks CLI.

# COMMAND ----------

# MAGIC %md
# MAGIC ### C1. Explore the databricks.yml Configuration
# MAGIC
# MAGIC Recall that to use a variable called `my_variable` in a bundle, refer to it using `${var.my_variable}`.
# MAGIC
# MAGIC #### Instructions
# MAGIC
# MAGIC 1. Navigate to the folder named **Full Project**.
# MAGIC    
# MAGIC 2. Click on the file **databricks.yml** and explore the bundle configuration.
# MAGIC
# MAGIC 3. Locate the mapping **targets**. 
# MAGIC    - Each target is a unique collection of artifacts, Databricks workspace settings, and Databricks job or pipeline details.
# MAGIC    - The targets mapping consists of one or more target mappings, which must each have a unique programmatic (or logical) name.
# MAGIC
# MAGIC 4. Locate the **development** target and examine the configuration. Notice the following:
# MAGIC    - The value for `default` is set to `True`.
# MAGIC    - The value for `existing_cluster_id` uses the variable `cluster_id`.
# MAGIC    - The **tasks** are set to use our lab compute cluster.
# MAGIC
# MAGIC 5. Locate the **stage** target and examine the configuration. Notice the following:
# MAGIC    - The `target_catalog` variable uses the variable `catalog_stage`.
# MAGIC    - The `raw_data_path` variable uses the volume `health` in `catalog_stage`.
# MAGIC    - The **tasks** are set to use our lab compute cluster.
# MAGIC
# MAGIC 6. Locate the **production** target and examine the configuration. Notice the following:
# MAGIC    - The `target_catalog` variable uses the variable `catalog_prod`.
# MAGIC    - The `raw_data_path` variable uses the volume `health` in `catalog_prod`.
# MAGIC    - No compute cluster is specified for the job. The default compute will use Serverless in production.
# MAGIC

# COMMAND ----------

print(f'Your user name: {my_catalog}')

# COMMAND ----------

# MAGIC %md
# MAGIC ### C2. Update `variables.yml`
# MAGIC
# MAGIC Next, we will update the file **variables.yml**.
# MAGIC
# MAGIC #### Instructions
# MAGIC
# MAGIC 1. Navigate to the **resources/** folder.
# MAGIC
# MAGIC 2. Click on the file **variables.yml**.
# MAGIC
# MAGIC 3. Fill in the following details for the variables:
# MAGIC
# MAGIC    - **TO DO**: `username`: Add your username here. Your username can be found in the cell above.
# MAGIC       - Use `${workspace.current_user.short_name}`
# MAGIC
# MAGIC    - **TO DO**: `my_email`: Enter your email address here. This is used to send notifications.
# MAGIC       - Use your email address.
# MAGIC
# MAGIC    - **TO DO**: `cluster_id`:
# MAGIC       - Use the `lookup` function with your username to obtain the cluster ID value.
# MAGIC       - Paste the value from the cell above for the lookup cluster ID variable.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Information
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC
# MAGIC - The file **variables_solution.yml** contains an example solution if you need help.
# MAGIC
# MAGIC - In the Databricks Academy lab environment, all catalogs, clusters, and usernames match and have no spaces by default.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Visualizing the Declarative Automation Bundle's Assets
# MAGIC
# MAGIC Here we'll look at how to manually update our YAML files to help get acquainted with the setup. 
# MAGIC
# MAGIC Since we are bringing in a pre-configured bundle, it's worth looking at the structure of files we'll be interacting with. Below is a diagram representing how the variables for the development catalog will be used.
# MAGIC
# MAGIC ![Full Pipeline](./images/06_img1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Notebook Execution
# MAGIC
# MAGIC Now that we are familiar with the various folders and files that make up our bundle, let's make sure the CLI is installed by authenticating. 

# COMMAND ----------

# MAGIC %md
# MAGIC ### E1. Development Bundle
# MAGIC
# MAGIC Here is what the configuration of our target mapping for development looks like in the databricks.yml file. 
# MAGIC ```YAML
# MAGIC targets:
# MAGIC
# MAGIC   development:
# MAGIC     mode: development
# MAGIC     default: true
# MAGIC     # In Development, we will use classic compute for our tasks 
# MAGIC     resources:
# MAGIC       jobs:
# MAGIC         health_etl_workflow:    
# MAGIC           name: health_etl_workflow_${bundle.target} 
# MAGIC           tasks:
# MAGIC             - task_key: Unit_Tests
# MAGIC               existing_cluster_id: ${var.cluster_id}
# MAGIC             - task_key: Visualization
# MAGIC               existing_cluster_id: ${var.cluster_id}
# MAGIC     workspace:
# MAGIC       root_path: /Workspace/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/${bundle.target}
# MAGIC ...
# MAGIC ```
# MAGIC
# MAGIC **NOTE:** Recall that with **development** and **stage** target environments we are using a mix of serverless and classic compute at the task level.

# COMMAND ----------

# MAGIC %md
# MAGIC 1. To validate the bundle, run the following cell. 
# MAGIC
# MAGIC     This uses all the default values from **variables.yml** (see diagram above).

# COMMAND ----------

# DBTITLE 1,Validate Development
# MAGIC %sh 
# MAGIC cd "Full Project" 
# MAGIC pwd;
# MAGIC databricks bundle validate -t development

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="
# MAGIC   border-left: 4px solid #ff9800;
# MAGIC   background: #fff3e0;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#e65100; margin-bottom:6px; font-size: 1.1em;">
# MAGIC      Troubleshooting
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC If you see the following error after validating your bundle, the format of your notebook could be incorrect.
# MAGIC
# MAGIC `Error: notebook xxx.ipynb not found`. 
# MAGIC
# MAGIC Check the format of your notebook and adjust accordingly. 
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC 2. After the development target validates, deploy the bundle to the development environment.

# COMMAND ----------

# DBTITLE 1,Deploy to Development
# MAGIC %sh
# MAGIC cd "Full Project" 
# MAGIC databricks bundle deploy -t development

# COMMAND ----------

# MAGIC %md
# MAGIC 3. Navigate to **Jobs & Pipelines** in a new tab and view your deployed job.
# MAGIC     - Leave this tab open.
# MAGIC
# MAGIC #### Checkpoint
# MAGIC ![Dev CICD Pipeline](../Includes/images/cicd-pipeline/dev-deployed-job.png)

# COMMAND ----------

# MAGIC %md
# MAGIC 4. To run the bundle using the Databricks CLI, run the following cell. Note that the job will show as **[dev <username>] health_etl_workflow_<target>** within **Jobs and Pipelines**.
# MAGIC
# MAGIC     This makes sense when you refer back to the structure of the **dabs_workflow.job.yml** file located in **resources/**:
# MAGIC
# MAGIC     ```yaml
# MAGIC     resources:
# MAGIC       jobs:
# MAGIC         health_etl_workflow:                          # <--- Job key (used by `bundle run`)
# MAGIC           name: health_etl_workflow_${bundle.target}  # <--- Job name (shown in the UI)
# MAGIC           description: Final Workflow SDK
# MAGIC     ```

# COMMAND ----------

# DBTITLE 1,Run Bundle in Development
# MAGIC %sh
# MAGIC cd "Full Project" 
# MAGIC databricks bundle run health_etl_workflow 

# COMMAND ----------

# MAGIC %md
# MAGIC 5. Navigate back to your Job and view the successful run on development.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Checkpoint - Dev Run
# MAGIC ![Dev CICD Pipeline](../Includes/images/cicd-pipeline/dev-job-run.png)
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Summary - Development
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC While the job is running, examine the tasks when using the `development` target. 
# MAGIC
# MAGIC   Note the following:
# MAGIC - Unit tests passed.
# MAGIC - The Lakeflow Spark Declarative Pipeline ETL and integration tests passed on a small sample of 7,500 rows of dev data.
# MAGIC - The visualization was created using the small sample of 7,500 rows of dev data.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### E2. Staging Bundle
# MAGIC
# MAGIC Here is what the configuration of our `targets` mapping for `stage` looks like in **databricks.yml**:
# MAGIC
# MAGIC ```yaml
# MAGIC   ...
# MAGIC
# MAGIC   stage:
# MAGIC     mode: development
# MAGIC       # In stage, we use classic compute for our tasks
# MAGIC     resources:
# MAGIC       jobs:
# MAGIC         health_etl_workflow:
# MAGIC           name: health_etl_workflow_${bundle.target}
# MAGIC           tasks:
# MAGIC             - task_key: Unit_Tests
# MAGIC               existing_cluster_id: ${var.cluster_id}
# MAGIC             - task_key: Visualization
# MAGIC               existing_cluster_id: ${var.cluster_id}
# MAGIC     workspace:
# MAGIC       root_path: /Workspace/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/${bundle.target}
# MAGIC     variables:
# MAGIC       target_catalog: ${var.catalog_stage}
# MAGIC       raw_data_path: /Volumes/${var.catalog_stage}/default/health
# MAGIC ```
# MAGIC
# MAGIC </br>
# MAGIC
# MAGIC Imagine you've reviewed your code, analyzed coverage, and so on, and you're ready to deploy and test in a staging environment. 
# MAGIC
# MAGIC DABs simplifies this by adjusting a few parameter values. Run the following cells to validate, deploy, and run with `stage` as the target.
# MAGIC
# MAGIC </br>
# MAGIC
# MAGIC In this example, since `target_catalog` and `raw_data_path` have default values, we override them when deploying to other targets like `stage` within the `targets` mapping. This makes the job read data from the staging catalog.
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Bonus Variable Overrides
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC You can also override variable values directly through the Databricks CLI. For example: `databricks bundle validate --var="target_catalog=<username>_2_stage" -t stage`. Keep in mind this will just reproduce the same job you just ran.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# DBTITLE 1,Validate Staging
# MAGIC %sh
# MAGIC cd "Full Project" 
# MAGIC databricks bundle validate -t stage

# COMMAND ----------

# DBTITLE 1,Deploy to Staging
# MAGIC %sh
# MAGIC cd "Full Project" 
# MAGIC databricks bundle deploy -t stage

# COMMAND ----------

# DBTITLE 1,Run Bundle in Staging
# MAGIC %sh
# MAGIC cd "Full Project" 
# MAGIC databricks bundle run health_etl_workflow -t stage

# COMMAND ----------

# MAGIC %md
# MAGIC #### Checkpoint - Stage Run
# MAGIC ![Stage CICD Pipeline](../Includes/images/cicd-pipeline/stage-job-run.png)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #1976d2;
# MAGIC   background: #e3f2fd;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#0d47a1; margin-bottom:6px; font-size: 1.1em;">
# MAGIC     Summary - Stage
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC While the job is running, open the staged job (**[dev labuser_UNIQUE_ID] health_etl_workflow_stage**)and examine the tasks when using the `stage` target. 
# MAGIC
# MAGIC   Note the following:
# MAGIC - Unit tests passed.
# MAGIC - The Lakeflow Spark Declarative Pipeline ETL and integration tests passed on a sample of 35,000 rows of stage data.
# MAGIC - The visualization was created using the sample of 35,000 rows of stage data.
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### E3. Production
# MAGIC Here is what the configuration of our target mapping for production looks like in the **databricks.yml** file.
# MAGIC ```YAML
# MAGIC   production:
# MAGIC     mode: production
# MAGIC     workspace:
# MAGIC       # host: can change host if isolating by workspace
# MAGIC       root_path: /Workspace/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/${bundle.target}
# MAGIC     variables:
# MAGIC       target_catalog: ${var.catalog_prod}
# MAGIC       raw_data_path: /Volumes/${var.catalog_prod}/default/health
# MAGIC ```
# MAGIC
# MAGIC Here, we'll repeat the same bash commands using `%sh`. 
# MAGIC
# MAGIC However, note that all production compute will run on **serverless instead of classic compute**, as we're not overriding the default compute.
# MAGIC
# MAGIC You can verify this by deploying the job and inspecting the tasks.

# COMMAND ----------

# DBTITLE 1,Validate Production
# MAGIC %sh
# MAGIC cd "Full Project" 
# MAGIC databricks bundle validate -t production

# COMMAND ----------

# DBTITLE 1,Deploy to Production
# MAGIC %sh
# MAGIC cd "Full Project" 
# MAGIC databricks bundle deploy -t production

# COMMAND ----------

# DBTITLE 1,Run Bundle in Production
# MAGIC %sh
# MAGIC cd "Full Project" 
# MAGIC databricks bundle run health_etl_workflow -t production

# COMMAND ----------

# MAGIC %md
# MAGIC #### Checkpoint - Production Run
# MAGIC ![Prod CICD Pipeline](../Includes/images/cicd-pipeline/prod-job-run.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## F. Destroy All Bundles
# MAGIC
# MAGIC Now that we've validated, deployed, and run the bundle against all three targets, clean up by destroying each one. The cell below destroys `development`, `stage`, and `production` in sequence.

# COMMAND ----------

# MAGIC %sh
# MAGIC cd "Full Project";
# MAGIC databricks bundle destroy -t development --auto-approve;
# MAGIC databricks bundle destroy -t stage --auto-approve;
# MAGIC databricks bundle destroy -t production --auto-approve;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this demonstration you walked an end-to-end CI/CD-style workflow using a single bundle promoted across three targets:
# MAGIC
# MAGIC 1. Inspected a real-world bundle that splits resources into per-asset YAML files (`job/`, `pipeline/`) and a dedicated `variables.yml`.
# MAGIC 2. Set the `username`, `my_email`, and `cluster_id` (lookup) variables so the bundle resolves correctly for your lab.
# MAGIC 3. Validated, deployed, and ran the workflow against the `development` target (7,500 rows on classic compute).
# MAGIC 4. Promoted the same bundle to the `stage` target (35,000 rows on classic compute) by overriding `target_catalog` and `raw_data_path`.
# MAGIC 5. Promoted the same bundle to the `production` target (full dataset on Serverless compute).
# MAGIC 6. Cleaned up by destroying all three targets with `databricks bundle destroy --auto-approve` per target.
# MAGIC
# MAGIC ## Next Steps
# MAGIC
# MAGIC ![ci_cd](./images/ci_cd_overview.png)
# MAGIC
# MAGIC Think about how you can use DABs to accelerate development by programmatically managing your workflows. With DABs you can create, manage, and deploy your different assets and artifacts in a consistent and repeatable manner for CI/CD workflows.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
