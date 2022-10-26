import rasterio
import fiona
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import rasterio.mask
import glob
import os

'''A POLYGON REPRESENTING PURE SNOW COVER SHOULD BE OBTAINED BEFOREHAND'''

path= "D:/Drivers/GGIT/SK_TEZ_110622/Cansu_Tez_Draft/02_TATRA/Work_Folder/23_Jan_2020_atmo_topo"
path_sc= "D:/Drivers/GGIT/SK_TEZ_110622/Cansu_Tez_Draft/02_TATRA/Work_Folder/23_Jan_2020_sc_only"



def pure_snow_polygon(path, path_sc, band_choice = "B02"):
    #THIS CODE IS FOR ATMOSPHERICALLY AND TOPOGRAPHICALLY CORRECTED IMAGES
    with fiona.open(path+"/Atmo_Topo_Check/puresnow.shp", "r") as shapefile:
        for feature in shapefile:
            shapes = [feature["geometry"]]

    with rasterio.open(path + "/S2_Bands_TIFF/"+ band_choice + ".tif") as src:
        out_image, out_trasform = rasterio.mask.mask(src, shapes, crop="True")
        out_meta = src.meta

    out_meta.update({
        'driver': 'Gtiff',
        'height': out_image.shape[1],
        'width': out_image.shape[2],
        'transform': out_trasform
    })
    with rasterio.open(path +"/Atmo_Topo_Check/" + band_choice + "_puresnow.tif", "w", **out_meta) as dst:
        dst.write(out_image)
    #THIS CODE IS FOR ORIGINAL/RESAMPLED ONLY IMAGES


    with fiona.open(path+"/Atmo_Topo_Check/puresnow.shp", "r") as shapefile:
        for feature in shapefile:
            shapes = [feature["geometry"]]

    with rasterio.open(path_sc + "/S2_Bands_TIFF/"+ band_choice + ".tif") as src:
        out_image, out_trasform = rasterio.mask.mask(src, shapes, crop="True")
        out_meta = src.meta

    out_meta.update({
        'driver': 'Gtiff',
        'height': out_image.shape[1],
        'width': out_image.shape[2],
        'transform': out_trasform
    })
    with rasterio.open(path +"/Atmo_Topo_Check/" + band_choice + "_puresnow_sconly.tif", "w", **out_meta) as dst:
        dst.write(out_image)

def plot_mean(path):
    b_2 = rasterio.open(path + "/Atmo_Topo_Check/" + 'B02_puresnow.tif').read().flatten()
    b_3 = rasterio.open(path + "/Atmo_Topo_Check/" + 'B03_puresnow.tif').read().flatten()
    b_4 = rasterio.open(path + "/Atmo_Topo_Check/" + 'B04_puresnow.tif').read().flatten()

    b2 = rasterio.open(path + "/Atmo_Topo_Check/" + 'B02_puresnow_sconly.tif').read().flatten()
    b3 = rasterio.open(path + "/Atmo_Topo_Check/" + 'B03_puresnow_sconly.tif').read().flatten()
    b4 = rasterio.open(path + "/Atmo_Topo_Check/" + 'B04_puresnow_sconly.tif').read().flatten()

    #nodata= -32768

    b_2 = b_2[b_2!=-32768]
    b_3 = b_3[b_3!=-32768]
    b_4 = b_4[b_4!=-32768]
    b2 = b2[b2!=-32768]
    b3 = b3[b3!=-32768]
    b4 = b4[b4!=-32768]

    mean_b_2= np.mean(b_2)/10000
    mean_b_3= np.mean(b_3)/10000
    mean_b_4= np.mean(b_4)/10000

    mean_b2= np.mean(b2)/10000
    mean_b3= np.mean(b3)/10000
    mean_b4= np.mean(b4)/10000


    x = ["band2(blue)","band3(green)","band4(red)"]
    y1=[mean_b_2,mean_b_3,mean_b_4]
    y2=[mean_b2,mean_b3,mean_b4]

    sns.lineplot(x=x, y=y1, legend="brief", label= "Atmospheric & Topographic Correction",color="red")
    sns.lineplot(x=x, y=y2, legend="brief", label="Original", color="blue")
    sns.set(rc = {'figure.figsize':(10,20)})
    plt.legend(loc="center")
    plt.yticks(np.arange(min(y2)+0.0003, max(y1), 0.02))
    plt.suptitle('TATRA - 23 January 2020') #change it as you go
    plt.xlabel('Sentinel-2 Bands')
    plt.ylabel('Reflectance Values')
    # function to show the plot
    # plt.show()
    plt.savefig("E:/TEZ/Presentations/070722/atmo_topo/Tatra_23_Jan_2020_new.png")

# band_names = ['B02', 'B03', 'B04']
#
# for name in band_names:
#     pure_snow_polygon(path, path_sc, band_choice=name)

plot_mean(path)





