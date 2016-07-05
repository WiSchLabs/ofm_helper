import factory

from users.models import OFMUser


class OFMUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OFMUser

    username = "ArthurDent"
    password = "42"
    email = "Arthur.Dent@ofmhelper.de"
    ofm_username = "Trillian"
    ofm_password = "so long and thanks for all the fish"
