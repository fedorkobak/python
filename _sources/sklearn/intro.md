# Intro

Is a library that implements many tools for machine learning and advanced data analysis.

## Data transform

The Sklearn provides a set of tools for data processing. The following table lists some of these classes.

| Area of Preprocessing | Class Name | Description |
| :--- | :--- | :--- |
| **Scaling & Standardization** | `StandardScaler` | Standardizes features by removing the mean and scaling to unit variance ($z$-score). |
| | `MinMaxScaler` | Scales features to a given range, typically $[0, 1]$. |
| | `MaxAbsScaler` | Scales each feature by its maximum absolute value, typically to the range $[-1, 1]$. Useful for sparse data. |
| | `RobustScaler` | Scales features using statistics that are robust to outliers (e.g., median and interquartile range). |
| **Normalization** | `Normalizer` | Normalizes samples individually to have unit norm (e.g., $l_1$ or $l_2$ norm). |
| **Missing Values Imputation** | `SimpleImputer` | Imputes missing values using a simple strategy (e.g., mean, median, most frequent, or a constant value). |
| | `KNNImputer` | Imputes missing values using the K-Nearest Neighbors approach. |
| | `IterativeImputer` | Imputes missing values by modeling each feature with missing values as a function of other features and using that estimate for imputation. |
| **Categorical Encoding** | `OneHotEncoder` | Encodes categorical features as a one-hot or dummy feature matrix. |
| | `OrdinalEncoder` | Encodes categorical features into ordinal integers. |
| **Feature Transformation** | `PolynomialFeatures` | Generates polynomial and interaction features (e.g., $x_1^2, x_1 x_2, x_2^2$). |
| | `FunctionTransformer` | Allows creating a transformer from an arbitrary function. |
| | `QuantileTransformer` | Transforms features using quantiles, forcing the data to follow a uniform or normal distribution. |
| | `PowerTransformer` | Applies power transforms (e.g., Yeo-Johnson or Box-Cox) to make data more Gaussian-like. |
| **Discretization / Binning** | `KBinsDiscretizer` | Bins continuous data into $k$ discrete intervals. |
| **Pipeline/Composition** | `Pipeline` | Sequentially applies a list of transformers and a final estimator. |
| | `ColumnTransformer` | Applies different transformers to different subsets of features. |

For more details, check the [Data Transform](data_transform.ipynb) page.
