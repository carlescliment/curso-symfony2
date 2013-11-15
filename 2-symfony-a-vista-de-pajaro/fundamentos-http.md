# Fundamentos HTTP

## Qué es HTTP

HTTP es un *protocolo de aplicación* usado en *la web* (www) para comunicaciones entre cliente y servidor. El servidor puede ser un ordenador que aloja una aplicación web, y el cliente web más común que conocemos es el navegador o *web browser". Pero con el tiempo han salido muchos otros modelos de cliente servidor. De hecho, en la actualidad es muy común que un servidor ejerza de cliente de otros servidores.

![La Pila OSI](http://www.washington.edu/lst/help/computing_fundamentals/networking/img/osi_model.jpg "La Pila OSI")

HTTP define cómo debe construirse una *petición* y cómo debe devolverse una *respuesta*.

## La petición

En una petición se especifica:
 * Una línea con el método, el recurso y la versión de HTTP
 * Cabeceras opcionales
 * La dirección del servidor
 * El cuerpo de la petición, separado por una línea en blanco.


```http-request
PUT /recetas/pollo-al-pil-pil HTTP/1.1
Host: cocinando.com
Content-Type: application/json

{nombre:"Pollo al Pil-Pil", dificultad:2, ingredientes:["1 chorrito de aceite de oliva", "2 pechugas de pollo fileteadas", "Una cabeza de ajos", "Guindillas", "Perejil", "1 limón", "Colorante", "1 vaso de cerveza", "Sal"]}

```


### Métodos

La versión HTTP/1.1 define [ocho posibles métodos](http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html) para una petición. Estos métodos pueden tener algunas propiedades, como _seguro_ e _idempotente_.

#### Métodos seguros

Son métodos que no desencadenan acciones en el servidor, aparte de recoger información. Entre ellos tenemos GET y HEAD. Aunque estos métodos estén definidos como seguros, depende de nosotros, los implementadores, que lo sean efectivamente. Es decir, debemos procurar que las llamadas GET y HEAD desencadenen acciones que alteren el estado del sistema.

#### Métodos idempotentes

Son métodos que podemos repetir varias veces obteniendo el mismo resultado en el servidor. Entre ellos tenemos GET, HEAD, PUT, DELETE, OPTIONS y TRACE. Por el contrario, el método POST no es idemponente, ya que repitiendo la misma operación alteramos el estado del sistema. Por definición, todos los métodos seguros son idempotentes.


#### Listado de métodos

| Método    | Seguro      | Idempotente  | Descripción   |
|-----------|-------------|--------------|---------------|
| OPTIONS   | Sí          | Sí           | Solicita información sobre las distintas opciones de comunicación disponibles. |
| GET       | Sí          | Sí           | Recupera cualquier información en forma de recurso. |
| HEAD      | Sí          | Sí           | Idéntico a GET, salvo que en la respuesta no se devuelve contenido. Usado para recibir algunos datos del recurso optimizando la transferencia. |
| POST      | No          | No           | Almacena la entidad enviada. El URN representa a otra entidad que se encargará de gestionar ese almacenamiento. |
| PUT       | No          | Sí           | Almacena la entidad enviada. El URN representa a la propia entidad. |
| DELETE    | No          | Sí           | Elimina la entidad representada por el URN. |
| TRACE     | Sí          | Sí           | Utiliza para debug, el servidor devuelve el propio contenido de la petición. |
| CONNECT   |             |              | Reservado para establecer conexiones permanentes (tunneling) |
| PATCH (*) | No          | Sí           | Realiza modificaciones parciales en entidades existentes. |

(*) El método PATCH es bastante novedoso y no se incluye en el protocolo, aunque está siendo utilizado cada vez más.



### Recursos

Los recursos se identifican por URNs (Uniform Resource Names). Los recursos deben estar identificados de manera unívoca, esto es, sólo debería haber un URN por cada recurso. Ejemplos de recursos válidos son:

 * `/`
 * `/clientes/23`
 * `/clientes/juan-martinez`


Los query parameters enviados no definen recursos. Por ejemplo los siguientes recursos serían equivalentes y no se ajustarían al estándar HTTP. Ambos apuntarían a la colección "clientes":

 * `/clientes?nombre=Juan`
 * `/clientes?nombre=Antonio`


### Cabeceras opcionales

El protocolo HTTP define [una serie de cabeceras](http://www.w3.org/Protocols/HTTP/HTRQ_Headers.html) que pueden enviarse adicionalmente en una petición. Adicionalmente se han extendido otras cabeceras no estándar que muchos servidores aceptan igualmente. Entre las cabeceras más comunes tenemos:

| Nombre   | Descripción      | Ejemplo |
|----------|------------------|---------|
| From     | Identifica al autor de la petición. | From: my@email.com |
| Accept   | Formatos que el cliente acepta | Accept: text/plain, text/html |
| Accept-Encoding | Similar a Accept, especifica los formatos de codificación aceptados. | Accept-Encoding: x-zip |
| Referer  | Especifica la dirección desde la que se ha accedido al recurso | Referer : http://misrecetas.com/pollo-al-pil-pil |


## La respuesta

Una respuesta HTTP consta de:

 * Una linea de status con la versión, el código de respuesta y el nombre del código.
 * Cabeceras opcionales
 * El cuerpo de la respuesta

```http-response
HTTP/1.1 200 OK
Date: Mon, 23 May 2005 22:38:34 GMT
Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)
Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT
ETag: "3f80f-1b6-3e1cb03b"
Content-Type: text/html; charset=UTF-8
Content-Length: 131
Connection: close

<html>
<head>
  <title>An Example Page</title>
</head>
<body>
  Hello World, this is a very simple HTML document.
</body>
</html>
```

### Códigos de respuesta

A continuación se describen algunos códigos de respuesta y su significado. Para una información más completa, consulta la [documentación oficial](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html).

| Código | Nombre | Descripción |
| -------|--------|-------------|
| 100    | Continue | El cliente debe continuar enviando más informacion de la petición. |
| 200    | OK | La petición ha tenido éxito |
| 201    | Created | Un nuevo recurso ha sido creado |
| 202    | Accepted | La petición se ha aceptado y será procesada. |
| 204    | No Content | La petición se ha llevado a cabo con éxito, pero no se devuelve contenido |
| 300    | Multiple choices | Indica al cliente distintas opciones donde encontrar el recurso |
| 301    | Moved permanently | El recurso ya no existe. La nueva ruta debería proporcionarse en el cuerpo de la respuesta |
| 400    | Bad Request | El servidor no pudo procesar la petición porque esta no estaba bien formada |
| 403    | Forbidden | La petición ha sido rechazada |
| 404    | Not Found | El recurso no se ha encontrado |
| 500    | Internal Server Error | Ha ocurrido un error en el servidor |
| 501    | Not Implemented | La funcionalidad aún no ha sido implementada |
| 505    | HTTP Version Not Supported | La versión indicada en la petición es compatible con el servidor |



