# Definición y manipulación de entidades


## Definir entidades

Las entidades en Doctrine son aquellos actores del sistema que necesitan ser persistidos. Para crear una entidad, en primer lugar empezaremos por escribir una clase en el directorio `entities` de nuestro bundle.

```Recipe.php
// src/My/RecipesBundle/Entity/Recipe.php
namespace My\RecipesBundle\Entity;


class Recipe
{
    private $id;

    protected $name;

    protected $difficulty;

    protected $description;
}
```

Posteriormente necesitaremos proporcionar la información de mapeo de los campos de esta clase con una tabla de la base de datos. Disponemos de varias maneras de hacerlo: anotaciones, xml e yml. En esta guía optaremos por la configuración en yml.


```Recipe.orm.yml
# src/My/RecipesBundle/Resources/config/doctrine/Recipe.orm.yml
My\RecipesBundle\Entity\Recipe:
    type: entity
    table: recipes
    id:
        id:
            type: integer
            generator: { strategy: AUTO }
    fields:
        name:
            type: string
            length: 255
        name:
            type: string
            length: 40
        description:
            type: text
```

## Creación de tablas en la base de datos

Estos dos archivos son ya suficientes para generar la entidad en la base de datos. Para comprobarlo, ejecuta la siguiente instrucción en el terminal.

```
$ php app/console doctrine:schema:create --dump-sql
CREATE TABLE recipes (id INT AUTO_INCREMENT NOT NULL, name VARCHAR(40) NOT NULL, description LONGTEXT NOT NULL, PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ENGINE = InnoDB;
```

Confirma la creación eliminando los parámetros opcionales.

```
$ php app/console doctrine:schema:create
ATTENTION: This operation should not be executed in a production environment.

Creating database schema...
Database schema created successfully!
```

Para poder acceder a los atributos de la clase necesitaremos algunos getters. El componente de formularios de symfony, por otra parte, necesitará algunos setters. Si queremos añadir estos métodos automáticamente podemos usar la consola:


```
$ app/console doctrine:generate:entities My/RecipesBundle/Entity/Recipe
Generating entity "My\RecipesBundle\Entity\Recipe"
  > backing up Recipe.php to Recipe.php~
  > generating My\RecipesBundle\Entity\Recipe
```

Si ahora visitamos la clase Recipe, veremos que se han creado accesores para todos los atributos.


Una forma más directa de crear una entidad es el comando `app/console doctrine:generate:entity`, que interactivamente permite la generación automática de la entidad.


## Persistir entidades

Para manipular entidades de Doctrine necesitaremos el `EntityManager`. Esta clase es la encargada de gestionar la persistencia.

Los controladores de Doctrine que extiendan la clase `Controller` pueden acceder al `EntityManager` con `$this->getDoctrine()->getManager()`.


```DefaultController.php
// src/My/RecipesBundle/Controller/DefaultController.php

use My\RecipesBundle\Entity\Recipe;
use Symfony\Component\HttpFoundation\Response;

public function createAction()
{
    $recipe = new Recipe();
    $recipe->setName('Pollo al pil-pil');
    $recipe->setDificulty('fácil');
    $recipe->setDescription('...');

    $em = $this->getDoctrine()->getManager();
    $em->persist($recipe);
    $em->flush();

    return new Response('Creada receta con id ' . $recipe->getId());
}
```

La instrucción `persist` no desencadena la operación `INSERT` hasta que se ejecuta la instrucción `flush()`. En ese momento, Doctrine persiste la entidad y actualiza su id.


## Recuperar entidades

La forma más sencilla de recuperar una entidad es a través de su `id` mediante el método `find()`. Para recuperar entidades necesitaremos un **Repositorio**. Doctrine proporciona repositorios por defecto para todas las entidades que definamos.


```DefaultController.php
// src/My/RecipesBundle/Controller/DefaultController.php

public function showAction($id)
{
    $repository = $this->getDoctrine()
        ->getRepository('MyRecipesBundle:Recipe');
    $recipe = $repository->find($id);
    // ...
}
```

Para recuperar todos los elementos utilizaremos `findAll`.

```
$repository->findAll(); // todas las instancias de Recipe.
```

También podemos especificar algunos criterios de filtrado y ordenación con findBy()
```
$repository->findBy(array('difficulty' => 'easy')); // Instancias filtradas por dificultad
$repository->findBy(array(), array('name' => 'DESC')); // Ordenación
```

Doctrine utiliza metaprogramación para permitir algunos métodos más legibles.
```
$repository->findByDifficulty('easy');
$repository->findOneByName('Pollo al pil-pil');
```


## Actualizar entidades

Para actualizar una entidad, basta con modificar sus atributos e invocar al método `flush()` del `EntityManager`.

```
$recipe = $repository->findOneByName('Pollo al pil-pil');
$recipe->setName('Pollo al chilindrón');
$this->getDoctrine()->getManager()->flush();
```


## Eliminar entidades
El borrado de entidades se realiza mediante el método `remove()` del `EntityManger`.

```
$recipe = $repository->find($id);
$em = $this->getDoctrine()->getManager();
$em->remove($recipe);
$em->flush();
```
