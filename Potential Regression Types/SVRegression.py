import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
import pandas as pd
from sklearn.preprocessing import StandardScaler
from bayesian_optimization import BayesianOptimization
datasets = pd.read_csv('Inputs_outputs.csv')
X = datasets.iloc[:, 0:3].values
Y = datasets.iloc[:, 3].values




Y = Y.reshape(-1,1)

# Feature Scaling
'''Standardize features by removing mean and scaling it to unit variance'''

sc_X = StandardScaler()
sc_Y = StandardScaler()
X = sc_X.fit_transform(X)
Y = sc_Y.fit_transform(Y)


# Fitting the SVR model to the data
regressor = SVR(kernel = 'rbf')
regressor.fit(X,Y)


def prediction(x,y,z):
    return float(sc_Y.inverse_transform(regressor.predict(sc_X.transform(np.array([x,y,z]).reshape(1,-1)))))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

a = []
b = []
j = []
cv = []

def slicex(x):
    for i in range(50000):
        x = x
        y = np.random.uniform(40, 65)
        z = np.random.uniform(2, 4)
        c = prediction(x, y, z)
        i = i + 1
        a.append(x)
        b.append(y)
        j.append(z)
        cv.append(c)
        i = i + 1
def slicey(y):
    for i in range(50000):
        x = np.random.uniform(1000,4000)
        y = y
        z = np.random.uniform(2, 4)
        c = prediction(x, y, z)
        i = i + 1
        a.append(x)
        b.append(y)
        j.append(z)
        cv.append(c)
        i = i + 1

def slicez(z):
    for i in range(50000):
        x = np.random.uniform(1000,4000)
        y = np.random.uniform(40, 65)
        z = z
        c = prediction(x, y, z)
        i = i + 1
        a.append(x)
        b.append(y)
        j.append(z)
        cv.append(c)
        i = i + 1


pbounds = {'y': (40, 65), 'z': (2, 4),'x':(1000,4000)}
optimizer = BayesianOptimization(
    f=prediction,
    pbounds=pbounds,
    verbose=1, # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    random_state=999
)
def probe_point(x,y,z):
    return optimizer.probe(params={"x": x, "y": y, "z":z},lazy=True,)

'''probe_point(4000,65,4)
probe_point(4000,65,2)
probe_point(3000,40,2)
probe_point(1000,40,2)
probe_point(2500,52.5,3)'''
optimizer.maximize(init_points = 7, n_iter = 20)

xlist = []
ylist = []
zlist = []
datalist = []
for res in enumerate(optimizer.res):
    xlist.append(float(res[1].get('params').get('x')))
    ylist.append(float(res[1].get('params').get('y')))
    zlist.append(float(res[1].get('params').get('z')))
    datalist.append(float(res[1].get('target')))

'''ax.scatter(xlist,ylist,zlist,marker='o')'''
datalist = np.array(datalist)
max_element = np.where(datalist == np.amax(datalist))

'''max_index = int(max_element[0])
slicex(xlist[max_index])
slicey(ylist[max_index])
slicez(zlist[max_index])'''
slicex(2341.9193)
slicey(59.8873)
slicez(3.0090)

img = ax.scatter(a, b, j,c=cv, cmap=plt.jet())
ax.view_init(elev=13., azim=-140)
fig.colorbar(img)
print('The maximum value observed on the plot was', max(cv))
print('The maximum value observed by bayesian optimisation was', np.max(datalist))
ax.set_xlabel('Welding Energy (J)')
ax.set_ylabel('Vibration amplitude(um)')
ax.set_zlabel('Clamping pressure (bar)')

plt.savefig('4D plot of environment')
plt.show()

