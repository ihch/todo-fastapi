import json
import os
from typing import List
from fastapi import FastAPI
from pydantic.dataclasses import dataclass

USERNAME: str = os.environ["USERNAME"]
# USERNAME = "ihch"
app = FastAPI()


@dataclass
class Todo:
    todo_name: str
    text: str

    def to_dict(self):
        return {
            "todo_name": self.todo_name,
            "text": self.text
        }


@dataclass
class TodoList:
    todo_list: List[Todo]

    def delete(self, todo_name):
        self.todo_list = [
            todo for todo in self.todo_list if todo.todo_name != todo_name
        ]

    def is_duplicate(self, todo_name):
        return [todo for todo in self.todo_list if todo.todo_name == todo_name].__len__() > 0

    def to_dict(self):
        return {
            "todo_list": [todo.to_dict() for todo in self.todo_list]
        }


@dataclass
class Result:
    success: bool


todo_list = TodoList([Todo('買い物', '卵')])


@app.get("/")
def read_index():
    return {
        "hello": "world",
        "user": USERNAME
    }


@app.get("/todos", response_model=TodoList)
def read_get_todo_list():
    return todo_list.to_dict()


@app.get("/todos/{todo_id}", response_model=Todo)
def read_get_todo(todo_id: int):
    return todo_list.todo_list[todo_id].to_dict()


@app.post("/todos", response_model=Result)
def create_todo_list(todo_name: str, text: str):
    if (todo_list.is_duplicate(todo_name)): return {"success": False}
    todo_list.todo_list.append(Todo(todo_name, text))
    return {"success": True}


@app.put("/todos", response_model=Result)
def create_todo_list(todo_name: str, text: str):
    if (not todo_list.is_duplicate(todo_name)): return {"success": False}
    todo_list.delete(todo_name)
    todo_list.todo_list.append(Todo(todo_name, text))
    return {"success": True}


@app.delete("/todos", response_model=Result)
def delete_todo(todo_name: str):
    todo_list.delete(todo_name)
    return {"success": True}
