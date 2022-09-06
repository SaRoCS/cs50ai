import calendar
import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer 0
        - Administrative_Duration, a floating point number 1
        - Informational, an integer 2
        - Informational_Duration, a floating point number 3
        - ProductRelated, an integer 4
        - ProductRelated_Duration, a floating point number 5
        - BounceRates, a floating point number 6
        - ExitRates, a floating point number 7
        - PageValues, a floating point number 8
        - SpecialDay, a floating point number 9
        - Month, an index from 0 (January) to 11 (December) 10
        - OperatingSystems, an integer 11
        - Browser, an integer 12
        - Region, an integer 13
        - TrafficType, an integer 14
        - VisitorType, an integer 0 (not returning) or 1 (returning) 15
        - Weekend, an integer 0 (if false) or 1 (if true) 16

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.DictReader(f)
        labels = []
        evidence = []
        # get month abbreviations and change "Jun" to "June"
        months = list(calendar.month_abbr)
        months.remove("")
        months[5] = "June"

        for row in reader:
            # add int representing the label
            if row["Revenue"] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)

            # create a list of values
            e = []
            for key, value in row.items():
                if key != "Revenue":
                    e.append(value)

            # convert values to the required types
            for count, value in enumerate(e):
                if count in [0, 2, 4, 11, 12, 13, 14]:
                    e[count] = int(value)
                elif count in [1, 3, 5, 6, 7, 8, 9]:
                    e[count] = float(value)
                elif count == 10:
                    e[count] = months.index(value)
                elif count in [15, 16]:
                    if value in ("Returning_Visitor", "TRUE"):
                        e[count] = 1
                    else:
                        e[count] = 0
            evidence.append(e)

        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positives = 0
    pos_id = 0
    negatives = 0
    neg_id = 0
    for lab, pred in zip(labels, predictions):
        if lab == pred and lab == 1:
            pos_id += 1
            positives += 1
        elif lab == pred and lab == 0:
            neg_id += 1
            negatives += 1
        elif lab == 1:
            positives += 1
        elif lab == 0:
            negatives += 1
    sensitivity = pos_id / positives
    specificity = neg_id / negatives
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
