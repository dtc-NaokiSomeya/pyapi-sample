import json

from pyapp.domain import sub_todo
from pyapp.rest import HttpMethods

# invoked method is mandatory
todo = sub_todo.Todo()
callstacks = [
    ["create",  HttpMethods.POST,  todo.create_todo    ],    # /api/todo/create
    ["update",  HttpMethods.POST,  todo.update_todo    ],    # /api/todo/update
    ["list",    HttpMethods.GET,   todo.list_todo      ]     # /api/todo/list
]
