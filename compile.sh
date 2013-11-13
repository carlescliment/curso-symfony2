#!/bin/bash
cd "1-introduccion" && pandoc -o ../compiled/docx/tema1.docx la-evolucion-de-php-y-los-frameworks-mvc.md ventajas-e-inconvenientes-de-los-frameworks.md que-es-symfony.md instalacion.md directorios.md composer.md profiler-y-consola.md -t docx
cd ..
cd "2-symfony-a-vista-de-pajaro" && pandoc -o ../compiled/docx/tema2.docx fundamentos-http.md request-response.md routing.md controller.md templating.md model.md -t docx

