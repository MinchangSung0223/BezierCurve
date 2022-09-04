from modern_robotics import *
from BezierCurve import *
import matplotlib.pyplot as plt
import numpy as np
from pyScurveGenerator import *
from draw_functions import drawTraj,drawTrajList

def diff_trajectory(val_list,alpha,dt):
    val_list = np.array(val_list)
    prev_val = val_list[0]
    prev_filtered_val = val_list[0]
    diff_val_list = []
    for i  in range(len(val_list)):
        val = val_list[i]
        diff_val = (val-prev_val)/dt;
        filtered_val = (alpha)*prev_filtered_val+ (1-alpha)*diff_val;
        diff_val_list.append(filtered_val)
        prev_filtered_val = filtered_val;
        prev_val = val;
    return np.array(diff_val_list)
def QuinticVelTimeScaling(Tf, t):
    return 10 *3*1.0/Tf* (1.0 * t / Tf) ** 2 - 15 *4*1.0/Tf *(1.0 * t / Tf) ** 3 \
           + 6 *5*1.0/Tf* (1.0 * t / Tf) ** 4
def QuinticAccTimeScaling(Tf, t):
    return 10 *3*1.0/Tf*2*1.0/Tf* (1.0 * t / Tf)  - 15 *4*1.0/Tf*3*1.0/Tf*(1.0 * t / Tf) ** 2 \
           + 6 *5*1.0/Tf*4*1.0/Tf* (1.0 * t / Tf) ** 3
def CartesianScurveTrajectory(X_list,sg,Times,N):
    X_list = np.array(X_list)
    size_X=len(X_list);
    N = int(N)
    traj_list = []
    dot_traj_list = []
    ddot_traj_list = []
    
    for i in range(0,size_X-1):
        Tf = Times[i]
        timegap = Tf / (N - 1.0)
        traj = [[None]] * N       
        dot_traj = [[None]] * N       
        ddot_traj = [[None]] * N       
        Rstart, pstart = TransToRp(X_list[i,:,:])
        Rend, pend = TransToRp(X_list[i+1,:,:])
        s_traj = sg.getTraj(0);     
        for j in range(N):

            val = sg.generate(s_traj,timegap*j)
            s = val[0]
            sdot = val[1]
            sddot = val[2]

            #s = QuinticTimeScaling(Tf, timegap * j)
            #sdot = QuinticVelTimeScaling(Tf, timegap * j)
            #sddot = QuinticAccTimeScaling(Tf, timegap * j)
            #P,dot_P,ddot_P = bc.get_bazier_curve_s(s);
            Rs = Rstart@ MatrixExp3(MatrixLog3(np.array(Rstart).T@Rend)* s)
            dRds =(MatrixLog3(np.array(Rstart).T@Rend))@Rs
            d2Rds2 =(MatrixLog3(np.array(Rstart).T@Rend))@(MatrixLog3(np.array(Rstart).T@Rend))@Rs         
            traj[j] \
                = np.r_[np.c_[ Rs, \
                       s * np.array(pend) + (1 - s) * np.array(pstart)], \
                       [[0, 0, 0, 1]]]

            dot_traj[j] \
                = np.r_[np.c_[dRds*sdot, \
                       sdot * np.array(pend)  - sdot * np.array(pstart)], \
                       [[0, 0, 0, 1]]]
            ddot_traj[j] \
                = np.r_[np.c_[d2Rds2*sdot*sdot+dRds*sddot, \
                       sddot * np.array(pend)  - sddot * np.array(pstart)], \
                       [[0, 0, 0, 1]]]
            
        traj_list.append(traj)
        dot_traj_list.append(dot_traj)
        ddot_traj_list.append(ddot_traj)
        
    return np.reshape(np.array(traj_list),(-1,4,4)),np.reshape(np.array(dot_traj_list),(-1,4,4)),np.reshape(np.array(ddot_traj_list),(-1,4,4))


if __name__ == "__main__":
	traj = Trajectory();
	traj.so =0.0;
	traj.vo =0.0;
	traj.ao =0.0;
	traj.sf =1.0;
	traj.vf =0.0;
	traj.af =0.0;	
	traj.vmax =10.0;
	traj.amax =50.0;
	traj.dmax =50.0;
	traj.j =200.0;
	traj.vp = traj.vmax;
	traj.a1 = traj.amax;
	traj.a2 = traj.dmax;
	sg = ScurveGenerator([traj])
	sg.syncTime();
	sg.syncTargetTime(2);	
	traj = sg.getTraj(0);    
	dt = 0.001	    
	pos_1 = [0,0,0]
	pos_2 = [2,1,0]
	pos_3 = [4,0,0]

	X1 = np.eye(4)
	X2 = np.eye(4)
	X3 = np.eye(4)
	theta = np.pi/2.0
	X2[0:3,0:3] = np.array([[cos(theta) ,-sin(theta) ,0],[sin(theta), cos(theta), 0],[0 ,0 ,1]])

	X1[0:3,3] = pos_1
	X2[0:3,3] = pos_2
	X3[0:3,3] = pos_3

	X_list = [X1,X2,X3]
	Times = [traj.tt,traj.tt,traj.tt]
	N = int(traj.tt/dt);
	traj,dot_traj,ddot_traj =CartesianScurveTrajectory(X_list,sg,Times,N)
	

	x_list = [x for x in traj[:,0,3]]
	diff_x_list = diff_trajectory(x_list,0.0,dt)
	dx_list = [x for x in dot_traj[:,0,3]]
	diff_dx_list = diff_trajectory(dx_list,0.0,dt)
	ddx_list = [x for x in ddot_traj[:,0,3]]

	y_list = [y for y in traj[:,1,3]]
	diff_y_list = diff_trajectory(y_list,0.0,dt)
	dy_list = [x for x in dot_traj[:,1,3]]
	diff_dy_list = diff_trajectory(dy_list,0.0,dt)
	ddy_list = [x for x in ddot_traj[:,1,3]]

	z_list = [z for z in traj[:,2,3]]
	diff_z_list = diff_trajectory(z_list,0.0,dt)
	dz_list = [x for x in dot_traj[:,2,3]]
	diff_dz_list = diff_trajectory(dz_list,0.0,dt)
	ddz_list = [x for x in ddot_traj[:,2,3]]

	t_list = [z*dt for z in range(0,len(x_list))]
	plt.clf();
	ax1 = plt.subplot(3,1,1)
	ax2 = plt.subplot(3,1,2)
	ax3 = plt.subplot(3,1,3)
	ax1.plot(t_list,x_list,'g')
	ax2.plot(t_list,dx_list,'b')
	ax2.plot(t_list,diff_x_list,':')
	ax3.plot(t_list,ddx_list,'r')	
	ax3.plot(t_list,diff_dx_list,'g:')
	plt.show()
	
	
	s_traj = sg.getTraj(0);
	timegap = s_traj.tt / (N - 1.0)
	s_list = [[None]] * 2*N       
	ds_list = [[None]] * 2*N       
	dds_list = [[None]] * 2*N       
	ddds_list = [[None]] * 2*N    
	t_list_ = [[None]] * 2*N       

	for j in range(N):
	    val = sg.generate(s_traj,timegap*j)
	    s_list[j] = val[0]
	    ds_list[j] = val[1]
	    dds_list[j] = val[2]
	    ddds_list[j] = val[3]
	    t_list_[j] = timegap*j;
	for j in range(N):
	    val = sg.generate(s_traj,timegap*j)
	    s_list[j+N] = val[0]
	    ds_list[j+N] = val[1]
	    dds_list[j+N] = val[2]
	    ddds_list[j+N] = val[3]
	    t_list_[j+N] = timegap*j+s_traj.tt;    
	s_list = np.array(s_list)
	ds_list = np.array(ds_list)
	dds_list = np.array(dds_list)
	ddds_list = np.array(ddds_list)
	plt.clf();
	ax1 = plt.subplot(4,1,1)
	ax2 = plt.subplot(4,1,2)
	ax3 = plt.subplot(4,1,3)
	ax4 = plt.subplot(4,1,4)
	ax1.plot(t_list,s_list)
	ax1.plot(t_list,x_list,'r--',markersize=0.5)

	ax2.plot(t_list,np.array(ds_list))
	ax2.plot(t_list,dx_list,'r--',markersize=0.5)

	ax3.plot(t_list,np.array(dds_list))
	ax3.plot(t_list,ddx_list,'r--',markersize=0.5)

	ax4.plot(t_list,ddds_list)
	plt.show()

