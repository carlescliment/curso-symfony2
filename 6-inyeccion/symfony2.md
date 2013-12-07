# El componente de inyección de dependencias en Symfony 2

## Entornos

Una aplicación Symfony puede ejecutarse en distintos entornos. Los entornos más típicos son `prod`, `dev` y `test`, que corresponden a producción, desarrollo y pruebas. Adicionalmente podemos configurar tantos entornos distintos como sean necesarios.

Si observamos el archivo `index.php` de nuestra instalación Symfony podremos ver la siguiente línea:

```
$kernel = new AppKernel('prod', false);
```

El primer argumento `prod` indica el entorno que se va a aplicar a la instancia de la aplicación. Con esta configuración, Symfony buscará el fichero `app/config/config_prod.yml`. Básicamente Symfony añade el nombre del entorno como sufijo del archivo de configuración.

Esta separación en entornos permite configurar los parámetros de forma independiente. Así, es posible separar las bases de datos a las que la aplicación ataca en función de si el entorno es `test` o `dev`. Pero además de configurar parámetros, también permitirá _inyectar_ servicios distintos de acuerdo a las necesidades de cada entorno.


## Cómo crear servicios

En nuestra aplicación de recetas teníamos una acción en el controlador `RecipeController` que permitía mostrar las últimas recetas publicadas.

    // src/My/RecipesBundle/Controller/RecipeController.php
    
    class RecipeController extends Controller
    {
    
        public function lastRecipesAction()
        {
            $date = new \DateTime('-10 days');
            $repository = $this->getDoctrine()->getRepository('MyRecipesBundle:Recipe');
            $recipes = $repository->findPublishedAfter($date);
            return array('recipes' => $recipes);
        }
    }


Vamos a extraer este fragmento de código a un servicio independiente. En primer lugar, moveremos el código a una nueva clase.

    // src/My/RecipesBundle/Model/LastRecipes.php
    namespace My\RecipesBundle\Model;

    use Doctrine\Common\Persistence\ObjectManager;

    class LastRecipes
    {
        private $repository;
    
        public function __construct(ObjectManager $om) {
            $this->repository = $om->getRepository('MyRecipesBundle:Recipe');
        }
    
        public function findFrom(\DateTime $from_date)
        {
            return $this->repository->findPublishedAfter($from_date);
        }
    }


Publicaremos el servicio en el archivo `services.yml`.

    services:
        #...
        my_recipes.last_recipes:
            class: My\RecipesBundle\Model\LastRecipes
            arguments: ["@doctrine.orm.entity_manager"]


Y modificaremos el controlador:

    // src/My/RecipesBundle/Controller/RecipeController.php
    
    class RecipeController extends Controller
    {
    
        public function lastRecipesAction()
        {
            $date = new \DateTime('-10 days');
            return array(
                'recipes' => $this->get('my_recipes.last_recipes')->findFrom($date),
                );
        }
    }


La extracción del código de controladores a servicios tiene diversas ventajas. Los controladores son la capa de la aplicación más cercana al framework, y la única que debería estar acoplada a él. Moviendo el código a servicios independientes conseguimos un diseño de la aplicación más portable. Por otra parte, ahora podemos sobreescribir el servicio proporcionado en cualquier entorno sin tener que modificar el controlador:

    # app/config/config_otherenvironment.yml
    services:
        #...
        my_recipes.last_recipes:
            class: My\RecipesBundle\Model\OtherClass


La inyección de dependencias resulta especialmente útil en los casos en los que nuestra aplicación conecta con otras aplicaciones del exterior. Por ejemplo, es posible que nuestra aplicación utilice una clase determinada para publicar mensajes en Twitter. Gracias a la inyección y a la configuración por entornos, podríamos evitar sencillamente que desde el entorno `dev` y  `test` se publicasen mensajes reales.

Para una descripción más exhaustiva del funcionamiento del componente de inyección de dependencias, consultad la [sección correspondiente](http://symfony.com/doc/current/components/dependency_injection/index.html) en la documentación oficial.



