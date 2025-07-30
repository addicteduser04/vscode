import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import numpy as np
import joblib
import os

# Configuration
DATA_PATHS = {
    'master': './afriware_julienne.csv',
    'gl': './Book2.csv',  # General Ledger
    'rp': './Book3.csv'   # Receivables/Payables
}
OUTPUT_PATHS = {
    'gl_predictions': 'gl_predictions.csv',
    'rp_predictions': 'rp_predictions.csv',
    'gl_model': 'gl_model.joblib',
    'rp_model': 'rp_model.joblib'
}
EXCLUDED_DOC_TYPES = ['BF', 'KI', 'S1', 'SC', 'SV', 'YG', 'YH', 'ZB']

# Document type encoding
DOC_TYPE_MAPPING = {
    "AD": 100, "BJ": 210, "BO": 220, "GB": 300, "GJ": 310,
    "GQ": 320, "GZ": 330, "OD": 400, "OE": 410, "XD": 500,
    "XE": 510, "YD": 600, "ZD": 700, "ZE": 710
}

def load_and_preprocess_data():
    """Load and preprocess all datasets"""
    # Load data with error handling
    try:
        dfs = {name: pd.read_csv(path, low_memory=False) for name, path in DATA_PATHS.items()}
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Data file not found: {e.filename}")

    # Preprocessing for each dataset
    # Master data
    dfs['master'] = dfs['master'].dropna().copy()
    dfs['master']['TypeFacture'] = dfs['master']['TypeFacture'].map(DOC_TYPE_MAPPING)
    
    # GL data
    dfs['gl'] = dfs['gl'].drop(columns=['GLMCU'], axis=1).dropna()
    dfs['gl'] = dfs['gl'][~dfs['gl']['GLDCT'].isin(EXCLUDED_DOC_TYPES)]
    dfs['gl']['GLDCT'] = dfs['gl']['GLDCT'].map(DOC_TYPE_MAPPING)
    
    # RP data
    dfs['rp'] = dfs['rp'].dropna()
    dfs['rp'] = dfs['rp'][~dfs['rp']['RPDCT'].isin(EXCLUDED_DOC_TYPES)]
    dfs['rp']['RPDCT'] = dfs['rp']['RPDCT'].map(DOC_TYPE_MAPPING)
    
    return dfs

def prepare_training_data(master, auxiliary, master_id_col, auxiliary_id_col):
    """Prepare training data by merging master and auxiliary datasets"""
    # Find common documents
    common_ids = set(master[master_id_col]).intersection(set(auxiliary[auxiliary_id_col]))
    
    # Filter to only include common documents for training
    master_common = master[master[master_id_col].isin(common_ids)]
    auxiliary_common = auxiliary[auxiliary[auxiliary_id_col].isin(common_ids)]
    
    # Merge datasets
    merged = pd.merge(
        master_common, 
        auxiliary_common, 
        left_on=master_id_col, 
        right_on=auxiliary_id_col,
        how='inner'
    )
    
    # Separate features and targets
    X = merged[master.columns.difference([master_id_col])]
    y = merged[auxiliary.columns.difference([auxiliary_id_col])]
    
    return X, y, common_ids

def train_model(X, y, model_name=""):
    """Train a multi-output regression model with proper validation"""
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create pipeline with scaling and model
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', MultiOutputRegressor(
            RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        ))
    ])
    
    # Train model
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Evaluation ({model_name}):")
    print(f"Test MSE: {mse:.4f}")
    print(f"Test R²: {r2:.4f}")
    
    return pipeline

def predict_missing_data(model, master_data, master_id_col, auxiliary_cols, common_ids):
    """Predict missing data for documents not in auxiliary dataset
    Args:
        model: Trained model
        master_data: DataFrame with master documents
        master_id_col: Name of ID column in master data
        auxiliary_cols: List of columns to predict
        common_ids: Set of IDs that exist in both master and auxiliary datasets
    Returns:
        DataFrame with predictions
    """
    missing_data = master_data[~master_data[master_id_col].isin(common_ids)]
    if missing_data.empty:
        print("No missing documents to predict")
        return pd.DataFrame(columns=[master_id_col] + auxiliary_cols)
    
    X_missing = missing_data[master_data.columns.difference([master_id_col])]
    predictions = model.predict(X_missing)
    
    # Create DataFrame with predictions
    predicted_df = pd.DataFrame(predictions, columns=auxiliary_cols)
    predicted_df.insert(0, master_id_col, missing_data[master_id_col].values)
    
    return predicted_df

def plot_feature_importance(model, feature_names, title=""):
    """Plot feature importances from trained model"""
    importances = model.named_steps['model'].estimators_[0].feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(12, 6))
    plt.title(f"Feature Importances {title}")
    plt.bar(range(len(importances)), importances[indices])
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
    plt.tight_layout()
    plt.show()

def save_outputs(df, path):
    """Save DataFrame to CSV with checks"""
    try:
        df.to_csv(path, index=False)
        print(f"Successfully saved to {path}")
    except Exception as e:
        print(f"Error saving {path}: {str(e)}")

def main():
    # Load and preprocess data
    print("Loading and preprocessing data...")
    dfs = load_and_preprocess_data()
    
    # Prepare GL (General Ledger) data
    print("\nPreparing GL training data...")
    X_gl, y_gl, common_gl_ids = prepare_training_data(
        dfs['master'], dfs['gl'], 'NumFacture', 'GLDOC'
    )
    
    # Train GL model
    print("\nTraining GL model...")
    gl_model = train_model(X_gl, y_gl, "GL Model")
    
    # Prepare RP (Receivables/Payables) data
    print("\nPreparing RP training data...")
    X_rp, y_rp, common_rp_ids = prepare_training_data(
        dfs['master'], dfs['rp'], 'NumFacture', 'RPDOC'
    )
    
    # Train RP model
    print("\nTraining RP model...")
    rp_model = train_model(X_rp, y_rp, "RP Model")
    
    # Predict missing GL data
    print("\nPredicting missing GL data...")
    gl_predictions = predict_missing_data(
    gl_model, dfs['master'], 'NumFacture', y_gl.columns, common_gl_ids
    )
    
    # Predict missing RP data
    print("\nPredicting missing RP data...")
    rp_predictions = predict_missing_data(
    rp_model, dfs['master'], 'NumFacture', y_rp.columns, common_rp_ids
)
    # Combine original data with predictions
    final_gl = pd.concat([dfs['gl'], gl_predictions], ignore_index=True)
    final_rp = pd.concat([dfs['rp'], rp_predictions], ignore_index=True)
    
    # Visualize feature importance
    plot_feature_importance(gl_model, X_gl.columns, "for GL Model")
    plot_feature_importance(rp_model, X_rp.columns, "for RP Model")
    
    # Save outputs
    print("\nSaving outputs...")
    save_outputs(final_gl, OUTPUT_PATHS['gl_predictions'])
    save_outputs(final_rp, OUTPUT_PATHS['rp_predictions'])
    
    # Save models
    joblib.dump(gl_model, OUTPUT_PATHS['gl_model'])
    joblib.dump(rp_model, OUTPUT_PATHS['rp_model'])
    
    print("\nPipeline completed successfully!")

if __name__ == "__main__":
    main()