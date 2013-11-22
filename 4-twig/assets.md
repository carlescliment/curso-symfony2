# Generación de assets

Los assets son aquellos contenidos estáticos no HTML que se cargan durante el renderizado de la página web. Entre ellos se encuentran las hojas de estilo (CSS), los scripts de cliente (JavaScript), las imágenes, vídeos y otros contenidos multimedia.

## JavaScript y CSS

Para enlazar a contenidos estáticos se utiliza la función `asset`.

```html
<img src="{{ asset('images/logo.png') }}" alt="Mis recetas" />
<link href="{{ asset('css/main.css') }}" rel="stylesheet" type="text/css" />
<script src="{{ asset('js/main.js') }}" type="text/javascript"></script>
```

Los assets se almacenan en el directorio `web/`, por lo que la imagen del ejemplo se encontraría en `web/images/logo.png`.

## Versiones

En un navegador moderno, el contenido estático se almacena en una caché la primera vez que se accede a una aplicación web. De este modo se mejora el rendimiento evitando nuevas peticiones al servidor cada vez que se actualiza una página.

El problema ocurre cuando se despliega una nueva versión del archivo estático en el servidor. Si el cliente (navegador) ha cacheado una imagen en una visita anterior, los cambios en la imagen no se verán reflejados. Para evitar este problema, assetic permite proporcionar un sufijo de versión:

```
# app/config/config.yml
framework:
    # ...
    templating: { engines: ['twig'], assets_version: v2 }
```

Internamente, Symfony añade un _query parameter_ en la función `asset()` que invalida la caché del cliente. Es decir, el enlace en la imagen `images/logo.png` se convertirá en `images/logo.png?v2.

## Assetic Bundle

El versionado de imagenes obliga a cambiar manualmente la configuración de `assets_version` cada vez que desplegamos cambios en el contenido estático. El bundle Assetic facilita la gestión de los assets automatizando esta tarea, además de proporcionar otras interesantes ventajas.



### Tags javascripts y stylesheets

Los bloques `javascripts` y `stylesheets` permiten añadir varios archivos a la vez y referenciar bundles.

```html
{% javascripts '@MyRecipesBundle/Resources/public/js/*'
               'js/*'
               'vendor/fundation/fundation.js' %}
    <script type="text/javascript" src="{{ asset_url }}"></script>
{% endjavascripts %}
```

### Filtros

Assetic bundle también permite añadir filtros para procesar los archivos estáticos. Entre otras utilidades permite comprimir, ofuscar y procesar las hojas de estilo con SAAS o LESS.


El ejemplo más común de filtro es el `yui compressor`, que reúne todos los scripts en uno solo reduciendo el número de peticiones en la carga de una página.

```yaml
# app/config/config.yml
assetic:
    filters:
        yui_js:
            jar: "%kernel.root_dir%/Resources/java/yuicompressor.jar"
```

```html
{% javascripts '@MyRecipesBundle/Resources/public/js/*' filter='yui_js' %}
    <script type="text/javascript" src="{{ asset_url }}"></script>
{% endjavascripts %}
```

### Generación de assets

Una vez configurado el bundle assetic, podremos regenerar los contenidos estáticos (incluyendo el procesamiento con los filtros indicados) ejecutando el siguiente comando de consola:

```bash
$ app/console assetic:dump
```


Para una información más extensa, consulta la [documentación oficial](http://symfony.com/doc/current/cookbook/assetic/asset_management.html)