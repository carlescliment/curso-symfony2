# Gestión de paquetes con Composer

## Qué es Composer
[Composer](http://getcomposer.org/) es una herramienta para la gestión de dependencias en PHP. A diferencia de un gestor de paquetes, la función de Composer no es instalar un paquete en un sistema operativo, sino gestionarlas dentro de una aplicación concreta.

Liberado en 2012, Composer ha supuesto una auténtica revolución en el mundo PHP, muy necesitado de esta herramienta. Supone la estandarización en la definición de las dependencias tal y como ya hicieron en NodeJS [npm](https://npmjs.org/) o Ruby [bundler](http://bundler.io/). Esta estandarización ha permitido el florecimiento de todo un ecosistema de bibliotecas base y para distintos frameworks que la han adoptado.

En Symfony, Composer fue introducido en su versión 2.1. En la versión anterior se utilizaba un gestor de dependencias propio.

## Cómo definir un proyecto con Composer
Toda aplicación que utilice Composer debe contener en su raíz un archivo `composer.json` que defina sus atributos básicos. Por ejemplo:

```composer.json
{
    "name": "carlescliment/html2pdf-service",
    "description": "A REST microservice that converts html input into pdf files. Written in Silex.",
    "version": "0.0.2",
    "type": "project",
    "keywords": ["printing", "pdf"],
    "license": "GPL-2.0",
    "authors": [
        {
            "name": "Carles Climent Granell",
            "email": "carlescliment@gmail.com",
            "homepage": "http://www.carlescliment.com",
            "role": "Developer"
        }
    ],
    "require": {
        "php": ">=5.3.2",
        # ...
    },
    "require-dev": {
        "symfony/browser-kit": ">=2.3,<2.4-dev",
        "phpunit/phpunit": "3.7.*"
    },
    "autoload": {
        "psr-0": { "carlescliment\\Html2Pdf": "src" }
    },
    "minimum-stability" : "stable"
}
```

De este ejemplo podemos extraer que:
* El nombre del paquete es `html2pdf-service`, y el vendor (autor) es `carlescliment`.
* Se encuentra en la versión `0.0.2`.
* Es de tipo "project". Los tipos válidos estándar son; `library` (por defecto), `project`, `metapackage` y `composer-plugin`. Otros tipos personalizados también son admitidos, como `wordpress-plugin`.
* Se han añadido dos palabras clave `printing` y `pdf` para facilitar su búsqueda.
* Está liberado bajo licencia GPL 2.
* Su autor es Carles Climent Granell.
* Tiene algunas dependencias necesarias para su puesta en producción (require) y otras para entornos de desarrollo (require-dev).
* Utiliza una estrategia de autocarga definida por el estándar PSR-0.
* Sólo admite dependencias estables.


Veamos cómo funciona con mayor detenimiento.

## Cómo establecer dependencias
Para establecer una dependencia introduciremos el nombre del paquete o biblioteca en una clave *"require"*.

```composer.json
{
    "require": {
        "php": ">=5.3.2",
        "monolog/monolog": "1.2.*"
    }
}
```

En la parte izquierda especificaremos el *nombre del paquete*, mientras que en la derecha especificamos la versión.

Las versiones pueden especificarse de distintas maneras:

|         |      |    |
|---------|-------|----|
| Exacta  | 1.0.2 | Descarga la versión especificada y solo esa. |
| Rango   | >=1.0 | Versión igual o mayor que 1.0 |
| Rango   | >=1.0,!=1.4 | Versión igual o mayor que 1.0, excepto la 1.4. La coma se interpreta como un AND. |
| Rango   | >=1.0,<2.0 | Versiones entre 1.0 y 2.0 |
| Rango   | >=1.0,<1.1 &#124; >=1.2 | Versiones entre 1.0 y 1.1, o mayor que la 1.2. La tubería se interpreta como un OR |
| Comodín | 1.0.* | Equivale a >=1.0,<1.1 |
| Tilde   | ~1.2  | Equivale a >=1.2,<2.0 |

Por defecto, solo se tendrán en cuenta las versiones estables de cada paquete. Este comportamiento puede ser modificado mediante la clave "minimum-stability". Las opciones son `dev`, `apha`, `beta`, `RC` y `stable`.

```composer.json
{
    # ...
    "minimum-stability": "dev"
}
```
Una vez especificadas las dependencias, basta con instalarlas ejecutando `php composer.phar update`. Tras ejecutar el comando se iniciará la descarga de las dependencias, se generará un autoloader y se creará un archivo `composer.lock`.

## Autoloading
Composer crea un archivo `vendor/autoload.php` que contiene la carga automática de clases y espacios de nombres de aquellos paquetes que lo necesiten. Esto te permitirá incluir fácilmente estos paquetes en tu proyecto añadiendo simplemente un *require* en tu aplicación:

`require 'vendor/autoload.php';`

Para cargar tu propio código en el autoloader puedes añadir la etiqueta `autoload` en `composer.json`.

```composer.json
{
    # ...
    "autoload": {
        "psr-0": { "carlescliment\\Html2Pdf": "src" }
    }
}
```

## El Lock File
El archivo `composer.lock` contiene las versiones instaladas actualmente en la aplicación. Si composer encuentra este archivo, descargará exactamente las versiones definidas en el archivo. Es recomendable añadir el archivos composer.lock al repositorio de versiones. De esta manera, cualquiera que se descargue el código instalará las mismas versiones que quien añadió el archivo. ¡Pensad por ejemplo en los sistemas de integración continua!.

En el caso de que Composer no encuentre un `composer.lock`, generará uno nuevo a partir del `composer.json`.

## Packagist
Si queremos publicar un proyecto para que otros puedan descargarlo via Composer, debemos dotarlo de un archivo `composer.json` válido y darlo de alta en la base de datos de la web [Packagist](https://packagist.org/). La mayoría de los gestores de versiones del mercado permiten disparar de manera automática acciones (hooks) que informarán a Packagist de nuevas versiones.

Es posible añadir otras fuentes, además de Packagist. [Satis](https://github.com/composer/satis), por ejemplo, es una herramienta que permite crearnos un *Packagist privado". Resulta muy útil cuando tenemos dependencias de código que no deseamos publicar. Para más información sobre cómo gestionar repositorios privados con composer ver el siguiente enlace:

[Handling private packages with Satis](https://github.com/composer/composer/blob/master/doc/articles/handling-private-packages-with-satis.md)
