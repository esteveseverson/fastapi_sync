from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

fake_db = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo'}


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': fake_db}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_by_id(user_id: int):
    if user_id < 1 or user_id > len(fake_db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='USER NOT FOUND'
        )

    return fake_db[user_id - 1]


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        id=len(fake_db) + 1,
        **user.model_dump(),  # transforma do pydentic para um dicionario
    )

    fake_db.append(user_with_id)

    return user_with_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(id=user_id, **user.model_dump())

    # validando alcance do user_id
    if user_id < 1 or user_id > len(fake_db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='USER NOT FOUND'
        )

    fake_db[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(fake_db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='USER NOT FOUND'
        )

    del fake_db[user_id - 1]

    return {'message': 'User deleted!'}
