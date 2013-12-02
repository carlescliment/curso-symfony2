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

La función `render` permite incrustar peticiones a un controlador. Con ello conseguimos un menor acoplamiento entre los controladores y la vista.

Imaginemos que queremos mostrar las últimas recetas publicadas en un bloque inferior en todas las vistas de la aplicación. Podríamos empezar modificando el layout.

```html
<!-- app/Resources/views/base.html.twig -->
<!DOCTYPE html>
<html>
    <head>
        {% include '::header.html.twig' %}
    </head>
    <body>
        {% block body %}{% endblock %}

        <h3>Últimas recetas</h3>
        <ul>
            {% for recipe in last_recipes %}
                <li>{{ recipe.name }}</li>
            {% endfor %}
        </ul>

        {% block javascripts %}{% endblock %}
    </body>
</html>
```

Con esta construcción será necesario proporcionar la variable `last_recipes` a cualquier plantilla que extienda el layout.


```php
// src/My/RecipesBundle/Controller/DefaultController.php
class DefaultController extends Controller
{

    /**
     * @Template()
     */
    public function showAction(Recipe $recipe)
    {
        return array(
            'last_recipes' => $this->getLastRecipes(),
            'recipe' => $recipe);
    }

    /**
     * @Template()
     */
    public function topChefsAction()
    {
        // ...
        return array(
            'last_recipes' => $this->getLastRecipes(),
            'chefs' => $chefs);
    }


    // ...

    private function getLastRecipes()
    {
        $date = new \DateTime('-10 days');
        $repository = $this->getDoctrine()->getRepository('MyRecipesBundle:Recipe');
        return $repository->findPublishedAfter($date);
    }
}
```


En cada acción que añadamos tendremos que recordar añadir las últimas recetas. A medida que añadamos nuevos bloques en la aplicación la situación puede volverse más y más inmanejable. Para corregir esta situación utilizaremos un controlador _embebido_.

En primer lugar, cambiaremos el layout sustituyendo el bloque por una instrucción `render()`.

```html
<!-- app/Resources/views/base.html.twig -->
<!DOCTYPE html>
<html>
    <head>
        {% include '::header.html.twig' %}
    </head>
    <body>
        {% block body %}{% endblock %}

        {{ render(controller('MyRecipesBundle:Default:lastRecipes')) }}

        {% block javascripts %}{% endblock %}
    </body>
</html>
```

Escribiremos la acción `lastRecipesAction` en el controlador `Default`.

```php
    /**
     * @Template()
     */
    public function lastRecipesAction()
    {
        $date = new \DateTime('-10 days');
        $repository = $this->getDoctrine()->getRepository('MyRecipesBundle:Recipe');
        $recipes = $repository->findPublishedAfter($date);;
        return array('recipes' => $recipes);
    }
```


Y moveremos el código HTML a la plantilla correspondiente.

```html
<!-- src/My/RecipesBundle/Resources/views/lastRecipes.html.twig -->
<h3>Últimas recetas</h3>
<ul>
    {% for recipe in recipes %}
        <li>{{ recipe.name }}</li>
    {% endfor %}
</ul>
```

El último paso será limpiar las referencias a `last_recipes` del resto de acciones del controlador, obteniendo un código mucho más limpio y organizado.

