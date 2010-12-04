from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import  Project
import appengineutils


class Handler(webapp.RequestHandler):

    def post(self):
        project_id = self.request.get('project-id')
        api_token = self.request.get('api-token')
        project = Project.get()
        project.project_id = project_id
        project.api_token = api_token
        project.put()
        self.redirect('/project')

    def get(self):
        project = Project.get()
        appengineutils.render_template(self.response, 'project.html', {'project' : project})

def main():
    application = webapp.WSGIApplication([('/project', Handler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()