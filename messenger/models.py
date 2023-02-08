from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


class ThreadManager(models.Manager):
    def find(self, user1, user2):
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset) > 0:
            return queryset[0]
        return None

    def find_or_create(self, user1, user2):
        thread = self.find(user1, user2)
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1, user2)
        return thread


class Thread(models.Model):
    users = models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message)
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de Edición')

    objects = ThreadManager()

    class Meta():
        ordering = ['-updated']


def messages_changed(sender, **kwargs):
    # Every value from kwargs.pop(...) return an object and as we know that when
    # we use another variable asignament to an object we do not get a new object
    # instead we point to the same memory space and therefore if we change the value
    # of that variable we also change the value of the original object, so if we change
    # instance, action or pk_set value we will modify the orginal value of the object
    instance = kwargs.pop("instance", None)
    action = kwargs.pop("action", None)
    pk_set = kwargs.pop("pk_set", None)

    # # The bellow lines are just for test
    # print('The instance is: ', instance)
    # print('The action is: ', action)
    # print('The pk_set is: ', pk_set)

    false_pk_set = set()
    # pre_add es la accion que se ejecuta antes de agregar informacion al campo ManyToMany
    if action == "pre_add":
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                # # The following print is just for test
                # print("Ups, ({}) no forma parte del hilo".format(msg.user))
                false_pk_set.add(msg_pk)

    # Borramos de pk_set los pk que se encuentran en false_pk_set
    # aca estamos afectando al valor original de pk_set que utiliza django
    # por dentro para guardar el registro por que al usar pk_set = kwargs.pop("pk_set", None)
    # estamos apuntando al mismo espacio de memoria del conjunto que pertence a la palabra clave pk_set de kwargs
    pk_set.difference_update(false_pk_set)

    # Forzar la actualizacion del campo updated en el modelo (Thread) ya que los campos ManyToMany no afectan directamente
    # a los campos DateTimeField, ellos se gestionan aparte y por lo tanto cada vez que agregamos nuevos mensajes nuestro
    # campo llamado updated no se actualiza, pero nosotros podemos hacer eso manualmente utilizando el metodo save() de la
    # instancia que se esta modificando
    instance.save()


# con Thread.messages.through especificamos el campo ManyToMany con el que vamos a conectar la señal
m2m_changed.connect(messages_changed, sender=Thread.messages.through)
