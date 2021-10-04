from django.template import Library

register = Library()


@register.filter
def get_rating(rating):
    star = '<i class="fas fa-star"></i>'
    half_star = '<i class="fas fa-star-half-alt"></i>'

    rating_split = [int(rating) for rating in str(rating).split('.')]
    print(rating_split[0] * star)
    return rating_split[0] * star + int(bool(rating_split[1])) * half_star
