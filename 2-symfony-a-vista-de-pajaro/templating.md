# La vista

En capítulos anteriores hemos visto que el enrutado se encarga de distribuir las peticiones entre los distintos controladores. Los controladores, a su vez, extraen la información necesaria de la petición y construyen con ellos una respuesta. Aunque sería posible devolver HTML directamente desde el controlador, es recomendable delegar esta función al motor de plantillas.


El motor por defecto en Symfony 2 es *twig*.


```base.html.twig
<!DOCTYPE html>
<html>
    <head>
        <title>Welcome to Symfony!</title>
    </head>
    <body>
        <h1>{{ page_title }}</h1>

        <ul id="navigation">
            {% for item in navigation %}
                <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
            {% endfor %}
        </ul>
    </body>
</html>
```

En twig, las llaves dobles `{{ ... }}` se utilizan para mostrar una variable, mientras que la combinación de llave y paréntesis `{% ... %}` simboliza el uso de una expresión.


Tal y como vimos en el capítulo de controladores, para renderizar una plantilla desde un controlador utilizamos el método `render()`.

```
public function showAction($id)
{
    // ...
    return $this->render('MyRecipesBundle:Recipe:show.html.twig', array(
        'recipe' => $recipe,
    ));
}
```

Symfony buscará la plantilla show.html.twig indicada en la ruta `src\My\RecipesBundle\Resources\views\Recipe\show.html.twig`.

Baste con esta pequeña introducción a las vistas por ahora, más adelante dedicaremos un tema completo a Twig y el renderizado de plantillas.
