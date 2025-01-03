from django.db import models


class Book(models.Model):
    goodreads_book_id = models.IntegerField(unique=True)
    best_book_id = models.IntegerField(unique=True)
    work_id = models.IntegerField(unique=True)
    books_count = models.IntegerField()
    isbn = models.CharField(max_length=20)
    isbn13 = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    authors = models.CharField(max_length=255)
    original_publication_year = models.FloatField()
    language_code = models.CharField(max_length=10, blank=True, null=True)
    average_rating = models.FloatField()
    ratings_count = models.IntegerField()
    work_ratings_count = models.IntegerField()
    work_text_reviews_count = models.IntegerField()
    ratings_1 = models.IntegerField()
    ratings_2 = models.IntegerField()
    ratings_3 = models.IntegerField()
    ratings_4 = models.IntegerField()
    ratings_5 = models.IntegerField()
    image_url = models.URLField()
    small_image_url = models.URLField()

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]

    def __str__(self):
        return self.title
