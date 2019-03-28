import json
import logging
from enum import Enum
from cerberus import Validator
from premailer import transform
from pynliner import Pynliner

message = {'id': 1, 'name': 'name1'}
str_message = json.dumps(message)
dict_message = json.loads(str_message)

print(json.dumps(message))
print(type(dict_message))


# output:
# {"id": 1, "name": "name1"}
# <class 'dict'>

def aaa(name, id):
    print("name is : {name}, id is {id}".format(id=id, name=name, ))


aaa(dict_message, 2)
# output:
# name is : {'id': 1, 'name': 'name1'}, id is 2

print(tuple(message.values()))


# print({**message})

# output:
# (1, 'name1')


class Color(Enum):
    red = 1
    green = 2
    blue = 3


print(Color.red.value)
# output:
# 1

a = ('a', 'b', 1, 2, 'c')
print(a[1])
# output:
# b


git_url = "git@git.jdb-dev.com:pluto/h5_template.git"
name = (git_url.split(':').pop())[:-4].replace('/', '-')
print(name)


# output:
# pluto-h5_template

def aa(a, b, c):
    print(a)
    print(b)
    print(c)


abc = {
    "a": 1,
    "b": 2,
    "c": 3,
}
aa(**abc)


# output:
# 1
# 2
# 3

def abcc(**x):
    print(x)


abcc(a=1, b=2, c=3)

# output:
# {'a': 1, 'b': 2, 'c': 3}

v = Validator()
schema = {
    'git_url': {
        'type': 'string',
        'required': True,
    },

}
document = {
}
print(v.validate(document, schema))
print(v.errors)
# output：
# False
# {'git_url': ['required field']}

schema = {'role': {'type': 'string', 'allowed': ['agent', 'client', 'supplier']}}
print(v.validate({'role': 'agent'}, schema))
print(v.errors)

a = {
    "a": 1,
    "b": 2,
    "c": 3
}
b = {
    "a": 2,
    "b": "aaa",
}
print({**a, **b})  # {'a': 2, 'b': 'aaa', 'c': 3}
print({**b, **a})  # {'a': 1, 'b': 2, 'c': 3}

print(transform("""
<style type="text/css">
  style .pure-table {
    border-collapse: collapse;
    border-spacing: 0;
    empty-cells: show;
    border: 1px solid #cbcbcb
  }

  .pure-table caption {
    color: #000;
    font: italic 85%/1 arial, sans-serif;
    padding: 1em 0;
    text-align: center
  }

  .pure-table td,
  .pure-table th {
    border-left: 1px solid #cbcbcb;
    border-width: 0 0 0 1px;
    font-size: inherit;
    margin: 0;
    overflow: visible;
    padding: .5em 1em
  }

  .pure-table td:first-child,
  .pure-table th:first-child {
    border-left-width: 0
  }

  .pure-table thead {
    background-color: #e0e0e0;
    color: #000;
    text-align: left;
    vertical-align: bottom
  }

  .pure-table td {
    background-color: transparent
  }

  .pure-table-odd td,
  .pure-table-striped tr:nth-child(2n-1) td {
    background-color: #f2f2f2
  }

  .pure-table-bordered td {
    border-bottom: 1px solid #cbcbcb
  }

  .pure-table-bordered tbody>tr:last-child>td {
    border-bottom-width: 0
  }

  .pure-table-horizontal td,
  .pure-table-horizontal th {
    border-width: 0 0 1px;
    border-bottom: 1px solid #cbcbcb
  }

  .pure-table-horizontal tbody>tr:last-child>td {
    border-bottom-width: 0
  }
</style>
<table class="pure-table">
  <thead>
    <tr>
      <td>a</td>
      <td>b</td>
      <td>c</td>
      <td>d</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>2</td>
      <td>3</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
 """))

print(Pynliner().from_string(
    """
    <style>
  table {
    border-collapse: collapse;
  }

  table, th, td {
    border: 1px solid black;
  }
  td {
    padding: 0 20px;
  }
  thead {
    background: rgb(42, 150, 228);
    color: #fff;
  }
</style>
<table>
  <thead>
    <tr>
      <td>a</td>
      <td>b</td>
      <td>c</td>
      <td>d</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>2</td>
      <td>3</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
    """
).run())

import os
import sys

print('_________________')

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


def render_template(template, **kwargs):
    if not os.path.exists(template):
        print('No template file present: %s' % template)
        sys.exit()

    import jinja2
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)
    return templ.render(**kwargs)


html = render_template(os.path.join(ROOT_DIR, 'template.html'), message={"a": 1, "b": 2})
print(html)


def a(**kwargs):
    print(**kwargs)


b = {"c": 2, "b": 1, "a": 0}


try:
    aaaz = json.loads('{"c": 2, "b": 1, "a": 0}')
except json.JSONDecodeError:
    aaaz = 'as sad sad'
print(aaaz)
