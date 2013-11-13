# Routing

El sistema de enrutado relaciona los recursos indicados en las peticiones con los controladores encargados de gestionarlos.

Symfony carga todas las rutas del archivo de enrutado de la aplicación, normalmente en `app/config/routing.yml`. En este archivo podemos incluir referencias a otras fuentes junto con otras opciones de configuración.

```app/config/routing.yml
my_recipes:
    resource: "@MyRecipesBundle/Resources/config/routing.yml"
    prefix:   /
```

Los archivos de configuración pueden escribirse en `yml`, `xml` o `php`. En este material didáctico veremos todos los ejemplos en yml.

Para una información más completa y actualizada, consultad la [documentación oficial](http://symfony.com/doc/current/book/routing.html).

## Crear una ruta

Es una buena práctica almacenar las rutas proporcionadas por nuestros bundles en sus propios archivos `routing.yml`. De esta manera garantizaremos su portabilidad y mantendremos el enrutado más organizado. Una ruta está formada por dos atributos básicos: el patrón de la ruta o `path` y un diccionario que define el controlador a utilizar:

```
recipes_list:
    path:     /recipes/
    defaults: { _controller: MyRecipesBundle:Recipe:list }

recipes_show:
    path:     /recipes/{recipe_name}
    defaults: { _controller: MyRecipesBundle:Recipe:show }
```

Estas dos acciones están capturando las peticiones a los recursos especificados en `path` y enviándolas a sendos controladores. Los valores entre llaves simbolizan parámetros que son transferidos al controlador.

La clase controladora concreta y el método a utilizar se especifican según el siguiente convenio:

`Nombre de bundle : Nombre del controlador : Nombre de la acción`

De acuerdo con los anteriores ejemplos, se invocaría finalmente a los siguientes métodos:

```
My\RecipesBundle\Controller\RecipeController::list();
My\RecipesBundle\Controller\RecipeController::show($recipe_name);
```


## Parámetros opcionales

Si tenemos rutas que comparten una misma acción del controlador, podemos reorganizarlas utilizando parámetros por defecto. Por ejemplo, en la siguiente configuración:

```
recipes_list:
    path:      /recipes/
    defaults: { _controller: MyRecipesBundle:Recipe:list }

recipes_list_page:
    path:      /recipes/{page}
    defaults:  { _controller: MyRecipesBundle:Recipe:list }
```

Ambas dirigen la petición al controlador `Acme\BlogBundle\Controller\BlogController::indexAction()`, con la diferencia de que en la ruta inferior se está especificando el número de página. Estas dos rutas podrían refactorizarse en una única ruta con parámetro por defecto:

```
recipes_list:
    path:      /recipes/{page}
    defaults:  { _controller: MyRecipesBundle:Recipe:list, page: 1 }
```

## Requisitos


### Validación de parámetros

Si volvemos a los ejemplos anteriores, el resultado en nuestro fichero de enrutado sería el siguiente:


```
recipes_list:
    path:      /recipes/{page}
    defaults:  { _controller: MyRecipesBundle:Recipe:list, page: 1 }

recipes_show:
    path:     /recipes/{recipe_name}
    defaults: { _controller: MyRecipesBundle:Recipe:show }
```

¿Cómo debería reaccionar Symfony ante la petición `/recipes/5`? ¿Debería responder con la página 5 del listado de recetas? ¿O, al contrario, devería responder con la receta de nombre "5"?

En este caso Symfony respondería con la primera opción, ya que *las rutas que se definen primero tienen prioridad*. Pero la segunda ruta se vería por tanto enmascarada por la primera.

En Symfony es posible asegurar que las rutas cumplen algunos requisitos mediante la clave requirements. El conflicto anterior podría resolverse añadiéndose la siguiente validación:

```
recipes_list:
    path:      /recipes/{page}
    defaults:  { _controller: MyRecipesBundle:Recipe:list, page: 1 }
    requirements:
        page: \d+

recipes_show:
    path:     /recipes/{recipe_name}
    defaults: { _controller: MyRecipesBundle:Recipe:show }
```

Nótese la adición del parámetro `requirements` en la ruta `recipes_list`, donde se especifica que el parámetro `page` debe ser un número entero (uno o más dígitos). Ante una petición al recurso `/recipes/pollo-al-pil-pil`, el componente de enrutado comprobaría en primer lugar que se cumplieran todos los requisitos de la ruta `recipes_list`. Al no cumplirse el requisito, repetiría la operación con `recipes_show`, vinculando la ruta a la acción `My\RecipesBundle\Controller\RecipeController::show()`.

----------------------------------------------------------------------
*Nota del Autor:* Aunque este caso se expone en la documentación oficial, en mi opinión es una mala práctica resolver estos conflictos mediante la etiqueta requirements. Los recursos deberían ser unívocos, no dar lugar a la ambigüedad. Imagínese el caso de la novela "1984", que en una aplicación para bibliotecas podría responder al recurso `/books/1984`. ¡Seguríamos teniendo colisiones con la página 1984 del listado de libros!. Una solución mejor para resolver el problema de la paginación es utilizar query arguments: `/books?page=1984`.
----------------------------------------------------------------------

Un mejor uso de la etiqueta requirements es validar las rutas anticipadamente, antes de que las peticiones lleguen al controlador. Si validamos en el enrutado que un parámetro numérico {id} es efectivamente numérico, evitaremos realizar futuras comprobaciones o consultas innecesarias a la base de datos.

```
recipes_show:
    path:     /recipes/{recipe_id}
    defaults: { _controller: MyRecipesBundle:Recipe:show }
    requirements:
        recipe_id: \d+
```

### Validación de método

En Symfony es posible enviar recursos a controladores distintos en función del método utilizado.

```
recipes_list:
    path:      /recipes/
    defaults:  { _controller: MyRecipesBundle:Recipe:list }
    methods: [GET]

recipes_add:
    path:      /recipes/
    defaults:  { _controller: MyRecipesBundle:Recipe:create }
    methods: [POST]
```

Según esta configuración, se utilizará la acción RecipeController::list() para las peticiones a '/recipes/' con el verbo 'GET', y RecipeController::create() para la misma petición con el verbo 'POST'.

### Validación de host

Symfony permite validar la dirección del host al que se envía la petición. Puede ser útil, por ejemplo, cuando queremos separar la web de un API REST utilizando subdominios:


```
recipes_api_list:
    path:     /recipes/
    host:     api.recipes.com
    defaults: { _controller: MyRecipesBundle:API:list }

recipes_list:
    path:     /recipes/
    defaults: { _controller: MyRecipesBundle:Recipe:list }
```

### Validación de formato

Con el filtro `_format` podemos cribar las peticiones según la cabecera HTTP `Content-Type`.

```
recipes_list:
    path:     /recipes/
    defaults: { _controller: MyRecipesBundle:Recipe:list }
    requirements:
        _format: html|rss

recipes_list_json:
    path:     /recipes/
    defaults: { _controller: MyRecipesBundle:API:list }
    requirements:
        _format: json
```

De este modo podemos obtener representaciones distintas del mismo recurso según el formato recibido.


## Generar rutas con el componente de enrutado

Cualquier clase con acceso al contenedor de inyección de dependencias de Symfony puede generar URIs.

```
$router = $this->get('router');
$uri = $router->generate('recipes_show', array('recipe_id' => 55));

// $uri == '/recipes/55';
```

A continación se describen otros modos de uso:

```
// Rutas absolutas: http://www.misrecetas.com/recipes/55
$router = $this->get('router');
$uri = $router->generate('recipes_show', array('recipe_id' => 55), true);

// Query strings: /recipes/55?param1=foo
$router = $this->get('router');
$uri = $router->generate('recipes_show', array('recipe_id' => 55, 'param1' => 'foo'), true);

```



Los controladores disponen de un método auxiliar `generateUrl()`.

```
$uri = $this->generateUrl('recipes_show', array('recipe_id' => 55));
// $uri == '/recipes/55';
```

