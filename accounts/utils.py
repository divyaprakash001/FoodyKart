# containing helper functions

def detectUser(user):
  if user.role == 1:
    redirectUrl = 'vendorDashboard'
    return redirectUrl
  elif user.role == 2:
    redirectUrl = 'customerDashboard'
    return redirectUrl
  elif user.role == None and user.is_superadmin:
    redirectUrl = '/admin'
    return redirectUrl