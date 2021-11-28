from helpers import get_data
from typing import List

with open("app/names/B.txt", "r") as f:
    data: List = []
    for dinoName in f:
        dinoName = dinoName.replace("\n", "")
        data.append(get_data(dinoName))
    print(data)
