import rioxarray
import xarray as xr
import geopandas as gpd

def preparar_para_recorte(dataset, crs="epsg:4326", xdim="lon", ydim="lat"):
    dataset = dataset.assign_coords(lon=(((dataset.lon + 180) % 360) - 180)).sortby(xdim)
    dataset = dataset.rio.set_spatial_dims(x_dim=xdim, y_dim=ydim) 
    dataset = dataset.rio.write_crs(crs)
    return dataset


shp_bacia = gpd.read_file("grande.shp").set_index("Name")

# leitura, preparação e recorte dos dados
dados = xr.open_dataset("precip.mon.mean.nc")
dados_preparados = preparar_para_recorte(dados.precip)
dados_recortados = dados_preparados.rio.clip([shp_bacia["geometry"]], "epsg:4326")