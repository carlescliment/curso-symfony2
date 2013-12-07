# Introducción

Ya hemos visto principios que facilitan el desacoplamiento del código y la extensibilidad, como la inyección de dependencias y el uso de servicios. En este tema veremos cómo llevar aún más allá estos principios gracias al uso de eventos.

Volvamos a la aplicación de recetas, concretamente a la acción del controlador en la que se creaba una nueva receta:

```
// src/My/RecipesBundle/Controller/RecipeController.php
class RecipeController extends Controller
{
    public function createAction(Request $request)
    {
        $recipe = new Recipe();
        $form = $this->createForm(new RecipeType, $recipe);
        $form->handleRequest($request);

        if ($form->isValid()) {
            $this->persistAndFlush($recipe);
            return $this->redirect($this->generateUrl('my_recipes_recipe_show', array('id' => $recipe->getId())));
        }
        return array('form' => $form->createView());
    }
}
```

La servicio encargado de crear la receta es el siguiente:

```
// src/My/RecipesBundle/Model/RecipeCreator.php
namespace My\RecipesBundle\Model;

use Doctrine\Common\Persistence\ObjectManager;
use My\RecipesBundle\Entity\Recipe;

class RecipeCreator
{

    private $om;

    public function __construct(ObjectManager $om) {
        $this->om = $om;
    }

    public function create(Recipe $recipe)
    {
        $this->om->persist($recipe);
        $this->om->flush();
    }
}
```


Imaginemos que uno de los requisitos de negocio es enviar un aviso por email al administrador de la web cada vez que se publica la receta. Podríamos decidir añadir este comportamiento a la clase `RecipeCreator`.


```
class RecipeCreator
{
    // ...
    public function create(Recipe $recipe)
    {
        $this->om->persist($recipe);
        $this->om->flush();
        $this->systemMailer->sendRecipeInfo($recipe);
    }
}
```

Posteriormente se nos solicita que registremos la operación en un log, por lo que de nuevo añadimos la nueva funcionalidad al `RecipeCreator`.

```
class RecipeCreator
{
    // ...
    public function create(Recipe $recipe)
    {
        $this->om->persist($recipe);
        $this->om->flush();
        $this->systemMailer->sendRecipeInfo($recipe);
        $this->systemLogger->log('info', sprintf('New recipe created with name %s', $recipe->getName()));
    }
}
```

Ahora nuestro creador tiene tres responsabilidades:

- Guarda la receta en la base de datos.
- Envía un email.
- Registra la operación en un log.


Aún así, dado que lo hemos encapsulado todo en otras clases, el código parece bastante sencillo, ¿verdad? En realidad hay varios aspectos en este diseño que son mejorables. En primer lugar hemos roto el llamado [Principio de una sola responsabilidad](https://docs.google.com/file/d/0ByOwmqah_nuGNHEtcU5OekdDMkk/edit) o SRP. Pero además también hemos introducido acoplamiento temporal.

El acoplamiento temporal significa que dos o más acciones son llevadas a cabo por el mismo componente sólo porque ocurren en el mismo instante. En este tema vamos a aprender a resolver el acoplamiento temporal con el uso de eventos.



