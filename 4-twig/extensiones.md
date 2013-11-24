# Extensiones

Las extensiones de Twig permiten encapsular porciones de código en clases reusables y bien organizadas. Por ejemplo, imaginemos el siguiente código:

```html
<p class="recipe {% if recipe.easy %}easy{% elseif recipe.normal %}normal{% else %}hard{% endif %}">
    {{ ... }}
</p>
```

El código anterior asigna una clase CSS en función de la dificultad de la receta. Esta operación es bastante común y es posible que tengamos que repetirla en otras construcciones HTML, como elementos de un listado.

```html
<ul>
    {% for recipe in recipes %}
        <li class="recipe {% if recipe.easy %}easy{% elseif recipe.normal %}normal{% else %}hard{% endif %}"></li>
    {% endif %}
</ul>
```

Para encapsular el código en clases reusables, una opción es crear una extensión.


## Extension Class

Empezaremos creando la extensión de nuestro bundle.

```php
// src/My/RecipesBundle/Twig/RecipesExtension.php

namespace My\RecipesBundle\Twig;

use My\RecipesBundle\Entity\Recipe;

class RecipesExtension extends \Twig_Extension
{
    public function getFilters()
    {
        return array(
            new \Twig_SimpleFilter('cssClass', array($this, 'cssClass')),
        );
    }

    public function cssClass($recipe)
    {
        if ($recipe->isEasy()) {
            return 'easy';
        }
        if ($recipe->isNormal()) {
            return 'normal';
        }
        if ($recipe->isHard()) {
            return 'hard';
        }
        return 'unknown';
    }

    public function getName()
    {
        return 'my_recipes_extension';
    }
}

## Registrar la extensión

Para registrar una extensión basta con exponerla como servicio en el archivo `services.yml` del bundle y añadirle el tag `twig.extension` tal y como se muestra a continuación:

```yaml
# src/My/RecipesBundle/Resources/config/services.yml
services:
    my.twig.recipes_extension:
        class: My\RecipesBundle\Twig\RecipesExtension
        tags:
            - { name: twig.extension }
```

## Usar la extensión

Ya podemos utilizar el filtro `cssClass` de nuestra extensión y limpiar las plantillas del viejo código replicado.

```html
<p class="recipe {{ recipe|cssClass }}">
    {{ ... }}
</p>
```

```html
<ul>
    {% for recipe in recipes %}
        <li class="recipe {{ recipe|cssClass }}"></li>
    {% endif %}
</ul>
```
