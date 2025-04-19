import duckdb, torch, transformers
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# model is too large to be saved to disk - follow link

# TO BE RUN - helper function to format for BERT input
def encode_features(sample, tokenizer, max_length=512):
    encoded_dict = tokenizer.encode_plus(
        row["Award_Name"] +
        row["Organization"] +
        row["Funding_Mechanism"] +
        row["Brief_Description"],
        add_special_tokens=True,
        max_length=max_length,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt'
        )
    return (
        encoded_dict["input_ids"],
        encoded_dict["attention_mask"],
        encoded_dict["token_type_ids"]
        )

# TO BE RUN - ingest data 
def ingest_tables(data_path):
    conn = duckdb.connect()
    conn.execute("""
    CREATE TABLE input
    AS SELECT *
    FROM read_csv({data_path}, header=True)
    """)
    X = conn.execute("""
    SELECT Award_Name, Organization, Funding_Mechanism, Brief_Description
    FROM input
    """).fetchdf()
    Y = conn.execute("""
    SELECT Availability
    FROM input
    """).inputdf()
    Y = Y["Availability"].map(lambda x: 1 if x == "Y" else 0)
    return X, Y

# TO BE RUN - convert from df to BERT tensor format
def format_tables(X, Y, tokenizer):
    (X["input_ids"], X["attention_mask"], X["token_type_ids"]) = zip(*X.apply(encode_features(tokenizer), axis=1))
    X = X[["input_ids", "attention_mask", "token_type_ids"]]
    X["input_ids"] = torch.cat(X["input_ids"].tolist())
    X["attention_mask"] = torch.cat(X["attention_mask"].tolist())
    X["token_type_ids"] = torch.cat(X["token_type_ids"].tolist())
    Y = torch.tensor(Y.tolist())
    return X, Y

# NOT TO BE RUN - code that created model
# original model creation
def create_model(learning_rate=2e-5):
    tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased')
    model = transformers.BertForSequenceClassification.from_pretrained('bert-base-uncased')
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    return tokenizer, model, optimizer

# NOT TO BE RUN - code that created model
# train test split dataset creation
def create_datasets(X, Y, test_size=0.2, batch_size=16):
    X_train, X_test, Y_train,Y_test = train_test_split(X, Y, test_size=test_size,
                                                       stratify=Y)
    train_input_ids = X_train["input_ids"]
    train_attention_mask = X_train["attention_mask"]
    train_token_type_ids = X_train["token_type_ids"]
    test_input_ids = X_test["input_ids"]
    test_attention_mask = X_test["attention_mask"]
    test_token_type_ids = X_test["token_type_ids"]

    train_dataset = torch.utils.data.TensorDataset(train_input_ids, train_attention_mask,
                                                   train_token_type_ids, Y_train)
    test_dataset = torch.utils.data.TensorDataset(test_input_ids, test_attention_mask,
                                                  test_token_type_ids, Y_test)
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size,
                                                   shuffle=True)
    test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size,
                                                  shuffle=True)
    return train_dataloader, test_dataloader 

# NOT TO BE RUN - code that created model
# original model training
def train_model(model, optimizer, train_dataloader, epochs=2):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.train()
    for epoch in epochs:
        # train in batches to save compute 
        for batch in train_dataloader:
            batch_input_ids, batch_attention_mask, batch_token_type_ids, batch_labels = batch
            batch_input_ids = batch_input_ids.to(device)
            batch_attention_mask = batch_attention_mask.to(device)
            batch_token_type_ids = batch_token_type_ids.to(device)
            batch_labels = batch_labels.to(device)

            optimizer.zero_grad()
            outputs = model(batch_input_ids, attention_mask=batch_attention_mask,
                            token_type_ids=batch_token_type_ids, labels=batch_labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
    print("Epoch: ", epoch+1, " of ", epochs, " - Loss: ", loss.item())

# NOT TO BE RUN - code that created model
# original model evaluation
def evaluate_model(model, test_dataloader):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    total_eval_loss = 0.0
    all_preds = []
    all_labels = []

    # evaluate in batches to save compute
    for batch in test_dataloader:
        batch_input_ids, batch_attention_mask, batch_token_type_ids, batch_labels = batch
        batch_input_ids = batch_input_ids.to(device)
        batch_attention_mask = batch_attention_mask.to(device)
        batch_token_type_ids = batch_token_type_ids.to(device)
        batch_labels = batch_labels.to(device)

        with torch.no_grad():
            outputs = model(batch_input_ids, attention_mask=batch_attention_mask,
                            token_type_ids=batch_token_type_ids, labels=batch_labels)
            loss = outputs.loss
            logits = outputs.logits

        total_eval_loss += loss.item()
        batch_preds = torch.argmax(logits, dim=1).cpu().numpy()
        label_ids = batch_labels.cpu().numpy()
        all_preds.extend(batch_preds)
        all_labels.extend(label_ids)

    # calculate and display overall metrics - most important is recall
    avg_loss = total_eval_loss / len(test_dataloader)
    cm_unlabeled = confusion_matrix(all_labels, all_preds)
    cm = {
        "TP": cm_unlabeled[0][0],
        "FN": cm_unlabeled[0][1],
        "FP": cm_unlabeled[1][0],
        "TN": cm_unlabeled[1][1]
    }

    accuracy = (cm["TP"] + cm["TN"]) / (cm["TP"] + cm["TN"] + cm["FP"] + cm["FN"])
    precision = cm["TP"] / (cm["TP"] + cm["FP"])
    recall = cm["TP"] / (cm["TP"] + cm["FN"])
    specificity = cm["TN"] / (cm["TN"] + cm["FP"])
    false_pos = cm["FP"] / (cm["FP"] + cm["TN"])
    false_neg = cm["FN"] / (cm["FN"] + cm["TP"])
    f1_score = (2*(precision*recall)) / (precision + recall)

    print("Loss: ", avg_loss)
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("Specificity: ", specificity)
    print("False Positive Rate: ", false_pos)
    print("False Negative Rate: ", false_neg)
    print("F1 Score: ", f1_score)

# NOT TO BE RUN - code that was used to create model
# save model and tokenizer to file
def save_model(model, tokenizer, model_path, tokenizer_path):
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(tokenizer_path)

# WILL BE RUN - load pretrained model
def load_model(model_path, tokenizer_path):
    model = transformers.AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = transformers.AutoTokenizer.from_pretrained(tokenizer_path)
    return model, tokenizer

# WILL BE RUN - make new predictions
def make_preds(data_path, model_path, tokenizer_path, batch_size=16):
    # load and format data
    model, tokenizer = load_model(model_path, tokenizer_path)
    X, Y = format_tables(ingest_tables(data_path), tokenizer)
    input_ids = X["input_ids"]
    attention_mask = X["attention_mask"]
    token_type_ids = X["token_type_ids"]
    dataset = torch.utils.data.TensorDataset(input_ids, attention_mask,
                                             token_type_ids,Y)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                             shuffle=False)
    # set up model on GPU/CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    all_preds = []
    # generate predictions
    for batch in dataloader:
        batch_input_ids, batch_attention_mask, batch_token_type_ids, batch_labels = batch
        batch_input_ids = batch_input_ids.to(device)
        batch_attention_mask = batch_attention_mask.to(device)
        batch_token_type_ids = batch_token_type_ids.to(device)

        with torch.no_grad():
            outputs = model(batch_input_ids, attention_mask=batch_attention_mask,
                            token_type_ids=batch_token_type_ids)

        batch_preds = torch.argmax(logits, dim=1).cpu().numpy()
        all_preds.extend(batch_preds)

    return all_preds
