# Lazy y Eager

La forma en la que Doctrine gestiona la carga de una entidad y las entidades con las que se relaciona tiene un gran impacto en el rendimiento de la aplicación. Por ello conviene estudiar detenidamente cuál es el comportamiento más conveniente.

## EAGER

```yml
My\RecipesBundle\Entity\Recipe:
    manyToOne:
        author:
            fetch: EAGER
            # ...
    # ...
```

La carga EAGER implica que cuando se recupera una entidad de la base de datos, automáticamente se cargarán todas las entidades relacionadas con él. De este modo, al cargar un `Recipe` se cargará automáticamente el objeto `Author` asociado, realizándose dos consultas a la base de datos.

## LAZY

```yml
My\RecipesBundle\Entity\Recipe:
    manyToOne:
        author:
            fetch: LAZY
            # ...
    # ...
```

En la carga LAZY - por defecto - los objetos se recuperan de la base de datos en tiempo de ejecución. El objeto `Author` asociado a `Recipe` no será cargado hasta el momento en que éste sea necesario, por ejemplo cuando ejecutemos `$recipe->getAuthor()`.

Si la relación de `Author` a `Recipe` se define como `LAZY`, entonces se cargará la colección completa la primera vez que sea accedida.

```
// Carga la colección completa de recetas.
$author->getRecipes();
```

## EXTRA_LAZY

La carga EXTRA_LAZY fue introducida en la versión 2.1 de Doctrine. Presenta algunos cambios sobre la carga LAZY, dado que evita la carga de la colección completa en llamadas a los siguientes métodos:

```
// No cargan la colección completa

Collection#contains($entity);
Collection#count();
Collection#slice($offset, $length);
Collection#add($entity);
Collection#offsetSet($key, $entity);
```

