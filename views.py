from todoapp.models import users,todos
#authenticate
#login
#view for listing all todos
#view creating a new todo
#view for fetching a specific todo
#list all todos created by authenticate user
#view for updating a specific todo
#view for deleting a specific todo
#logout

session={}

def signin_required(fn):
    def wraper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("You must login")
    return wraper




def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user=[user for user in users if user["username"]==username and user["password"]==password ]
    return user


class SignInView:
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            session["user"]=user[0]
            print("Login Success")
        else:
            print("Invalid username or password !")


class TodoView:
    @signin_required
    def get(self,*args,**kwargs):
        return todos

    @signin_required
    def post(self,*args,**kwargs):
        userId=session["user"]["id"]
        kwargs["userId"]=userId
        todos.append(kwargs)
        print("Todo added")
        print(todos)


class AuthenticTodoListView:
    def get(self,*args,**kwargs):
        userId=session["user"]["id"]
        aut_todos=[todo for todo in todos if todo["userId"]==userId]
        return aut_todos


class TodosDetails():
    def get_object(self,id):
        todo=[todo for todo in todos if todo["todoId"]==id]
        return todo

    @signin_required
    def get(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        todo=self.get_object(todo_id)
        return todo

    @signin_required
    def delete(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        data=[todo for todo in todos if todo["todoId"]==todo_id]
        if data:
            todo=data[0]
            todos.remove(todo)
            print("Todo deleted")

    @signin_required
    def put(self,*args,**kwargs):
        todo_id=kwargs.get("post_id")
        value=self.get_object(todo_id)
        data=kwargs.get("data")
        if value:
            todo_obj=value[0]
            todo_obj.update(data)
            print(todo_obj)



def signout(*args,**kwargs):
    user=session.pop("user")
    print(f"The user {user['username']}  has been logged out")



login=SignInView()
login.post(username="akhil",password="Password@123")
print(session)


Authen_todos=AuthenticTodoListView()
print("Todos created by logged user")
print(Authen_todos.get())


todo_detail=TodosDetails()
# todo_detail.delete(todo_id=8)
# print(todo_detail.get(todo_id=7))

data={
    "task_name": "wifibill"
}

print(todo_detail.put(todo_id=2,data=data))



signout()


# data=TodoView()
# print(data.get())
# data.post(todoId=9,task_name="ibill",completed=True)
