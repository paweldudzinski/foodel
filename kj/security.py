def groupfinder(userid, request):
    user = request.user
    if user and user.is_admin:
        return ['admin']
    elif user:
        return ['user']
