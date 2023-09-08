# This is the script for the figure \cref{NS-cmp}, we only use the `else` block 
# to do the plot
from utils import *
from simulator import *
from models import *
from test import test_simulator

simulator_list_ols = []
simulator_list_tr = []

for i in range(10):
    simulator_list_ols.append(test_simulator(test_index=i)[0])
    simulator_list_tr.append(test_simulator(test_index=i, model_type='TR')[0])
type = test_simulator(test_index=i, model_type='TR')[1]

plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.dpi']  = 300 
width = 10
height = 4
labelsize = 10
#################################################################
#               Plot of the simulation result                   #
# we only plot the result of the test history                   #
#################################################################
test_index = 5
simulator_ols = simulator_list_ols[test_index]
simulator_tr = simulator_list_tr[test_index]

'''fig = plt.figure(figsize=(width, height))
fig_num = 5
hspace = 0.01
wspace = -0.765
fraction = 0.016
pad = 0.001
time_scale = 140
t_array = (np.array([0.0, 0.2, 0.4, 0.6, 1.0])*time_scale).astype(int)
print(t_array)
ax1 = []
ax2 = []
ax3 = []
im = []
for i in range(fig_num):
    ax1.append(fig.add_subplot(3,fig_num,i+1))
    ax2.append(fig.add_subplot(3,fig_num,i+fig_num+1))
    ax3.append(fig.add_subplot(3,fig_num,i+fig_num*2+1))
fig.tight_layout()
for i in range(fig_num):
    ax1[i].imshow(simulator_ols.u_hist[t_array[i]][1:33, 1:-1], cmap=cm.jet)
    ax1[i].set_axis_off()
    tmp_im = ax2[i].imshow(simulator_ols.u_hist_simu[t_array[i]][1:33, 1:-1], cmap=cm.jet)
    im.append(tmp_im)
    ax2[i].set_axis_off()
    ax3[i].imshow(simulator_tr.u_hist_simu[t_array[i]][1:33, 1:-1], cmap=cm.jet)
    ax3[i].set_axis_off()
plt.subplots_adjust(hspace=hspace)
plt.subplots_adjust(wspace=wspace)
for i in range(fig_num):
    cbar = fig.colorbar(im[i], ax=[ax1[i], ax2[i], ax3[i]], fraction=fraction, pad=pad, orientation='horizontal')
    cbar.ax.tick_params(labelsize=5)
plt.savefig('../../fig/exp4/{}/1.svg'.format(type), dpi = 1000, bbox_inches='tight', pad_inches=0, format='svg')
plt.show()
plt.clf()'''


#################################################################
#              Plot of the ds & error comparison                #
#################################################################
avg_err_hist_ols = 0
avg_err_hist_tr = 0
avg_ds_hist_ols = 0
avg_ds_hist_tr = 0
std_err_hist_ols = 0
std_err_hist_tr = 0
std_ds_hist_ols = 0
std_ds_hist_tr = 0
for i in range(10):
    avg_err_hist_ols = avg_err_hist_ols + simulator_list_ols[i].error_hist
    avg_err_hist_tr = avg_err_hist_tr + simulator_list_tr[i].error_hist
    avg_ds_hist_ols = avg_ds_hist_ols + simulator_list_ols[i].ds_hist
    avg_ds_hist_tr = avg_ds_hist_tr + simulator_list_tr[i].ds_hist
avg_err_hist_tr = avg_err_hist_tr/10
avg_err_hist_ols = avg_err_hist_ols/10
for i in range(10):
    std_err_hist_ols = std_err_hist_ols + (simulator_list_ols[i].error_hist - avg_err_hist_ols)**2
    std_err_hist_tr = std_err_hist_tr + (simulator_list_tr[i].error_hist - avg_err_hist_tr)**2
    std_ds_hist_ols = std_ds_hist_ols + (simulator_list_ols[i].ds_hist - avg_ds_hist_ols)**2
    std_err_hist_tr = std_err_hist_tr + (simulator_list_tr[i].ds_hist - avg_ds_hist_tr)**2
std_err_hist_ols = np.sqrt(std_err_hist_ols/10)
std_err_hist_tr = np.sqrt(std_err_hist_tr/10)
std_ds_hist_ols = np.sqrt(std_ds_hist_ols/10)
std_ds_hist_tr = np.sqrt(std_ds_hist_tr/10)

fig = plt.figure(figsize=(width, height//2))
ax = fig.add_subplot(111)
time_scale = avg_ds_hist_ols.shape[0]
#pdb.set_trace()
ax.errorbar(np.linspace(0, 800, time_scale), avg_err_hist_ols, std_err_hist_ols, fmt='.', label=r'$\left\| \widehat u_{OLS} - u \right\|_{2}^2$', ms=0.1)
ax.errorbar(np.linspace(0, 800, time_scale), avg_err_hist_tr, std_err_hist_tr, fmt='o', label=r'$\left\| \widehat u_{TR} - u \right\|_{2}^2$')
#ax.plot(np.linspace(0, 800, time_scale), simulator_ols.error_hist[:time_scale], label='OLS error', color='r', linewidth=.5)
ax.legend(bbox_to_anchor = (0.1, 0.9), loc = 'upper left', borderaxespad = 0., fontsize=10)
ax1 = ax.twinx()
ax.errorbar(np.linspace(0, 800, time_scale), avg_ds_hist_ols, std_ds_hist_ols, fmt='.', label=r'$\log(F(\widehat u_{OLS}))$', ms=0.1)
ax.errorbar(np.linspace(0, 800, time_scale), avg_ds_hist_tr, std_ds_hist_tr, fmt='o', label=r'$\log(F(\widehat u_{TR}))$')
ax1.legend(bbox_to_anchor = (0.1, 0.7), loc = 'upper left', borderaxespad = 0., fontsize=10)
ax1.set_ylabel(r'$\log(F(\widehat u(t)))$', fontsize=10)
ax.xaxis.set_tick_params(labelsize=labelsize)
ax1.yaxis.set_tick_params(labelsize=labelsize)
ax.set_ylabel(r'$\left\| u(t) - \widehat u(t) \right\|_{F}^2$', fontsize=10)
plt.savefig('../../fig/exp4/{}/2.jpg'.format(type), dpi = 1000, bbox_inches='tight', pad_inches=0)
plt.show()