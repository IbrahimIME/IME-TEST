from flask import jsonify, make_response
from flask_restx import Namespace, Resource

api = Namespace(path = "/<any_other_path>", name = "Invalid Endpoint")

# GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
@api.route("")
class ApiNotFound(Resource):
	@api.doc(
		description = "404 Not Found",
		responses = { 404: "Endpoint not found" }
	)
	def get(self, any_other_path):
		response = {
			"error": "Invalid endpoint URL",
			"method": "GET",
			"url": "/" + any_other_path
		}
		return make_response(jsonify(response), 404)

	@api.doc(
		description = "404 Not Found",
		responses = { 404: "Endpoint not found" }
	)
	def post(self, any_other_path):
		response = {
			"error": "Invalid endpoint URL",
			"method": "POST",
			"url": "/" + any_other_path
		}
		return make_response(jsonify(response), 404)

	@api.doc(
		description = "404 Not Found",
		responses = { 404: "Endpoint not found" }
	)
	def put(self, any_other_path):
		response = {
			"error": "Invalid endpoint URL",
			"method": "PUT",
			"url": "/" + any_other_path
		}
		return make_response(jsonify(response), 404)

	@api.doc(
		description = "404 Not Found",
		responses = { 404: "Endpoint not found" }
	)
	def patch(self, any_other_path):
		response = {
			"error": "Invalid endpoint URL",
			"method": "PATCH",
			"url": "/" + any_other_path
		}
		return make_response(jsonify(response), 404)

	@api.doc(
		description = "404 Not Found",
		responses = { 404: "Endpoint not found" }
	)
	def delete(self, any_other_path):
		response = {
			"error": "Invalid endpoint URL",
			"method": "DELETE",
			"url": "/" + any_other_path
		}
		return make_response(jsonify(response), 404)

	@api.doc(
		description = "404 Not Found",
		responses = { 404: "Endpoint not found" }
	)
	def head(self, any_other_path):
		response = {
			"error": "Invalid endpoint URL",
			"method": "HEAD",
			"url": "/" + any_other_path
		}
		return make_response(jsonify(response), 404)

	@api.doc(
		description = "404 Not Found",
		responses = { 404: "Endpoint not found" }
	)
	def options(self, any_other_path):
		response = {
			"error": "Invalid endpoint URL",
			"method": "OPTIONS",
			"url": "/" + any_other_path
		}
		return make_response(jsonify(response), 404)
