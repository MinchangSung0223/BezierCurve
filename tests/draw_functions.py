from pyScurveGenerator import *
import matplotlib.pyplot as plt
import numpy as np
def drawTraj_(sg,traj,number,fig,ax):
	t_list = np.linspace(0,traj.tt,number)
	s_list = []
	ds_list = []
	dds_list = []
	ddds_list = []
	state_list = []
	for j in range(len(t_list)):
		val = sg.generate(traj,t_list[j]);	
		s_list.append(val[0])
		ds_list.append(val[1])
		dds_list.append(val[2])
		ddds_list.append(val[3])
		state_list.append(val[4]+1)
	state_list = np.array(state_list);
	t_list = np.array(t_list);
	s_list = np.array(s_list);
	ds_list = np.array(ds_list);
	dds_list = np.array(dds_list);
	ddds_list = np.array(ddds_list);

	ax[0].plot(t_list,s_list, linestyle='--', linewidth=1)
	ax[1].plot(t_list,ds_list, linestyle='--', linewidth=1)	
	ax[2].plot(t_list,dds_list,linestyle='--', linewidth=1)	
	ax[3].plot(t_list,ddds_list,linestyle='--', linewidth=1)	
		
	
	
	print("Trajectory Time : ",t_list[-1])

def drawTraj(sg,traj,number):
	t_list = np.linspace(0,traj.tt,number)
	s_list = []
	ds_list = []
	dds_list = []
	ddds_list = []
	state_list = []
	for j in range(len(t_list)):
		val = sg.generate(traj,t_list[j]);	
		s_list.append(val[0])
		ds_list.append(val[1])
		dds_list.append(val[2])
		ddds_list.append(val[3])
		state_list.append(val[4]+1)

	fig, ax = plt.subplots(4,1)
	fig.tight_layout() 
	state_list = np.array(state_list);
	t_list = np.array(t_list);
	s_list = np.array(s_list);
	ds_list = np.array(ds_list);
	dds_list = np.array(dds_list);
	ddds_list = np.array(ddds_list);
	color_list = np.array([[1,0,0],[1,0.5,0],[0,0,1],[0,1,0],[0,0,1],[1,0.5,0],[1,0,0]])
	t0 = 0
	try:
		t1 = t_list[state_list==1][-1]
	except:
		t1 = t0
	try:
		t2 = t_list[state_list==2][-1]
	except:
		t2 = t1
	try:
		t3 = t_list[state_list==3][-1]
	except:
		t3 = t2
	try:
		t4 = t_list[state_list==4][-1]
	except:
		t4 = t3		
	try:		
		t5 = t_list[state_list==5][-1]
	except:
		t5 = t4		
	try:
		t6 = t_list[state_list==6][-1]
	except:
		t6 = t5		
	try:
		t7 = t_list[state_list==7][-1]
	except:
		t7 = t6		

	for i in range(1,8):
		ax[0].plot(t_list[state_list==i],s_list[state_list==i],color= color_list[i-1,:])
		ax[0].set_title("s")
		ax[0].axvline(x=t1, color='k', linestyle=':', linewidth=0.1)
		ax[0].axvline(x=t2, color='k', linestyle=':', linewidth=0.1)
		ax[0].axvline(x=t3, color='k', linestyle=':', linewidth=0.1)
		ax[0].axvline(x=t4, color='k', linestyle=':', linewidth=0.1)
		ax[0].axvline(x=t5, color='k', linestyle=':', linewidth=0.1)
		ax[0].axvline(x=t6, color='k', linestyle=':', linewidth=0.1)	
		ax[0].axvline(x=t7, color='k', linestyle=':', linewidth=0.1)		
		ax[0].set_xticks([t0,t1,t2,t3,t4,t5,t6,t7])
		ax[1].plot(t_list[state_list==i],ds_list[state_list==i],color= color_list[i-1,:])
		ax[1].set_title("ds")		
		ax[1].axvline(x=t1, color='k', linestyle=':', linewidth=0.1)
		ax[1].axvline(x=t2, color='k', linestyle=':', linewidth=0.1)
		ax[1].axvline(x=t3, color='k', linestyle=':', linewidth=0.1)
		ax[1].axvline(x=t4, color='k', linestyle=':', linewidth=0.1)
		ax[1].axvline(x=t5, color='k', linestyle=':', linewidth=0.1)
		ax[1].axvline(x=t6, color='k', linestyle=':', linewidth=0.1)		
		ax[1].axvline(x=t7, color='k', linestyle=':', linewidth=0.1)		
		ax[1].set_xticks([t0,t1,t2,t3,t4,t5,t6,t7])

		ax[2].plot(t_list[state_list==i],dds_list[state_list==i],color= color_list[i-1,:])
		ax[2].set_title("dds")

		ax[2].axvline(x=t1, color='k', linestyle=':', linewidth=0.1)
		ax[2].axvline(x=t2, color='k', linestyle=':', linewidth=0.1)
		ax[2].axvline(x=t3, color='k', linestyle=':', linewidth=0.1)
		ax[2].axvline(x=t4, color='k', linestyle=':', linewidth=0.1)
		ax[2].axvline(x=t5, color='k', linestyle=':', linewidth=0.1)
		ax[2].axvline(x=t6, color='k', linestyle=':', linewidth=0.1)				
		ax[2].axvline(x=t7, color='k', linestyle=':', linewidth=0.1)		
		ax[2].set_xticks([t0,t1,t2,t3,t4,t5,t6,t7])

		ax[3].plot(t_list[state_list==i],ddds_list[state_list==i],color= color_list[i-1,:])
		ax[3].set_title("ddds")

		ax[3].axvline(x=t1, color='k', linestyle=':', linewidth=0.1)
		ax[3].axvline(x=t2, color='k', linestyle=':', linewidth=0.1)
		ax[3].axvline(x=t3, color='k', linestyle=':', linewidth=0.1)
		ax[3].axvline(x=t4, color='k', linestyle=':', linewidth=0.1)
		ax[3].axvline(x=t5, color='k', linestyle=':', linewidth=0.1)
		ax[3].axvline(x=t6, color='k', linestyle=':', linewidth=0.1)				
		ax[3].axvline(x=t7, color='k', linestyle=':', linewidth=0.1)	
		ax[3].set_xticks([t0,t1,t2,t3,t4,t5,t6,t7])	
	print("Trajectory Time : ",t_list[-1])
	plt.show()
def drawTrajList(sg,traj_list,number):
	fig, ax = plt.subplots(4,1)
	fig.tight_layout() 	
	for i in range(len(traj_list)):
		drawTraj_(sg, traj_list[i],number,fig,ax)
	plt.show()
