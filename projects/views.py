from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from projects.models import Project


def project(request, slug):
    """
    Responsible for publishing a project
    """
    project = get_object_or_404(Project, slug=slug)
    
    return render_to_response(
        "projects/project_yes.html", {
            "project": project,
            "entity": project.get_hosted_by,
            "meta": {"description": project.summary,}
        }, RequestContext(request))
