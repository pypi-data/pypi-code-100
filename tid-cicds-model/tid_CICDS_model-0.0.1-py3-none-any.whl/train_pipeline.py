from config.core import config
from pipeline import pipe
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )
    X_train["Date_first_seen"] = X_train.Date_first_seen.astype("datetime64[ms]")
    X_test["Date_first_seen"] = X_test.Date_first_seen.astype("datetime64[ms]")
    y_train = y_train.str.replace("---", "normal")
    y_test = y_test.str.replace("---", "normal")
    le = LabelEncoder()
    le.fit(y_train)
    y_train = le.transform(y_train)
    y_test = le.transform(y_test)
    # fit model
    pipe.fit(X_train, y_train)

    # persist trained model
    save_pipeline(pipeline_to_persist=pipe)


if __name__ == "__main__":
    run_training()
