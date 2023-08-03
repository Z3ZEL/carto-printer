from .printer import Printer
from .obj import DisplayObj
from PIL import Image
import contextily as ctx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import geopandas
import io
class CartoPrinter(Printer):
    def __init__(self,geojsons:list[dict[str,str]], title: DisplayObj, infos: list[DisplayObj], logo:Image=None, map:str = None, aspect_ratio:float = 1.3, legends: list[dict[str,str]] = []):
        '''
        Create a new printer for a cartography

        Parameters
        ----------
        geojson: list of 
            geojsons to display, needs to contains a key 'geojson' with either the path to the geojson file, the str, or the geojson dict
            the geojson file needs to contains a property 'color' with the color of the geojson
            the rest of the properties in the dict will be passed to the plot function. The first element will be used for the bounds of the map

        title: DisplayObj
            title of the report

        infos: list
            list of DisplayObj to display as information

        logo: Image
            logo to display on the report

        map: str
            the path to a tiff file to use as a map

        aspect_ratio: float
            the aspect ratio of the map

        legends: list of dict
            list of legend to display on the map
            each key will be passed to the patch constructor


        '''
        super().__init__(None, title, infos, logo)
        
        self.map = ctx.providers.GeoportailFrance.plan(apikey='decouverte') if map is None else map
        

        for geojson in geojsons:
            if not 'geojson' in geojson:
                raise ValueError("geojsons needs to contains a key 'path' with the path to the geojson file")
            

        
        self.geojsons = geojsons
        self.aspect_ratio = aspect_ratio
        self.legends = legends



    def __pre_process__(self, schema="schema_1", dist_dir="./dist"):
            # Load data
        df : list[geopandas.GeoDataFrame] = []
        for geojson in self.geojsons:
            df.append(geopandas.read_file(geojson['geojson']))
            #remove the path from the dict
            del geojson['geojson']
        

        geoseries = geopandas.GeoSeries(df[0].geometry)

        # Set crs
        geoseries.crs = "EPSG:4326"

        # Get bound of the data
        bounds = geoseries.total_bounds

        # Set plt rcParams for figure size and dpi at high resolution
        plt.rcParams['figure.autolayout'] = True
        plt.rcParams['savefig.dpi'] = 500
        plt.rcParams['font.size'] = 5
  
        # Create figure and axes
        fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=500)
        self.progress.next(25)

        # Plot data
        for i in range(len(df)):
            df[i].plot(ax=ax, color=df[i]['color'], **self.geojsons[i])
        self.progress.next(25)


        # Center the map on the data with a margin 1/8 of the distance between bounds
        # For the x and y limits they must be set as preserving a ration of 1.3
        max_length = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        ax.set_xlim(bounds[0] - max_length/8, bounds[0] + max_length + max_length/8)
        ax.set_ylim(bounds[1] - max_length/8, bounds[1] + max_length*(1/self.aspect_ratio) + max_length/8)
        



        legend_elements = []

        for legend in self.legends: 
            l_type  = legend['type']
            del legend['type']
            if l_type == 'Line2D':
                legend_elements.append(Line2D([0], [0], **legend))
            elif l_type == 'Patch':
                legend_elements.append(Patch(**legend))


        ax.legend(handles=legend_elements, fontsize=15)

        ax.axis('off')

        ctx.add_basemap(ax, crs=geoseries.crs.to_string(), source=self.map)
        self.progress.next(25)


        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0)
        self.progress.next(25)

        self.content = Image.open(img_buf)
