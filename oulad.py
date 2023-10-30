import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def preprocessing(data):
    encode = LabelEncoder()
    data['region'] = encode.fit_transform(data['region'])
    data['highest_education'] = encode.fit_transform(data['highest_education'])
    data['imd_band'] = encode.fit_transform(data['imd_band'])
    data['age_band'] = encode.fit_transform(data['age_band'])
    data['disability'] = encode.fit_transform(data['disability'])
    data['final_result'] = encode.fit_transform(data['final_result'])

    x = data.drop('final_result', axis=1)
    y = data['final_result']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)
    x_train = x_train.values.reshape(x_train.shape[0], 1, x_train.shape[1])
    x_test = x_test.values.reshape(x_test.shape[0], 1, x_test.shape[1])

    return x_train, x_test, y_train, y_test


def modeling(x_train, x_test, y_train, y_test):
    model = Sequential([
        LSTM(64, activation='relu', input_shape=(1, x_train.shape[2])),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['acc']
    )

    model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
    loss, accuracy = model.evaluate(x_test, y_test)
    print(f"Test accuracy: {accuracy}")


if __name__ == '__main__':
    df = pd.read_csv('studentInfo.csv')
    df = df[['region', 'highest_education', 'imd_band', 'age_band', 'studied_credits', 'disability', 'final_result']]
    df['final_result'] = df['final_result'].apply(lambda x: 'pass' if x in ['pass', 'Distinction'] else 'fail')
    df = df[df['imd_band'].notna()]
    df['imd_band'].fillna('ValueToReplaceMissing', inplace=True)

    pd.set_option('display.max_columns', None)
    print(df)

    _x_train, _x_test, _y_train, _y_test = preprocessing(df)
    modeling(_x_train, _x_test, _y_train, _y_test)