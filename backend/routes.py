from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    
    return {"message": "Internal server error"}, 500


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        pictures = [item for item in data if item["id"]== id]

        if len(pictures) > 0:
            return pictures[0],200
        else:
            return {"error":"Picture not found"}, 404
    
    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json(silent=True)

    if not picture:
        return {"error": "Request body is required"}, 400
    
    if data:
        existing_picture = [item for item in data if item["id"]==picture["id"]]
        
        if len(existing_picture)>0:
            return {"Message": f"picture with id {picture['id']} already present"}, 302
        
        data.append(picture)

        return picture,201
    
    return {"message": "Internal server error"}, 500




######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json(silent=True)

    if not picture:
        return {"error": "Request body is required"}, 400
    
    if data:picture = request.get_json(silent=True)

    if not picture:
        return {"error": "Request body is required"}, 400
    
    if data:
        existing_picture = [(id,item) for (id,item) in enumerate(data) if item["id"]==picture["id"]]
        
        if len(existing_picture)>0:
            id,_ = existing_picture[0]
            data[id]=picture
            return picture

        return {"message": "picture not found"},404
    
    return {"message": "Internal server error"}, 500
        
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        existing_picture = [(idx,item) for (idx,item) in enumerate(data) if item["id"]==id]
        
        if len(existing_picture)>0:
            idx,_ = existing_picture[0]
            del data[idx]
            return {"message":"deleted successfully"},204

        return {"message": "picture not found"},404
    
    return {"message": "Internal server error"}, 500
