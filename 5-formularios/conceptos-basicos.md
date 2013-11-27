# Conceptos básicos

Es difícil imaginar una aplicación web sin formularios. El [componente de formularios de Symfony 2](https://github.com/symfony/Form) permite gestionar la creación, representación y renderizado de los mismos, además de proporcionar multitud de otras funcionalidades. Como el resto de componentes de Symfony 2, el componente de formularios puede ser instalado por separado en cualquier aplicación PHP.


## Formularios desde controladores

Podemos crear formularios desde nuestros controladores con el método `createFormBuilder()`. Retomaremos nuestra aplicación de recetas proporcionando un formulario para crear autores.

En primer lugar nos aseguraremos de que nuestra clase `Author` dispone de todos los métodos necesarios.

```bash
$ app/console doctrine:generate:entities MyRecipesBundle:Author
Generating entity "My\RecipesBundle\Entity\Author"
  > backing up Author.php to Author.php~
  > generating My\RecipesBundle\Entity\Author
```

Añadiremos la nueva ruta al formulario.

```yaml
# src/My/RecipesBundle/Resources/config/routing.yml
my_recipes_author_create:
    pattern:  /authors/create
    defaults: { _controller: MyRecipesBundle:Author:create }
```

Escribiremos la acción del controlador.

```php
// src/My/RecipesBundle/Controller/AuthorController.php
namespace My\RecipesBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Template;

use My\RecipesBundle\Entity\Author;

class AuthorController extends Controller
{

    /**
     * @Template()
     */
    public function createAction()
    {
        $author = new Author;
        $form = $this->createFormBuilder($author)
            ->add('name', 'text')
            ->add('surname', 'text')
            ->add('save', 'submit')
            ->getForm();
        return array('form' => $form->createView());
    }

}
```
El argumento que recibe el método `createFormBuilder` es el objeto `$author`. El método `add()` permite añadir elementos al formulario. El primer argumento del elemento identifica el campo en el objeto, mientras que el segundo especifica qué tipo de campo es. En Symfony debe haber una correspondencia entre el nombre del campo y el atributo o método del objeto. Esto es así porque el componente de formularios accede a los getters y setters del objeto durante el renderizado y manipulación del formulario.

Para terminar crearemos una plantilla a la que le pasaremos una vista del formulario con `$form->createView()`.

```html
{# src/My/RecipesBundle/Resources/views/Author/create.html.twig #}
{% extends '::base.html.twig' %}

{% block title %}Create author{% endblock %}

{% block body %}
    {{ form(form) }}
{% endblock %}
```

Si accedemos a la ruta `/authors/create` podremos ver nuestro nuevo formulario.

![Formulario de Author](form.png "Formulario de Author")

De momento este formulario no reacciona a los submits, por lo que vamos a añadir la lógica necesaria en el controlador.


```php
// src/My/RecipesBundle/Controller/AuthorController.php
// ...


use Symfony\Component\HttpFoundation\Request;
// ...

    public function createAction(Request $request)
    {
        $author = new Author;
        $form = $this->createFormBuilder($name)
            ->add('name', 'text')
            ->add('surname', 'text')
            ->add('save', 'submit')
            ->getForm();

        $form->handleRequest($request);

        if ($form->isValid()) {
            $em = $this->getDoctrine()->getManager();
            $em->persist($author);
            $em->flush();
            return $this->redirect($this->generateUrl('my_recipes_author_show', array('id' => $author->getId())));
        }
        return array('form' => $form->createView());
    }
```

Cuando accedamos a `/authors/create`, el método `isValid()` de `$form` devolverá `false`. En `handleRequest()` hemos proporcionado al formulario el objeto `$request` por lo que el formulario sabe que estamos mostrando el formulario y no recibiendo información a través del mismo.

Al hacer submit, los datos del objeto request serán cargados en la entidad Author en la llamada a `handleRequest()`. Internamente, Symfony invocará a los setters de `Author` y les pasará el contenido de `name` y `surname`. Posteriormente se ejecutará `isValid()` que efectuará las validaciones pertinentes y generará los mensajes de error necesarios. Si todo va bien y no hay errores de validación, se ejecutará el bloque del `if`, persistiendo la instancia y generando la redirección.



## Form Classes

Aunque los controladores de Symfony permiten crear formularios con `createFormBuilder()`, es una buena práctica llevar la lógica de estos formularios a una clase aparte para _adelgazar_ los controladores y favorecer la reusabilidad.

Crearemos nuestra propia clase AuthorType.

```php
// src/My/RecipesBundle/Form/Type/AuthorType.php
namespace My\RecipesBundle\Form\Type;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;

class AuthorType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('name', 'string')
            ->add('surname', 'string')
            ->add('save', 'submit');
    }

    public function getName()
    {
        return 'author';
    }
}
```

Ahora podemos reescribir la acción de nuestro controlador:

```php
// src/My/RecipesBundle/Controller/AuthorController.php
// ...
use My\RecipesBundle\Form\Type\AuthorType;


    public function createAction(Request $request)
    {
        $author = new Author;
        $form = $this->createForm(new AuthorType, $author);
        $form->handleRequest($request);

        if ($form->isValid()) {
            $em = $this->getDoctrine()->getManager();
            $em->persist($author);
            $em->flush();
            return $this->redirect($this->generateUrl('my_recipes_author_show', array('id' => $author->getId())));
        }
        return array('form' => $form->createView());
    }


```



## Renderizado

Previamente hemos visto cómo renderizar un formulario completo con la función `form`. Veamos ahora un modo más detallado de renderizar un formulario:

```html
{% extends '::base.html.twig' %}

{% block title %}Create author{% endblock %}

{% block body %}
    {{ form_start(form, {'attr' : { 'id' : 'author-create'}}) }}
    {{ form_errors(form) }}
    {{ form_row(form.name) }}
    {{ form_row(form.surname) }}
    {{ form_row(form.save) }}
    {{ form_end(form) }}
{% endblock %}
```

- `form_start` introduce la cabecera `<form>` con los campos necesarios.
- `form_errors` muestra los errores que aplican a todo el formulario.
- `form_row` renderiza un campo concreto del formulario. Por defecto Symfony enmarca los campos en `<div>`, aunque como veremos más adelante este comportamiento es modificable.
- `form_end` renderiza todos los campos que no hayan sido renderizados explícitamente y cierra la etiqueta `<form>`.

Como vemos, en `form_start()` hemos pasado un diccionario con el atributo `id`. De este modo estamos indicando algunos atributos HTML que deseamos que se apliquen al formulario. De este modo podemos personalizar cada elemento del formulario.


Una manera aún más detallada de renderizar el formulario es la siguiente:

```html
{% extends '::base.html.twig' %}

{% block title %}Create author{% endblock %}

{% block body %}
    {{ form_start(form, {'attr' : { 'id' : 'author-create'}}) }}
    {{ form_errors(form) }}
    <ul>
        <li>
            {{ form_label(form.name) }}: 
            {{ form_errors(form.name) }}
            {{ form_widget(form.name) }}
        </li>
        <li>
            {{ form_label(form.surname) }}: 
            {{ form_errors(form.surname) }}
            {{ form_widget(form.surname) }}
        </li>
        <li>
            {{ form_widget(form.save) }}
        </li>
    </ul>
    {{ form_end(form) }}
{% endblock %}
```

- `form_label` genera automáticamente etiquetas para los campos proporcionados.
- `form_errors`, cuando se proporciona un campo concreto, muestra los errores de validación que aplican a dicho campo.
- `form_widget` genera el código mínimo para reproducir el campo en HTML.



## Personalizar la acción y método HTTP

Como hemos visto, la función `form_start(form)` genera el encabezado del método.

```html
<form id='author-create' action='' method='post'>
```

El método por defecto es `POST`, pero Symfony permite modificar el método de un formulario.

```php
class AuthorType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->setMethod('PUT')
            //...
            ;
    }
}
```

Al renderizar ahora el formulario, veremos la siguiente cabecera:

```html
<form id='author-create' action='' method='post'><input type="hidden" name="_method" value="PUT" />
```

Aunque el componente de formularios no modifica el método en los casos `PUT`, `PATCH` y `DELETE`, añade un campo oculto `_method` que utilizará posteriormente para construir el objeto Request con el método seleccionado.


Podemos personalizar la acción y el método desde el controlador:

```php
$form = $this->createForm(new AuthorType(), $author, array(
    'action' => $this->generateUrl('my_recipes_author_create'),
    'method' => 'PUT',
));
```

## Protección CSRF

El componente de formularios de Symfony proporcionan automáticamente protección contra ataques CSRF [Cross-Site Request Forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery) generando un ID único en cada formulario. Aunque está activada por defecto, podemos desactivar la protección CSRF en la configuración de la aplicación:

```yaml
# app/config/config.yml
framework:
    csrf_protection: ~
```


Adicionalmente podemos controlar la protección CSRF por formulario, incluso añadiendo semillas para ayudar a la generación de códigos únicos:

```php
use Symfony\Component\OptionsResolver\OptionsResolverInterface;


class AuthorType extends AbstractType
{
    // ...
    public function setDefaultOptions(OptionsResolverInterface $resolver)
    {
        $resolver->setDefaults(array(
            'csrf_protection' => true,
            'csrf_field_name' => '_token',
            // a unique key to help generate the secret token
            'intention'       => 'author_item',
        ));
    }
}
```
