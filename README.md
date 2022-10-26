# ms_thesis_additional_scripts

This repository is for additional Python scripts that I have used in my Master's thesis

- std_mean.py  - This is a script that I have used to obtain mean reflectance of a specific area for three visible bands, to check whether the Sentinel-2 image is atmospherically corrected or not

- nc.py - This is a script for ERA5 Land Monthly reanalysis data files

    1. The code converts the .nc data to individual rasters for each month (for 30 years of data - it is adjustable for any number of data)
    
    2. Code then proceeds to clip every raster with a polygon, and get the mean value for that area
    
    3. Code groups the means of clipped rasters into each month for 30 years of data, and obtain the average of these means
    
   For this study, this process is done for total precipitation, 2 m temperature and snow depth ERA5 Land Monthly reanalysis data.
    
