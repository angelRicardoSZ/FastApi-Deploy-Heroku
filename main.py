#Python
from typing import Optional

#pydantic
from pydantic import BaseModel
from pydantic import Field

# fastapi
from fastapi import FastAPI
from fastapi import Body, Query, Path


app = FastAPI()


# Models
class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Puebla"
        )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Puebla"
        )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="México"
        )




class Person(BaseModel):
    first_name: str 
    last_name: str 
    age: int 
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"hello", "world"}


# request and response body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

@app.get("/person/detail")
def show_person(
    name: str = Query(
        ...,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name (required). It's between 1 and 50 characters",
        example="Pedro"
        ),
    age: Optional[str] = Query(
        None,
        title="Person Age",
        description="This is the person age (optional)",
        example=20
        )
):  
    return {name: age}
    

# Validaciones: Path Parameters
persons = [1,2,3,4,5]


@app.get(
    path="/person/detail/{person_id}",
    # status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person ID. It's required and it's more than 0.",
        example=123
        )
):  
    # if person_id not in persons:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="¡This person doesn´t exist!"    
    #     )
    return {person_id: "It exists!"}


# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    # status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def update_person(
    person_id: int = Path(
        ...,
        title="PERSON_ID",
        desciption="This is the person ID",
        gt=0,
        example=40        
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
