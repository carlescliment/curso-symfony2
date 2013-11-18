import os

themes = { "1-introduccion" :
                ["la-evolucion-de-php-y-los-frameworks-mvc",
                 "ventajas-e-inconvenientes-de-los-frameworks",
                 "que-es-symfony",
                 "instalacion",
                 "directorios",
                 "composer",
                 "profiler-y-consola"],
           "2-symfony-a-vista-de-pajaro" :
                ["fundamentos-http",
                 "request-response",
                 "routing",
                 "controller",
                 "templating",
                 "model"],
         }

def convert(theme, files):
    full_path_files = [full_path(theme, file) for file in files]
    execute_conversion("docx", theme, full_path_files);

def full_path(theme, file):
    return theme + "/" + file + ".md"

def execute_conversion(doctype, theme, files):
    joined = ' '.join(files)
    command = "pandoc -o ./compiled/%s/%s.docx %s -t %s"%(doctype, theme, joined, doctype);
    os.system(command)


for theme, files in themes.items() :
    convert(theme, files)