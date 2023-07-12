from .printer import Printer
from .obj import DisplayObj
from PIL import Image
import contextily as ctx
import matplotlib.pyplot as plt
import geopandas
import io
class CartoPrinter(Printer):
    def __init__(self,geojson:dict, title: DisplayObj, infos: list, logo:Image=None):
        super().__init__(None, title, infos, logo)
        
        # self.map = ctx.providers.GeoportailFrance.plan(apikey='decouverte')
        self.map = ctx.providers.OpenStreetMap.France()
        self.geogson = geojson




    def __pre_process__(self, schema="schema_1", dist_dir="./dist"):
        # Load data
        gdf = geopandas.GeoDataFrame.from_features(self.geogson)
        geoseries = geopandas.GeoSeries(gdf.geometry)
        # Set crs
        geoseries.crs = "EPSG:4326"

        # Get bound of the data
        bounds = geoseries.total_bounds

        # Set plt rcParams for figure size and dpi at high resolution
        plt.rcParams['figure.figsize'] = (10, 10)
        plt.rcParams['figure.autolayout'] = True
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300
        plt.rcParams['font.size'] = 5

        self.progress.next(25)
        #Plot data
        plt.figure()
        ax = geoseries.plot(edgecolor='black', color='red')
        ax.set_rasterized(True)
        # Set bounds with a margin #TODO: set  margin relatively of the distance between the points
        ax.set_xlim(bounds[0]-0.01, bounds[2]+0.01)
        ax.set_ylim(bounds[1]-0.01, bounds[3]+0.01)
        self.progress.next(25)
        # Add basemap with high resolution
        ctx.add_basemap(ax, crs=geoseries.crs, source=self.map)
        self.progress.next(25)
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0, dpi=300)
        self.progress.next(25)

        self.content = Image.open(img_buf)
