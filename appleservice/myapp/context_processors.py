def session_user(request):
    return {
        'is_logged_in': 'user_id' in request.session,
        'session_uid': request.session.get('user_id'),
        'session_email': request.session.get('email'),
        'session_worker': request.session.get('worker'),
        'session_location': request.session.get('location'),
    }