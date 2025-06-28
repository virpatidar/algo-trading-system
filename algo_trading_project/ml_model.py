from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def prepare_features(df):
    df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
    df['Target'] = df['Close'].shift(-1) > df['Close']
    df.dropna(inplace=True)
    X = df[['RSI', 'MACD', 'Volume']]
    y = df['Target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, X_test, y_train, y_test):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    return model, acc
