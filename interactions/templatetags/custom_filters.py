from django import template


register = template.Library()


@register.filter(name='zip_lists')
def zip_lists(list1, list2):
    """ Zips two lists (or list like objects) together. Used in 
    ``interactions/questions.html``. Raises ``TemplateSyntaxError``
    if ``list1`` and ``list2`` are of unequal lengths. """

    if len(list1) != len(list2):
        raise template.TemplateSyntaxError(
            'Only lists of equal length can be zipped'
        )
    return zip(list1, list2)

@register.filter(name='truncate_name')
def truncate_name(string, size):
	""" Truncate an str whose length is greater than size,
	and add ellipsis at the end. """
	return f"{string[:size]}..."

@register.filter(name='make_subsets')
def make_subsets(data, size: int) -> list:
    """ Creates subsets out of ``data``, each subset having ``size``
    elements. Used in ``graphs/multiple_results.html`` and 
    ``graphs/single_result.html``. """

    subset_list = list()
    if type(data) is list:
        subset = list()
        while True:
            subset.append(data.pop())
            if len(subset) == size:
                subset_list.append(subset)
                subset = list()
            if not data:
                subset_list.append(subset)
                break

    elif type(data) is dict:
        subset = dict()
        while True:
            key, value = data.popitem()
            subset.update({key: value})
            if len(subset) == size:
                subset_list.append(subset)
                subset = dict()
            if not data:
                subset_list.append(subset)
                break

    return subset_list
