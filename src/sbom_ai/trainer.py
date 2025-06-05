from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import joblib

def train_random_forest(X_train, y_train, params: dict):
    rf = RandomForestClassifier(**params)
    rf.fit(X_train, y_train)
    return rf

def train_lightgbm(X_train, y_train, params: dict):
    lgbm = LGBMClassifier(**params)
    lgbm.fit(X_train, y_train)
    return lgbm

def train_catboost(X_train, y_train, params: dict):
    cb = CatBoostClassifier(**params)
    cb.fit(X_train, y_train)
    return cb

def save_models(rf, lgbm, cb, output_dir: str):
    joblib.dump(rf, f"{output_dir}/random_forest.pkl")
    lgbm.booster_.save_model(f"{output_dir}/lightgbm_model.txt")
    cb.save_model(f"{output_dir}/catboost_model.cbm")
