# This script plot \cref{RD-ds}
# This script plot \cref{NS-ds}
from utils import *
from simulator import *
from models import *

r.seed(0)
n, beta, Re, type, GPU, ds_parameter = parsing()
device = torch.device('cuda:{}'.format(GPU) if torch.cuda.is_available() else 'cpu')

arg, u, v, label = read_data('../../data/{}/{}-{}.npz'.format(type, n, ds_parameter))

nx, ny, dt, T, label_dim, traj_num, step_num, test_index, u, v, label = preprocessing(arg, type, u, v, label, device, flag=False)

print('Plotting {} model with n = {}, beta = {:.1f}, Re = {} ...'.format(type, n, beta, Re))
    
if type == 'NS':
    model_ols = UNet([2,4,8,16,32,64,1]).to(device)
    u64_np = copy.deepcopy(u[test_index].numpy()).reshape([step_num, nx+2, ny+2])
    v64_np = copy.deepcopy(v[test_index].numpy()).reshape([step_num, nx+2, ny+1])
else:
    model_ols = UNet().to(device)
    u64_np = copy.deepcopy(u[test_index].numpy()).reshape([step_num, nx, ny])
    v64_np = copy.deepcopy(v[test_index].numpy()).reshape([step_num, nx, ny])
model_ols.load_state_dict(torch.load('../../models/{}/OLS-{}-{}.pth'.format(type, n, ds_parameter), 
                                    map_location=torch.device('cpu')))
model_ols.eval()
model_ed = EDNet().to(device)
model_ed.load_state_dict(torch.load('../../models/{}/ED-{}-{}.pth'.format(type, n, ds_parameter),
                                    map_location=torch.device('cpu')))
model_ed.eval()


if type == 'RD':
    simulator_ols = RD_Simulator(model_ols, 
                                 model_ed, 
                                 device, 
                                 u_hist=u64_np, 
                                 v_hist=v64_np, 
                                 step_num=step_num,
                                 dt=dt)
else:
    simulator_ols = NS_Simulator(model_ols, 
                                 model_ed, 
                                 device, 
                                 u_hist=u64_np, 
                                 v_hist=v64_np, 
                                 step_num=step_num,
                                 dt=dt)
simulator_ols.simulator()  


plt.rcParams['savefig.dpi'] = 500
plt.rcParams['figure.dpi']  = 500 
width = 7.5
height = 3
labelsize = 10
#################################################################
#               Plot of the simulation result                   #
#################################################################
fig = plt.figure(figsize=(width, height))
fig_num = 5
hspace = 0.01
wspace = -0.40
fraction = 0.024
pad = 0.001
time_scale = 700
t_array = (np.array([0.0, 0.2, 0.4, 0.6, 1.0])*time_scale).astype(int)
print(t_array)
ax1 = []
ax2 = []
im = []
for i in range(fig_num):
    ax1.append(fig.add_subplot(2,fig_num,i+1))
    ax2.append(fig.add_subplot(2,fig_num,i+fig_num+1))
fig.tight_layout()
for i in range(fig_num):
    ax1[i].imshow(simulator_ols.u_hist[t_array[i]][1:33, 1:-1], cmap=cm.jet)
    ax1[i].set_axis_off()
    im.append(ax2[i].imshow(simulator_ols.u_hist_simu[t_array[i]][1:33, 1:-1], cmap=cm.jet))
    ax2[i].set_axis_off()
plt.subplots_adjust(hspace=hspace)
plt.subplots_adjust(wspace=wspace)
for i in range(fig_num):
    cbar = fig.colorbar(im[i], ax=[ax1[i], ax2[i]], fraction=fraction, pad=pad, orientation='horizontal')
    cbar.ax.tick_params(labelsize=5)
plt.savefig('../../fig/exp1/{}/1.svg'.format(type), dpi = 1000, bbox_inches='tight', pad_inches=0, format='svg')
#plt.show()
plt.clf()


#################################################################
#              Plot of the ds & error comparison                #
#################################################################
fig = plt.figure(figsize=(width, height/2))
ax = fig.add_subplot(111)
ax.plot(np.linspace(0, 800, time_scale), simulator_ols.error_hist[:time_scale]*10, label=r'$\left\| u(t) - \widehat u(t) \right\|_{2}^2$', color='r', linewidth=.5)
ax.legend(bbox_to_anchor = (0.1, 0.9), loc = 'upper left', borderaxespad = 0., fontsize=10)
ax1 = ax.twinx()
ax1.plot(np.linspace(0, 800, time_scale), np.log10(simulator_ols.ds_hist[:time_scale])+2, label=r'$\log(F(\widehat u(t)))$', color='r', linewidth=.5, linestyle='dashed')
ax1.legend(bbox_to_anchor = (0.1, 0.6), loc = 'upper left', borderaxespad = 0., fontsize=10)
ax1.set_ylabel(r'$\log(F(\widehat u(t)))$', fontsize=10)
ax.xaxis.set_tick_params(labelsize=labelsize)
ax1.yaxis.set_tick_params(labelsize=labelsize)
ax.set_ylabel(r'$\left\| u(t) - \widehat u(t) \right\|_{2}^2$', fontsize=10)
plt.savefig('../../fig/exp1/{}/2.svg'.format(type), dpi = 1000, bbox_inches='tight', pad_inches=0, format='svg')
plt.show()


# For the comparison bewteen RD & NS, we need to show following features of our figures
# 1. Two figures should be of the same time scope: same \Delta t & same number of step_num
# 2. RD should suffer from less severe distribution shift comparing to NS, meaning that 
# both the error and ds should be smaller than NS.
# 3. Currently, the ds legend in NS is too small.