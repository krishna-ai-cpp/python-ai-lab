import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
import os
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, mean_absolute_error, mean_squared_error, r2_score
)

# ── File Load ─────────────────────────────────────────────────
try:
    f = input("enter your file path: ").strip().strip('"').strip("'")
except ValueError as e:
    print(e)

if not os.path.exists(f):
    print("invalid file ......")
    exit()
else:
    df = pd.read_csv(f)

# ── Exploring Dataset ─────────────────────────────────────────
print(f"Displaying overview of the uploaded Dataset: \n{df.head(6)}")
print()
print(f"Number of columns: {df.shape[1]}")
print()
print(f"Number of rows: {df.shape[0]}")
print()
print(f"Missing values: \n{df.isnull().sum()}")
print()
print(f"Duplicates found: \n{df.duplicated().sum()}")
print()
print(f"Data types: \n{df.dtypes}")
print()
print(f"Memory usage: {df.memory_usage(deep=True).sum()}")
for col in df.select_dtypes(include=["object", "category"]).columns:
    unique = df[col].nunique()
    ratio = unique/len(df)
    if ratio > 0.5:
        print(col,"High Cardinality....")
    else:
        print(col,"Low cardinality.....")
for col in df.columns:
    types = df[col].apply(type).unique()
    if len(types)>1:
        print(col,"Mixed Datatype")
# Phase 3 — Automatic Preprocessing
nc = df.select_dtypes(include="number").columns.to_list()
cc = df.select_dtypes(include=["object", "category"]).columns.to_list()
if df.duplicated().sum() > 0:
    df.drop_duplicates(inplace=True)
else:
    print("No duplicates found.....")
s = SimpleImputer(strategy="median")
df[nc] = s.fit_transform(df[nc])
print("Handled numerical missing values....")

if cc:
    s = SimpleImputer(strategy="most_frequent")
    df[cc] = s.fit_transform(df[cc])
    print("Handled categorical missing values....")

df = pd.get_dummies(df,columns= cc , dtype= int)
print("Categorical columns encoded.....")

sc = StandardScaler()
df[nc] = sc.fit_transform(df[nc])

q1  = df[nc].quantile(0.25)
q3  = df[nc].quantile(0.75)
iqr = q3 - q1
ul  = q3 + (1.5 * iqr)
ll  = q1 - (1.5 * iqr)
print(f"Upper limit:\n{ul}")
print()
print(f"Lower limit:\n{ll}")
print()
o = df[((df[nc] < ll) | (df[nc] > ul)).any(axis=1)]
if len(o) > 0:
    print(f"Outlier found:\n{o}")
    print()
    # FIX 1: actually drop the outliers instead of just showing them
    df = df[~((df[nc] < ll) | (df[nc] > ul)).any(axis=1)]
    print(f"Outliers removed.... rows remaining: {len(df)}")
    print()
else:
    print("NO outliers......")
try:
    target = input("enter the target coumn: ")
except ValueError as e:
    print(e)


if target in df.columns:
    x = df.drop(columns= target)
    y = df[target]
    if df[target].nunique() <= 10 or pd.api.types.is_object_dtype(df[target]) or isinstance(df[target].dtype, pd.CategoricalDtype):
        le = LabelEncoder()
        y = pd.Series(le.fit_transform(y), index=y.index)
    pca = PCA(n_components=0.95)
    X_pca = pca.fit_transform(x)
    
    x_train , x_test, y_train, y_test = train_test_split(X_pca,y,test_size=0.2,random_state=42)
    
    if (pd.api.types.is_integer_dtype(df[target]) or pd.api.types.is_float_dtype(df[target])) and df[target].nunique() > 10:
        l = LinearRegression()
        
        l.fit(x_train, y_train)
        lr_pred = l.predict(x_test)
        user = {}
        for col in nc:
            if col == target:
                continue
            val = input(f"Enter {col}: ")
            user[col] = float(val)
        for col in cc:
            if col == target:
                continue
            val = input(f"Enter {col}: ")
            user[col] = val
        input_df = pd.DataFrame([user])
        input_df = pd.get_dummies(input_df, columns=cc, dtype=int)
        input_df = input_df.reindex(columns=x.columns, fill_value=0)
        for col in nc:
            if col == target:
                continue
            i = nc.index(col)
            input_df[col] = (input_df[col].astype(float) - sc.mean_[i]) / sc.scale_[i]
        input_pca = pca.transform(input_df)
        lr_input_pred = l.predict(input_pca)
        # FIX 2a: show the predicted number clearly instead of raw array
        print(f"Predicted {target} : {round(float(lr_input_pred[0]), 2)}")
    elif pd.api.types.is_bool_dtype(df[target]) or pd.api.types.is_object_dtype(df[target]) or isinstance(df[target].dtype, pd.CategoricalDtype) or df[target].nunique() <= 10:

        l1 = LogisticRegression()
        
        l2 = DecisionTreeClassifier(random_state=42)
       
        l1.fit(x_train, y_train)
        l2.fit(x_train, y_train)
        lg_pred = l1.predict(x_test)
        dc_pred = l2.predict(x_test)
        user = {}
        for col in nc:
            if col == target:
                continue
            val = input(f"Enter {col}: ")
            user[col] = float(val)
        for col in cc:
            if col == target:
                continue
            val = input(f"Enter {col}: ")
            user[col] = val
        input_df = pd.DataFrame([user])
        input_df = pd.get_dummies(input_df, columns=cc, dtype=int)
        input_df = input_df.reindex(columns=x.columns, fill_value=0)
        for col in nc:
            if col == target:
                continue
            i = nc.index(col)
            input_df[col] = (input_df[col].astype(float) - sc.mean_[i]) / sc.scale_[i]
        input_pca = pca.transform(input_df)

        lg_input_pred = l1.predict(input_pca)
        dc_input_pred = l2.predict(input_pca)
        # FIX 2b: decode the label back to the original class name and show clearly
        lg_label = le.inverse_transform(lg_input_pred)[0]
        dc_label = le.inverse_transform(dc_input_pred)[0]
        print(f"Logistic Regression predicted {target} : {lg_label}")
        print(f"Decision Tree predicted {target} : {dc_label}")
    if (pd.api.types.is_integer_dtype(df[target]) or pd.api.types.is_float_dtype(df[target])) and df[target].nunique() > 10:
        
        mdf = pd.DataFrame({"Target:" : y_test, "Prediction" : lr_pred})
        print()
        
        mae = mean_absolute_error(y_test, lr_pred)
        mse = mean_squared_error(y_test, lr_pred)
        r2  = r2_score(y_test, lr_pred)
        print("___________THE MODEL OVERVIEW_______")
        print(f"MAE: {mae}")
        print(f"MSE: {mse}")
        print(f"R2 Score: {r2}")
        print()
        print(mdf)
    else:
        mdf = pd.DataFrame({"Target:" : y_test, "Prediction" : lg_pred})
        print()
       
        f1 = f1_score(y_test,lg_pred, average='weighted')
        if f1 >= 0.2 and f1 <= 1:
            print("GREAT !! MODEL IS WORKING WELL ")
        elif f1 >= 0 and f1 <= 0.1:
            print("MODEL NEEDS MORE TRAINING....")
        else:
            print("MODEL IS WORKING WORST THAN EVER...")
        print()
        print("___________THE MODEL OVERVIEW_______")
        acc = accuracy_score(y_test,lg_pred)
        p = precision_score(y_test,lg_pred, average='weighted')
        re = recall_score(y_test,lg_pred, average='weighted')
        print(f"Accuracy: : {acc}")
        print(f"Precision: {p}")
        print(f"Recall: {re}")
        print(f"F1 score: {f1}")
        print()
        print(mdf)

        mdf = pd.DataFrame({"Target:" : y_test, "Prediction" : dc_pred})
        print()
        f2 = f1_score(y_test,dc_pred, average='weighted')
        if f2 >= 0.2 and f2 <= 1:
            print("GREAT !! MODEL IS WORKING WELL ")
        elif f2 >= 0 and f2 <= 0.1:
            print("MODEL NEEDS MORE TRAINING....")
        else:
            print("MODEL IS WORKING WORST THAN EVER...")
        print()
        print("___________THE MODEL OVERVIEW_______")
        acc = accuracy_score(y_test,dc_pred)
        p = precision_score(y_test,dc_pred, average='weighted')
        re = recall_score(y_test,dc_pred, average='weighted')
        print(f"Accuracy: : {acc}")
        print(f"Precision: {p}")
        print(f"Recall: {re}")
        print(f"F1 score: {f2}")
        print()
        print(mdf)
else:
    X = df
   
    pca = PCA(n_components=0.95)
    X_pca = pca.fit_transform(X)
    print("Original Features :",X.shape[1])
    print("Reduced Features :",X_pca.shape[1])
    print("Variance :",sum(pca.explained_variance_ratio_))
    variance = np.cumsum(pca.explained_variance_ratio_)
    
    plt.plot(variance)
    
    os.makedirs("reports", exist_ok=True)
    
    plt.savefig("reports/pca_variance.png")
    plt.show()
    plt.close()
    wcss = []
    for k in range(1,11):
        model = KMeans(n_clusters=k, random_state=42)
        model.fit(X_pca)
        wcss.append(model.inertia_)
    plt.figure(figsize=(10,7))
    
    plt.plot(range(1,11),wcss,marker= "o")
    plt.xlabel("CLUSTERS (K)")
    plt.ylabel("WCSS (INERTIA)")
    plt.title("ELBOW GRAPH FOR BEST K")
    plt.grid(True)
    try:
        
        bestk = int(input("enter the best k shown in the graph: "))
    except ValueError:
        print("INVALID K....")
    model = KMeans(n_clusters= bestk, random_state=42, n_init=10)
    model.fit(X_pca)
    pred = model.predict(X_pca)
    user = {}
    for col in nc:
        val = input(f"Enter {col}: ")
        user[col] = float(val)
    for col in cc:
        val = input(f"Enter {col}: ")
        user[col] = val
    input_df = pd.DataFrame([user])
    input_df = pd.get_dummies(input_df, columns=cc, dtype=int)
    input_df = input_df.reindex(columns=X.columns, fill_value=0)
    for col in nc:
        i = nc.index(col)
        input_df[col] = (input_df[col].astype(float) - sc.mean_[i]) / sc.scale_[i]
    input_pca = pca.transform(input_df)
    pred_input = model.predict(input_pca)
    # FIX 3: show which cluster clearly and what range of clusters exist
    print(f"Based on your input, you belong to Cluster {pred_input[0]} (clusters range from 0 to {bestk - 1})")
    
    mdf = pd.DataFrame({"Cluster" : pred})
   
    if bestk >= 2:
        ss = silhouette_score(X_pca,pred)
        print(f"Silhouette Score: {ss}")
    else:
        print("Silhouette Score requires at least 2 clusters.....")
    print()
    print(mdf)
