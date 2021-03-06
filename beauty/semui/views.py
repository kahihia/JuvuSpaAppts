from django.http import HttpResponse, Http404
from beauty.util.restful_resource import RESTResource
from semui.models import GET_staff, GET_staff_member, POST_staff


def spa_only(f):
    def w(self, request, *args, **kw):
#        print args, kw
        spa = kw.pop('spa_tag')
        # Check that the user is logged in and a spa-person, get spa.
        return f(self, request, spa, *args, **kw)
    return w


class SpaStaff(RESTResource):

    @spa_only
    def GET(self, request, spa, *args, **kw):
        return HttpResponse(
            GET_staff(spa),
            content_type = 'application/rdf+xml'
        )

    @spa_only
    def PUT(self, request, spa, *args, **kw):
        pass

    @spa_only
    def POST(self, request, spa, *args, **kw):
        print 'POST', spa, repr(request.raw_post_data)
        response_data, url_slug = POST_staff(spa, request.raw_post_data)
        response = HttpResponse(
            response_data,
            status=201,
            content_type = 'application/rdf+xml',
            )
        response['Location'] = 'staff/' + url_slug
        return response

    @spa_only
    def DELETE(self, request, spa, *args, **kw):
        pass


class SpaStaffMember(RESTResource):

    @spa_only
    def GET(self, request, spa, staff_tag, *args, **kw):
        return HttpResponse(
            GET_staff_member(spa, staff_tag),
            content_type = 'application/rdf+xml'
        )

    @spa_only
    def PUT(self, request, spa, staff_tag, *args, **kw):
        pass

    @spa_only
    def POST(self, request, spa, staff_tag, *args, **kw):
        pass

    @spa_only
    def DELETE(self, request, spa, staff_tag, *args, **kw):
        pass
