# Sample python rest api app using flask

## How to enhance

### Add API

You add python file to "pyapp/rest".
For example, you add "xxx.py", So https://{your_fqdn}/xxx API path will be created.

xxx.py should be write following statement.

```py
from pyapp.rest import HttpMethods
from pyapp.domain.sample import Sample
sample = Sample()
callstacks = [
    ["subpath1", HttpMethods.POST,  sample.post_function]
    ["subpath2", HttpMethods.GET,   sample.get_function]
]
```

On this example, following API is defined.

```
1: POST    xxx/subpath1
2: GET     xxx/subpath2
```
1 -> call `post_function`
2 -> call `get_function`

### Add business(domain) logic

You add python file to "pyapp/domain".
The function implement domain logic must be called by module on pyapp.rest package.

### Add exception

You add Exception class inherit BaseRestException to pyapp/exceptions.py
See InvalidContentType class.

## Appendix

### Why not use Flask-RESTful ?

Flask-RESTful is awesome project to quickly bulild RESTful API app.
But it is not general public.