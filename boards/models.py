from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse


BOARD_TYPE_CHOICES = (
    ('P', 'Personal'),
    ('T', 'Team')
)


class Board(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='board')
    board_type = models.CharField(choices=BOARD_TYPE_CHOICES, max_length=1)
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    team = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='team')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('boards:board_detail', kwargs={'slug': self.slug})


class BoardList(models.Model):
    board = models.ForeignKey(
        'Board', on_delete=models.CASCADE, related_name='board_list')
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_archived_cards(self):
        cards = ListCard.objects.filter(board_list=self.pk, archived=True)
        print(cards)
        return cards

    def get_non_archived_cards(self):
        cards = ListCard.objects.filter(board_list=self.pk, archived=False)
        return cards


class ListCard(models.Model):
    board_list = models.ForeignKey(
        'BoardList', on_delete=models.CASCADE, related_name='list_card')
    due_date = models.DateField()
    title = models.CharField(max_length=250)
    description = models.TextField()
    attachment = models.FileField(
        upload_to='media/attachment/', blank=True, null=True)
    archived = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Board)
def create_slug(sender, instance, created, **kwargs):
    if created:
        slug_var = instance.title + " " + str(instance.pk)
        instance.slug = slugify(slug_var)
        # print(slugify(slug_var))
        instance.save()
