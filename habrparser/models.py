from django.db import models
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Hub(models.Model):
    slug = models.SlugField(unique=True, verbose_name="Название хаба")
    period = models.TimeField(verbose_name="Период обхода")

    def __str__(self) -> str:
        return self.slug

    def save(self, *args, **kwargs):
        super(__class__, self).save(*args, **kwargs)

        interval, _ = IntervalSchedule.objects.get_or_create(
            every=self.period.second,
            period="seconds",
        )

        PeriodicTask.objects.create(
            name=f"HabrParser Task {self.id}",
            interval=interval,
            task="habrparser.tasks.parse_habr_task",
            args=f'["{self.slug}"]',
        )


class Article(models.Model):
    title = models.CharField("Название статьи")
    link = models.CharField("Ссылка на статью")
    date = models.DateTimeField("Дата публикации")
    author = models.CharField("Никнейм автора")
    author_link = models.CharField("Ссылка на автора")
    text = models.TextField(verbose_name="Текст статьи")

    def __str__(self) -> str:
        return self.title
