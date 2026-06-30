from functools import wraps
from django.shortcuts import redirect

def allowed_roles(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):

           
            user_role = request.user.role

            # If user not logged in → go to login page
            if not request.user.is_authenticated:
                return redirect('dologin')

            # If role is allowed → continue
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # If role is NOT allowed → redirect to their role home page
            role_redirect_map = { 
                # MoJ Role               
                'moj_head': 'moj_head_home',
                'moj_officers': 'moj_officers_home',
                'moj_it_head': 'moj_it_head',
                # LDEA Role
                'ldea_head': 'ldea_head_home',
                'officers': 'officers_home',  
                'ldea_head_of_it': 'ldea_head_of_it_home',
                # MoH Role
                'moh_head': 'moh_head_home',
                'moh_officers': 'moh_officers_home',
                
                # MoG Role
                'mog_head': 'mog_head_home',
                'mog_officers': 'mog_officers_home',
                
                
                
            }

            redirect_url = role_redirect_map.get(user_role)

            if redirect_url:
                return redirect(redirect_url)

            return redirect('dologin')

        return wrapper_func

    return decorator