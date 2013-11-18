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
    command = "pandoc -o ./compiled/docx/" + theme + ".docx ";
    full_path_files = ' '.join([theme + "/" + file + ".md" for file in files])
    command += full_path_files + " -t docx"
    os.system(command)

for theme, files in themes.items() :
    convert(theme, files)