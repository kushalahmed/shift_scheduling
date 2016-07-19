from pyramid.view import view_config


@view_config(route_name='home', renderer='shift_scheduling:templates/mytemplate.pt')
def my_view(request):
    return {'project': 'shift_scheduling'}