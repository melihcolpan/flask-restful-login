from flask import jsonify

SERVER_ERROR_500 = ({"message": "An error occured."}, 500)
NOT_FOUND_404 = ({"message": "Resource could not be found."}, 404)
NO_INPUT_400 = ({"message": "No input data provided."}, 400)
INVALID_INPUT_422 = ({"message": "Invalid input."}, 422)
ALREADY_EXIST = ({"message": "Already exists."}, 409)

DOES_NOT_EXIST = ({"message": "Does not exists."}, 409)