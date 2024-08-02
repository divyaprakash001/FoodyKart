from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User,UserProfile

 # create a receiver
  
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
  print(created)
  print(instance)
  if created:
    UserProfile.objects.create(user=instance)
    print("User profile is created")
  
  else:
    try:
      profile = UserProfile.objects.get(user=instance)
      profile.save()
      print("user is updated")
    except:
      #create the user profile if not exist
      UserProfile.objects.create(user=instance)
      print("User profile was not exist but I created once again")

    

# this is the one way connecting receiver to sender but we use decorator for this
# post_save.connect(post_save_create_profile_receiver, sender=User)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
  print(instance.username, "this user is being saved.")