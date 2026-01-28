# your_app/context_processors.py
def customer_session(request):
    return {
        'session_customer_name': request.session.get('customer_name')
    }