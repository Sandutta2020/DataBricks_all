-- Databricks notebook source
-- MAGIC %run ./Classroom-Setup-Common

-- COMMAND ----------

DROP SCHEMA IF EXISTS lab_4 CASCADE;
CREATE SCHEMA IF NOT EXISTS lab_4;
USE SCHEMA lab_4;

-- COMMAND ----------

-- MAGIC %run ./Oracle-HR-Schema-Setup

-- COMMAND ----------

SELECT "lab_4" AS `Created Schema`,
       "OK" AS Status;
