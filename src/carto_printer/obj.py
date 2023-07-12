class DisplayObj():
    def __init__(self, title="", content="",title_options={}, content_options={}):
        self.title = title
        self.content = content
        self.title_options = title_options
        self.content_options = content_options

    def __str__(self):
        return self.name
