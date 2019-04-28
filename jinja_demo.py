from jinja2 import Template

my_string = 'Hello {{ substitute }}'
t = Template(my_string)

my_string = (t.render(substitute="World"))

print(my_string)
