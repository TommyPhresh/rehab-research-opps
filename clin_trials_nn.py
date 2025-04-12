import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


MAX_LEN = 100

def preprocessing():
    df = pd.read_csv("C:\\Users\\Student\\Downloads\\OUTPUT.csv")
    df.fillna("", inplace=True)
    # only clinical trials data I've labeled will be used for training
    df = df[df["Funding Mechanism"] == "Clinical Trial"]
    df = df[df["Availability"] != ""]
    # prepare text columns for analysis
    # Process: merge cols, tokenize, create vocabulary,
    # map words to sequence, create padded sequences
    X = df["Award Name"] + "\n" + df["Organization"] + "\n" + df["Brief Description"]
    X = X.str.lower().str.strip().apply(lambda text: text.split())
    vocab = {}
    for tokens in X:
        for token in tokens:
            if token not in vocab:
                vocab[token] = len(vocab) + 1
    X = X.apply(lambda tokens: [vocab[token] for token in tokens])
    X = X.apply(lambda seq: seq[:MAX_LEN] if len(seq) >= MAX_LEN else seq + [0]*(MAX_LEN-len(seq)))
    X = np.array(X.tolist())
    Y = df["Availability"].str.strip()
    Y = Y.map(lambda x: 1 if x == "Y" else 0)
    return X, Y, vocab

def get_inputs(X, Y, batch_size=32, num_workers):
    # split between training and testing datasets, then convert to input format
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y)
    X_train_tensor = torch.tensor(X_train, dtype=torch.long)
    Y_train_tensor = torch.tensor(Y_train, dtype=torch.long)
    X_test_tensor = torch.tensor(X_test, dtype=torch.long)
    Y_test_tensor = torch.tensor(Y_test.values, dtype=torch.long)
    train_dataset = TensorDataset(X_train_tensor, Y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size,
                              shuffle=True, num_workers=num_workers)

    return train_loader, X_test_tensor, Y_test_tensor

# implementation choice is a convolutional neural network
# below is network architecture definitions
class convolutional_nn(nn.Module):
    def __init__(self, vocab_size, embedded_dim,
                 num_classes, kernel_sizes=(3,4,5),
                 num_filters=100, dropout=0.5):
        super(convolutional_nn, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedded_dim)
        # create num_filters 'kernels' or 'windows' to pass over input
        self.convs = nn.ModuleList([
            nn.Conv2d(in_channels=1, out_channels=num_filters,
                      kernel_size=(k, embedded_dim))
            for k in kernel_sizes
            ])
        # prevent overfitting 
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(num_filters * len(kernel_sizes), num_classes)

    def forward(self, x):
        # create embedding for sample text input 
        embedded = self.embedding(x).unsqueeze(1)
        conv_results = []
        # pass kernel over embedding 
        for convolution in self.convs:
            output = F.relu(convolution(embedded))
            output = output.squeeze(3)
            max_pooled = F.max_pool1d(output, output.size(2))
            conv_results.append(max_pooled)

        # use dropout to prevent overfitting
        features = torch.cat(conv_results, dim=1)
        features = self.dropout(features)
        # output logits for each class (False (0) or True (1))
        logits = self.linear(features)
        return logits

# create clinical trials model
def create_model(vocab):
    vocab_size = len(vocab) + 1
    embedded_dim = MAX_LEN
    num_classes = 2
    return convolutional_nn(vocab_size, embedded_dim, num_classes)

# train clinical trials model
def train_model(model, lr=1e-3, max_epochs=24, patience=1):
    # set model hyperparameters
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    # initialize variables to facilitate short-circuiting 
    best_loss = float('inf')
    patience_counter = 0
    model.train()
    for epoch in range(max_epochs):
        running_loss = 0.0
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            # obtain logits for both classes (False or True)
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * batch_x.size(0)
        # determine whether to short-circuit
        epoch_loss = running_loss / len(train_dataset)
        if epoch_loss < best_loss:
            # continue to improve
            best_loss = epoch_loss
            torch.save(model.state_dict(),
                       "C:\\Users\\Student\\Documents\\Projects\\rehab-research-opps\\trials_model_weights.pth")
            patience_counter = 0
        else: patience_counter += 1
        # short-circuit
        if patience_counter >= patience: break
        print("Epoch ", epoch+1, " of a possible ", max_epochs, ", Loss: ", epoch_loss)
    # load and return lowest-loss version of model 
    model.load_state_dict(torch.load("C:\\Users\\Student\\Documents\\Projects\\rehab-research-opps\\trials_model_weights.pth"))
    return model

# evaluate model performance to adjust hyperparameters and/or architecture
def evaluate_model(model, X_test_tensor, Y_test_tensor, threshold=0.5):
    model.eval()
    with torch.no_grad():
        logits_test = model(X_test_tensor)
        # convert to probability input falls into each class 
        probs_test = torch.softmax(logits_test, dim=1).cpu().numpy()
        # extract only the probability the input is True 
        probs_test = probs_test[:, 1]

    Y_pred = (probs_test >= threshold).astype(int)
    Y_true = Y_test_tensor.cpu().numpy().astype(int)

    cm = confusion_matrix(Y_true, Y_pred)
    cm_defs = {
        "TN": cm[0][0],
        "FP": cm[0][1],
        "FN": cm[1][0],
        "TP": cm[1][1]
        }
    # model metrics 
    precision = cm_defs["TP"] / (cm_defs["TP"] + cm_defs["FP"])
    recall = cm_desf["TP"] / (cm_defs["TP"] + cm_defs["FN"])
    accuracy = (cm_defs["TP"] + cm_defs["TN"]) / (cm[0][0] + cm[0][1] + cm[1][0] + cm[1][1])
    fpr = cm_defs["FP"] / (cm_defs["FP"] + cm_defs["TN"])
    f1 = 2 * ((precision * recall) / (precision + recall))
    specificity = cm_defs["TN"] / (cm_defs["TN"] + cm_defs["FP"])
    return {
        "precision": precision, "recall": recall, "accuracy": accuracy,
        "fpr": fpr, "f1": f1, "specificity": specificity
        }

# takes user through workflow (only needed to be run once to generate model weights)
def build_model()
    X, Y, vocab = preprocessing()
    train_loader, X_test_tensor, Y_test_tensor = get_inputs(X, Y, num_workers=4)
    model = create_model(vocab)
    trained_model = train_model(model)
    # threshold for final model ended up being 0.4
    evaluate_model(
        trained_model, X_test_tensor, Y_test_tensor, threshold=0.4
        )
    return trained_model
    
    
