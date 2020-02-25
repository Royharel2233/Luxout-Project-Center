# LUXOUT Project Management
All request parameters are expected in the JSON-formatted body.

**POST** `/getProjectsForUser`


Accepts: 


> “userID” - unique user ID with which projects are associated 

Returns:

> List of projects in the following JSON format:
> 
> {	"name": “",
>   ”description": “”,
>   "notes": “",
>   "creation-date": datetime.datetime,
>   "status": “incomplete",
>   "swatches": [{"id": 0}],
>   "shades": [{"typeid": 0, "length": 0, "width": 0, "materialId": 0}],
>   "userID": 0,
>   "projectID": "0"}


**POST** `/getProject`

Accepts:


> “projectID” - unique project ID 

Returns:

> Project details in the following JSON format:
> 
> {	"name": “",
> 	”description": “”,
> 	"notes": “",
> 	"creation-date": datetime.datetime,
> 	"status": “incomplete",
> 	"swatches": [{"id": 0}],
>             "shades": [{"typeid": 0, "length": 0, "width": 0, "materialId": 0}],
>             "userID": 0}


**POST** `/newProject`

Accepts:

> “name” - new project’s name
>
> “description” - new project’s description
>
> “notes” - (optional) new project’s notes


Returns:


> (string) new project’s ID 

**POST** `/addSwatchToProject`

Accepts:

> “projectID” - project to add the swatch to
> 
> “swatchID” - swatch ID (from external DB)

Returns:

>  (json) updated list of swatches for the project

**POST** `/addShadeToProject`

Accepts:

> “projectID” - new project’s name
> 
> “shadeTypeID” - new project’s description
> 
> “shadeLength” - (double) shade’s length
> 
> “shadeWidth” - (double) shade’s width
> 
> “shadeMaterialID” - (optional) external material ID for the shade

Returns:

>  (json) updated list of shades for the project

**POST** `/editProjectDetails`

Accepts:

> “projectID” - project to update
>
> “name” - (optional) updated project name
>
> “description” - (optional) updated project description
>
> “notes” - (optional) updated project notes

Returns:

> (string) “Success”

**POST** `/removeSwatchFromProject`

Accepts:

> “projectID” - project to remove swatch from
>
> “swatchLocalID” - (int) local index of the swatch to remove, within the project

Returns:

> (json) updated list of swatches for the project

**POST** `/removeAllSwatchesFromProject`

Accepts:

> “projectID” - project to remove all swatches from

Returns:

> (string) “Success”

**POST** `/removeShadeFromProject`

Accepts:

> “projectID” - project to remove shade from
>
> “shadeLocalID” - (int) local index of the shade to remove, within the project

Returns:

> (json) updated list of shades for the project

**POST** `/removeAllShadesFromProject`

Accepts:

> “projectID” - project to remove all shades from

Returns:

> (string) “Success”

**POST** `/deleteProject`

Accepts:

> “projectID” - project to delete

Returns:

> (string) “Success”

