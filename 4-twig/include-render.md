# Vistas parciales

A medida que las aplicaciones crecen, las plantillas se van haciendo más y más complejas. Para garantizar su mantenimiento es conveniente limpiar de forma constante esas plantillas y controlar que se mantengan organizadas y en buena forma. Una buena forma de conseguirlo es a través de las vistas parciales.

En Symfony hay dos formas de utilizar vistas parciales; el tag `include` de Twig, y la función `render()` de la extensión Twig de Symfony.

## Include

El tag `include` carga y muestra el contenido de la plantilla que está siendo incluída. Permite organizar plantillas demasiado grandes y aislar fragmentos que pueden ser utilizados desde otras plantillas.

```html
<!-- app/Resources/views/base.html.twig -->
<!DOCTYPE html>
<html>
    <head>
        {% include '::header.html.twig' %}
    </head>
    <body>
        {% block body %}{% endblock %}
        {% block javascripts %}{% endblock %}
    </body>
</html>


<!-- app/Resources/views/header.html.twig -->
<meta charset="UTF-8" />
<title>{% block title %}Welcome!{% endblock %}</title>
{% block stylesheets %}{% endblock %}
<link rel="icon" type="image/x-icon" href="{{ asset('favicon.ico') }}" />
```

## Render

La función `render` permite incrustar peticiones a un controlador. Esto permite un menor acoplamiento entre los controladores y la vista.

Imaginemos que queremos mostrar las últimas recetas publicadas en un bloque inferior en todas las vistas de la aplicación.

(TO BE CONTINUED)
