from flask import  json, request
from pedidos.application.articulo_service import ArticulosService
from pedidos import app
from pedidos import articulos_repository
from pedidos.domain.articulo import Articulo


@app.route("/articulos-api", methods=["GET"])
def articulos_api_get_all():
    articulosService = ArticulosService(articulos_repository)
    articulos = articulosService.find_all("")

    data = []
    for articulo in articulos:
        data.append({
            "id": articulo.id(),
            "codigo": articulo.codigo(),
            "nombre": articulo.nombre()
        })

    return app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )

@app.route("/articulos-api/<id>", methods=["GET"])
def articulos_api_get_one(id):
    articulosService = ArticulosService(articulos_repository)
    articulo = articulosService.get_by_id(id)

    if(articulo is None):
        data = {
            "success": "0",
            "error": "Articulo no encontrado",
        }
        return app.response_class(
            response=json.dumps(data),
            mimetype='application/json'
        )        

    data = {
        "success": "1",
        "articulo": {
            "id": articulo.id(),
            "codigo": articulo.codigo(),
            "nombre": articulo.nombre()
        }
    }
    return app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )

@app.route("/articulos-api/update/<id>", methods=["POST"])
def articulos_api_update(id):
    articulosService = ArticulosService(articulos_repository)
    articulo = articulosService.get_by_id(id)
    if request.method == "POST":
        articulo.setCodigo(request.form["codigo"])
        articulo.setNombre(request.form["nombre"])
        articulosService.update(articulo)

        data = {
            "success": "1",
            "message": "Articulo actualizado"
        }
        return app.response_class(
            response=json.dumps(data),
            mimetype='application/json'
        )

@app.route("/articulos-api/create/", methods=["POST"])
def articulos_api_create():
    articulosService = ArticulosService(articulos_repository)
    
    try:
        data = request.get_json()
        if not data or "codigo" not in data or "nombre" not in data:
            return app.response_class(
                response=json.dumps({"success": "0", "message": "Datos inválidos"}),
                mimetype='application/json'
            ), 400

        # Usar get_next_id para obtener el id si es necesario
        new_id = articulosService.get_next_id()
        nuevo_articulo = Articulo(new_id, data["codigo"], data["nombre"])
        articulosService.add(nuevo_articulo)

        response_data = {
            "success": "1",
            "message": "Articulo creado",
            "articulo": {
                "id": nuevo_articulo.id(),
                "codigo": nuevo_articulo.codigo(),
                "nombre": nuevo_articulo.nombre()
            }
        }
        return app.response_class(
            response=json.dumps(response_data),
            mimetype='application/json'
        ), 201

    except Exception as e:
        error_response = {
            "success": "0",
            "message": "Error al crear el articulo",
            "error": str(e)
        }
        print("Error en articulos_api_create:", str(e))
        return app.response_class(
            response=json.dumps(error_response),
            mimetype='application/json'
        ), 500


    
@app.route("/articulos-api/delete/<id>", methods=["GET"])
def articulos_api_delete(id):
    articulosService = ArticulosService(articulos_repository)
    articulo = articulosService.get_by_id(id)
    if articulo is None:
        data = {
            "success": "0",
            "error": "Articulo no encontrado"
        }
        return app.response_class(
            response=json.dumps(data),
            mimetype='application/json'
        )

    articulosService.remove(articulo)

    data = {
        "success": "1",
        "message": "Articulo eliminado"
    }
    return app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )