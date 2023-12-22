import argparse
import logging
import os

import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from sklearn.calibration import LabelEncoder
from sklearn.model_selection import train_test_split

logging.getLogger().setLevel(logging.INFO)


# Data preparation
def preparation(dataset_path: str) -> pd.DataFrame:
    data_frame = pd.read_csv(dataset_path)
    columns_to_drop = [
        "full_name",
        "birth_date",
        "nationality",
        "value_euro",
        "wage_euro",
        "preferred_foot",
        "release_clause_euro",
        "national_team",
        "national_rating",
        "national_team_position",
        "national_jersey_number",
    ]

    data_frame = data_frame.drop(columns=columns_to_drop)
    le = LabelEncoder()
    data_frame["positions"] = le.fit_transform(data_frame["positions"])
    data_frame["body_type"] = le.fit_transform(data_frame["body_type"])
    return data_frame


def model_creation_and_training(data_frame: pd.DataFrame):
    target = "overall_rating"
    # Split the data into features (X) and target (y)
    X = data_frame.drop([target, "name"], axis=1)
    y = data_frame[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the model architecture
    model = Sequential()
    model.add(Dense(512, input_dim=X_train.shape[1], activation="relu"))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(1, activation="linear"))

    model.compile(loss="mean_squared_error", optimizer="adam")

    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)

    loss = model.evaluate(X_test, y_test, verbose=1)
    print("Test Loss: ", loss)
    return model, X_test, y_test, X_train, y_train


def predict(
    model_output_path: str,
    data_frame,
    model: Sequential,
    X_test,
    y_test,
    X_train,
    y_train,
):
    y_pred = model.predict(X_test)

    # Print the first 10 predicted and actual values
    for i in range(10):
        print(f"Predicted: {y_pred[i]}, Actual: {y_test.iloc[i]}")

    # Calculate the residuals for the test set
    residuals_test = np.abs(y_test - y_pred.reshape(-1))

    # Get the indices of the top 10 most off predictions in the test set
    top10_test_indices = residuals_test.argsort()[-10:]

    """ Print the top 10 most off predictions
    in the test set and their corresponding names
    """
    logging.info("Top 10 most off predictions in the test set:")
    for i in top10_test_indices:
        logging.info(
            f"""
            "Name: {data_frame.loc[X_test.index[i], 'name']},
            Predicted: {y_pred[i]},
            Actual: {y_test.iloc[i]}"
            """
        )

    """
        Calculate the residuals for the training set
    """
    y_pred_train = model.predict(X_train)
    residuals_train = np.abs(y_train - y_pred_train.reshape(-1))

    """
        Get the indices of the top 10 most off predictions in the training set
    """
    top10_train_indices = residuals_train.argsort()[-10:]

    """
        Print the top 10 most off predictions in the training
        set and their corresponding names
    """
    logging.info("Top 10 most off predictions in the training set:")
    for i in top10_train_indices:
        logging.info(
            f"""
            "Name: {data_frame.loc[X_train.index[i], 'name']},
            Predicted: {y_pred_train[i]},
            Actual: {y_train.iloc[i]}"
            """
        )

    # Save the model

    model.save(filepath=model_output_path, save_format="tf")


def train(dataset_path: str, model_output_path: str):
    logging.info(f"getting the Dataset... => {dataset_path}")
    data_frame = preparation(dataset_path=dataset_path)
    logging.info("Dataset prepared successfully")
    model, X_test, y_test, X_train, y_train = model_creation_and_training(data_frame=data_frame)
    logging.info("Model created and trained successfully")
    predict(model_output_path, data_frame, model, X_test, y_test, X_train, y_train)
    logging.info("Model predicted successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dp", "--dataset-path", type=str, default="./dataset/fifa_players.csv", required=False)
    parser.add_argument("-mv", "--model-version", type=str, default="v1.0.0", required=False)
    parser.add_argument("-mbp", "--model-base-path", type=str, default="model/", required=False)
    args = parser.parse_args()
    model_version = args.model_version
    model_name = "fifa-predictior"
    model_base_path = args.model_base_path
    model_output_path = os.path.join(model_base_path, model_name)
    model_output_file = os.path.join(model_output_path, model_version)
    if not os.path.exists(model_output_path):
        os.makedirs(model_output_path)
    train(args.dataset_path, model_output_file)
