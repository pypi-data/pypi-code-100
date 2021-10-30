import wandb
import argparse
import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier


logging.disable(logging.WARNING)

my_parser = argparse.ArgumentParser(description='Runs a W&B sweep (hyperparameter search) on the nationality dataset using different sklearn models.')
my_parser.add_argument('--data_path',
                       type=str,
                       required=True,
                       help='path to the cleaned dataset to load.')
args = my_parser.parse_args()


def train_clf(clf):
    run = wandb.init(project="vm01-nationality-detection-sklearn", entity='fabiangroeger', reinit=True)
    print('_' * 80)
    print("Training: ")
    print(clf)

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)
    y_pred_proba = clf.predict_proba(X_val)
    acc_val = metrics.accuracy_score(y_val, y_pred)
    f1_val = metrics.f1_score(y_val, y_pred, average='binary', pos_label='T')
    print("accuracy val:   %0.3f" % acc_val)
    print("f1 score val:   %0.3f" % f1_val)

    print("classification report:")
    print(metrics.classification_report(y_val, y_pred, target_names=target_names))
    print("confusion matrix:")
    print(metrics.confusion_matrix(y_val, y_pred))
    clf_descr = str(clf).split('(')[0]

    # log the classifier in W&B
    wandb.sklearn.plot_classifier(clf, X_train, X_val, y_train, y_val, y_pred, y_pred_proba, target_names,
                                                         model_name=clf_descr, feature_names=None)
    wandb.log({'accuracy val': acc_val,
               'f1 val': f1_val,
               'classifier name': clf_descr})
    run.save()
    run.finish()


if __name__ == '__main__':
    """
    Problems with this approach:
    - doesn't use the context of the sentence, looks at the words one by one
    - OOV gets completely ignored during inference time, the model will thus not be able to generalize to new words
    """
    # Load data from the training set
    df = pd.read_csv(args.data_path, index_col=0)
    df = df[df['prediction'] != 'X']
    target_names = list(df.prediction.unique())
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    df_train, df_val = train_test_split(df, test_size=0.15, random_state=42)
    X_train, y_train = df_train.text, df_train.prediction
    X_val, y_val = df_val.text, df_val.prediction
    X_test, y_test = df_test.text, df_test.prediction

    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=1.0)
    X_train = vectorizer.fit_transform(X_train)
    X_val = vectorizer.transform(X_val)
    X_test = vectorizer.transform(X_test)
    print("TRAIN: n_samples: %d, n_features: %d" % X_train.shape)
    print("VAL: n_samples: %d, n_features: %d" % X_val.shape)
    print("TEST: n_samples: %d, n_features: %d" % X_test.shape)
    # mapping from integer feature name to original token string
    feature_names = vectorizer.get_feature_names()

    classifiers = [KNeighborsClassifier(3),
                   SVC(gamma=2, C=1, probability=True),
                   DecisionTreeClassifier(max_depth=5),
                   RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
                   MLPClassifier(alpha=1, max_iter=1000),
                   AdaBoostClassifier()]

    results = []
    for clf in classifiers:
        print('=' * 80)
        print(str(clf).split('(')[0])
        train_clf(clf)
