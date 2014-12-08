from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from timezone_field import TimeZoneField
from thumbs import ImageWithThumbsField

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    telefono = models.PositiveIntegerField(null=True, blank=True)
    provincia = models.CharField(max_length=40)
    distrito = models.CharField(max_length=40)
    departamento = models.CharField(max_length=50)
    zona_horaria = TimeZoneField(default='America/Lima')
    picture = ImageWithThumbsField(upload_to='profile_images', blank=True)

    class Meta:
        permissions = (
            ('list_profil', 'Puedes listar'),
            ('view_profil', 'Puedes visualizar'),
            ('add_profil', 'Can agregar'),
            ('change_profil', 'Puedes editar'),
            ('delete_profil', 'Puedes eliminar'),
        )
    def __unicode__(self):
        return self.user.username
    @models.permalink
    def get_absolute_url(self):
        return ('user_profile_detail', [int(self.pk)])
