import numpy as np
import matplotlib.pyplot as plt
import itertools
from scipy.interpolate import griddata
from scipy import ndimage
def Mid_Bins(arr):
	new_array=[]
	for i in range(len(arr)-1):
		new_array.append((arr[i]+arr[i+1])/2.0)

	return new_array	

mlclass, mag, fbox2, fake_flux, host_background, fbox3, lmt_mag, see_ref, see_new, field, ccdid, medsky=np.genfromtxt('All_Fields.allfields', usecols=(4,28,51,29,41,52,67,12,62, 32, 33, 64), unpack=True)
########## Magnitude Efficiency
mlclass_mag=mlclass
mag_bin=np.linspace(13,23,30) #30 Bins between 13mag and 23mag
n_mag, bin_mag= np.histogram(mag, bins=mag_bin) #Binning ALL the data for a 'Total' array
n_mag2, bin_mag2 = np.histogram(mag[~np.isnan(mlclass_mag)], bins=mag_bin) #Binning the succesfully recovered data
n_mag_eff=np.divide(n_mag2.astype(float), n_mag.astype(float)) #Successful divided by total gives efficiency in each bin
tot_mag, totbm =np.histogram(mag, bins=mag_bin)
tot_mag= tot_mag.astype(float)/max(tot_mag)
########## FBox3 Efficiency
mlclass_fbox=mlclass
fbox_bin=np.logspace(-4.,3., 30)
##Filtering
fake_flux_filtered=fake_flux[host_background!=99999.99]
hb_filtered=host_background[host_background!=99999.99]
fbox3_filtered=fbox3[host_background!=99999.99]
mlclass_filtered=mlclass_fbox[host_background!=99999.99]
fr_total=(fbox3_filtered-(hb_filtered*9.))/fake_flux_filtered
fake_flux_good=fake_flux_filtered[~np.isnan(mlclass_filtered)]
fbox3_filtered_good=fbox3_filtered[~np.isnan(mlclass_filtered)]
hb_f_good=hb_filtered[~np.isnan(mlclass_filtered)]
fr_good=np.divide(np.subtract(fbox3_filtered_good,(hb_f_good*9.)),fake_flux_good)
nbox, nb= np.histogram(fr_total, bins=fbox_bin)
nboxg, nbg = np.histogram(fr_good, bins=fbox_bin)
nbox_eff=np.divide(nboxg.astype(float),nbox.astype(float))
tot_fbox, totfbb =np.histogram(fr_total, bins=mag_bin)
tot_fbox= tot_fbox.astype(float)/max(tot_fbox)
####### Limiting Magnitude
lmt_bin=np.linspace(19.0,21.5,30)
lmt_magb, lmt_mag_bin=np.histogram(lmt_mag, bins=lmt_bin)
lmt_magb2, lmt_mag_bin2=np.histogram(lmt_mag[~np.isnan(mlclass)], bins=lmt_bin)
lmt_eff=np.divide(lmt_magb2.astype(float), lmt_magb.astype(float))
tot_lmt= lmt_magb.astype(float)/max(lmt_magb)
#####Seeing New Seeing Ref
see_bin=np.linspace(0.5,2.2,30)
see_ref_arr=[]
see_ref_arr.append(see_ref[0])
for i in range(1,len(see_ref)):
	if np.isnan(see_ref[i]) == True:
		see_ref_arr.append(see_ref_arr[-1])
	else: see_ref_arr.append(see_ref[i])
see_ref=np.array(see_ref_arr)
see_frac=np.divide(see_new.astype(float),see_ref.astype(float))
see_tot, seeb1=np.histogram(see_frac, bins=see_bin)
see_frac_good, seeb2=np.histogram(see_frac[~np.isnan(mlclass)], bins=see_bin)
see_rat=np.divide(see_frac_good.astype(float),see_tot.astype(float))
#####Medsky
mskybin=np.logspace(2.2,4.2,30)
msky, mskyb= np.histogram(medsky, bins=mskybin)
msky2, mskyb2= np.histogram(medsky[~np.isnan(mlclass)], bins=mskybin)
msky_eff=np.divide(msky2.astype(float),msky.astype(float))

mag_bin=np.linspace(15,23,30)
fbox_bin=np.logspace(-4.,3., 30)
lmt_bin=np.linspace(19.,21.5,30)
see_bin=np.linspace(0.6,2.2,30)
mskybin=np.logspace(2.5,4.2,30)

mag_dig=np.digitize(mag, bins=mag_bin, right=True)
lmt_dig=np.digitize(lmt_mag, bins=lmt_bin,right=True)
see_dig=np.digitize(see_frac, bins=see_bin)
msky_dig=np.digitize(medsky, bins=mskybin)

grid=np.zeros((len(Mid_Bins(mag_bin)),len(Mid_Bins(lmt_bin))))
#grid2=np.zeros((len(Mid_Bins(mag_bin)),len(Mid_Bins(see_bin))))
#grid3=np.zeros((len(Mid_Bins(mag_bin)),len(Mid_Bins(mskybin))))

itlist=[range(0,len(Mid_Bins(mag_bin))),range(0,len(Mid_Bins(lmt_bin)))]
for i in itertools.product(*itlist):
	grid[i[0],i[1]]= np.divide(np.subtract(float(len(mag[(mag_dig==i[0]+1) & (lmt_dig==i[1]+1)])), float(len(mag[(np.isnan(mlclass_mag[((mag_dig==i[0]+1) & (lmt_dig==i[1]+1))]))]))) , float(len(mag[(mag_dig==i[0]+1) & (lmt_dig==i[1]+1)])))
p=[]
for i in range(0,len(Mid_Bins(mag_bin))):
    p.append([Mid_Bins(lmt_bin)[i], Mid_Bins(mag_bin)[i]])
#x=griddata([[Mid_Bins(lmt_bin)], [Mid_Bins(mag_bin)]],grid,([[16],[22]]), method='nearest')
#mag_interp=np.digitize()
x=ndimage.map_coordinates(grid, [[15.3], [22.9]], order=1)

print x

