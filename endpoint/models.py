from django.db.models import CharField, ForeignKey, Model


class Pair(Model):
    key = CharField(max_length=20)
    value = CharField(blank=True, max_length=100)
    owner = ForeignKey('auth.User', related_name='pairs')

    def __str__(self):
        return self.token + ': ' + self.key + '/' + self.value