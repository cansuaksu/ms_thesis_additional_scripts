from shapely.geometry import mapping
import xarray as xr
import rioxarray
import geopandas as gpd
import numpy as np
import pandas as pd
import statistics as st


shp_path_alps='D:/Drivers/GGIT/SK_TEZ_110622/Cansu_Tez_Draft/04_Sentinel_2_Tiles_Borders/T32TPS_Alps.shp'
shp_path_tatra='D:/Drivers/GGIT/SK_TEZ_110622/Cansu_Tez_Draft/04_Sentinel_2_Tiles_Borders/T34UCV_Tatra.shp'
shp_path_turkey='D:/Drivers/GGIT/SK_TEZ_110622/Cansu_Tez_Draft/04_Sentinel_2_Tiles_Borders/T37TFE_Turkey.shp'
list_range = list(range(776,865)) #covering from January 1990 to December 2021


#lists for individual months - needed to get the mean of the months for 31 years for each region
list_january = list (range(480,865,12))
list_february = list (range(480+1,865,12))
list_march = list (range(480+2,865,12))
list_april = list (range(480+3,865,12))
list_may = list (range(480+4,865,12))
list_june = list (range(480+5,865,12))
list_july = list (range(480+6,865,12))
list_august = list(range(480+7,865,12))
list_september = list (range(480+8,865,12))
list_october = list (range(480+9,865,12))
list_november = list (range(480+10,865,12))
list_december = list (range(480+11,865,12))




#region= "alps", "tatra", "turkey"
def get_raster_sde(i):
# Open the NetCDF

    sde_full = xr.open_dataset('E:/indirilenler/sde_full.nc')
    sde= sde_full['sde']
    sde.rio.write_crs("epsg:4326", inplace=True)
#(Optional) convert longitude from (0-360) to (-180 to 180) (if required)
    sde.coords['longitude'] = (sde.coords['longitude'] + 180) % 360 - 180
    sde = sde.sortby(sde.longitude)

#Define lat/long
    sde = sde.rio.set_spatial_dims('longitude', 'latitude')
    sde[i].rio.to_raster("E:/indirilenler/sde/sde_" + str(i) + ".tiff", compress='LZMA', tiled=True, dtype="int32")



def clip_and_get_mean_sde(shp_path, i):
    sde_alps_try = rioxarray.open_rasterio("E:/indirilenler/sde/sde_"+str(i)+".tiff",
                                    masked=True).squeeze()
    shapes_alps = gpd.read_file(shp_path)
    sde_clipped = sde_alps_try.rio.clip(shapes_alps.geometry.apply(mapping), shapes_alps.crs)
    sde_array = sde_clipped.to_masked_array().flatten().compressed()
    sde_array = list(sde_array)
    # return sde_array
    return np.mean(sde_array)

# '''GET RASTERS FIRST'''
# for i in list_range:
#     get_raster_sde(i)
#     print("done:" + str(i))

'''MEAN OF MONTHS FOR ALPINE REGION'''

# mean_list_sde_alps_january=[]
# for i in list_january:
#     mean_list_sde_alps_january.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_sde_alps_february=[]
# for i in list_february:
#     mean_list_sde_alps_february.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_sde_alps_march=[]
# for i in list_march:
#     mean_list_sde_alps_march.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_sde_alps_april=[]
# for i in list_april:
#     mean_list_sde_alps_april.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_sde_alps_may=[]
# for i in list_may:
#     mean_list_sde_alps_may.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_sde_alps_june=[]
# for i in list_june:
#     mean_list_sde_alps_june.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_sde_alps_july=[]
# for i in list_july:
#     mean_list_sde_alps_july.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_sde_alps_august=[]
# for i in list_august:
#     mean_list_sde_alps_august.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_sde_alps_september=[]
# for i in list_september:
#     mean_list_sde_alps_september.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
#
# mean_list_sde_alps_october=[]
# for i in list_october:
#     mean_list_sde_alps_october.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
#
# mean_list_sde_alps_november=[]
# for i in list_november:
#     mean_list_sde_alps_november.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
# #
# mean_list_sde_alps_december=[]
# for i in list_december:
#     mean_list_sde_alps_december.append(clip_and_get_mean_sde(shp_path_alps, i))
#     print("done:" + str(i))
#
# alps_sde= {'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#         'Means': [st.mean(mean_list_sde_alps_january), st.mean(mean_list_sde_alps_february), st.mean(mean_list_sde_alps_march), st.mean(mean_list_sde_alps_april), st.mean(mean_list_sde_alps_may), st.mean(mean_list_sde_alps_june), st.mean(mean_list_sde_alps_july), st.mean(mean_list_sde_alps_august), st.mean(mean_list_sde_alps_september), st.mean(mean_list_sde_alps_october), st.mean(mean_list_sde_alps_november), st.mean(mean_list_sde_alps_december)]}
# alps_sde =pd.DataFrame(alps_sde).to_csv("E:/indirilenler/sde/alps_sde_means.csv")

'''MEAN OF MONTHS FOR TATRA MOUNTAINS'''
#
# mean_list_sde_tatra_january=[]
# for i in list_january:
#     mean_list_sde_tatra_january.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_sde_tatra_february=[]
# for i in list_february:
#     mean_list_sde_tatra_february.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_sde_tatra_march=[]
# for i in list_march:
#     mean_list_sde_tatra_march.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_sde_tatra_april=[]
# for i in list_april:
#     mean_list_sde_tatra_april.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_sde_tatra_may=[]
# for i in list_may:
#     mean_list_sde_tatra_may.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_sde_tatra_june=[]
# for i in list_june:
#     mean_list_sde_tatra_june.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_sde_tatra_july=[]
# for i in list_july:
#     mean_list_sde_tatra_july.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_sde_tatra_august=[]
# for i in list_august:
#     mean_list_sde_tatra_august.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_sde_tatra_september=[]
# for i in list_september:
#     mean_list_sde_tatra_september.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
#
# mean_list_sde_tatra_october=[]
# for i in list_october:
#     mean_list_sde_tatra_october.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
#
# mean_list_sde_tatra_november=[]
# for i in list_november:
#     mean_list_sde_tatra_november.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
# #
# mean_list_sde_tatra_december=[]
# for i in list_december:
#     mean_list_sde_tatra_december.append(clip_and_get_mean_sde(shp_path_tatra, i))
#     print("done:" + str(i))
#
# tatra_sde= {'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#         'Means': [st.mean(mean_list_sde_tatra_january), st.mean(mean_list_sde_tatra_february), st.mean(mean_list_sde_tatra_march), st.mean(mean_list_sde_tatra_april), st.mean(mean_list_sde_tatra_may), st.mean(mean_list_sde_tatra_june), st.mean(mean_list_sde_tatra_july), st.mean(mean_list_sde_tatra_august), st.mean(mean_list_sde_tatra_september), st.mean(mean_list_sde_tatra_october), st.mean(mean_list_sde_tatra_november), st.mean(mean_list_sde_tatra_december)]}
# tatra_sde =pd.DataFrame(tatra_sde).to_csv("E:/indirilenler/sde/tatra_sde_means.csv")
# print(mean_list_sde_tatra_january)
# print(mean_list_sde_tatra_february)
# print(mean_list_sde_tatra_march)
# print(mean_list_sde_tatra_april)
# print(mean_list_sde_tatra_may)
# print(mean_list_sde_tatra_june)
# print(mean_list_sde_tatra_july)
# print(mean_list_sde_tatra_august)
# print(mean_list_sde_tatra_september)
# print(mean_list_sde_tatra_october)
# print(mean_list_sde_tatra_november)
# print(mean_list_sde_tatra_december)
'''MEAN OF MONTHS FOR KAÇKAR MOUNTAINS'''

# mean_list_sde_kackar_january=[]
# for i in list_january:
#     mean_list_sde_kackar_january.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_sde_kackar_february=[]
# for i in list_february:
#     mean_list_sde_kackar_february.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_sde_kackar_march=[]
# for i in list_march:
#     mean_list_sde_kackar_march.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_sde_kackar_april=[]
# for i in list_april:
#     mean_list_sde_kackar_april.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_sde_kackar_may=[]
# for i in list_may:
#     mean_list_sde_kackar_may.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_sde_kackar_june=[]
# for i in list_june:
#     mean_list_sde_kackar_june.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_sde_kackar_july=[]
# for i in list_july:
#     mean_list_sde_kackar_july.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_sde_kackar_august=[]
# for i in list_august:
#     mean_list_sde_kackar_august.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_sde_kackar_september=[]
# for i in list_september:
#     mean_list_sde_kackar_september.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
#
# mean_list_sde_kackar_october=[]
# for i in list_october:
#     mean_list_sde_kackar_october.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
#
# mean_list_sde_kackar_november=[]
# for i in list_november:
#     mean_list_sde_kackar_november.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
# #
# mean_list_sde_kackar_december=[]
# for i in list_december:
#     mean_list_sde_kackar_december.append(clip_and_get_mean_sde(shp_path_turkey, i))
#     print("done:" + str(i))
#
#kackar_sde= {'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#         'Means': [st.mean(mean_list_sde_kackar_january), st.mean(mean_list_sde_kackar_february), st.mean(mean_list_sde_kackar_march), st.mean(mean_list_sde_kackar_april), st.mean(mean_list_sde_kackar_may), st.mean(mean_list_sde_kackar_june), st.mean(mean_list_sde_kackar_july), st.mean(mean_list_sde_kackar_august), st.mean(mean_list_sde_kackar_september), st.mean(mean_list_sde_kackar_october), st.mean(mean_list_sde_kackar_november), st.mean(mean_list_sde_kackar_december)]}
# kackar_sde =pd.DataFrame(kackar_sde).to_csv("E:/indirilenler/sde/kackar_sde_means.csv")

def get_raster_t2m(i):
#Open the NetCDF

    sde_full = xr.open_dataset('E:/indirilenler/t2m_full.nc')
    sde= sde_full['t2m']
    sde.rio.write_crs("epsg:4326", inplace=True)
#(Optional) convert longitude from (0-360) to (-180 to 180) (if required)
    sde.coords['longitude'] = (sde.coords['longitude'] + 180) % 360 - 180
    sde = sde.sortby(sde.longitude)

#Define lat/long
    sde = sde.rio.set_spatial_dims('longitude', 'latitude')
#Save individual rasters
    sde[i].rio.to_raster("E:/indirilenler/t2m/t2m_" + str(i) + ".tiff", compress='LZMA', tiled=True, dtype="int32")

def clip_and_get_mean_t2m(shp_path, i):
    sde_alps_try = rioxarray.open_rasterio("E:/indirilenler/t2m/t2m_"+str(i)+".tiff",
                                    masked=True).squeeze()
    shapes_alps = gpd.read_file(shp_path)
    sde_clipped = sde_alps_try.rio.clip(shapes_alps.geometry.apply(mapping), shapes_alps.crs)
    sde_array = sde_clipped.to_masked_array().compressed()
    sde_array = list(sde_array)
    return np.mean(sde_array)

# '''GET RASTERS FIRST'''
# for i in list_range:
#     get_raster_t2m(i)
#     print("done:" + str(i))
'''MEAN OF MONTHS FOR ALPINE REGION'''

# mean_list_t2m_alps_january=[]
# for i in list_january:
#     mean_list_t2m_alps_january.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_t2m_alps_february=[]
# for i in list_february:
#     mean_list_t2m_alps_february.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_t2m_alps_march=[]
# for i in list_march:
#     mean_list_t2m_alps_march.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_t2m_alps_april=[]
# for i in list_april:
#     mean_list_t2m_alps_april.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_t2m_alps_may=[]
# for i in list_may:
#     mean_list_t2m_alps_may.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_t2m_alps_june=[]
# for i in list_june:
#     mean_list_t2m_alps_june.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_t2m_alps_july=[]
# for i in list_july:
#     mean_list_t2m_alps_july.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_t2m_alps_august=[]
# for i in list_august:
#     mean_list_t2m_alps_august.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_t2m_alps_september=[]
# for i in list_september:
#     mean_list_t2m_alps_september.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
#
# mean_list_t2m_alps_october=[]
# for i in list_october:
#     mean_list_t2m_alps_october.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
#
# mean_list_t2m_alps_november=[]
# for i in list_november:
#     mean_list_t2m_alps_november.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
# #
# mean_list_t2m_alps_december=[]
# for i in list_december:
#     mean_list_t2m_alps_december.append(clip_and_get_mean_t2m(shp_path_alps, i))
#     print("done:" + str(i))
#
# alps_t2m= {'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#         'Means': [st.mean(mean_list_t2m_alps_january), st.mean(mean_list_t2m_alps_february), st.mean(mean_list_t2m_alps_march), st.mean(mean_list_t2m_alps_april), st.mean(mean_list_t2m_alps_may), st.mean(mean_list_t2m_alps_june), st.mean(mean_list_t2m_alps_july), st.mean(mean_list_t2m_alps_august), st.mean(mean_list_t2m_alps_september), st.mean(mean_list_t2m_alps_october), st.mean(mean_list_t2m_alps_november), st.mean(mean_list_t2m_alps_december)]}
# alps_t2m =pd.DataFrame(alps_t2m).to_csv("E:/indirilenler/t2m/alps_t2m_means.csv")

'''MEAN OF MONTHS FOR TATRA MOUNTAINS'''
#
# mean_list_t2m_tatra_january=[]
# for i in list_january:
#     mean_list_t2m_tatra_january.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_t2m_tatra_february=[]
# for i in list_february:
#     mean_list_t2m_tatra_february.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_t2m_tatra_march=[]
# for i in list_march:
#     mean_list_t2m_tatra_march.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_t2m_tatra_april=[]
# for i in list_april:
#     mean_list_t2m_tatra_april.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_t2m_tatra_may=[]
# for i in list_may:
#     mean_list_t2m_tatra_may.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_t2m_tatra_june=[]
# for i in list_june:
#     mean_list_t2m_tatra_june.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_t2m_tatra_july=[]
# for i in list_july:
#     mean_list_t2m_tatra_july.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_t2m_tatra_august=[]
# for i in list_august:
#     mean_list_t2m_tatra_august.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_t2m_tatra_september=[]
# for i in list_september:
#     mean_list_t2m_tatra_september.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
#
# mean_list_t2m_tatra_october=[]
# for i in list_october:
#     mean_list_t2m_tatra_october.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
#
# mean_list_t2m_tatra_november=[]
# for i in list_november:
#     mean_list_t2m_tatra_november.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
# #
# mean_list_t2m_tatra_december=[]
# for i in list_december:
#     mean_list_t2m_tatra_december.append(clip_and_get_mean_t2m(shp_path_tatra, i))
#     print("done:" + str(i))
#
# tatra_t2m= {'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#         'Means': [st.mean(mean_list_t2m_tatra_january), st.mean(mean_list_t2m_tatra_february), st.mean(mean_list_t2m_tatra_march), st.mean(mean_list_t2m_tatra_april), st.mean(mean_list_t2m_tatra_may), st.mean(mean_list_t2m_tatra_june), st.mean(mean_list_t2m_tatra_july), st.mean(mean_list_t2m_tatra_august), st.mean(mean_list_t2m_tatra_september), st.mean(mean_list_t2m_tatra_october), st.mean(mean_list_t2m_tatra_november), st.mean(mean_list_t2m_tatra_december)]}
# tatra_t2m =pd.DataFrame(tatra_t2m).to_csv("E:/indirilenler/t2m/tatra_t2m_means.csv")

'''MEAN OF MONTHS FOR KAÇKAR MOUNTAINS'''

# mean_list_t2m_kackar_january=[]
# for i in list_january:
#     mean_list_t2m_kackar_january.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_t2m_kackar_february=[]
# for i in list_february:
#     mean_list_t2m_kackar_february.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_t2m_kackar_march=[]
# for i in list_march:
#     mean_list_t2m_kackar_march.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_t2m_kackar_april=[]
# for i in list_april:
#     mean_list_t2m_kackar_april.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_t2m_kackar_may=[]
# for i in list_may:
#     mean_list_t2m_kackar_may.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_t2m_kackar_june=[]
# for i in list_june:
#     mean_list_t2m_kackar_june.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_t2m_kackar_july=[]
# for i in list_july:
#     mean_list_t2m_kackar_july.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_t2m_kackar_august=[]
# for i in list_august:
#     mean_list_t2m_kackar_august.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_t2m_kackar_september=[]
# for i in list_september:
#     mean_list_t2m_kackar_september.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
#
# mean_list_t2m_kackar_october=[]
# for i in list_october:
#     mean_list_t2m_kackar_october.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
#
# mean_list_t2m_kackar_november=[]
# for i in list_november:
#     mean_list_t2m_kackar_november.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
# #
# mean_list_t2m_kackar_december=[]
# for i in list_december:
#     mean_list_t2m_kackar_december.append(clip_and_get_mean_t2m(shp_path_turkey, i))
#     print("done:" + str(i))
#
# kackar_t2m= {'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#         'Means': [st.mean(mean_list_t2m_kackar_january), st.mean(mean_list_t2m_kackar_february), st.mean(mean_list_t2m_kackar_march), st.mean(mean_list_t2m_kackar_april), st.mean(mean_list_t2m_kackar_may), st.mean(mean_list_t2m_kackar_june), st.mean(mean_list_t2m_kackar_july), st.mean(mean_list_t2m_kackar_august), st.mean(mean_list_t2m_kackar_september), st.mean(mean_list_t2m_kackar_october), st.mean(mean_list_t2m_kackar_november), st.mean(mean_list_t2m_kackar_december)]}
# kackar_t2m =pd.DataFrame(kackar_t2m).to_csv("E:/indirilenler/t2m/kackar_t2m_means.csv")


def get_raster_tp(i):
#Open the NetCDF

    sde_full = xr.open_dataset('E:/indirilenler/tp_full.nc')
    sde= sde_full['tp']
    sde.rio.write_crs("epsg:4326", inplace=True)
#(Optional) convert longitude from (0-360) to (-180 to 180) (if required)
    sde.coords['longitude'] = (sde.coords['longitude'] + 180) % 360 - 180
    sde = sde.sortby(sde.longitude)

#Define lat/long
    sde = sde.rio.set_spatial_dims('longitude', 'latitude')
    sde[i].rio.to_raster("E:/indirilenler/tp/tp_" + str(i) + ".tiff", compress='LZMA', tiled=True, dtype="float64")

def clip_and_get_mean_tp(shp_path, i):


    sde_alps_try = rioxarray.open_rasterio("E:/indirilenler/tp/tp_"+str(i)+".tiff",
                                    masked=True).squeeze()
    shapes_alps = gpd.read_file(shp_path)
    sde_clipped = sde_alps_try.rio.clip(shapes_alps.geometry.apply(mapping), shapes_alps.crs)
    sde_array = sde_clipped.to_masked_array().compressed()
    sde_array=list(sde_array)
    return np.mean(sde_array)

# '''GET RASTERS FIRST'''
# for i in list_range:
#     get_raster_tp(i)
#     print("done:" + str(i))


'''MEAN OF MONTHS FOR ALPINE REGION'''

# mean_list_tp_alps_january=[]
# for i in list_january:
#     mean_list_tp_alps_january.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_tp_alps_february=[]
# for i in list_february:
#     mean_list_tp_alps_february.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_tp_alps_march=[]
# for i in list_march:
#     mean_list_tp_alps_march.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_tp_alps_april=[]
# for i in list_april:
#     mean_list_tp_alps_april.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_tp_alps_may=[]
# for i in list_may:
#     mean_list_tp_alps_may.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_tp_alps_june=[]
# for i in list_june:
#     mean_list_tp_alps_june.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_tp_alps_july=[]
# for i in list_july:
#     mean_list_tp_alps_july.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_tp_alps_august=[]
# for i in list_august:
#     mean_list_tp_alps_august.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
# mean_list_tp_alps_september=[]
# for i in list_september:
#     mean_list_tp_alps_september.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
#
# mean_list_tp_alps_october=[]
# for i in list_october:
#     mean_list_tp_alps_october.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
#
# mean_list_tp_alps_november=[]
# for i in list_november:
#     mean_list_tp_alps_november.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
# #
# mean_list_tp_alps_december=[]
# for i in list_december:
#     mean_list_tp_alps_december.append(clip_and_get_mean_tp(shp_path_alps, i))
#     print("done:" + str(i))
#
# alps_tp= {'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#         'Means': [np.nanmean(mean_list_tp_alps_january), st.mean(mean_list_tp_alps_february), st.mean(mean_list_tp_alps_march), st.mean(mean_list_tp_alps_april), st.mean(mean_list_tp_alps_may), st.mean(mean_list_tp_alps_june), st.mean(mean_list_tp_alps_july), st.mean(mean_list_tp_alps_august), st.mean(mean_list_tp_alps_september), st.mean(mean_list_tp_alps_october), st.mean(mean_list_tp_alps_november), np.nanmean(mean_list_tp_alps_december)]}
# alps_tp =pd.DataFrame(alps_tp).to_csv("E:/indirilenler/tp/alps_tp_means.csv")

'''MEAN OF MONTHS FOR TATRA MOUNTAINS'''

# mean_list_tp_tatra_january=[]
# for i in list_january:
#     mean_list_tp_tatra_january.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_tp_tatra_february=[]
# for i in list_february:
#     mean_list_tp_tatra_february.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_tp_tatra_march=[]
# for i in list_march:
#     mean_list_tp_tatra_march.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_tp_tatra_april=[]
# for i in list_april:
#     mean_list_tp_tatra_april.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_tp_tatra_may=[]
# for i in list_may:
#     mean_list_tp_tatra_may.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_tp_tatra_june=[]
# for i in list_june:
#     mean_list_tp_tatra_june.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_tp_tatra_july=[]
# for i in list_july:
#     mean_list_tp_tatra_july.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_tp_tatra_august=[]
# for i in list_august:
#     mean_list_tp_tatra_august.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
# mean_list_tp_tatra_september=[]
# for i in list_september:
#     mean_list_tp_tatra_september.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
#
# mean_list_tp_tatra_october=[]
# for i in list_october:
#     mean_list_tp_tatra_october.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
#
# mean_list_tp_tatra_november=[]
# for i in list_november:
#     mean_list_tp_tatra_november.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
# #
# mean_list_tp_tatra_december=[]
# for i in list_december:
#     mean_list_tp_tatra_december.append(clip_and_get_mean_tp(shp_path_tatra, i))
#     print("done:" + str(i))
#
# tatra_tp= {'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#         'Means': [np.nanmean(mean_list_tp_tatra_january), st.mean(mean_list_tp_tatra_february), st.mean(mean_list_tp_tatra_march), st.mean(mean_list_tp_tatra_april), st.mean(mean_list_tp_tatra_may), st.mean(mean_list_tp_tatra_june), st.mean(mean_list_tp_tatra_july), st.mean(mean_list_tp_tatra_august), st.mean(mean_list_tp_tatra_september), st.mean(mean_list_tp_tatra_october), st.mean(mean_list_tp_tatra_november), np.nanmean(mean_list_tp_tatra_december)]}
# tatra_tp =pd.DataFrame(tatra_tp).to_csv("E:/indirilenler/tp/tatra_tp_means.csv")

'''MEAN OF MONTHS FOR KAÇKAR MOUNTAINS'''

# mean_list_tp_kackar_january=[]
# for i in list_january:
#     mean_list_tp_kackar_january.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_tp_kackar_february=[]
# for i in list_february:
#     mean_list_tp_kackar_february.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_tp_kackar_march=[]
# for i in list_march:
#     mean_list_tp_kackar_march.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_tp_kackar_april=[]
# for i in list_april:
#     mean_list_tp_kackar_april.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_tp_kackar_may=[]
# for i in list_may:
#     mean_list_tp_kackar_may.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_tp_kackar_june=[]
# for i in list_june:
#     mean_list_tp_kackar_june.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_tp_kackar_july=[]
# for i in list_july:
#     mean_list_tp_kackar_july.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_tp_kackar_august=[]
# for i in list_august:
#     mean_list_tp_kackar_august.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
# mean_list_tp_kackar_september=[]
# for i in list_september:
#     mean_list_tp_kackar_september.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
#
# mean_list_tp_kackar_october=[]
# for i in list_october:
#     mean_list_tp_kackar_october.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
#
# mean_list_tp_kackar_november=[]
# for i in list_november:
#     mean_list_tp_kackar_november.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
# #
# mean_list_tp_kackar_december=[]
# for i in list_december:
#     mean_list_tp_kackar_december.append(clip_and_get_mean_tp(shp_path_turkey, i))
#     print("done:" + str(i))
#
# kackar_tp= {'Months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#         'Means': [np.nanmean(mean_list_tp_kackar_january), st.mean(mean_list_tp_kackar_february), st.mean(mean_list_tp_kackar_march), st.mean(mean_list_tp_kackar_april), st.mean(mean_list_tp_kackar_may), st.mean(mean_list_tp_kackar_june), st.mean(mean_list_tp_kackar_july), st.mean(mean_list_tp_kackar_august), st.mean(mean_list_tp_kackar_september), st.mean(mean_list_tp_kackar_october), st.mean(mean_list_tp_kackar_november), np.nanmean(mean_list_tp_kackar_december)]}
# kackar_tp =pd.DataFrame(kackar_tp).to_csv("E:/indirilenler/tp/kackar_tp_means.csv")










