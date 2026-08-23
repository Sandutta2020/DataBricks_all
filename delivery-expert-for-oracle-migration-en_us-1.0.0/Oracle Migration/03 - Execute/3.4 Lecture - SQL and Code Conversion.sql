-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">03 - Execute</span>
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
-- MAGIC # SQL and Code Conversion
-- MAGIC
-- MAGIC This lesson covers the translation of Oracle SQL queries, functions, and procedural code to Databricks equivalents. You will convert scalar functions, aggregate patterns, UDFs, and stored procedures while understanding the nuances between platforms.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC
-- MAGIC - Convert Oracle SQL functions to Databricks SQL equivalents
-- MAGIC - Translate date/time, string, and aggregate function syntax
-- MAGIC - Migrate Oracle UDFs (SQL and Python) to Databricks
-- MAGIC - Convert stored procedures to stored procedures in Databricks or Python notebooks
-- MAGIC - Transform semi-structured data queries using `JSON`, `STRUCT`, and `ARRAY` types
-- MAGIC - Use Lakebridge to accelerate SQL/code conversion at scale

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 1. SQL Conversion Workflow
-- MAGIC
-- MAGIC SQL and code conversion follows a structured approach: identify platform-specific patterns, translate syntax, validate results, and test at scale. Because of the major differences between the two platforms, simple syntax conversion might not be enough. Consider Databricks best practices and follow them in the new solution, instead of blindly bringing over the existing logic. 
-- MAGIC
-- MAGIC For example: even though stored procedures exist in Databricks, it might be better to convert an Oracle stored procedure into a Lakeflow Job with tasks that run individual queries, notebooks and/or Python code. This approach could provide better observability and maintainability than just translating the stored procedure syntax to Databricks.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     subgraph ORCL["Oracle SQL"]
-- MAGIC         FUNCS["Functions<br/><i>ADD_MONTHS, LISTAGG</i>"]
-- MAGIC         UDF["UDFs<br/><i>User Defined Functions</i>"]
-- MAGIC         SP["Stored Procedures<br/><i>Oracle Scripting</i>"]
-- MAGIC     end
-- MAGIC     subgraph CONVERT["Conversion"]
-- MAGIC         SYNTAX["Syntax<br/>Translation"]
-- MAGIC         TYPES["Type<br/>Mapping"]
-- MAGIC         ORC["Determining<br/>Orchestration"]
-- MAGIC         TEST["Validation"]
-- MAGIC     end
-- MAGIC     subgraph DB["Databricks"]
-- MAGIC         DBSQL["Databricks<br/>SQL"]
-- MAGIC         PYUDF["Python<br/>UDFs"]
-- MAGIC         NB["Notebooks /<br/>Workflows"]
-- MAGIC     end
-- MAGIC     FUNCS --> CONVERT
-- MAGIC     UDF --> CONVERT
-- MAGIC     SP --> CONVERT
-- MAGIC     CONVERT --> DBSQL
-- MAGIC     CONVERT --> PYUDF
-- MAGIC     CONVERT --> NB
-- MAGIC     style ORCL fill:#fff,stroke:#F80102,stroke-width:2px
-- MAGIC     style CONVERT fill:#fff,stroke:#607d8b,stroke-width:2px
-- MAGIC     style DB fill:#fff,stroke:#FF3621,stroke-width:2px
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "neutral" }); </script>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Databricks/Spark SQL Compatibility</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC             Many Oracle functions work identically in Databricks SQL. Start by running your queries as-is. Databricks SQL has broad compatibility with ANSI SQL and includes aliases for common Oracle functions like <code>NVL</code>, <code>DECODE</code>, and date-based <code>TRUNC</code>.
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
-- MAGIC             <strong style="color: #00695c; font-size: 1.1em;"><code>remote_query</code> function</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">During migration, the `remote_query` Databricks SQL function might be useful.
-- MAGIC This allows one to run queries in the <b>source system's SQL dialect</b> over a Lakehouse federated Unity Catalog <code>CONNECTION</code>.
-- MAGIC
-- MAGIC With this, we can run the original Oracle query from Databricks, and compare the results with the migrated query on the migrated data.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 remote_query illustration (source)</summary>
-- MAGIC
-- MAGIC Note how ROWNUM is not valid in Databricks SQL, but since the query is sent to Oracle as a string, it will work as expected.
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC SELECT * FROM remote_query(
-- MAGIC   'oracle_federation',    -- connection name
-- MAGIC   service_name => 'ORCL',
-- MAGIC   query => 'SELECT * FROM HR.EMPLOYEES WHERE ROWNUM <= 5'
-- MAGIC );
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
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
-- MAGIC
-- MAGIC **Note:** `remote_query` is limited to read-only queries.
-- MAGIC
-- MAGIC <a href="https://docs.databricks.com/aws/en/query-federation/remote-queries" target="_blank">Query external databases using the remote_query function</a>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 2. Function Mapping Reference
-- MAGIC
-- MAGIC Most Oracle functions have direct equivalents in Databricks SQL. The following tables provide quick reference for common conversion patterns.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### Date and Time Functions
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Notes |
-- MAGIC |------------------|----------------------|-------|
-- MAGIC | `date + INTERVAL 'n' DAY` | `date + INTERVAL n DAY` or `DATEADD(DAY, n, date)` | Syntax differs |
-- MAGIC | `end_date - start_date` | `DATEDIFF(end_date, start_date)` | Oracle uses direct subtraction |
-- MAGIC | `TRUNC(date, 'MM')` | `DATE_TRUNC('month', date)` | Different syntax |
-- MAGIC | `EXTRACT(part FROM date)` | `DATE_PART(part, date)` or `EXTRACT(part FROM date)` | Both work in Databricks |
-- MAGIC | `TO_DATE(expr)` | `TO_DATE(expr)` or `CAST(expr AS DATE)` | Direct mapping |
-- MAGIC | `TO_TIMESTAMP(expr)` | `TO_TIMESTAMP(expr)` | Direct mapping |
-- MAGIC | `CURRENT_DATE` | `CURRENT_DATE()` | Minor syntax difference |
-- MAGIC | `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP()` | Minor syntax difference |
-- MAGIC | `LAST_DAY(date)` | `LAST_DAY(date)` | Direct mapping |
-- MAGIC | `TO_CHAR(date, 'Month')` | `DATE_FORMAT(date, 'MMMM')` | Month name |
-- MAGIC | `TO_CHAR(date, 'Day')` | `DATE_FORMAT(date, 'EEEE')` | Day name |
-- MAGIC | `ADD_MONTHS(date, n)` | `date + INTERVAL n MONTH` or `ADD_MONTHS(date, n)` | Databricks supports `ADD_MONTHS` directly |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Date/Time Conversion Notes
-- MAGIC
-- MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Conversion |
-- MAGIC |--------|-----------|------------|------------|
-- MAGIC | **Add days to date** | `date + 30` | `DATEADD(DAY, 30, date)` or `date + INTERVAL 30 DAYS` | Oracle uses direct arithmetic |
-- MAGIC | **Add months to date** | `ADD_MONTHS(date, 1)` | `ADD_MONTHS(date, 1)` or `date + INTERVAL 1 MONTH` | Direct mapping |
-- MAGIC | **Date difference (days)** | `end_date - start_date` | `DATEDIFF(end_date, start_date)` | Oracle uses subtraction |
-- MAGIC | **Month name extraction** | `TO_CHAR(date, 'Month')` | `DATE_FORMAT(date, 'MMMM')` | Formatting differs |
-- MAGIC | **Day name extraction** | `TO_CHAR(date, 'Day')` | `DATE_FORMAT(date, 'EEEE')` | Formatting differs |
-- MAGIC | **Date parts extraction** | `EXTRACT(part FROM date)` | `DATE_PART(part, date)` or `EXTRACT(part FROM date)` | Syntax differs |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### String Functions
-- MAGIC
-- MAGIC Most string functions have identical syntax between Oracle and Databricks, the main string functions in Oracle are listed below with their equivalents in Databricks.
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Notes |
-- MAGIC |------------------|----------------------|-------|
-- MAGIC | `CONCAT(a, b)` | `CONCAT(a, b, c)` | Oracle supports 2 args only; use `||` for multiple |
-- MAGIC | `a \|\| b` | `\|\|` or `CONCAT()` | Direct mapping |
-- MAGIC | `SUBSTR(str, pos, len)` | `SUBSTR(str, pos, len)` or `SUBSTRING()` | Direct mapping |
-- MAGIC | `SUBSTR(str, 1, n)` | `LEFT(str, n)` | Oracle uses SUBSTR |
-- MAGIC | `SUBSTR(str, -n)` | `RIGHT(str, n)` | Oracle uses SUBSTR |
-- MAGIC | `TRIM(str)` | `TRIM(str)` | Direct mapping |
-- MAGIC | `LTRIM(str)` | `LTRIM(str)` | Direct mapping |
-- MAGIC | `RTRIM(str)` | `RTRIM(str)` | Direct mapping |
-- MAGIC | `UPPER(str)` | `UPPER(str)` | Direct mapping |
-- MAGIC | `LOWER(str)` | `LOWER(str)` | Direct mapping |
-- MAGIC | `REPLACE(str, from, to)` | `REPLACE(str, from, to)` | Direct mapping |
-- MAGIC | `REGEXP_SUBSTR(str, pat)` | `REGEXP_EXTRACT(str, pat)` | Different function name |
-- MAGIC | `REGEXP_REPLACE(str, pat, rep)` | `REGEXP_REPLACE(str, pat, rep)` | Direct mapping |
-- MAGIC | `LISTAGG(col, delim)` | `ARRAY_JOIN(COLLECT_LIST(col), delim)` | Different approach 
-- MAGIC | `INSTR(str, substr)` | `LOCATE(substr, str)` or `INSTR(str, substr)` | Argument order differs; Databricks also supports `INSTR` |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Aggregate and Window Functions
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Notes |
-- MAGIC |------------------|----------------------|-------|
-- MAGIC | `SUM(col)` | `SUM(col)` | Direct mapping |
-- MAGIC | `AVG(col)` | `AVG(col)` | Direct mapping |
-- MAGIC | `COUNT(*)` | `COUNT(*)` | Direct mapping |
-- MAGIC | `COUNT(DISTINCT col)` | `COUNT(DISTINCT col)` | Direct mapping |
-- MAGIC | `MIN(col)` / `MAX(col)` | `MIN(col)` / `MAX(col)` | Direct mapping |
-- MAGIC | `LISTAGG(col, delim)` | `ARRAY_JOIN(COLLECT_LIST(col), delim)` | Different approach |
-- MAGIC | `MEDIAN(col)` | `PERCENTILE(col, 0.5)` or `MEDIAN(col)` | `MEDIAN` available in DBR 14+ |
-- MAGIC | `MODE(col)` | `MODE(col)` | Direct mapping (DBR 14+) |
-- MAGIC | `NVL(col, 0)` | `COALESCE(col, 0)` or `IFNULL(col, 0)` | Null handling |
-- MAGIC | `NULLIF(col, 0)` | `NULLIF(col, 0)` | Direct mapping |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. Semi-Structured Data (JSON vs VARIANT)
-- MAGIC
-- MAGIC Oracle stores semi-structured data as `CLOB` or `VARCHAR2` with JSON content and accesses it using JSON functions. Databricks supports the `VARIANT` type (DBR 15.3+) with `:` path notation for direct field access.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### Access Patterns (Oracle JSON vs Databricks VARIANT)
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Notes |
-- MAGIC |------------------|----------------------|-------|
-- MAGIC | `JSON_VALUE(col, '$.field')` | `col:field` | Different access pattern |
-- MAGIC | `CAST(JSON_VALUE(col, '$.field') AS VARCHAR2(4000))` | `col:field::STRING` or `CAST(col:field AS STRING)` | Cast syntax supported |
-- MAGIC | `JSON_VALUE(col, '$.nested.field')` | `col:nested.field` | Different access pattern |
-- MAGIC | `JSON_VALUE(col, '$.array[0]')` | `col:array[0]` | Different access pattern |
-- MAGIC | `JSON_OBJECT(k VALUE v, ...)` | `NAMED_STRUCT(k, v, ...)` or JSON | Use `NAMED_STRUCT` or build JSON |
-- MAGIC | `JSON_TRANSFORM(obj, ...)` | Custom UDF or rebuild | No direct equivalent |
-- MAGIC | `JSON_ARRAY(a, b, c)` | `ARRAY(a, b, c)` | Different function name |
-- MAGIC | `JSON_ARRAY_LENGTH(arr)` | `ARRAY_SIZE(arr)` | Equivalent function |
-- MAGIC | `JSON_EXISTS(arr, '$?(@ == val)')` | `ARRAY_CONTAINS(arr, val)` | Different approach |
-- MAGIC | `JSON_TABLE(col, '$[*]' COLUMNS (...))` | `EXPLODE(col)` | Different function name |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### `JSON_TABLE` to `explode` mapping
-- MAGIC
-- MAGIC | Oracle                                    | Databricks                          |
-- MAGIC |--------------------------------------------|-------------------------------------|
-- MAGIC | `JSON_TABLE(...)`                         | `EXPLODE(arr)`                      |
-- MAGIC | `JSON_TABLE with OUTER join`               | `EXPLODE_OUTER(arr)`                |
-- MAGIC | Row number via `FOR ORDINALITY`           | `POSEXPLODE(arr)` returns pos, val  |
-- MAGIC | Column alias from `JSON_TABLE`             | Alias from `LATERAL VIEW`           |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">JSON_EXISTS Argument Order</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Oracle uses <code>JSON_EXISTS</code> with path filter expressions to check array membership.
-- MAGIC             Databricks uses <code>ARRAY_CONTAINS</code> - a simpler, direct approach.</p>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li><b>Oracle:</b> <code>JSON_EXISTS(col, '$.path[*]?(@ == "value")')</code></li>
-- MAGIC                 <li><b>Databricks:</b> <code>ARRAY_CONTAINS(array, value)</code></li>
-- MAGIC             </ul>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 4. User-Defined Function (UDF) Conversion
-- MAGIC
-- MAGIC Both platforms support SQL UDFs. Databricks also supports Python UDFs, while Oracle uses PL/SQL for procedural logic. The syntax differs slightly, but the concepts are similar.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### UDF Type Mapping
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Notes |
-- MAGIC |------------------|----------------------|-------|
-- MAGIC | SQL UDF | SQL UDF | Minor syntax differences |
-- MAGIC | PL/SQL Function | Python UDF | Oracle logic rewritten in Python |
-- MAGIC | Java Stored Procedure | Java/Scala UDF | Supported via JAR registration |
-- MAGIC | JavaScript (external) | Python UDF | Convert to Python |
-- MAGIC | Pipelined Table Function | Python UDTF | Supported in DBR 14+ |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">SQL UDF Conversion</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Both platforms support SQL UDFs. Oracle uses PL/SQL-based functions, while Databricks uses SQL UDF syntax with RETURN expressions. The core concepts are similar, but the syntax differs.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### SQL UDF Syntax Comparison
-- MAGIC
-- MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
-- MAGIC |--------|-----------|------------|
-- MAGIC | **Body delimiter** | `BEGIN ... END` | `RETURN expression` |
-- MAGIC | **Multi-statement** | Supported in PL/SQL | Use Python UDF instead |
-- MAGIC | **Type names** | `NUMBER`, `NUMBER(p,s)` | `DOUBLE`, `DECIMAL(p,s)` |
-- MAGIC | **Namespace** | `schema.function_name` | `catalog.schema.function_name` |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Python UDF Conversion
-- MAGIC
-- MAGIC Databricks supports Python UDFs for advanced logic and external library usage. Oracle does not natively support Python UDFs, so such logic is typically implemented using PL/SQL or moved outside the database.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Python UDF Conversion</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Unlike Oracle, Databricks enables Python-based execution inside the engine. This allows use of external libraries and more complex transformations beyond standard SQL or PL/SQL capabilities.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #4caf50; background: #e8f5e9; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">✅</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #2e7d32; font-size: 1.1em;">Why <code>pandas_udf</code> is Preferred</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;"><b>Understanding the performance difference:</b> Spark is implemented in Scala and runs on the Java Virtual Machine (JVM). When you call a Python UDF, data must be serialized from the JVM to a Python process and back. With <code>@udf</code>, this serialization happens for <i>every single row</i>, this results in a significant overhead resulting in excessive execution time.</p>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;"><code>pandas_udf</code> solves this by using <a href="https://arrow.apache.org/" target="_blank"><b>Apache Arrow</b></a>, a language-independent columnar memory format, to transfer data in columnar batches:</p>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li><b>10x-100x faster</b> - Batch serialization amortizes JVM to Python transfer cost across thousands of rows</li>
-- MAGIC                 <li><b>Zero-copy data transfer</b> - Arrow's columnar format enables direct memory access without pickle serialization</li>
-- MAGIC                 <li><b>Vectorized execution</b> - Operations on <code>pd.Series</code> use optimized NumPy/C backends, not Python loops</li>
-- MAGIC                 <li><b>Better memory efficiency</b> - Processes data in configurable chunks rather than loading entire partitions</li>
-- MAGIC             </ul>
-- MAGIC             <p style="margin: 12px 0 0 0; color: #333;"><b>Migration note:</b> Oracle Python UDFs execute row-at-a-time with scalar inputs. When converting to Databricks <code>pandas_udf</code>, change function signatures from scalar values to <code>pd.Series</code>.</p>
-- MAGIC
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;"><b>When to use row-at-a-time <code>@udf</code>:</b> Only when calling external APIs per-row or when complex control flow cannot be vectorized.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Python UDF Syntax Comparison
-- MAGIC
-- MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
-- MAGIC |--------|-----------|------------|
-- MAGIC | **Definition** | Not supported | SQL DDL, `@udf`, or `@pandas_udf` decorator |
-- MAGIC | **Recommended approach** | Use PL/SQL or external processing | **`@pandas_udf`** (vectorized, faster) |
-- MAGIC | **Handler** | N/A | Function name in `$$` block or decorator |
-- MAGIC | **Input type** | N/A | pandas Series (pandas_udf) or scalar (@udf) |
-- MAGIC | **Packages** | N/A | Cluster libraries or `%pip install` |
-- MAGIC | **Runtime** | N/A | Cluster Python version |
-- MAGIC | **Registration** | N/A | `spark.udf.register()` for SQL access |
-- MAGIC | **Performance** | Row-by-row (PL/SQL) | Vectorized with Arrow (pandas_udf) |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 5. Stored Procedure Conversion
-- MAGIC
-- MAGIC Oracle stored procedures can be converted to Databricks SQL stored procedures, SQL scripts, notebooks, or Python functions. The conversion approach depends on the procedure complexity.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Conversion Approaches
-- MAGIC
-- MAGIC | Oracle SP Type | Databricks Alternative | Best For |
-- MAGIC |-------------------|------------------------|----------|
-- MAGIC | Simple SQL SP | SQL Stored Procedure (Preview) | Single-statement logic, reusable procedures |
-- MAGIC | PL/SQL Procedure | SQL Scripting or Python notebook | Control flow, loops, cursors, condition handling |
-- MAGIC | External Python logic | Python notebook or UDF | Complex transformations |
-- MAGIC | Multi-statement DML | SQL Scripting or Notebook with `%sql` cells | ETL pipelines |
-- MAGIC | Scheduled SP | Lakeflow Job Notebook Task | Orchestrated jobs |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Databricks SQL Scripting Support</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Databricks now supports SQL/PSM standard-based scripting (DBR 16.3+) with control flow statements (IF, <code>CASE</code>, <code>LOOP</code>, <code>FOR</code>, <code>WHILE</code>), exception handling, and compound statements. SQL Stored Procedures (DBR 17.0+, Preview) allow you to persist scripts in Unity Catalog with <code>GRANT/CALL</code> semantics. See the <a href="https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-scripting">SQL Scripting documentation</a> for details.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Stored Procedure -> Notebook Pattern</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">An alternate approach for complex stored procedures:</p>
-- MAGIC             <ol style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li><b>Create a notebook</b> with the procedure logic as Python functions</li>
-- MAGIC                 <li><b>Use widgets (<code>dbutils.widgets</code>)</b></li>
-- MAGIC                 <li><b>Schedule with Lakeflow Jobs</b> to replicate Oracle <code>TASK</code> behavior</li>
-- MAGIC             </ol>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 6. Type Casting and Conversion
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### Casting Syntax Comparison
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Notes |
-- MAGIC |------------------|----------------------|-------|
-- MAGIC | `CAST(col AS VARCHAR2(100))` | `col::STRING` or `CAST(col AS STRING)` | Oracle uses `CAST`, not `::` |
-- MAGIC | `CAST(col AS NUMBER)` | `CAST(col AS DECIMAL)` | `NUMBER` maps to `DECIMAL` |
-- MAGIC | `CAST(col AS NUMBER(10,2))` | `CAST(col AS DECIMAL(10,2))` | `NUMBER` maps to `DECIMAL` |
-- MAGIC | `CAST(col AS TIMESTAMP)` | `col::TIMESTAMP` | Direct mapping |
-- MAGIC | `CAST(col AS DATE)` | `col::DATE` | Direct mapping |
-- MAGIC | `CAST(col AS BINARY_DOUBLE)` | `col::DOUBLE` | `FLOAT` equivalent |
-- MAGIC | N/A | `col::BOOLEAN` | Oracle has no BOOLEAN in SQL |
-- MAGIC | N/A | `col::VARIANT` | Not supported in Oracle |
-- MAGIC | `VALIDATE_CONVERSION(col AS type)` | `TRY_CAST(col AS type)` | Oracle 12.2+; returns 1/0 instead of NULL |
-- MAGIC | `TO_CHAR(col)` | `CAST(col AS STRING)` | Equivalent |
-- MAGIC | `TO_NUMBER(col)` | `CAST(col AS DECIMAL)` | Equivalent |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 7. Conditional and NULL Functions
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### Conditional Function Mapping
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Notes |
-- MAGIC |------------------|----------------------|-------|
-- MAGIC | `CASE WHEN ... END` | `CASE WHEN ... END` | Direct mapping |
-- MAGIC | N/A | `IF(cond, true, false)` or `IFF(cond, true, false)` | Not supported in Oracle |
-- MAGIC | N/A | `IFNULL(a, b)` or `COALESCE(a, b)` | Use `NVL` or `COALESCE` in Oracle |
-- MAGIC | `NVL(a, b)` | `NVL(a, b)` or `COALESCE(a, b)` | Direct mapping |
-- MAGIC | `NVL2(a, b, c)` | `NVL2(a, b, c)` | Direct mapping |
-- MAGIC | `NULLIF(a, b)` | `NULLIF(a, b)` | Direct mapping |
-- MAGIC | `COALESCE(a, b, c)` | `COALESCE(a, b, c)` | Direct mapping |
-- MAGIC | N/A | `COALESCE(col, 0)` | Use `NVL(col, 0)` in Oracle |
-- MAGIC | N/A | `NULLIF(col, 0)` | Same function in Oracle |
-- MAGIC | `DECODE(col, v1, r1, ...)` | `CASE` or nested `IF` | Convert to CASE |
-- MAGIC | N/A | `a <=> b` | Use `(a = b OR (a IS NULL AND b IS NULL))` |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 8. QUALIFY Clause
-- MAGIC
-- MAGIC Databricks SQL supports the `QUALIFY` clause for filtering window function results. Oracle does not support `QUALIFY`, so equivalent logic is implemented using subqueries or CTEs.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #009688; background: #e0f2f1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">💡</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #00695c; font-size: 1.1em;">QUALIFY in Databricks</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;"><code>QUALIFY</code> is natively supported in Databricks SQL (DBR 10.4+), allowing direct filtering of window function results. This simplifies query structure and improves readability.</p>
-- MAGIC             <p style="margin: 12px 0 0 0; color: #333;"><b>Oracle Equivalent:</b> Oracle requires a subquery or CTE pattern to achieve the same result:</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Qualify illustration on Databricks</summary>
-- MAGIC
-- MAGIC   <div class="code-block" data-language="sql">
-- MAGIC   SELECT * FROM table
-- MAGIC   QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY ts) = 1;
-- MAGIC   </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle equivalent</summary>
-- MAGIC
-- MAGIC   <div class="code-block" data-language="sql">
-- MAGIC WITH ranked AS (
-- MAGIC     SELECT t.*, ROW_NUMBER() OVER (PARTITION BY id ORDER BY ts) AS rn
-- MAGIC     FROM table t
-- MAGIC )
-- MAGIC SELECT * FROM ranked WHERE rn = 1;
-- MAGIC   </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
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
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 9. Automated Conversion with Lakebridge
-- MAGIC
-- MAGIC **Lakebridge** is a Databricks Labs project that can automate SQL and code transpilation. While manual understanding of conversion patterns is essential, Lakebridge can accelerate large-scale migrations, but requires validation and manual adjustments.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     subgraph INPUT["Input Sources"]
-- MAGIC         SQL["SQL Queries, UDFs & SPs<br/><i>.sql files, DDL scripts</i>"]
-- MAGIC     end
-- MAGIC     subgraph LB["Lakebridge"]
-- MAGIC         ANALYZE["analyze<br/><i>Assessment</i>"]
-- MAGIC         TRANSPILE["transpile<br/><i>Conversion</i>"]
-- MAGIC     end
-- MAGIC     subgraph OUTPUT["Output"]
-- MAGIC         REPORT["Compatibility<br/>Report (.xlsx)"]
-- MAGIC         DBSQL["Databricks<br/>SQL"]
-- MAGIC     end
-- MAGIC     SQL --> ANALYZE
-- MAGIC     SQL --> TRANSPILE
-- MAGIC     ANALYZE --> REPORT
-- MAGIC     TRANSPILE --> DBSQL
-- MAGIC     style INPUT fill:#e3f2fd,stroke:#1976d2
-- MAGIC     style LB fill:#fff3e0,stroke:#ff9800
-- MAGIC     style OUTPUT fill:#e8f5e9,stroke:#4caf50
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "neutral" }); </script>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Lakebridge SQL Conversion Notes</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Lakebridge automates some Oracle conversions, but several patterns require manual review:</p>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;"><b>Automatically converted:</b></p>
-- MAGIC             <ul style="margin: 4px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li><code>SYSDATE</code> -> <code>current_date()</code></li>
-- MAGIC                 <li><code>TRUNC(date)</code> -> <code>date_trunc('DD', date)</code></li>
-- MAGIC             </ul>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;"><b>May require manual adjustment:</b></p>
-- MAGIC             <ul style="margin: 4px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li><code>NVL()</code> -> <code>COALESCE()</code></li>
-- MAGIC                 <li><code>DECODE()</code> -> <code>CASE WHEN</code></li>
-- MAGIC                 <li><code>ROWNUM</code> -> <code>LIMIT</code> or <code>ROW_NUMBER()</code></li>
-- MAGIC                 <li><code>LISTAGG()</code> -> <code>ARRAY_JOIN(COLLECT_LIST())</code></li>
-- MAGIC                 <li><code>CONNECT BY</code> -> recursive CTE (<code>WITH RECURSIVE</code>)</li>
-- MAGIC                 <li>PL/SQL stored procedures -> Notebook / Python / SQL workflows</li>
-- MAGIC             </ul>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">See <a href="https://github.com/databrickslabs/lakebridge" target="_blank">Lakebridge GitHub repository</a> for documentation.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## Summary
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC ### SQL Conversion Checklist
-- MAGIC
-- MAGIC ✅ Date functions converted (`DATE + n`, `ADD_MONTHS`)  
-- MAGIC ✅ String functions validated (`LISTAGG` -> `ARRAY_JOIN(COLLECT_LIST())`, `REGEXP_SUBSTR` -> `REGEXP_EXTRACT`)  
-- MAGIC ✅ Aggregate functions migrated (`COLLECT_LIST/COLLECT_SET`, `COALESCE`)  
-- MAGIC ✅ JSON queries converted to function-based access (`JSON_VALUE`, `JSON_QUERY`)  
-- MAGIC ✅ Array handling adapted (`JSON_TABLE` instead of `FLATTEN`)  
-- MAGIC ✅ `ARRAY_CONTAINS` argument order corrected (array first in Databricks)  
-- MAGIC ✅ `QUALIFY` converted to CTE with `WHERE` filter  
-- MAGIC ✅ SQL UDFs converted (PL/SQL -> `RETURN` expressions)  
-- MAGIC ✅ Python UDFs introduced as new capability in Databricks  
-- MAGIC ✅ Stored procedures converted to notebooks or SQL scripting  
-- MAGIC ✅ Type casting verified (`NUMBER` -> `DECIMAL`, `CAST` instead of `::`)  
-- MAGIC ✅ Conditional functions mapped (`NVL`, `COALESCE`, `CASE`)  
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Validation Checkpoint</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Before marking SQL conversion complete, verify:</p>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li>Row counts match between source and target queries</li>
-- MAGIC                 <li>Aggregate values (<code>SUM</code>, <code>AVG</code>, <code>COUNT</code>) align within tolerance</li>
-- MAGIC                 <li><code>NULL</code> handling produces equivalent results</li>
-- MAGIC                 <li>Date/time calculations account for timezone differences</li>
-- MAGIC                 <li>Floating-point precision is acceptable for analytics use cases</li>
-- MAGIC             </ul>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### Key Takeaways
-- MAGIC
-- MAGIC **What Converts Directly:**
-- MAGIC - Most scalar functions (math, string basics, date basics)
-- MAGIC - `CASE WHEN`, `COALESCE`, `NULLIF`, `NVL`, `NVL2`
-- MAGIC - Type casting with `CAST()`
-- MAGIC - Window functions (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`)
-- MAGIC
-- MAGIC **What Requires Adjustment:**
-- MAGIC - Date arithmetic differences (`DATE + n`, `ADD_MONTHS`)
-- MAGIC - `LISTAGG()` -> `ARRAY_JOIN(COLLECT_LIST())`
-- MAGIC - JSON handling (`JSON_VALUE`, `JSON_QUERY` vs `:` notation)
-- MAGIC - `JSON_TABLE` -> `LATERAL VIEW EXPLODE`
-- MAGIC - `ARRAY_CONTAINS` argument order reversal
-- MAGIC - `QUALIFY` -> CTE/subquery with `WHERE` clause
-- MAGIC - `DECODE` -> `CASE`
-- MAGIC - `OBJECT_CONSTRUCT` -> `NAMED_STRUCT` or JSON building
-- MAGIC - Stored procedures -> Databricks SQL scripting or notebooks
-- MAGIC - Python UDFs -> new capability in Databricks (not available in Oracle)
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## References
-- MAGIC
-- MAGIC - [Databricks SQL Language Reference](https://docs.databricks.com/en/sql/language-manual/index.html)
-- MAGIC - [Built-in Functions](https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html)
-- MAGIC - [User-Defined Functions](https://docs.databricks.com/en/udf/index.html)
-- MAGIC - [VARIANT Type](https://docs.databricks.com/en/sql/language-manual/data-types/variant-type.html)
-- MAGIC - [Delta Lake MERGE](https://docs.databricks.com/en/delta/merge.html)
-- MAGIC - [Lakebridge Documentation](https://databrickslabs.github.io/lakebridge/)

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
