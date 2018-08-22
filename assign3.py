import pandas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

#import matplotlib.colors.Colormap as cm
path = "/home/shyam8/Sem2/DV/a1-dataset-indian-ocean-consolidated/temp1.csv"
df = pandas.read_csv(path)
arr=np.asarray(df)
print(type(arr[0][0]))
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
		if(arr[i][j]!=out):
			sum1+=arr[i][j]

for i in range(len(arr)):
	for j in range(len(arr[0])):
		if(arr[i][j]!=out):
			arr[i][j]=(arr[i][j]/sum1)*255
		else:
			arr[i][j]=((out-1)/sum1)*0
X=range(len(arr))
Y=range(len(arr[0]))
arr = np.ma.array(arr)
threshold = out
arr_masked = np.ma.masked_where(arr < threshold, arr)
print(arr_masked)
#arr = np.ma.masked_greater(arr, maxi)
print(arr[0][:10])

#arr=np.transpose(arr)
#plt.cm(arr,cmap="rainbow")
plt.pcolor(Y, X, arr_masked, cmap=plt.cm.get_cmap('rainbow'),vmin=maxi, vmax=outlier)
plt.colorbar()
#plt.imshow(arr,cmap="rainbow")
plt.show()


