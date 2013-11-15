# Controlador

Para una información más completa y actualizada, consultad la [documentación oficial](http://symfony.com/doc/current/book/controller.html).

Un controlador es una función o método que recoge la información de una petición HTTP y devuelve una respuesta HTTP. Tal y como se ha descrito en el capítulo de [enrutado](2-symfony-a-vista-de-pajaro/routing.md), el enrutador es el encargado de buscar qué controlador se utiliza en cada petición y proporcionarle los parámetros necesarios.

```routing.yml
recipes_list:
    path:     /recipes/
    defaults: { _controller: MyRecipesBundle:Recipe:list }

recipes_show:
    path:     /recipes/{recipe_id}
    defaults: { _controller: MyRecipesBundle:Recipe:show }
```

```RecipeController.php
// src/My/RecipesBundle/Controller/RecipeController.php
namespace My\RecipesBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;

class RecipeController extends Controller
{
    public function listAction()
    {
        return new Response('<html><body><p>No hay recetas</p></body></html>');
    }

    public function showAction($recipe_id)
    {
        return new Response('...');
    }
}

```

## Paso de parámetros

Además de los parámetros proporcionados por el enrutador, en Symfony podemos inyectar el propio objeto Request.

```RecipeController.php
    public function showAction($recipe_id, Request $request)
    {
        return new Response('...');
    }
```

Gracias al uso de la [reflexión](http://en.wikipedia.org/wiki/Reflection_(computer_programming)) no importa el orden en el que especifiquemos estos parámetros.

## El controlador base
Symfony proporciona una clase base `Controller` que podemos extender en nuestros controladores y que proporciona algunos métodos útiles.:

### Redirigir
Crea una respuesta de tipo RedirectResponse.

```
public function showAction()
{
    return $this->redirect($this->generateUrl('redirect_path'));
}
```

### Reenviar
En lugar de redirigir al cliente indicándole una nueva ruta, pasa la petición a otro controlador.

```
public function showAction($id)
{
    return $this->forward('MyForwardingBundle:Forwarded:show', array(
        'id' => $id,
    ));
}
```

Internamente se realiza una [sub-request](http://symfony.com/doc/current/components/http_kernel/introduction.html#http-kernel-sub-requests). El objeto Request se clona y se resuelve como si se tratase de una nueva petición.


### Renderizar
La mayoría de aplicaciones web hacen uso de plantillas para renderizar contenido HTML y devolverlo en la respuesta. El controlador base de Symfony dispone de un método para ello:

```
public function showAction($id)
{
    // ...
    return $this->render('MyRecipesBundle:Recipe:show.html.twig', array(
        'recipe' => $recipe,
    ));
}
```

### Acceder a servicios
El controlador base de Symfony implementa la interfaz `ContainerAwareInterface`, y por tanto el framework automáticamente proporciona el contenedor de inyección de dependencias a cualquier clase que lo extienda.

```
public function showAction($id)
{
    $templating = $this->get('templating');
    $router = $this->get('router');
    $mailer = $this->get('mailer');
}
```

### Errores y excepciones

Para generar una respuesta con el código 404 basta con levantar una excepción de tipo `NotFoundException`.

```
public function showAction($id)
{
    throw $this->createNotFoundException('...');
    throw \Exception(...);
}
```

Cualquier excepción será capturada por Symfony, devolviendo un código de error 500.

---------------------------
¡Ojo! En entornos de desarrollo, las excepciones son capturadas y se muestra una página de debugging, pero el código de respuesta es 200. Debe tenerse este factor en cuenta cuando se realicen pruebas manuales o automáticas sobre los códigos de respuesta, para evitar posibles falsos negativos/positivos.
---------------------------


## La sesión
Por defecto, Symfony 2 utiliza cookies para almacenar los datos de la sesión del cliente. Es posible manipular el contenido de estas cookies mediante el objeto sesión contenido en la petición:

```
public function showAction($id, Request $request)
{
    $session = $request->getSession();
    $session->set('clave', 'valor');
    $session->get('clave');
}
```


### Mensajes Flash
Los mensajes Flash se almacenan en la sesión y su objetivo es mostrar mensajes del sistema al cliente. Pueden definirse varios niveles de mensaje flash para representar la urgencia o importancia de cada uno de ellos.


```php
public function createAction(Request $request)
{
    $session = $request->getSession();
    $session->getFlashBag()->add(
        'notice',
        'Has publicado una nueva receta'
    );
}
```

Es nuestra labor renderizar estos mensajes en la plantilla correspondiente. Veremos más sobre esto en el capítulo de Twig.

```template.html.twig
{% for flashMessage in app.session.flashbag.get('notice') %}
    <div class="flash-notice">
        {{ flashMessage }}
    </div>
{% endfor %}
```

## SensioFrameworkExtraBundle
El Bundle SensioFrameworkExtraBundle proporciona algunas funcionalidades interesantes que podemos añadir a nuestros controladores en forma de anotaciones. Consulta [la documentación oficial](http://symfony.com/doc/current/bundles/SensioFrameworkExtraBundle/index.html) para obtener una información más completa y actualizada.

### @Route y @Method

Utiliza la anotación `@Route` para indicar la ruta de la que el controlador es responsable sin necesidad de ficheros de enrutamiento específicos. `@Method 


```
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;

/**
 * @Route('/recipes')
 */
class RecipeController extends Controller

    /**
     * @Route('/{id}', name="recipe_show", requirements={"id" = "\d+"})
     * @Method({"GET"})
     */
    public function showAction($id)
    {
        // ...
    }
}
```


### @ParamConverter

Permite realizar algunas transformaciones sobre los parámetros de entrada del controlador. Útil, por ejemplo, en servicios REST donde los identificadores de los recursos están enmascarados.

```php
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\ParamConverter;

/**
 * @Route('/{id}', name="recipe_show", requirements={"id" = "\d+"})
 * @ParamConverter("id", class="My\ReceiptBundle\MaskedResource")
 */
public function showAction(MaskedResource $id)
{
    $public_id = $id->getPublic();
    $private_id = $id->getPrivate();
    // ...
}
```

El bundle proporciona dos conversores base. El de Doctrine permite cargar automáticamente entidades de la base de datos a partir de ids.

```php
use My\RecipeBundle\Entity\Recipe;

/**
 * @Route('/{id}', name="recipe_show", requirements={"id" = "\d+"})
 */
public function showAction(Recipe $recipe)
{
    // ...
}
```

El DateTimeConverter transforma automáticamente fechas en objetos DateTime

```php
use My\RecipeBundle\Entity\Recipe;

/**
 * @Route('/{start}/{end}', name="recipe_show")
 * @ParamConverter("start", options={"format": "Y-m-d"})
 * @ParamConverter("end", options={"format": "Y-m-d"})
 */
public function listByDatesAction(\DateTime $start, \DateTime $end)
{
    // ...
}
```

### @Template

Con Template() podemos escribir controladores de un modo más elegante utilizando convenios en la organización de plantillas. Los métodos a continuación serían equivalentes:


```
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Template;

public function showAction($id)
{
    // ...
    return $this->render('MyRecipesBundle:Recipe:show.html.twig', array(
        'recipe' => $recipe,
    ));
}

/**
 * @Template()
 */
public function showAction($id)
{
    // ...
    return array(
        'recipe' => $recipe,
    );
}
```
