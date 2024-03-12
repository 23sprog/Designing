from django.core.paginator import Paginator

def paginator_sprog(query_set, page_num=None, per_page=1):
    next_page = False
    after_next_page = False
    previous_page = False
    before_previous_page = False
    if page_num == None:
        page_num = 1
    p = Paginator(query_set, per_page)
    this_page = p.get_page(page_num)
    if this_page.has_next():
        next_page = p.get_page(this_page.number + 1)
        if next_page.has_next():
            after_next_page = p.get_page(next_page.number + 1)
    if this_page.has_previous():
        previous_page = p.get_page(this_page.number - 1)
        if previous_page.has_previous():
            before_previous_page = p.get_page(previous_page.number - 1)
    obj = {"page_obj": p, "this_page": this_page, "next_page": next_page,
                                        "previous_page":previous_page, "after_next_page": after_next_page,
                                        "before_previous_page": before_previous_page}
    return obj


def get_list_to_ten():
    return [num for num in range(1,11)]


def get_overall_price_of_carts(query_set):
    overall_price = 0
    for obj in query_set:
        overall_price += obj.get_overall_price()
    return overall_price