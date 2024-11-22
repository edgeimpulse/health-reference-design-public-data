# health-reference-design-public-data

PPG-DaLiA Data Processing Pipeline see our [Health Reference Design Documentation](https://docs.edgeimpulse.com/docs/edge-impulse-studio/organizations/health-reference-design) for more information.

This repository is a reference design for an end-to-end machine learning workflow using Edge Impulse to process the PPG-DaLiA dataset, and assumes that the data is available and the transformation blocks have been set up. It demonstrates how to:

- Process raw sensor data (accelerometer and PPG) from multiple subjects.
- Extract and attach metadata to each subject's data.
- Combine all processed data into a single dataset suitable for machine learning tasks like heart rate variability (HRV) analysis and activity classification.

This reference design includes:

### Transformation Blocks:

- **DataProcessor**: Processes raw data files for each subject.
- **MetadataGenerator**: Extracts metadata from questionnaire files and attaches it to the data.
- **DataCombiner**: Combines all processed data into a single dataset.
- **Edge Impulse Pipeline**: Automates the data processing workflow by chaining the transformation blocks.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [Setting Up the Repository](#setting-up-the-repository)
- [Transformation Blocks](#transformation-blocks)
  1. [DataProcessor](#dataprocessor)
  2. [MetadataGenerator](#metadatagenerator)
  3. [DataCombiner](#datacombiner)
- [Creating the Pipeline in Edge Impulse](#creating-the-pipeline-in-edge-impulse)
- [Running the Pipeline](#running-the-pipeline)
- [Using the Combined Dataset](#using-the-combined-dataset)
- [Contributing](#contributing)
- [License](#license)

## Overview

The PPG-DaLiA dataset consists of data collected from 15 subjects performing various activities while wearing a wristband equipped with sensors. The dataset includes:

- Accelerometer data (ACC.csv)
- Photoplethysmography (PPG) data (BVP.csv)
- Heart rate data (HR.csv)
- Electrodermal activity (EDA.csv)
- Skin temperature (TEMP.csv)
- Activity labels (S*_activity.csv)
- Subject metadata (S*_quest.csv)

This repository provides a workflow to process this data using Edge Impulse transformation blocks, culminating in a combined dataset ready for machine learning projects.

## Prerequisites

- **Edge Impulse Account**: You need an Edge Impulse account with access to create custom transformation blocks and pipelines.
- **Edge Impulse CLI**: Install the Edge Impulse CLI (`edge-impulse-cli`) version 1.21.1 or higher.
- **Python**: Python 3.7 or higher.
- **Docker**: Required for building and pushing transformation blocks.
- **Git**: For version control and repository management.

## Repository Structure

```plaintext
health-reference-design-public-data/
├── DataProcessor/
│   ├── transform.py
│   ├── parameters.json
│   ├── requirements.txt
│   └── Dockerfile
├── MetadataGenerator/
│   ├── transform.py
│   ├── parameters.json
│   ├── requirements.txt
│   └── Dockerfile
├── DataCombiner/
│   ├── transform.py
│   ├── parameters.json
│   ├── requirements.txt
│   └── Dockerfile
├── README.md
└── LICENSE
```

- **DataProcessor/**: Contains the transformation block for processing raw data.
- **MetadataGenerator/**: Contains the transformation block for extracting and attaching metadata.
- **DataCombiner/**: Contains the transformation block for combining all processed data.
- **README.md**: Documentation and instructions.
- **LICENSE**: License information.

## Setting Up the Repository

### Clone the Repository:

```bash
cd health-reference-design-public-data
```

### Navigate to Each Transformation Block:

The repository contains separate folders for each transformation block. You'll need to set up each one individually.

## Transformation Blocks

### 1. DataProcessor

Processes raw sensor data for each subject.

**Files:**

- `transform.py`: Script to process raw data files.
- `parameters.json`: Defines parameters for the transformation block.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Docker configuration for the block.

**Steps:**

1. Navigate to the DataProcessor directory:

    ```bash
    cd DataProcessor
    ```

2. Initialize the Transformation Block:

    ```bash
    edge-impulse-blocks init --clean
    ```

    - Select Transformation block when prompted.
    - Provide a name and description.

3. Push the Block to Edge Impulse:

    ```bash
    edge-impulse-blocks push
    ```

4. Repeat: After pushing, return to the main directory:

    ```bash
    cd ..
    ```

### 2. MetadataGenerator

Extracts metadata from questionnaire files and attaches it to the data.

**Files:**

- `transform.py`
- `parameters.json`
- `requirements.txt`
- `Dockerfile`

**Steps:**

1. Navigate to the MetadataGenerator directory:

    ```bash
    cd MetadataGenerator
    ```

2. Initialize the Transformation Block:

    ```bash
    edge-impulse-blocks init --clean
    ```

    - Select Transformation block when prompted.
    - Provide a name and description.

3. Push the Block to Edge Impulse:

    ```bash
    edge-impulse-blocks push
    ```

4. Repeat: Return to the main directory:

    ```bash
    cd ..
    ```

### 3. DataCombiner

Combines all processed data into a single dataset.

**Files:**

- `transform.py`
- `parameters.json`
- `requirements.txt`
- `Dockerfile`

**Steps:**

1. Navigate to the DataCombiner directory:

    ```bash
    cd DataCombiner
    ```

2. Initialize the Transformation Block:

    ```bash
    edge-impulse-blocks init --clean
    ```

    - Select Transformation block when prompted.
    - Provide a name and description.

3. Push the Block to Edge Impulse:

    ```bash
    edge-impulse-blocks push
    ```

4. Return to the main directory:

    ```bash
    cd ..
    ```

## Creating the Pipeline in Edge Impulse

Now that all transformation blocks are pushed to Edge Impulse, you can create a pipeline to chain them together.

**Steps:**

### Access Pipelines:

1. In Edge Impulse Studio, navigate to your organization.
2. Go to Data > Pipelines.

### Add a New Pipeline:

1. Click on `+ Add a new pipeline`.
2. Name: `PPG-DaLiA Data Processing Pipeline`
3. Description: `Processes PPG-DaLiA data from raw files to a combined dataset`.
Output Dataset: combined-dataset

### Configure Pipeline Steps:Parameters:

#### Step 1: Process Subject Datajson
 code
- **Transformation Block**: DataProcessor
- **Filter**: `name LIKE '%S%_E4%'` (Selects subjects S1_E4 to S15_E4) "dataset-name": "ppg_dalia_combined.parquet"
- **Input Dataset**: `raw-dataset` (Replace with your dataset name)
- **Output Dataset**: `processed-dataset`ave the Pipeline.
- **Parameters**:
Running the Pipeline
    ```json
    {
      "in-directory": "."In the pipeline list, click on the ⋮ (ellipsis) next to your pipeline.
    }
    ```

#### Step 2: Generate MetadataCheck the pipeline logs to ensure each step runs successfully.

- **Transformation Block**: MetadataGenerator
- **Filter**: Same as Step 1
- **Input Dataset**: `processed-dataset`After completion, verify that the datasets (processed-dataset and combined-dataset) have been created and populated.
- **Output Dataset**: `processed-dataset` (Update in place)
- **Parameters**:(ppg_dalia_combined.parquet), you can:

    ```jsonImport the Data into an Edge Impulse Project:
    {
      "in-directory": "."Create a new project in Edge Impulse.
    }d the combined dataset.
    ```

#### Step 3: Combine Processed Data
Build models for HRV analysis and activity classification.
- **Transformation Block**: DataCombinerraining, and evaluation.- **Filter**: `name LIKE '%'` (Selects all data items)
- **Input Dataset**: `processed-dataset`
- **Output Dataset**: `combined-dataset`
- **Parameters**:

    ```json
    {
      "dataset-name": "ppg_dalia_combined.parquet"
    }
    ```

### Save the Pipeline.

## Running the Pipeline

### Run the Pipeline:

1. In the pipeline list, click on the ⋮ (ellipsis) next to your pipeline.
2. Select `Run pipeline now`.

### Monitor Execution:

- Check the pipeline logs to ensure each step runs successfully.
- Address any errors that may occur.

### Verify Output:

- After completion, verify that the datasets (`processed-dataset` and `combined-dataset`) have been created and populated.

## Using the Combined Dataset

With the combined dataset (`ppg_dalia_combined.parquet`), you can:

### Import the Data into an Edge Impulse Project:

1. Create a new project in Edge Impulse.
2. Use the Data Acquisition tab to upload the combined dataset.
3. Ensure data is correctly labeled and metadata is intact.

### Develop Machine Learning Models:

- Build models for HRV analysis and activity classification.
- Utilize Edge Impulse's tools for data exploration, model training, and evaluation.