import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

# Load data
data = pd.read_csv('Delinquency_prediction_dataset.csv')

# Convert payment history to features
payment_statuses = ['Late', 'Missed', 'On-time']
for month in ['Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6']:
    for status in payment_statuses:
        data[f'{month}_{status}'] = (data[month] == status).astype(int)
    data.drop(month, axis=1, inplace=True)

# Define features and target
X = data.drop(['Customer_ID', 'Delinquent_Account'], axis=1)
y = data['Delinquent_Account']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Preprocessing pipeline
numeric_features = ['Age', 'Income', 'Credit_Score', 'Credit_Utilization', 
                   'Missed_Payments', 'Loan_Balance', 'Debt_to_Income_Ratio', 
                   'Account_Tenure']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_features = ['Employment_Status', 'Credit_Card_Type', 'Location']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# Add feature selection if needed
# from sklearn.neural_network import MLPClassifier

# nn_pipeline = Pipeline(steps=[
#     ('preprocessor', preprocessor),
#     ('classifier', MLPClassifier(hidden_layer_sizes=(50,), random_state=42, early_stopping=True))
# ])

# nn_pipeline.fit(X_train, y_train)
# y_pred_nn = nn_pipeline.predict(X_test)
# y_proba_nn = nn_pipeline.predict_proba(X_test)[:, 1]

# print("\nNeural Network Performance:")
# print(classification_report(y_test, y_pred_nn))
# print("ROC AUC:", roc_auc_score(y_test, y_proba_nn))
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

lr_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))
])

lr_pipeline.fit(X_train, y_train)
y_pred_lr = lr_pipeline.predict(X_test)
y_proba_lr = lr_pipeline.predict_proba(X_test)[:, 1]

print("Logistic Regression Performance:")
print(classification_report(y_test, y_pred_lr))
print("ROC AUC:", roc_auc_score(y_test, y_proba_lr))
