from django.contrib import admin
from .models import Book, Author, BookReview, BookAuthor


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')

class AuthorAdmin(admin.ModelAdmin):
    pass

class BookAuthorAdmin(admin.ModelAdmin):
    pass

class BookReviewAdmin(admin.ModelAdmin):
    pass



admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
