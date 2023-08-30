
# Print My Report

A simple package to generate cool report with a content, header, and some info items.
You can manage the skeleton of your report with a html/css skeleton



---

[![Static Badge](https://img.shields.io/badge/Download-0.1.0-green)](https://github.com/Z3ZEL/print-my-report/releases/download/0.1.0/PrintMyReport-0.1.0.tar.gz)

## Installation

Install it with pip
```bash
  pip install https://github.com/Z3ZEL/print-my-report/releases/download/0.1.0/PrintMyReport-0.1.0.tar.gz
```
    
## Features

- Simple Printer 
- Carto Printer (Build a map report from geojson data)
- No Content Print (Build a empty report with no content only generated text for instance)




## Usage/Examples

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Survol</title>
</head>
<body>
    <div class="content">
        <div class="carto">
            <div class="carto-header">
                <div class="carto-logo">
                </div>
                <div class="carto-title"></div>
            </div>
            <div class="carto-content">
                
            </div>
        </div>
        <div class="info-box">
        </div>

    </div>
</body>
</html>
```


From this html sample skeleton

You need to respect class, the programm will search for them to fill with info you provided


```python
title=DisplayObj("Autorisation de survol en coeur de parc", "Plan de vol n°202")
info1=DisplayObj("Référence : ", "20002123")

printer  = NoContentPrinter(title,[info2],logo=Image.open('internal-test/logo.png'))
printer.build_pdf(dist_dir="./internal-test/dist", output_name="new2.pdf",output_dir="./internal-test/out")
```

> You can create `DisplayObje` to add some content
When you create a printer you need to assign title, items list, content and other extra options (as the logo for instance)

Then you can build the pdf specifying some output options
