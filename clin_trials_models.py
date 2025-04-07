import pandas as pd 
import numpy as np
from sklearn.feature_extracion.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
from sklearn.metrics import recall_score, make_scorer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# this file informs my decision-making around which model to use to fill out
# the 'Relevance' column for data sourced from clinicaltrials.gov
# 
# the metric to evaluate performance is recall, because we want this 'Relevance'
# filter to be relatively 'easy' to get through, so clinicians do not miss out on
# opportunities
#
# I also perform k-fold cross validation on each model archetype so that one bad
# run does not rule that archetype out 

# create and test logistic regression models
def logistic_reg(X, Y):
    model = LogisticRegression(max_iter=1000)
    scoring = make_scorer(recall_score)
    kfold = StratifiedKFold(n_splits=5)
    results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    print("Logistic Regression Recall: %.2f.%%" % (results.mean() *100))

# create 'standard-shaped' neural network
class neural_net(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(neural_net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

# create and test neural network for our data
def neural_network(X, Y):
    # hyperparameters
    hidden_size = 20
    epochs = 10
    batch_size = 8
    # format datasets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=315)
    X_train_tensor = torch.tensor(X_train.toarray(), dtype=torch.float32)
    Y_train_tensor =  torch.tensor(Y_train.values, dtype=torch.float32).unsqueeze(1)
    X_test_tensor = torch.tensor(X_test.toarray(), dtype=torch.float32)
    Y_test_tensor = torch.tensor(Y_test.values, dtype=torch.float32).unsqueeze(1)
    # initialize model
    model = neural_net(X_train.shape[1], hidden_size, Y_train.shape[1])
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    # train model
    for epoch in range(epochs):
        model.train()
        for i in range(0, X_train.shape[0], batch_size):
            x_batch = X_train_tensor[i:i+batch_size]
            y_batch = Y_train_tensor[i:i+batch_size]
            optimizer.zero_grad()
            predictions = model(x_batch)
            loss = criterion(predictions, y_batch)
            loss.backward()
            optimizer.step()
        print("Epoch ", {epoch+1}, "/", epochs, " | Loss: ", {loss.item()})

    # evaluate model
    model.eval()
    with torch.no_grad():
        test_predictions = model(X_test_tensor)
        test_loss = criterion(test_predictions, Y_test_tensor)
        accuracy = ((test_predictions > 0.5) == Y_test_tensor).float().mean()
        print("Test Loss: ", test_loss.item():.4f, " | Test Accuracy: ", accuracy.item():.4f)
        
    print("Neural Network Recall: %.2f.%%" % (results.mean() * 100))

# create and test random forest for our data
def random_forest(X, Y):
    model = RandomForestClassifier(n_estimators=100)
    scoring = make_scorer(recall_score)
    kfold = StratifiedKFold(n_splits=5)
    results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    print("Random Forest Recall: %.2f.%%" % (results.mean() * 100))

# I manually labeled relevance for 725 trials to create training data
clin_df = pd.read_csv("C:\\Users\\Student\\Downloads\\OUTPUT.csv").loc[:725]
features = ["Award Name", "Organization", "Brief Description"]
X = clin_df[features]
Y = clin_df["Availability"].map(lambda x: 1 if x == "Y" else 0)
tv = TfidfVectorizer()
X_combined = X.apply(lambda row: ' '.join(row), axis=1)
X_tfidf = tv.fit_transform(X_combined)
# testing 
logistic_reg(X_tfidf, Y)
neural_network(X_tfidf, Y)
random_forest(X_tfidf, Y)
