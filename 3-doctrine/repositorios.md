# Repositorios

En [el capítulo anterior](dql.md) se explica cómo realizar consultas complejas utilizando **DQL**. Pero, ¿dónde y cómo organizar consultas?.

En general, toda las consultas a la base de datos deberían organizarse en repositorios de Doctrine.

## Qué es un repositorio

Un repositorio es una clase que agrupa un conjunto de métodos para realizar consultas sobre una determinada entidad. Cuando se ejecuta el método `getRepository('MyRecipesBundle:Author')`, Doctrine comprobará en primer lugar si se ha definido un repositorio para la entidad `Author`. De no ser así, construye un repositorio base de clase `Doctrine\ORM\EntityRepository`.

## Crear un repositorio

Para crear un repositorio sobre la clase `Author` escribiremos una clase `AuthorRepository` en el directorio `src/My/RecipesBundle/Repository`.

```
namespace My\RecipesBundle\Repository;

use Doctrine\ORM\EntityRepository;

class AuthorRepository extends EntityRepository {

    public function findTopChefs() {
        return $this->getEntityManager()
            ->createQuery('SELECT a
                           FROM MyRecipesBundle:Author a
                           JOIN a.recipes r
                           WHERE r.difficulty = :difficulty')
            ->setParameter('difficulty', 'difícil')
            ->getResult();
    }
}
```

El siguiente paso será indicar a Doctrine que la entidad `Author` estará gestionada por nuestro propio repositorio.

```
My\RecipesBundle\Entity\Author:
    type: entity
    repositoryClass: My\RecipesBundle\Repository\AuthorRepository
    # ...
```


Y ya sólo queda utilizar el nuevo método implementado.


```
    /**
     * @Template()
     */
    public function topChefsAction()
    {
        $repository = $this->getDoctrine()->getRepository('MyRecipesBundle:Author');
        $chefs = $repository->findTopChefs();
        return array('chefs' => $chefs);
    }
```
