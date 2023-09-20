from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import UserModel , UserProfileModel


@receiver(post_save , sender=UserModel)
def post_save_create_profile_reciver(sender , instance , created , **kwargs):
    if created :
        UserProfileModel.objects.create(user=instance)
        # print("create the user profile !")
    else:
        try :
            profile = UserProfileModel.objects.get(user = instance)
            profile.save()
        except :
            UserProfileModel.objects.create(user=instance)
        #     print("user profile created again !")
        # print('user  updated !')


# @receiver(pre_save , sender=UserModel)
# def pre_save_profile_reciver(sender , instance ,  **kwargs):
#     print(instance.username ,'this user begin saved ')
