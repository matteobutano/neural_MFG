import matplotlib.pyplot as plt
import tensorflow as tf
import matplotlib
from dgm_library import warmstart, sample_room, init_DGM, train, env_initializing, thick_room, sample_room_polar, train_TFC, warmstart_TFC
from DGM import * # NOQA
import numpy as np
import keras

env_initializing()

#######################################################################################################################
DTYPE = 'float64'
# Problem contraints
#sigma = 0.7
#g = -0.2 


V = 10e2

sigma = 0.35
g     = -0.005
mu    = 1
gamma = 0
m0    = 2.5
alpha = 0
l     = -((g*m0)/(1+alpha*m0))+(gamma*mu*sigma**2*np.log(np.sqrt(m0)))
u_b   = -mu*sigma**2*np.log(np.sqrt(m0))
R     = 0.37
s     =  tf.constant([0, -0.6],  dtype=DTYPE, shape=(1, 2))
v0 = m0**((-mu*sigma**2)/2)

# Constants of the agents
Xi = np.sqrt(np.abs((mu*sigma**4)/(2*g*m0)))
Cs = np.sqrt(np.abs((g*m0)/(2*mu)))


B = 10

#######################################################################################################################


verbose=1

u_theta = init_DGM(RNN_layers = 1, FNN_layers=1, nodes_per_layer=4,activation="tanh")
m_theta = init_DGM(RNN_layers = 1, FNN_layers=1, nodes_per_layer=4,activation="tanh")
m_theta, u_theta = warmstart(u_theta,m_theta,verbose=2)
m_theta, u_theta = train(u_theta,m_theta,verbose=2)
X0 = thick_room(0)
x = X0.iloc([0])
y = X0.iloc([1])
m = m_theta(X0)
u = u_theta(X0)


# solution via TFC - not updated!
# f_theta = init_DGM(RNN_layers = 2, FNN_layers=0, nodes_per_layer=10,activation="tanh")
# g_theta = init_DGM(RNN_layers = 2, FNN_layers=0, nodes_per_layer=10,activation="tanh")
# f_theta, g_theta = warmstart_TFC(f_theta,g_theta, verbose)
# X0, dC, dB, rho, theta, F0m, F0u = sample_room_polar(0)
# v = f_theta(X0) +  (1/(B-R))*((rho-B)*f_theta(dC)  + (rho-R)*(v0 - f_theta(dB)))
# m = g_theta(X0) +  (1/(B-R))*((rho-B)*g_theta(dC)  + (rho-R)*(m0 - g_theta(dB)))
# u = -tf.math.log(v)
# x = rho.numpy()*np.cos(theta)
# y = rho.numpy()*np.sin(theta)

usual = matplotlib.cm.hot_r(np.arange(256))
saturate = np.ones((int(256 / 20), 4))
for i in range(3):
    saturate[:, i] = np.linspace(usual[-1, i], 0, saturate.shape[0])
cmap1 = np.vstack((usual, saturate))
cmap1 = matplotlib.colors.ListedColormap(cmap1, name='myColorMap', N=cmap1.shape[0])

fig = plt.figure(figsize=(7,6))
plt.scatter(x, y, c=m, cmap=cmap1, marker='.', alpha=0.3)
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.colorbar()
plt.show()

fig = plt.figure(figsize=(7,6))
plt.scatter(x, y, c=u, cmap=cmap1, marker='.', alpha=0.3)
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.colorbar()
plt.show()

#f_theta_trained, g_theta_trained = train_TFC(f_theta,g_theta,verbose=10)

# f_theta_trained.save("f_theta")
# g_theta_trained.save("g_theta")

# f_theta = keras.models.load_model("f_theta")
# g_theta = keras.models.load_model("g_theta")
# g_theta = g_theta_trained
# f_theta = f_theta_trained
# v = f_theta(X0) +  (1/(B-R))*((rho-B)*f_theta(dC)  + (rho-R)*(v0 - f_theta(dB)))
# m = g_theta(X0) +  (1/(B-R))*((rho-B)*g_theta(dC)  + (rho-R)*(m0 - g_theta(dB)))
# u = -tf.math.log(v)

# x = rho.numpy()*np.cos(theta)
# y = rho.numpy()*np.sin(theta)

# usual = matplotlib.cm.hot_r(np.arange(256))
# saturate = np.ones((int(256 / 20), 4))
# for i in range(3):
#     saturate[:, i] = np.linspace(usual[-1, i], 0, saturate.shape[0])
# cmap1 = np.vstack((usual, saturate))
# cmap1 = matplotlib.colors.ListedColormap(cmap1, name='myColorMap', N=cmap1.shape[0])

# fig = plt.figure(figsize=(7,6))
# plt.scatter(x, y, c=m, cmap=cmap1, marker='.', alpha=0.3)
# plt.xlabel('$x$')
# plt.ylabel('$y$')
# plt.colorbar()
# plt.show()

# fig = plt.figure(figsize=(7,6))
# plt.scatter(x, y, c=u, cmap=cmap1, marker='.', alpha=0.3)
# plt.xlabel('$x$')
# plt.ylabel('$y$')
# plt.colorbar()
# plt.show()