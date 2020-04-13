#buying, maint, door, persons, lug_boot, safety, cls
import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing

data = pd.read_csv("car.data")
print(data.head())

le = preprocessing.LabelEncoder()
buying = le.fit_transform(list(data["buying"])) # przetwarza kolumny buying z pliku car.data z high na 3 medium na 2 low na 1 itd
maint = le.fit_transform(list(data["maint"]))
door = le.fit_transform(list(data["door"]))
persons = le.fit_transform(list(data["persons"]))
lug_boot = le.fit_transform(list(data["lug_boot"]))
safety = le.fit_transform(list(data["safety"]))
cls = le.fit_transform(list(data["class"]))
#print(buying)
predict = "class"
#zip - iterator tupli, w ktorym pierwszy element w kazdej przekazanej iteracji jest ze soba sparowany
X = list(zip(buying, maint, door, persons, lug_boot, safety)) # konwersja buying, maint w jedna duza liste
y = list(cls)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)

model = KNeighborsClassifier(n_neighbors=9)

model.fit(x_train,y_train)
acc = model.score(x_test,y_test)
print(acc)

predcted = model.predict(x_test)
names = ["unacc", "acc", "good", "vgood"] # zmiana z systemu liczbowego na słowny: 0 - unacc, 1 - acc, 2 - good, 3 - vgood

for x in range(len(x_test)):
    print("Predicted: ", names[predcted[x]], " Data: ", x_test[x], " Actual: ", names[y_test[x]])
    n = model.kneighbors([x_test[x]], 9, True)
    print("N: ", n)
