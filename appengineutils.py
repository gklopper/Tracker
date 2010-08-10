import os
from google.appengine.ext.webapp import template

def render_template(response, template_name, model):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    response.out.write(template.render(path, model))