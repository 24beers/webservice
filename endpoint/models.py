from django.db import models


class Pair(models.Model):
    key = models.CharField(max_length=20, primary_key=True)
    value = models.CharField(blank=True, max_length=100, null=True)
    owner = models.ForeignKey('auth.User', related_name='pairs')

    def __str__(self):
        return self.owner.username + ': ' + self.key + '/' + self.value

    class Meta:
        ordering = ('owner', 'key')