import pandas as pd
import ast


def transformData(messages):
    messageValuetoArray = ast.literal_eval(messages.value.decode())
    df = pd.DataFrame(
        {
            "CityName": [messageValuetoArray[0][0], messageValuetoArray[1][0]],
            "Temperature": [messageValuetoArray[0][1], messageValuetoArray[1][1]],
            "TimeZone": [messageValuetoArray[0][2], messageValuetoArray[1][2]],
        }
    )

    return df
