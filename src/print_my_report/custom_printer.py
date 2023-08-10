from .printer import Printer
from .obj import DisplayObj
from PIL import Image
import contextily as ctx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib
import geopandas
import io
class CartoPrinter(Printer):
    def __init__(self,geojsons:list[dict[str,str]], title: DisplayObj, infos: list[DisplayObj], logo:Image=None, map:str = None, aspect_ratio:float = 1.3, legends: list[dict[str,str]] = [], **kwargs):
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

        kwargs: dict
            custom_crs : str
                the crs to use for the map
        '''
        super().__init__(None, title, infos, logo)
        matplotlib.use('Agg')
        self.map = ctx.providers.GeoportailFrance.plan(apikey='decouverte') if map is None else map
        

        for geojson in geojsons:
            if not 'geojson' in geojson:
                raise ValueError("geojsons needs to contains a key 'path' with the path to the geojson file")
            

        
        self.geojsons = geojsons
        self.aspect_ratio = aspect_ratio
        self.legends = legends

        if 'custom_crs' in kwargs:
            self.custom_crs = kwargs['custom_crs']
        else:
            self.custom_crs = "EPSG:2154"



    def __pre_process__(self, schema="schema_1", dist_dir="./dist"):
            # Load data
        df : list[geopandas.GeoDataFrame] = []
        gs : list[geopandas.GeoSeries] = []
        for geojson,i in zip(self.geojsons,range(len(self.geojsons))):
            df.append(geopandas.read_file(geojson['geojson']))
            gs.append(geopandas.GeoSeries(df[i].geometry).to_crs(self.custom_crs))
            
            #remove the path from the dict
            del geojson['geojson']
        

        geoseries = geopandas.GeoSeries(df[0].geometry)

        # Set crs
        geoseries = gs[0]
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
            gs[i].plot(ax=ax, color=df[i]['color'], **self.geojsons[i])
        self.progress.next(25)


        # Center the map on the data with a margin 1/8 of the distance between bounds but the bound must be in the map
        # For the x and y limits they must be set as preserving a ration of 1.3
        # The aspect ratio is the ratio between the width and the height of the map

        # Get the distance between the bounds
        x_dist = bounds[2] - bounds[0]
        y_dist = bounds[3] - bounds[1]

        if x_dist > y_dist:
            #Case where the width is bigger than the height
            #The height is the limiting factor

            #Get the new height
            new_height = x_dist / self.aspect_ratio

            #Get the new y limits
            y_min = bounds[1] - (new_height - y_dist) / 2
            y_max = bounds[3] + (new_height - y_dist) / 2

            #Set the new limits
            ax.set_ylim(y_min, y_max)
            ax.set_xlim(bounds[0] - x_dist / 8, bounds[2] + x_dist / 8)

        else:
            #Case where the height is bigger than the width
            #The width is the limiting factor

            #Get the new width
            new_width = y_dist * self.aspect_ratio

            #Get the new x limits
            x_min = bounds[0] - (new_width - x_dist) / 2
            x_max = bounds[2] + (new_width - x_dist) / 2

            #Set the new limits
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(bounds[1] - y_dist / 8, bounds[3] + y_dist / 8)




 
        



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
