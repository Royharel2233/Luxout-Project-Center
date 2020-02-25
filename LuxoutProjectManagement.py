import pymongo
from bson.objectid import ObjectId
import datetime
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
projectDB = mongoClient.get_database("projects")
projectCollection = projectDB.get_collection("projects")

"""
This is the project record structure:

sampleProj = {"name": "",
            "description": "",
            "notes": "",
            "creation-date": datetime.datetime.now(),
            "status": "incomplete",
            "swatches": [{"id": 0}],
            "shades": [{"typeid": 0, "length": 0, "width": 0, "materialId": 0}],
            "userID": 0}
"""
@app.route('/getProjectsForUser', methods=['POST'])
def getProjectsForUser():
    userID = request.get_json(force=True)["userID"]
    projects = projectCollection.find({"userID": userID})
    projectList = []
    for project in projects:
        projectList.append({"name": project["name"],
                            "description": project["description"],
                            "notes": project["notes"],
                            "creation-date": project["creation-date"],
                            "status": project["status"],
                            "swatches": project["swatches"],
                            "shades": project["shades"],
                            "userID": project["userID"],
                            "projectID": str(project["_id"])})
    return jsonify(projectList)

@app.route("/getProject", methods=['POST'])
def getProject():
    projectID = request.get_json(force=True)["projectID"]
    project = projectCollection.find({"_id": ObjectId(projectID)})[0]
    projectJSON = {"name": project["name"],
                   "description": project["description"],
                   "notes": project["notes"],
                   "creation-date": project["creation-date"],
                   "status": project["status"],
                   "swatches": project["swatches"],
                   "shades": project["shades"],
                   "userID": project["userID"]}
    return projectJSON

@app.route('/newProject', methods=['POST'])
def newProject():
    userID = request.get_json(force=True)["userID"]
    name = request.get_json(force=True)["name"]
    description = request.get_json(force=True)["description"]
    notes = ""
    if "notes" in request.get_json(force=True):
        notes = request.get_json(force=True)["notes"]
    proj = {"name": name,
            "description": description,
            "notes": notes,
            "creation-date": datetime.datetime.now(),
            "status": "incomplete",
            "swatches": list(),
            "shades": list(),
            "userID": userID}
    projectID = projectCollection.insert_one(proj).inserted_id
    return str(projectID)

@app.route('/addSwatchToProject', methods=['POST'])
def addSwatchToProject():
    projectID = request.get_json(force=True)["projectID"]
    swatchID = request.get_json(force=True)["swatchID"]
    project = projectCollection.find({"_id": ObjectId(projectID)})[0]
    swatch = {"id": swatchID}
    if project["swatches"] == None:
        newSwatchesList = list()
    else:
        newSwatchesList = project["swatches"]
    newSwatchesList.append(swatch)
    projectCollection.update_one({"_id": ObjectId(projectID)}, {"$set": {"swatches": newSwatchesList}})
    return jsonify(newSwatchesList)

@app.route('/addShadeToProject', methods=['POST'])
def addShadeToProject():
    projectID = request.get_json(force=True)["projectID"]
    shadeTypeID = request.get_json(force=True)["shadeTypeID"]
    shadeLength = request.get_json(force=True)["shadeLength"]
    shadeWidth = request.get_json(force=True)["shadeWidth"]
    shadeMaterialID = 0
    if "shadeMaterialID" in request.get_json(force=True):
        shadeMaterialID = request.get_json(force=True)["shadeMaterialID"]
    project = projectCollection.find({"_id": ObjectId(projectID)})[0]
    shade = {"typeid": shadeTypeID,
             "length": shadeLength,
             "width": shadeWidth,
             "materialId": shadeMaterialID}
    if project["shades"] == None:
        newShadesList = list()
    else:
        newShadesList = project["shades"]
    newShadesList.append(shade)
    projectCollection.update_one({"_id": ObjectId(projectID)}, {"$set": {"shades": newShadesList}})
    return jsonify(newShadesList)

@app.route('/editProjectDetails', methods=['POST'])
def editProjectDetails():
    changes = {}
    projectID = request.get_json(force=True)["projectID"]
    attributeList = ["name", "description", "notes", "status"]
    for attribute in attributeList:
        if attribute in request.get_json(force=True):
            changes[attribute] = request.get_json(force=True)[attribute]
    projectCollection.update_one({"_id": ObjectId(projectID)}, {"$set": changes})
    return "Success"

# swatchLocalID = index of the swatch in project's swatch list
@app.route('/removeSwatchFromProject', methods=['POST'])
def removeSwatchFromProject():
    projectID = request.get_json(force=True)["projectID"]
    swatchLocalID = request.get_json(force=True)["swatchLocalID"]
    project = projectCollection.find({"_id": ObjectId(projectID)})[0]
    swatchList = project["swatches"]
    swatchList.pop(swatchLocalID)
    projectCollection.update_one({"_id": ObjectId(projectID)}, {"$set": {"swatches": swatchList}})
    return jsonify(swatchList)

@app.route('/removeAllSwatchesFromProject', methods=['POST'])
def removeAllSwatchesFromProject():
    projectID = request.get_json(force=True)["projectID"]
    project = projectCollection.find({"_id": ObjectId(projectID)})[0]
    projectCollection.update_one({"_id": ObjectId(projectID)}, {"$set": {"swatches": []}})
    return "Success"

# shadeLocalID = index of the shade in the project's shade list
@app.route('/removeShadeFromProject', methods=['POST'])
def removeShadeFromProject():
    projectID = request.get_json(force=True)["projectID"]
    shadeLocalID = request.get_json(force=True)["shadeLocalID"]
    project = projectCollection.find({"_id": ObjectId(projectID)})[0]
    shadeList = project["shades"]
    shadeList.pop(shadeLocalID)
    projectCollection.update_one({"_id": ObjectId(projectID)}, {"$set": {"shades": shadeList}})
    return jsonify(shadeList)

@app.route('/removeAllShadesFromProject', methods=['POST'])
def removeAllShadesFromProject():
    projectID = request.get_json(force=True)["projectID"]
    project = projectCollection.find({"_id": ObjectId(projectID)})[0]
    projectCollection.update_one({"_id": ObjectId(projectID)}, {"$set": {"shades": []}})
    return "Success"

@app.route('/deleteProject', methods=['POST'])
def deleteProject():
    projectID = request.get_json(force=True)["projectID"]
    projectCollection.delete_one({"_id": ObjectId(projectID)})
    return "Success"

if __name__ == '__main__':
    app.run(debug=True)
    mongoClient.close()