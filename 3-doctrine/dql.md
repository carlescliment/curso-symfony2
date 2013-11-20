# Doctrine Query Language

Symfony proporciona algunos métodos para realizar operaciones básicas sobre entidades tales como la creación, borrado, carga, filtrado y ordenación. En ocasiones, sin embargo, es necesario realizar consultas más complejas que no pueden resolverse con estos métodos. Por ello, Doctrine proporciona la herramienta **Doctrine Query Builder** basada en el **Doctrine Query Language** (DQL).

DQL es similar a SQL en su sintaxis, pero se centra en las clases que representan a las entidades, y no en las tablas subyacentes.


## Crear consultas con DQL.

El Entity Manager de Doctrine proporciona un acceso a DQL a través del método `createQuery()`.

```
$em = $this->getDoctrine()->getManager();
$query = $em->createQuery(
    'SELECT a
    FROM MyRecipesBundle:Author a
    JOIN a.recipes r
    WHERE r.difficulty = :difficulty
    ORDER BY a.surname DESC'
)->setParameter('difficulty', 'difícil');

$hardcore_authors = $query->getResult();
```


Otra forma de realizar la consulta es a través del `QueryBuilder`.


```
$em = $this->getDoctrine()->getManager();
$repository = $em->getRepository('MyRecipesBundle:author');
$query = $repository->createQueryBuilder('a')
    ->innerJoin('a.recipes', 'r')
    ->where('r.difficulty = :difficulty')
    ->orderBy('a.surname', 'DESC')
    ->setParameter('difficulty', 'difícil')
    ->getQuery();

$hardcore_authors = $query->getResult();
```

`getResult()` devolverá una colección de entidades, mientras que `getSingleResult()` espera una sola entidad. En el caso de encontrar varias entidades o no encontrar ninguna, `getSingleResult()` levantará una excepción.


## Limit y offset

Los equivalentes `LIMIT` y `OFFSET` de DQL se consiguen a través de los métodos `setMaxResults($limit)` y `setFirstResult($offset)`.

```
$query = $em->createQuery(
    'SELECT r
    FROM MyRecipesBundle:Recipes r
    JOIN r.author a
    JOIN r.ingredients i'
)->setFirstResult(100)
 ->setMaxResults(10)
 ->getQuery();
```

## Valores escalares

En DQL también es posible recuperar valores escalares en lugar de objetos.

```
$query = $em->createQuery(
    'SELECT MAX(a.id)
    FROM MyRecipesBundle:Author a'
)->getQuery();
$last_id = $query->getSingleScalarResult();
```

## Optimización básica

Podemos optimizar las consultas facilitando información al `hydrator`, que se encarga de construir los objetos cargados.

```
$query = $em->createQuery(
    'SELECT r, a, i
    FROM MyRecipesBundle:Recipes r
    JOIN r.author a
    JOIN r.ingredients i'
);
$full_built_recipes = $query->getResult();
```

Obsérvese la cláusula SELECT de la consulta anterior, que contiene `r, a, i`. De este modo, Doctrine cargará todos los objetos `Ingredient` y `Author` en `Recipe` en el menor número de consultas posible. Si bien supone mayor consumo de memoria, permite optimizar enormemente las transferencias con la base de datos.


Otra forma de optimizar recursos es utilizar arrays en lugar de entidades completas.

```
$query = $em->createQuery(
    'SELECT i.id, i.name
    FROM MyRecipesBundle:Ingredient i'
)->getQuery();
$ingredients = $query->getArrayResult();
```
