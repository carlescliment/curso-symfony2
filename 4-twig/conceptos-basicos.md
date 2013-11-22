# Conceptos básicos

## Sintaxis

Twig proporciona tres tipos de marcas:

| Marca     | Ejemplo                                  | Propósito                            |
|-----------|------------------------------------------|--------------------------------------|
| `{{ ... }}` | `{{ recipe.name }}`                        | Muestra contenido                    |
| `{% ... %}` | `{% if expression %} ... {% endif %}`      | Estructuras de control, evaluaciones |
| `{# ... #}` | `{# Some comment here #}`                  | Inserta un comentario HTML           |
| `var&#124;filter` | `{{ recipe.created&#124;date }}`      | Aplica un filtro a la variable       |


## Renderizado

Una de las mayores ventajas de Twig es la seguridad que proporciona ante ataques de [Cross Site Scripting](http://en.wikipedia.org/wiki/Cross-site_scripting) (XSS). Imaginemos que, en la aplicación de recetas, un usuario malintencionado creara una receta con nombre `<script>alert('You have been hacked')</script>`. Imaginemos ahora una plantilla en PHP como la siguiente:

```html
<h1><?php echo $recipe->getName(); ?></h1>
<!-- The rest of the template here -->
```

El HTML en consecuencia sería:
```html
<h1><script>alert('You have been hacked')</script></h1>
<!-- The rest of the template here -->
```

Cualquier usuario que accediese a esa página ejecutaría un código JavaScript indeseado. ¡Las consecuencias podrían ser gravísimas!.

Afortunadamente, en Twig, todas las variables que mostremos a través de `{{ ... }}` serán escapadas automáticamente.
```html
<h1>&lt;script&gt;alert(&#39;You have been hacked&#39;)&lt;/script&gt;</h1>
<!-- The rest of the template here -->
```

Twig también proporciona atajos al acceder a objetos. En twig, las llamadas `recipe.name` y `recipe.getName()` son equivalentes. Cuando utilizamos la forma abreviada, twig buscará en el objeto `recipe` un atributo público `name`. Si no lo encuentra, buscará los métodos `name()`, `getName()` e `isName()`. Debido a que existe una compilación y guardado en caché esta funcionalidad no tiene impacto en el rendimiento.


## Tags

### Estructuras de control

En Twig existen dos estructuras de control; bucles y condicionales. Los condicionales se representan con el *tag* `if`.

```twig
{% if recipe.difficulty == 'fácil' %}
  No tendrás problemas para concinar esta receta.
{% elseif recipe.difficulty == 'media' %}
  Esta receta requiere conocimientos avanzados de cocina.
{% else %}
  ¡Para dominar esta receta necesitas ser un Top Chef!
{% endif %}
```

Podremos recorrer arrays y colecciones con el tag `for`.

```twig
<h3>Recetas del autor</h3>
<ul>
    {% for recipe in author.recipes %}
        <li class="recipe">{{ recipe.name }}</li>
    {% endfor %}
</ul>
```

En los bucles podemos recuperar el número de la iteración con `loop.index` y `loop.index0`:

```twig
{% for recipe in author.recipes %}
  <li class="recipe {% if loop.index0 is odd %}odd{% else %}even{% endif %}">{{ recipe.name }}</li>
{% endfor %}
```



### Macros
Las macros equivales a funciones de un lenguaje de programación. Permite reusar componentes en varias plantillas.

```twig
{% macro list_recipes(recipes) %}
    <ul>
    {% for recipe in recipes %}
        <li class="recipe">{{ recipe.name }}</li>
    {% endfor %}
    </ul>
{% endmacro %}
```

De este modo, el ejemplo del tag `for` podría ser reescrito:

```twig
{% import "recipe_helpers.html" as helpers %}

<h3>Recetas del autor</h3>
{{ helpers.list_recipes(author.recipes) }}
```

### Otros tags

El tag `{% spaceless %}` eliminará los espacios en blanco, ofreciendo documentos HTML más limpios.

```twig
{% spaceless %}
  <div>
      <p>Aquí una linea de texto</p>
  </div>
{% endspaceless %}


<div><p>Aquí una linea de texto</p></div>
```


El tag `verbatim` permite que el texto que el texto en su interior se muestre tal cual en el cliente. Útil cuando queremos representar código.

```html
{% verbatim %}
    <div>Esto se mostrará tal cual, con los tags HTML visbiles.</div>
{% endverbatim %}
```

Twig ofrece una amplia variedad de tags documentada en [la web oficial](http://twig.sensiolabs.org/doc/tags/index.html).



## Filtros
Los filtros son funciones aplicamos sobre el contenido. Existe una [larga lista de filtros](http://twig.sensiolabs.org/doc/filters/index.html) proporcionados por Twig, a la que podemos añadir nuestros propios filtros mediante extensiones.

El elemento sobre el que apliquemos el filtro será tomado como input, y a partir de él se devolverá un output. Este output será el que finalmente se muestre en pantalla. Por ejemplo, el filtro `upper` convierte un texto a mayúsculas.

```html
<h1>{{ recipe.name|upper }}</h1>

<h1>POLLO AL PIL-PIL</h1>
```

## Funciones

En Twig pueden añadirse funciones que extiendan las capacidades de nuestras plantillas. Symfony añade algunas funciones al motor, como las relativas a la [gestión de formularios](http://symfony.com/doc/current/reference/forms/twig_reference.html#reference-form-twig-functions) o a la creación dinámica de enlaces. Para la generación de enlaces disponemos de las funciones `url` y `path`. Mientras que la primera genera una url completa, la segunda sólo añade una URI relativa.

```html
<a href="{{ url('recipes_show', { id: recipe.id }) }}">Ver</a>
<a href="http://misrecetas.com/recipes/55">Ver</a>

<a href="{{ path('recipes_show', { id: recipe.id }) }}">Ver</a>
<a href="/recipes/55">Ver</a>
```


## Caché

La primera vez que se renderiza una plantilla se genera un código equivalente en PHP. A este proceso se le denomina _compilado_. Las plantillas compiladas se almacenan por defecto en el directorio `app/cache/{environment}/twig`, donde `{environment}` es el nombre del entorno.

Para que los efectos se manifiesten cuando modifiquemos una plantilla, deberemos limpiar la caché. Esto no ocurre en los entornos de `test` y `dev`, donde la caché está desactivada.

