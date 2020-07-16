from django import template

register = template.Library()

CURRENCY_SYMBOLS = {
    "GBP": "£",
    "USD": "$",
    "EUR": "€"
}

NUMBER_FORMATTING_OPTIONS = {
    "currency_standard": "{:,.2f}",
    "number_standard": "{:.2f}",
    "currency_rounded": "{:,.0f}",
    "number_rounded": "{:.0f}"
}

@register.simple_tag(takes_context=True)
def as_currency(context, value):
    return as_currency_with_user(context['user'], value)


def as_currency_with_user(user, value):
    formatted_number = apply_formatting(value, user.settings.number_format)
    formatted_currency = apply_symbol(formatted_number, user.settings.currency)
    return formatted_currency


def apply_formatting(value, number_format):
    return NUMBER_FORMATTING_OPTIONS.get(number_format).format(value)


def apply_symbol(string, currency):
    if currency in CURRENCY_SYMBOLS.keys():
        return CURRENCY_SYMBOLS.get(currency) + string

    return string
