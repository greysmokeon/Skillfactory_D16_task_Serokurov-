from django import template

register = template.Library()

restricted_words = ['подлец', 'редиска', 'фигляр']


@register.filter()
def censor(value):
    words = value.split()
    corrected_words = []
    for word in words:
        if word.lower() in restricted_words:
            word = word = list(word)[0] + ''.join([i.replace(i, "*") for i in list(word)[1:-1]]) + list(word)[-1]
            corrected_words.append(word)
        else:
            corrected_words.append(word)

    corrected_words = ' '.join(corrected_words)
    return corrected_words
