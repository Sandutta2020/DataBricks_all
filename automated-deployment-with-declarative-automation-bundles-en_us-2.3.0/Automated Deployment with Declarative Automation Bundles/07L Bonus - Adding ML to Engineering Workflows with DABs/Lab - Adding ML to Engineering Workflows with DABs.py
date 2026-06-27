# Databricks notebook source
# MAGIC %md
# MAGIC ![DB Academy](../Includes/images/common/db-academy.png)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="
# MAGIC   border-left: 4px solid #7b1fa2;
# MAGIC   background: #f3e5f5;
# MAGIC   padding: 14px 18px;
# MAGIC   border-radius: 4px;
# MAGIC   margin: 16px 0;
# MAGIC ">
# MAGIC   <strong style="display:block; color:#4a148c; margin-bottom:6px; font-size: 1.1em;">Lab Information</strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC This is a comprehensive demonstration of adding an ML model to a DAB. Due to live class time constraints, this content is optional and best explored at the end of class.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # 07L Bonus - Adding ML to Engineering Workflows with Declarative Automation Bundles (DABs)
# MAGIC
# MAGIC ### Estimated Duration: 25-30 minutes
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC Your data engineering workflow is in good shape. The ML team has now asked you to add a model-inference task so the workflow runs predictions against a registered Unity Catalog model the team already trained. **You don't need to know any ML for this lab.** Your goal is to wire the existing model into the bundle: declare the right variables, add a new task that calls the inference notebook, and promote the same bundle through `development` and `stage` targets.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lab, you will be able to:
# MAGIC
# MAGIC 1. **Add new bundle variables** (including a `lookup` variable for `cluster_id`) to a pre-existing `variables.yml`.
# MAGIC 2. **Extend an existing job YAML** with a new task that depends on prior tasks and passes parameters into a notebook.
# MAGIC 3. **Use `databricks bundle summary`** to inspect what will be deployed before deploying it.
# MAGIC 4. **Validate, deploy, run, and destroy** the bundle against `development`, then promote the same bundle to `stage`.

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
# MAGIC Recall that your environment was set up using the **0 - REQUIRED - Course Setup and Authentication** notebook.
# MAGIC
# MAGIC If you end your lab or your lab session times out, your environment will be reset. You will need to rerun the **0 - REQUIRED - Course Setup and Authentication** notebook to recreate the catalogs and refresh your Databricks CLI credentials.
# MAGIC
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Classroom Setup
# MAGIC
# MAGIC Run the following cell to configure your working environment for this course.
# MAGIC
# MAGIC **NOTE:** The `DA` object is only used in Databricks Academy courses and is not available outside of them. It dynamically references the information needed to run the course.
# MAGIC
# MAGIC **NOTE:** This will take 2-3 minutes to set up and create the models.

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-7L

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Lab Scenario
# MAGIC
# MAGIC Congratulations! You've successfully built the bulk of your workflow. 
# MAGIC
# MAGIC The ML team has asked you to ensure your tests meet their requirements for inferencing a model they've deployed in the dev environment. **You don't need to learn ML for this lab.** Just attach the model to the workflow using the bundle you've already built.
# MAGIC
# MAGIC **Optional task before starting:** if you have ML knowledge, you can inspect the pre-trained model by navigating to **Experiments**. Otherwise, your goal is simply to add it to your bundle.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Pre-flight Checks
# MAGIC
# MAGIC Confirm the Databricks CLI is authenticated against your workspace before starting the lab tasks. Run the cells below and check for errors.

# COMMAND ----------

# MAGIC %sh 
# MAGIC databricks catalogs list

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Task 1 - Update `variables.yml`
# MAGIC
# MAGIC In the folder where this notebook lives, you'll find a sub-folder named **TODO - Lab DABs Workflow**. 
# MAGIC
# MAGIC You'll edit a couple of files there to attach the registered ML model to the workflow. 
# MAGIC
# MAGIC **You do not need to know what the model does**, your goal is to understand how to attach an additional Unity Catalog asset (a registered ML model in this case).
# MAGIC
# MAGIC #### What's in the bundle
# MAGIC
# MAGIC 1. Navigate to the **src/** folder. You'll find:
# MAGIC     - **dlt_pipelines/**
# MAGIC     - **helpers/**,
# MAGIC     - Two notebooks: **Final Visualization** and **Inference**. 
# MAGIC         - The notebook this lab focuses on is **Inference**.
# MAGIC
# MAGIC 2. In the **Inference** notebook, look at the section **Parameterize the notebook for our workflow and passing variables**. Two variables are read by the notebook:
# MAGIC     - **base_model_name**: the registered model name
# MAGIC     - **silver_table_name**: the silver table name and location, expected as **catalog.schema.silver_sample_ml**
# MAGIC
# MAGIC 3. In a separate tab, open **resources/variables.yml**. You'll add a few variables here.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 1.1 - Add `base_model_name` to **variables.yml**
# MAGIC
# MAGIC Add a `base_model_name` variable in the section marked 
# MAGIC
# MAGIC - To find the default value, locate the model in your dev catalog (**labuser_UNIQUE_ID_1_dev.default**) under **Models**.
# MAGIC
# MAGIC ### Step 1.2 - View the `silver_table_name` to **variables.yml**
# MAGIC
# MAGIC View the `silver_table_name` variable. 
# MAGIC   - The default value should be set to `${var.username}_1_dev.default.silver_sample_ml`.
# MAGIC
# MAGIC ### Step 1.3 - Add `cluster_id` to **variables.yml**
# MAGIC
# MAGIC The inference task needs an existing cluster. Define a `cluster_id` variable. You have four options:
# MAGIC
# MAGIC - **Option 1:** Define a `lookup` variable on `username` and reference it via `${var.username}`.
# MAGIC - **Option 2:** Use `lookup` and set the `cluster` value to `${workspace.current_user.userName}`.
# MAGIC - **Option 3:** Hardcode the default value using the `lookup` method.
# MAGIC - **Option 4:** Find your cluster ID by navigating to **Compute** in the left menu, opening your cluster, clicking the kebab menu, and choosing **View JSON**. Copy the cluster ID near the top of the JSON. Alternatively, run `print(spark.conf.get("spark.databricks.clusterUsageTags.clusterId"))` in a new cell. 
# MAGIC   - Paste this value as the `default` for `cluster_id`.
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
# MAGIC     Summary
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC After this task, **variables.yml** should have three new variables: `base_model_name`, `silver_table_name`, and `cluster_id`. Each has a description and a default value.
# MAGIC
# MAGIC **HINT:** Variable substitution and lookups documentation:
# MAGIC [AWS](https://docs.databricks.com/aws/en/dev-tools/bundles/variables) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/variables) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/dev-tools/bundles/variables)
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Task 2 - Update `resources/dabs_workflow_with_ml.job.yml`
# MAGIC
# MAGIC Now that **variables.yml** is updated, extend the workflow with a new inference task. (You will not be configuring the Spark Declarative Pipeline in this step.)
# MAGIC
# MAGIC Navigate to **resources/job/** and open **dabs_workflow_with_ml.job.yml**. You'll see all the existing tasks. 
# MAGIC
# MAGIC Add a new task with the following constraints under the comment `### Complete your ML TASK HERE`:
# MAGIC
# MAGIC 1. Add task name (`task_key`) **ML_test**.
# MAGIC
# MAGIC 2. The task must depend on **Health_ETL** via `depends_on`.
# MAGIC
# MAGIC 3. Add an `existing_cluster_id` key whose value references the `cluster_id` variable you created in Task 1.
# MAGIC     - Reference your `cluster_id` variable: `${var.cluster_id}`. 
# MAGIC
# MAGIC 4. Add a `notebook_task` containing `notebook_path`, `base_parameters`, and `source`:
# MAGIC
# MAGIC     - `notebook_path` should reference the **Inference** notebook (**HINT**: Go back to folders).
# MAGIC
# MAGIC     - `base_parameters` should have **3** keys: 
# MAGIC         - Two referencing the new variables (`base_model_name` and `silver_table_name`)
# MAGIC         - One that references the dev catalog. 
# MAGIC         - **HINT:** use a variable that's already pre-configured in **variables.yml**.
# MAGIC
# MAGIC     - You can also add a description if you'd like.
# MAGIC
# MAGIC **HINT:** Use the existing tasks in this file as templates.

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
# MAGIC     Summary
# MAGIC   </strong>
# MAGIC   <div style="color:#333;">
# MAGIC
# MAGIC After this task, **dabs_workflow_with_ml.job.yml** has a new task wired to the existing **Health_ETL** dependency, and you're ready to validate the bundle.
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## F. Task 3 - View the Bundle Summary
# MAGIC
# MAGIC Use `databricks bundle summary` to print out the resources defined in the project and the names that will be generated after deploying the bundle.
# MAGIC
# MAGIC **NOTE:** Each `%sh` cell starts a fresh shell, so you must `cd` into the **TODO - Lab DABs Workflow** folder *and* run the CLI command in the **same** cell.

# COMMAND ----------

# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC databricks bundle summary

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
# MAGIC `Error: notebook xxx not found`. 
# MAGIC
# MAGIC Check the format of your notebook and adjust accordingly. 
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## G. Task 4 - Validate the Bundle
# MAGIC
# MAGIC Validate your **databricks.yml** bundle configuration file using the Databricks CLI for the `development` target. Confirm validation succeeds. If there is an error, fix the YAML and re-run.
# MAGIC
# MAGIC **HINT:** `databricks bundle` CLI commands documentation:
# MAGIC [AWS](https://docs.databricks.com/aws/en/dev-tools/cli/bundle-commands) |
# MAGIC [Azure](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/bundle-commands) |
# MAGIC [GCP](https://docs.databricks.com/gcp/en/dev-tools/cli/bundle-commands)

# COMMAND ----------

# <FILL-IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##### ANSWER
# MAGIC
# MAGIC <details>
# MAGIC   <summary>EXPAND FOR SOLUTION CODE</summary>
# MAGIC
# MAGIC <button onclick="copyBlock()">Copy to clipboard</button>
# MAGIC
# MAGIC <pre id="copy-block" style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; border:1px solid #e5e7eb; border-radius:10px; background:#f8fafc; padding:14px 16px; font-size:0.85rem; line-height:1.35; white-space:pre;">
# MAGIC <code>
# MAGIC <!-------------------ADD SOLUTION CODE BELOW------------------->
# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC pwd
# MAGIC databricks bundle validate -t development
# MAGIC <!-------------------END SOLUTION CODE------------------->
# MAGIC </code></pre>
# MAGIC
# MAGIC
# MAGIC <script>
# MAGIC function copyBlock() {
# MAGIC   const el = document.getElementById("copy-block");
# MAGIC   if (!el) return;
# MAGIC
# MAGIC   const text = el.innerText;
# MAGIC
# MAGIC   // Preferred modern API
# MAGIC   if (navigator.clipboard && navigator.clipboard.writeText) {
# MAGIC     navigator.clipboard.writeText(text)
# MAGIC       .then(() => alert("Copied to clipboard"))
# MAGIC       .catch(err => {
# MAGIC         console.error("Clipboard write failed:", err);
# MAGIC         fallbackCopy(text);
# MAGIC       });
# MAGIC   } else {
# MAGIC     fallbackCopy(text);
# MAGIC   }
# MAGIC }
# MAGIC
# MAGIC function fallbackCopy(text) {
# MAGIC   const textarea = document.createElement("textarea");
# MAGIC   textarea.value = text;
# MAGIC   textarea.style.position = "fixed";
# MAGIC   textarea.style.left = "-9999px";
# MAGIC   document.body.appendChild(textarea);
# MAGIC   textarea.select();
# MAGIC   try {
# MAGIC     document.execCommand("copy");
# MAGIC     alert("Copied to clipboard");
# MAGIC   } catch (err) {
# MAGIC     console.error("Fallback copy failed:", err);
# MAGIC     alert("Could not copy to clipboard. Please copy manually.");
# MAGIC   } finally {
# MAGIC     document.body.removeChild(textarea);
# MAGIC   }
# MAGIC }
# MAGIC </script>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ## H. Task 5 - Deploy to the `development` Target
# MAGIC
# MAGIC Deploy the bundle to the `development` target.

# COMMAND ----------

# <FILL-IN>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##### ANSWER
# MAGIC
# MAGIC <details>
# MAGIC   <summary>EXPAND FOR SOLUTION CODE</summary>
# MAGIC
# MAGIC <button onclick="copyBlock()">Copy to clipboard</button>
# MAGIC
# MAGIC <pre id="copy-block" style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; border:1px solid #e5e7eb; border-radius:10px; background:#f8fafc; padding:14px 16px; font-size:0.85rem; line-height:1.35; white-space:pre;">
# MAGIC <code>
# MAGIC <!-------------------ADD SOLUTION CODE BELOW------------------->
# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC databricks bundle deploy -t development
# MAGIC <!-------------------END SOLUTION CODE------------------->
# MAGIC </code></pre>
# MAGIC
# MAGIC
# MAGIC <script>
# MAGIC function copyBlock() {
# MAGIC   const el = document.getElementById("copy-block");
# MAGIC   if (!el) return;
# MAGIC
# MAGIC   const text = el.innerText;
# MAGIC
# MAGIC   // Preferred modern API
# MAGIC   if (navigator.clipboard && navigator.clipboard.writeText) {
# MAGIC     navigator.clipboard.writeText(text)
# MAGIC       .then(() => alert("Copied to clipboard"))
# MAGIC       .catch(err => {
# MAGIC         console.error("Clipboard write failed:", err);
# MAGIC         fallbackCopy(text);
# MAGIC       });
# MAGIC   } else {
# MAGIC     fallbackCopy(text);
# MAGIC   }
# MAGIC }
# MAGIC
# MAGIC function fallbackCopy(text) {
# MAGIC   const textarea = document.createElement("textarea");
# MAGIC   textarea.value = text;
# MAGIC   textarea.style.position = "fixed";
# MAGIC   textarea.style.left = "-9999px";
# MAGIC   document.body.appendChild(textarea);
# MAGIC   textarea.select();
# MAGIC   try {
# MAGIC     document.execCommand("copy");
# MAGIC     alert("Copied to clipboard");
# MAGIC   } catch (err) {
# MAGIC     console.error("Fallback copy failed:", err);
# MAGIC     alert("Could not copy to clipboard. Please copy manually.");
# MAGIC   } finally {
# MAGIC     document.body.removeChild(textarea);
# MAGIC   }
# MAGIC }
# MAGIC </script>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC Navigate to **Jobs & Pipelines** and open the Job `[dev labuser_UNIQUE_ID] ml_health_etl_workflow_development`
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### Checkpoint - Dev Deployment
# MAGIC ![Ml Job Deploy](../Includes/images/ml-lab/dev-deployment-job-checkpoint.png)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## I. Task 6 - Run the `development` Workflow
# MAGIC
# MAGIC Run the deployed workflow against the `development` target. 
# MAGIC
# MAGIC The job key in the bundle is `ml_health_etl_workflow`.

# COMMAND ----------

# <FILL-IN>

# COMMAND ----------

# MAGIC %md
# MAGIC #### Checkpoint - Dev Run 
# MAGIC ![Ml Job Deploy](../Includes/images/ml-lab/dev-job-run.png)
# MAGIC

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
# MAGIC If you see the following error after running your bundle, the format of your notebook could be incorrect.
# MAGIC
# MAGIC ```
# MAGIC Error: Task Health_ETL failed!
# MAGIC Error:
# MAGIC Please refer to the logs for this pipeline in the pipelines page.
# MAGIC ```
# MAGIC
# MAGIC Check the format of your notebook for the SDP and adjust accordingly!
# MAGIC
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##### ANSWER
# MAGIC
# MAGIC <details>
# MAGIC   <summary>EXPAND FOR SOLUTION CODE</summary>
# MAGIC
# MAGIC <button onclick="copyBlock()">Copy to clipboard</button>
# MAGIC
# MAGIC <pre id="copy-block" style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; border:1px solid #e5e7eb; border-radius:10px; background:#f8fafc; padding:14px 16px; font-size:0.85rem; line-height:1.35; white-space:pre;">
# MAGIC <code>
# MAGIC <!-------------------ADD SOLUTION CODE BELOW------------------->
# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC databricks bundle run ml_health_etl_workflow -t development
# MAGIC <!-------------------END SOLUTION CODE------------------->
# MAGIC </code></pre>
# MAGIC
# MAGIC
# MAGIC <script>
# MAGIC function copyBlock() {
# MAGIC   const el = document.getElementById("copy-block");
# MAGIC   if (!el) return;
# MAGIC
# MAGIC   const text = el.innerText;
# MAGIC
# MAGIC   // Preferred modern API
# MAGIC   if (navigator.clipboard && navigator.clipboard.writeText) {
# MAGIC     navigator.clipboard.writeText(text)
# MAGIC       .then(() => alert("Copied to clipboard"))
# MAGIC       .catch(err => {
# MAGIC         console.error("Clipboard write failed:", err);
# MAGIC         fallbackCopy(text);
# MAGIC       });
# MAGIC   } else {
# MAGIC     fallbackCopy(text);
# MAGIC   }
# MAGIC }
# MAGIC
# MAGIC function fallbackCopy(text) {
# MAGIC   const textarea = document.createElement("textarea");
# MAGIC   textarea.value = text;
# MAGIC   textarea.style.position = "fixed";
# MAGIC   textarea.style.left = "-9999px";
# MAGIC   document.body.appendChild(textarea);
# MAGIC   textarea.select();
# MAGIC   try {
# MAGIC     document.execCommand("copy");
# MAGIC     alert("Copied to clipboard");
# MAGIC   } catch (err) {
# MAGIC     console.error("Fallback copy failed:", err);
# MAGIC     alert("Could not copy to clipboard. Please copy manually.");
# MAGIC   } finally {
# MAGIC     document.body.removeChild(textarea);
# MAGIC   }
# MAGIC }
# MAGIC </script>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ## J. Task 7 - Destroy the `development` Bundle
# MAGIC
# MAGIC Clean up the `development` deployment.

# COMMAND ----------

# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC databricks bundle destroy -t development --auto-approve

# COMMAND ----------

# MAGIC %md
# MAGIC ## K. Task 8 - Promote the Bundle to `stage`
# MAGIC
# MAGIC Imagine you've reviewed your code, analyzed coverage, and so on, and you're ready to deploy and test in a staging environment. DABs make this easy: you change one CLI flag (`-t stage`) and the bundle's `stage` target overrides take care of the rest.
# MAGIC
# MAGIC Walk through the same lifecycle, this time against the `stage` target. First, take a moment to look at the `stage` block inside **databricks.yml** and notice what overrides have already been set for you.
# MAGIC
# MAGIC ### Step 8.1 - Bundle summary for `stage`

# COMMAND ----------

# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC databricks bundle summary -t stage

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 8.2 - Validate `stage`

# COMMAND ----------

# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC databricks bundle validate -t stage

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 8.3 - Deploy to `stage`

# COMMAND ----------

# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC databricks bundle deploy -t stage

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 8.4 - Run the `stage` workflow

# COMMAND ----------

# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC databricks bundle run ml_health_etl_workflow -t stage

# COMMAND ----------

# MAGIC %md
# MAGIC #### Checkpoint - Stage Run
# MAGIC
# MAGIC ![Ml Job Deploy Stage](../Includes/images/ml-lab/stage-job-run.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 8.5 - Destroy the `stage` bundle

# COMMAND ----------

# MAGIC %sh
# MAGIC cd "./TODO - Lab DABs Workflow"
# MAGIC databricks bundle destroy -t stage --auto-approve

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC Nice work. In this lab you wired a registered Unity Catalog ML model into an existing engineering bundle without changing the rest of the workflow:
# MAGIC
# MAGIC 1. Added the `base_model_name`, `silver_table_name`, and `cluster_id` variables to **variables.yml**.
# MAGIC 2. Added a new inference task to **dabs_workflow_with_ml.job.yml**, depending on **Health_ETL**, calling the **Inference** notebook with three `base_parameters`.
# MAGIC 3. Used `databricks bundle summary` to inspect the resolved bundle before deploying.
# MAGIC 4. Validated, deployed, ran, and destroyed the bundle against `development`.
# MAGIC 5. Promoted the same bundle to `stage` with a single `-t stage` flag and ran the same lifecycle there.
# MAGIC
# MAGIC ## Next Steps
# MAGIC
# MAGIC Try building your own DAB from scratch using what you learned here. It helps to grow the workflow incrementally, one task at a time, validating after each change so problems stay easy to isolate.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
