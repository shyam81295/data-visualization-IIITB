import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import pandas as pd

np.random.seed(19680801)
npts = 200
ngridx = 100
ngridy = 200

data= pd.read_csv("/home/shyam8/Sem2/DV/a1-dataset-indian-ocean-consolidated/temp1.csv")
arr=np.asarray(data)

outlier=arr.max()
out=np.min(arr)
sum1=np.float(0)
maxi=np.float64(outlier)
print(type(maxi))
print(type(outlier))
for i in range(len(arr)):
	for j in range(len(arr[0])):
		if(arr[i][j]!=out):
			if(arr[i][j]<maxi):
				maxi=arr[i][j]
print(maxi)

for i in range(len(arr)):
	for j in range(len(arr[0])):
		if(arr[i][j]==out):
			arr[i][j]=np.nan

X=range(len(arr))
Y=range(len(arr[0]))

#arr_masked = np.ma.array(arr,mask=np.isnan(arr))

levels = [maxi,21.8,25,26,27,28,29.5,31,32.5,outlier]
contour = plt.contour(arr,levels,colors='k')
plt.clabel(contour,colors='k',fmt='%2.1f',fontsize=12)
CS = plt.contourf(arr,levels)
#plt.clabel(CS,inline=True,fmt='%1.1f',fontsize=10)
plt.colorbar(CS)
plt.show()

'''
arr_masked = np.ma.array(arr,mask=np.isnan(arr))

#arr_masked = np.transpose(arr_masked)

#z = data['TEMP']#temp

fig = plt.figure()
ax1=fig.add_subplot(111)

# -----------------------
# Interpolation on a grid
# -----------------------
# A contour plot of irregularly spaced data coordinates
# via interpolation on a grid.

# Create grid values first.
#xi = np.linspace(x.min()-1, x.max()+1, ngridx)
'''
