# 🏭 ICT5101 - IoT Project Part B Predictive Maintenance Using Machine Learning

This folder contains **Part B** of the ICT5101 Internet of Things coursework.

The project focuses on **predictive maintenance in an Industrial Internet of Things (IIoT) context**. It uses a synthetic smart factory sensor dataset to train and evaluate machine learning models that predict whether a factory machine is likely to fail within the next seven days.

The implementation builds an end-to-end machine learning workflow covering data loading, data cleaning, feature engineering, model training, model evaluation, and model interpretation.

## 📚 Table of Contents

- [📋 Project Overview](#-project-overview)
- [📊 Dataset](#-dataset)
- [🗃️ Folder Structure](#️-folder-structure)
- [🧠 Machine Learning Pipeline](#-machine-learning-pipeline)
- [🤖 Models Used](#-models-used)
- [📈 Evaluation Metrics](#-evaluation-metrics)
- [📤 Outputs](#-outputs)
- [⚙️ Installation](#️-installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
- [📝 Notes](#-notes)
- [👍 Acknowledgments](#-acknowledgments)
- [📧 Contact](#-contact)

## 📋 Project Overview

In industrial environments, unexpected machine failures can lead to downtime, repair costs, and reduced productivity. Predictive maintenance aims to reduce these issues by using sensor readings and operational data to identify machines that may require attention before failure occurs.

This project applies machine learning models to Industrial IoT sensor data to classify whether a machine is at risk of failure within the next seven days.

The target variable used in this project is:

```text
Failure_Within_7_Days
```

where:

```text
0 = No Failure
1 = Failure
```

## 📊 Dataset

The dataset used in this project is the **Industrial IoT Dataset (Synthetic)** from Kaggle.

**Dataset source:** https://www.kaggle.com/datasets/canozensoy/industrial-iot-dataset-synthetic/data

The dataset contains simulated smart factory machine data, including machine information, operational readings, sensor values, maintenance history, and failure-related fields.

Examples of dataset features include:

- `Machine_Type`
- `Operational_Hours`
- `Temperature_C`
- `Vibration_mms`
- `Sound_dB`
- `Oil_Level_pct`
- `Coolant_Level_pct`
- `Power_Consumption_kW`
- `Last_Maintenance_Days_Ago`
- `Maintenance_History_Count`
- `Failure_History_Count`
- `AI_Supervision`
- `Error_Codes_Last_30_Days`
- `Failure_Within_7_Days`

The notebook also removes columns that could either provide no useful learning value or create data leakage, such as:

- `Machine_ID`
- `Remaining_Useful_Life_days`

## 🗃️ Folder Structure

```bash
PartB/
│
├── Docs/
│   ├── ICT5101 Part B Assignment Specification.pdf
│   └── ICT5101_IoT_PartB_Project_Report.pdf
│
├── Kaggle_Industrial_IoT_Dataset/
│   └── factory_sensor_simulator_2040.csv
│
├── src/
│   └── IoT_PartB_Predictive_Maintenance.ipynb
│
├── requirements.txt
└── README.md
```

### 📂 Folder Description

| Folder/File | Description |
|---|---|
| `Docs/` | Contains the assignment specification and the final Part B project report. |
| `Kaggle_Industrial_IoT_Dataset/` | Contains the Industrial IoT synthetic dataset used for model training and evaluation. |
| `src/` | Contains the Jupyter Notebook implementation of the predictive maintenance pipeline. |
| `requirements.txt` | Contains the Python dependencies required to run the Part B notebook and machine learning pipeline. |
| `README.md` | Provides documentation for Part B of the project. |

## 🧠 Machine Learning Pipeline

The notebook implements a full predictive maintenance pipeline with the following stages:

### 1. Data Loading

The dataset is loaded from:

```text
../Kaggle_Industrial_IoT_Dataset/factory_sensor_simulator_2040.csv
```

Before loading, the notebook validates that the dataset exists, is a file, and has the expected `.csv` extension.

### 2. Data Cleaning

The dataset is cleaned by removing unsuitable columns, handling missing values, and preparing the data for machine learning.

`Machine_ID` is removed because it is only an identifier and could lead to memorisation rather than useful generalisation.

`Remaining_Useful_Life_days` is removed because it is directly related to the prediction target and could cause data leakage.

### 3. Feature Engineering

Additional features are created to improve model learning:

| Feature | Purpose |
|---|---|
| `Machine_Age` | Represents the age of each machine using the installation year. |
| `Operational_Hours_Per_Year` | Measures how heavily a machine has been used relative to its age. |
| `Maintenance_Pressure` | Combines time since last maintenance with failure history. |
| `Low_Oil` | Flags machines with low oil levels. |
| `Low_Coolant` | Flags machines with low coolant levels. |

### 4. Class Distribution Analysis

The target class distribution is analysed because failure cases are less common than non-failure cases. This means that accuracy alone is not enough to judge model quality.

For this reason, the project evaluates models using multiple metrics.

### 5. Dataset Splitting

The data is split into training, validation, and test sets so that the models can be trained, compared, and finally evaluated on unseen data.

### 6. Encoding and Preprocessing

Categorical values such as `Machine_Type` are encoded so that they can be used by machine learning models.

A machine learning pipeline is used where appropriate to keep preprocessing and modelling steps organised.

## 🤖 Models Used

The following machine learning models are trained and compared:

- Logistic Regression
- Random Forest
- HistGradientBoosting
- XGBoost

These models were selected to compare a simple baseline model against more advanced tree-based methods.

## 📈 Evaluation Metrics

Since the dataset is imbalanced, multiple evaluation metrics are used:

| Metric | Purpose |
|---|---|
| Accuracy | Measures overall correctness. |
| Precision | Measures how many predicted failures were actually failures. |
| Recall | Measures how many actual failures were detected. |
| F1-Score | Balances precision and recall. |
| ROC-AUC | Measures ranking performance across thresholds. |
| PR-AP | Measures precision-recall performance, useful for imbalanced datasets. |

Confusion matrices, ROC curves, precision-recall curves, comparison plots, and feature importance outputs are also generated.

## 📤 Outputs

Running the notebook creates output files in an `Out/` directory.

Generated outputs include:

- Trained model files saved with `joblib`
- Validation result tables
- Final test result tables
- Model comparison plots
- Confusion matrices
- ROC curves
- Precision-recall curves
- Feature importance results

These outputs help compare model performance and understand which features contributed most to the predictions.

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DavidF-22/ICT5101-IoT_Project.git
cd ICT5101-IoT_Project/PartB
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python dependencies using:

```bash
pip install -r requirements.txt
```

Alternatively, install the main packages manually:

```bash
pip install ipykernel numpy pandas scikit-learn plotly kaleido matplotlib joblib xgboost notebook
```

Then run the notebook cells from top to bottom.

## 📝 Notes

- The dataset file must remain inside the `Kaggle_Industrial_IoT_Dataset/` folder unless the dataset path in the notebook is updated.
- The notebook is designed to be run from within the `src/` directory.
- The generated `Out/` directory is used to store trained models, plots, and evaluation results.
- The project is intended for coursework and educational purposes.

## 👍 Acknowledgments

This individual project was carried out as part of the partial fulfilment of the requirements for the **ICT5101 Internet of Things** course @ **[The University of Malta](https://www.um.edu.mt/)**.

## 📧 Contact

For any inquiries or feedback, please contact [David Farrugia](mailto:david.farrugia.22@um.edu.mt).