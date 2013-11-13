#!/bin/bash
cd "1-introduccion" && pandoc -o ../compiled/docx/tema1.docx la-evolucion-de-php-y-los-frameworks-mvc.md ventajas-e-inconvenientes-de-los-frameworks.md que-es-symfony.md instalacion.md directorios.md composer.md -t docx

