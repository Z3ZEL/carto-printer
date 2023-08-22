from .obj import DisplayObj

def __dict_to_style__(d: dict):
    return " ".join([f"{k}:{v};" for k,v in d.items()])

def make_info_box_item(obj: DisplayObj):
    return f"""
    <div class="info-box-item">
        <div class="info-box-item-title" style="{__dict_to_style__(obj.title_options)}">{obj.title}</div>
        <div class="info-box-item-content" style="{__dict_to_style__(obj.content_options)}">{obj.content}</div>
    </div>
    """
def make_title_content(obj: DisplayObj):
    return f"""
    <div class="title-content">
        <div class="title-content-title" style="{__dict_to_style__(obj.title_options)}">{obj.title}</div>
        <div class="title-content-content" style="{__dict_to_style__(obj.content_options)}">{obj.content}</div>
    </div>
    """
def make_logo(custom_src="./assets/logo.png"):
    return f"""<img src={custom_src} alt='logo' id=logo>"""
def make_content(custom_src="./assets/content.png"):
    return f"""
    <img src="{custom_src}" alt="content" id=content>
    """