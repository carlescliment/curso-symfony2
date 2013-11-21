# Conceptos básicos

## Sintaxis

Twig proporciona tres tipos de marcas:

| Marca     | Ejemplo                                  | Propósito                            |
|-----------|------------------------------------------|--------------------------------------|
| {{ ... }} | {{ recipe.name }}                        | Mostrar contenido                    |
| {% ... %} | {% if expression %} ... {% endif %}      | Estructuras de control, evaluaciones |
| {# ... #} | {# Some comment here #}                  | Inserta un comentario HTML           |
| var&#124;filter| {{ recipe.created|date }}           | Aplica un filtro a la variable       |


## Renderizado

Una de las mayores ventajas de Twig es la seguridad que proporciona ante ataques de [Cross Site Scripting](http://en.wikipedia.org/wiki/Cross-site_scripting) (XSS). Imaginemos que, en la aplicación de recetas, un usuario malintencionado creara una receta con nombre `<script>alert('You have been hacked')</script>`. Imaginemos ahora una plantilla en PHP como la siguiente:

```php
<h1><?php echo $recipe->getName(); ?></h1>
<!-- The rest of the template here -->
```

El HTML en consecuencia sería:
```php
<h1><script>alert('You have been hacked')</script></h1>
<!-- The rest of the template here -->
```

Cualquier usuario que accediese a esa página ejecutaría un código JavaScript indeseado. ¡Las consecuencias podrían ser gravísimas!.

Afortunadamente, en Twig, todas las variables que mostremos a través de `{{ ... }}` serán escapadas automáticamente.
```php
<h1>&lt;script&gt;alert(&#39;You have been hacked&#39;)&lt;/script&gt;</h1>
<!-- The rest of the template here -->
```
