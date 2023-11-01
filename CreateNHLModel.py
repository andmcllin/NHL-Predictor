import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint, EarlyStopping

def createModel():
    df = pd.read_csv('nhlGameResults.csv.gz', compression='gzip', header=0, sep=',', quotechar='"')

    X = df.drop(columns=['Date', 'Visiting Team', 'Home Team', 'Home Win'], axis=1)
    y = df['Home Win']

    del df

    n_cols = X.shape[1]

    model = Sequential()

    model.add(Dense(n_cols, activation='leaky_relu', input_shape=(n_cols,)))
    model.add(Dense(n_cols, activation='leaky_relu'))
    model.add(Dense(n_cols, activation='leaky_relu'))
    model.add(Dense(n_cols, activation='leaky_relu'))
    model.add(Dense(n_cols, activation='leaky_relu'))
    model.add(Dense(n_cols, activation='leaky_relu'))
    model.add(Dense(n_cols, activation='leaky_relu'))
    model.add(Dense(n_cols, activation='leaky_relu'))

    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    callbacks = [
        ModelCheckpoint('NHLPredictor.h5', save_best_only=True, verbose=0),
        EarlyStopping(patience=3, monitor='val_loss', verbose=1)
        ]

    model.fit(X, y, epochs=100, validation_split=0.25, callbacks=callbacks)

    del model, callbacks

    return 0