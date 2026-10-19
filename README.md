# Python · Data Analysis & AI Lab

**From small Python exercises to data workflows and neural networks.**

My learning collection brings together Python fundamentals, NumPy exercises, interactive data-analysis scripts, scikit-learn workflows, and TensorFlow CNN experiments. The programs are kept as individual files so their steps are easy to follow.

`Python` · `NumPy` · `pandas` · `scikit-learn` · `TensorFlow` · `Matplotlib`

[Featured work](#featured-work) · [Learning index](#learning-index) · [Run locally](#run-locally) · [Project applications](#project-applications)

## Featured work

| Program | Focus |
| :--- | :--- |
| [AutoML pipeline](automl_pipeline.py) | CSV inspection, missing-value handling, encoding, scaling, and supervised or clustering workflows |
| [Analytics Insights Studio](smart_analytics_insights_studio.py) | Interactive CSV/Excel exploration, summaries, charts, and data export |
| [Financial Data Analysis System](Smart%20Financial%20Data%20Analysis%20System) | Financial dataset exploration, cleaning options, visualizations, and export |
| [Defect-detection CNN](defect_detection_cnn_tensorflow.py) | Image classification with augmentation, checkpointing, and evaluation |
| [Cats vs. dogs CNN](cats_vs_dogs_cnn_tensorflow.py) | Binary image classification with TensorFlow |

## Learning index

| Area | Files |
| :--- | :--- |
| Python fundamentals | [Number guessing](number_guessing_game.py), [password generator exercise](password_generator.py), [file processing](file_data_processor.py), [file search](file_search_utility.py) |
| NumPy & numerical work | [Matrix operations](matrix_operations_numpy.py), [matrix value counter](matrix_value_counter.py), [sensor statistics & alerts](sensor_stats_alerts.py), [simulated machine anomalies](machine_anomaly_detector.py) |
| Data analysis | [Analytics studio](smart_analytics_insights_studio.py), [business data manager](smart-business-data-manager), [financial data analysis](Smart%20Financial%20Data%20Analysis%20System) |
| Machine learning | [AutoML pipeline](automl_pipeline.py), [earlier pipeline exercise](auto-ml-pipeline), [income prediction neural network](income-prediction-nn) |
| Computer vision | [MNIST CNN](MNIST), [cats vs. dogs](cats_vs_dogs_cnn_tensorflow.py), [defect detection](defect_detection_cnn_tensorflow.py) |

Some original Python files have no `.py` extension. They can still be opened as text or passed directly to the Python interpreter.

## Run locally

Open your **existing repository folder** in PowerShell. Create one environment if you do not already have a suitable one:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy
.\.venv\Scripts\python.exe .\matrix_operations_numpy.py
```

This calls the environment's interpreter directly, so PowerShell activation is not required. The matrix exercise asks for 16 numbers.

For the analysis and scikit-learn scripts, add the libraries they use:

```powershell
.\.venv\Scripts\python.exe -m pip install pandas matplotlib seaborn scikit-learn openpyxl
.\.venv\Scripts\python.exe .\smart_analytics_insights_studio.py
```

Provide a CSV or Excel file when prompted. Programs may write cleaned data and charts into their configured output folders.

For CNN experiments, use a Python version supported by the TensorFlow release you install, in a separate environment if needed:

```powershell
python -m pip install tensorflow numpy matplotlib scikit-learn
python .\MNIST
```

`MNIST` loads the dataset through Keras and may download it on first use. The cats/dogs script contains local training and test paths that must be updated. The defect script expects class folders under `dataset/train` and `dataset/test`, then asks for a local prediction image or folder. Image datasets and trained checkpoints are not included in this repository.

## What this work demonstrates

- Inspecting real tabular data before choosing a workflow.
- Working with missing values, numerical operations, charts, and file output.
- Exploring regression, classification, clustering, and neural networks.
- Keeping intermediate steps visible through straightforward scripts and printed results.

## Current scope

These are learning experiments, with script-specific inputs and dependencies rather than one packaged application. Some tabular scripts preprocess data before splitting; their reported metrics should be treated as exploratory until preprocessing is fitted only on training data. CNN results depend on the supplied dataset and split. No benchmark accuracy is claimed here.

Next improvements include configurable dataset paths, separate dependency files for each workflow, and reproducible evaluation examples.

## Project applications

For work with a browser interface, see [Fog Visibility & Vehicle Detection](https://github.com/krishna-ai-cpp/Fog-detection-system), [IBDE](https://github.com/krishna-ai-cpp/IBDE-Intelligent---Business--Decision--Engine-), and [Decision Intelligence Platform](https://github.com/krishna-ai-cpp/Decision-Intelligence-Platform).

---

**Krishna Agrawal** · [C++ & DSA](https://github.com/krishna-ai-cpp/learning-cpp) · [GitHub profile](https://github.com/krishna-ai-cpp)
