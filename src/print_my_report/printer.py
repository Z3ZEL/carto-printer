from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image
from weasyprint import HTML, CSS
from os import path

from progress.bar import IncrementalBar
from .obj import DisplayObj
from .custom_div import make_info_box_item, make_title_content, make_logo, make_content


class Printer():
    def __init__(self,content:Image, title: DisplayObj, infos: list, logo:Image=None):
        self.content = content
        self.title = title
        self.infos = infos
        self.logo = logo
        self.progress = IncrementalBar('Preprocessing', max=100)
    def __init_progress__(self,title="Building PDF"):
        self.progress.message = title
        self.progress.index = 0
        self.progress.finish()
    def __pre_process__(self,schema="schema_1", dist_dir="./dist"):
        pass
    def __build_html__(self, schema="schema_1", dist_dir="./dist"):
        if not './' in schema:
            path_to_html = Path(__file__).parent / "schemas" / f"{schema}.html"
        else:
            path_to_html = Path(schema+".html")
        
        with open(path_to_html, "r", encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        
        info_box = soup.find(attrs={"class":"info-box"})
        carto_title = soup.find(attrs={"class":"carto-title"})

        for item in self.infos:
            info_box.append(BeautifulSoup(make_info_box_item(item), 'html.parser'))
        
        carto_title.append(BeautifulSoup(make_title_content(self.title), 'html.parser'))

        asbolute_path = path.abspath("./") + "/" + dist_dir + "/assets/"


        if self.logo is not None:
            logo = soup.find(attrs={"class":"carto-logo"})
            logo.append(BeautifulSoup(make_logo(), 'html.parser'))
        

        content = soup.find(attrs={"class":"carto-content"})
        content.append(BeautifulSoup(make_content(), 'html.parser'))

        self.progress.next(25)
        return soup.prettify()
    def __build_css__(self, schema="schema_1", dist_dir="./dist"):
        if not './' in schema:
            path_to_css = Path(__file__).parent / "schemas" / f"{schema}.css"
        else:
            path_to_css = Path(schema+".css")
        with open(path_to_css, "r") as f:
            css = f.read()
        self.progress.next(25)
        return css
    def __build_dist__(self,dist_dir="./dist"):
        '''Build dist folder with assets'''
        #build logo & content
        Path(dist_dir + "/assets").mkdir(parents=True, exist_ok=True)
        if self.logo is not None:
            #Save img
            self.logo.save(Path(dist_dir + "/assets") / "logo.png")
        self.progress.next(50)
        self.content.save(Path(dist_dir + "/assets") / "content.png") 
        self.progress.next(50)

    def __remove_dist__(self,schema="schema_1", dist_dir="./dist"):
        '''Remove recursively dist schema.css assets folder and schema.html'''
        import os
        import shutil
        self.progress.next(50)
        shutil.rmtree(dist_dir+"/assets")
        self.progress.next(50)

    def build_pdf(self, schema="schema_1", dist_dir="./dist", output_name="output.pdf", output_dir="./dist", delete_dist=True):
        #Etape 1 : Preprocess
        self.__pre_process__(schema, dist_dir)


        ###
        self.__init_progress__(title="Building HTML & CSS")
        ###
        #Etape 2 : Build html & css


        self.__build_dist__(dist_dir)

        ###
        self.__init_progress__(title="Building PDF")
        ###
        #Etape 3 : Build pdf

        html = HTML(string=self.__build_html__(schema=schema,dist_dir=dist_dir), base_url=dist_dir)
        css = CSS(string=self.__build_css__(schema=schema,dist_dir=dist_dir), base_url=dist_dir)

        #check if output_dir exists if not create it
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        html.write_pdf(output_dir + "/" + output_name, stylesheets=[css], encoding="utf-8")
        self.progress.next(50)

        ###
        self.__init_progress__(title="Cleaning")
        ###
        #Etape 4 : Remove dist


        if delete_dist:
            self.__remove_dist__(schema, dist_dir)

        self.progress.finish()
        