# Validación
Aunque la documentación oficial sobre [validación de formularios](http://symfony.com/doc/current/book/forms.html#form-validation) proporciona una extensísima información, aquí resumiremos los puntos más importantes.


## El servicio de validación

El servicio de validación de symfony permite validar cualquier clase a la que se haya sometido a reglas. Estas reglas reciben el nombre de **constraints**.

Podemos añadir constraints utilizando anotaciones, archivos xml o archivos yml. Por mantener la coherencia con el resto del material utilizaremos el tercer formato. Implementar un par de constraints de ejemplo sobre la clase `Author`:

```yaml
# src/My/RecipesBundle/Resources/config/validation.yml
My\RecipesBundle\Entity\Author:
    properties:
        name:
            - NotBlank: ~
        surname:
            - NotBlank: ~
```

Una vez establecidas las constraints, desde cualquier controlador o clase con acceso a la capa de servicios podemos utilizar el validador.

```php
    $author = new Author('Iñaki', '');
    $validator = $this->get('validator');
    $errors = $validator->validate($author);
```

En el caso anterior estamos construyendo un objeto `Author` con el atributo `surname` vacío, por lo que `$validator>validate($author)` devolverá un array indicando el error encontrado. En caso contrario, devolverá un array vacío.

Cuando invocamos el método `isValid()` de un formulario, internamente se está utilizando el servicio de validación para validar la clase subyacente. Además, el componente de formularios es capaz de interpretar el valor de retorno y contextualizarlo en el campo del formulario que corresponda.


## Constraints

Los constraints pueden aplicarse a atributos del objeto y a métodos. Los métodos proporcionan mayor potencia en la validación al introducir nuestra propia lógica. Por ejemplo, para vincular un constraint a un método `isValid()` deberemos añadir una sección `getters` al archivo de validación.

```yaml
# src/My/RecipesBundle/Resources/config/validation.yml
My\RecipesBundle\Entity\Author:
    getters:
        valid:
            - "True": { message: "No aceptamos recetas del autor" }
    # ...
```

```php
// src/My/RecipesBundle/Entity/Author.php

class Author
{
    // ...
    public function isValid()
    {
        return $this->__toString() != 'Karlos Arguiñano';
    }
}
```


El servicio de validación proporciona una larga lista de constraints con distintos propósitos. Para mayor información consultad la [documentación oficial](http://symfony.com/doc/current/book/validation.html#constraints). Si los constraints proporcionados no fuesen suficiente, el componente de validación permite [definir constraints personalizados](http://symfony.com/doc/current/cookbook/validation/custom_constraint.html).
