import serial
import pandas as pd
import numpy as np
import joblib

LEN_N = 128

PORT = "/dev/cu.usbserial-1140"
BAUDRATE = 115200

data = []
ser = serial.Serial(PORT, BAUDRATE, timeout=1)

print("Приём данных...")
print("Для завершения нажмите Ctrl+C\n")

def sma_f(df, x, y, z):
    df["abs_sum"] = np.abs(df[x]) + np.abs(df[y]) + np.abs(df[z])
    return df["abs_sum"].sum()/LEN_N

def energy_f(df, column):
    return (df[column] ** 2).sum() / LEN_N

def iqr_f(df, column):
    return df[column].quantile(0.75) - df[column].quantile(0.25)


cnt = 0
results_lst = []

while True:
    line = ser.readline().decode("utf-8", errors="ignore").strip()

    if line:
        #print(line)
        data.append(list(map(float, line.split(","))))
    cnt += 1
    if cnt % 10 == 0:
        df = pd.DataFrame(data, columns=["accX","accY","accZ","tempRaw","gyroX","gyroY","gyroZ"])
        data = []
        #cnt = 0
        df["M_i"] = (df["accX"] ** 2 + df["accY"] ** 2 + df["accZ"] ** 2) ** 0.5
        column_values_48 = ['tBodyAcc-mean()-X', 'tBodyAcc-mean()-Y', 'tBodyAcc-mean()-Z',
                            'tBodyAcc-std()-X', 'tBodyAcc-std()-Y', 'tBodyAcc-std()-Z',
                            'tBodyAcc-mad()-X', 'tBodyAcc-mad()-Y', 'tBodyAcc-mad()-Z',
                            'tBodyAcc-max()-X', 'tBodyAcc-max()-Y', 'tBodyAcc-max()-Z',
                            'tBodyAcc-min()-X', 'tBodyAcc-min()-Y', 'tBodyAcc-min()-Z',
                            'tBodyAcc-sma()',
                            'tBodyAcc-energy()-X', 'tBodyAcc-energy()-Y', 'tBodyAcc-energy()-Z',
                            'tBodyAcc-iqr()-X', 'tBodyAcc-iqr()-Y', 'tBodyAcc-iqr()-Z',

                            'tBodyGyro-mean()-X', 'tBodyGyro-mean()-Y', 'tBodyGyro-mean()-Z',
                            'tBodyGyro-std()-X', 'tBodyGyro-std()-Y', 'tBodyGyro-std()-Z',
                            'tBodyGyro-mad()-X', 'tBodyGyro-mad()-Y', 'tBodyGyro-mad()-Z',
                            'tBodyGyro-max()-X', 'tBodyGyro-max()-Y', 'tBodyGyro-max()-Z',
                            'tBodyGyro-min()-X', 'tBodyGyro-min()-Y', 'tBodyGyro-min()-Z',
                            'tBodyGyro-sma()',
                            'tBodyGyro-energy()-X', 'tBodyGyro-energy()-Y', 'tBodyGyro-energy()-Z',
                            'tBodyGyro-iqr()-X', 'tBodyGyro-iqr()-Y', 'tBodyGyro-iqr()-Z',

                            'tBodyAccMag-mean()', 'tBodyAccMag-std()', 'tBodyAccMag-mad()',
                            'tBodyAccMag-max()', 'tBodyAccMag-min()']

        list_of_parameters = [df["accX"].mean(), df["accY"].mean(), df["accZ"].mean(),
                              df["accX"].std(), df["accY"].std(), df["accZ"].std(),
                              df["accX"].median(), df["accY"].median(), df["accZ"].median(),
                              df["accX"].max(), df["accY"].max(), df["accZ"].max(),
                              df["accX"].min(), df["accY"].min(), df["accZ"].min(),
                              sma_f(df, "accX", "accY", "accZ"),
                              energy_f(df, "accX"), energy_f(df, "accY"), energy_f(df, "accZ"),
                              iqr_f(df, "accX"), iqr_f(df, "accY"), iqr_f(df, "accZ"),

                              df["gyroX"].mean(), df["gyroY"].mean(), df["gyroZ"].mean(),
                              df["gyroX"].std(), df["gyroY"].std(), df["gyroZ"].std(),
                              df["gyroX"].median(), df["gyroY"].median(), df["gyroZ"].median(),
                              df["gyroX"].max(), df["gyroY"].max(), df["gyroZ"].max(),
                              df["gyroX"].min(), df["gyroY"].min(), df["gyroZ"].min(),
                              sma_f(df, "gyroX", "gyroY", "gyroZ"),
                              energy_f(df, "gyroX"), energy_f(df, "gyroY"), energy_f(df, "gyroZ"),
                              iqr_f(df, "gyroX"), iqr_f(df, "gyroY"), iqr_f(df, "gyroZ"),

                              df["M_i"].mean(), df["M_i"].std(), df["M_i"].median(),
                              df["M_i"].max(), df["M_i"].min()]

        lst = [list_of_parameters]
        new_df = pd.DataFrame(lst, columns=column_values_48)

        filename = 'model.bin'
        x_test = new_df
        restored_model = joblib.load(filename)
        result = restored_model.predict_proba(x_test)
        print(result)
        results_lst.append(result)
    if cnt == 100:
        break
print(results_lst)
#TODO: watch range (max - min) in accelerometer's values and in dataset's