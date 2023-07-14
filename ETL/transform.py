import pandas as pd
import ast
from datetime import datetime


def transformData(messages):
    messageValuetoArray = ast.literal_eval(messages.value.decode())
    df = pd.DataFrame(
        {
            "CityName": [
                messageValuetoArray[0][0],
                messageValuetoArray[1][0],
                messageValuetoArray[2][0],
                messageValuetoArray[3][0],
                messageValuetoArray[4][0],
            ],
            "Temperature": [
                messageValuetoArray[0][1],
                messageValuetoArray[1][1],
                messageValuetoArray[2][1],
                messageValuetoArray[3][1],
                messageValuetoArray[4][1],
            ],
            "Humidity": [
                messageValuetoArray[0][2],
                messageValuetoArray[1][2],
                messageValuetoArray[2][2],
                messageValuetoArray[3][2],
                messageValuetoArray[4][2],
            ],
            "TimeZone": [
                messageValuetoArray[0][3],
                messageValuetoArray[1][3],
                messageValuetoArray[2][3],
                messageValuetoArray[3][3],
                messageValuetoArray[4][3],
            ],
        }
    )

    df["Temperature"] = (df["Temperature"] - 273.15).astype(int)
    df["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return df
