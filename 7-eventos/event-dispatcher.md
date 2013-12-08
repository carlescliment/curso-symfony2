# El EventDispatcher Component

Como vimos [a principios de este curso](/2-symfony-a-vista-de-pajaro/request-response.md), el kernel de Symfony 2 utiliza el sistema de eventos durante el procesamiento de una petición para permitir puntos de extensión. En esta sección veremos cómo utilizar el componente de eventos para nuestros propios propósitos.



## El Dispatcher

La clase `EventDispatcher` es el eje sobre el que gira el sistema de eventos. El `EventDispatcher` mantiene una lista de _escuchantes_ (en adelante listeners). Cuando una instancia notifica un evento al `EventDispatcher`, éste es el encargado de notificar a los listeners adecuados.

Un listener es cualquier objeto o función capaz de recibir y procesar un evento determinado cuando éste se produce.

```php
use Symfony\Component\EventDispatcher\EventDispatcher;

$dispatcher = new EventDispatcher();
$listener = new RecipesListener();
$dispatcher->addListener('recipe.create', array($listener, 'onRecipeCreate'));
```


En el ejemplo anterior hemos utilizado el método `addListener` de `EventDispatcher` para pasarle un objeto de `RecipesListener`. El dispatcher invocará al método `onRecipeCreate` cada vez que se le notifique un evento `recipe.create`.

## El Listener

```php

namespace My\RecipesBundle\Event;

use My\RecipesBundle\Entity\Recipe;

class RecipesListener
{

    private $mailer;

    public function __construct(\SwiftMailer $mailer)
    {
        $this->mailer = $mailer;
    }

    public function onRecipeCreate(RecipeEvent $event)
    {
        $recipe = $event->getRecipe();
        $this->notifyToAdmins($recipe);
    }


    private function notifyToAdmins(Recipe $recipe)
    {
        // ...
        $this->mailer->send($email);
    }
}

```

En esta implementación concreta, el listener `RecipesListener` recibe el evento y lo procesa para generar un email. Aunque podemos utilizar la clase genérica `Symfony\Component\EventDispatcher\Event` para algunos casos, siempre que necesitemos pasar información a los listeners tendremos que crear nuestra propia clase.


## El Evento

```
namespace My\RecipesBundle\Event;

use My\RecipesBundle\Entity\Recipe;

class RecipeEvent
{

    private $recipe;

    public function __construct(Recipe $recipe)
    {
        $this->recipe = $recipe;
    }
}
```

## Lanzar eventos en aplicaciones Symfony

Para registrar un listener, en Symfony utilizaremos el contenedor escribiendo una entrada en el archivo `services.yml` de nuestro bundle.

```yaml

services:
    #...

    my_recipes.recipes_listener:
        class: My\RecipesBundle\Event\RecipesListener
        arguments: ["@mailer"]
        tags:
          - { name: kernel.event_listener, event: recipe.create, method: onRecipeCreate }
```

Dado que los controladores tienen acceso al contenedor de inyección de dependencias, y que en éste está registrado el propio dispatcher, resulta bastante natural que sea el controlador el encargado de disparar el evento.


```php
class RecipeController extends Controller
{

    /**
     * @Template()
     */
    public function createAction(Request $request)
    {
        $recipe = new Recipe();
        // ...

        if ($form->isValid()) {
            // ...
            $this->get('event_dispatcher')->dispatch('recipe.create', new RecipeEvent($recipe));
            return $this->redirect($this->generateUrl('my_recipes_recipe_show', array('id' => $recipe->getId())));

        }
        return array('form' => $form->createView());
    }
```

Además del controlador, cualquier objeto con acceso al `EventDispatcher` puede lanzar un evento. Aun así, dado que que el uso del `EventDispatcher` es una decisión de diseño del sistema, lo recomendable es mantener las clases del modelo agnósticas al funcionamiento del sistema. Es decir, así como en el patrón Observer decíamos que una clase no debería saber que está siendo observada, tampoco debería saber que hay un EventDispatcher por encima de ella.




## Eventos en cadena

Todo objeto `Event` contiene el propio `EventDispatcher`. Esto permite encadenar unos eventos con otros. Así, el listener presentado como ejemplo podría a su vez disparar eventos en cadena.


```php

class RecipesListener
{

    // ...

    private function notifyToAdmins(Recipe $recipe)
    {
        // ...
        $this->mailer->send($email);
        $event->getDispatcher->dispatch('email.sent', new EmailEvent($email));
    }
}
```


