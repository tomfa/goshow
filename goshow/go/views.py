# -*- encoding: utf-8 -*-#
from django.http import Http404
from django.shortcuts import render
from go.models import List, ListItem
from django.core import serializers


# When people go to www.webpage.com | POST: none
def index(request):
    context = {
        'title': 'Go!',
        'username': request.user.username,
    }
    return render(request, 'go/index.html', context)


# Returns all the lists for a spesific user in an Lists-view | Post: none
def getAllLists(request):
    try:
        lists = List.objects.permitted_objects(user=request.user).filter(removed=False)
    except (TypeError, List.DoesNotExist):
        if List.objects.filter(user=request.user, removed=False).count() == 0:
            # If user has no lists, we create example lists
            createDefaultList(request)
        else:
            raise Http404

    return render(request, 'go/lists.html', {
        'list': serializers.serialize("json", lists),
        'user': request.user.username,
    })


# Returns a serializes JSON-object of a spesific list | Post: list.key
def getList(request):
    try:
        key = request['id']  # Searches POST first, then GET
        list = List.objects.filter(pk=key)
        if not (request.user == list.user or list.public):  # User has access
            raise Http404
    except (TypeError, List.DoesNotExist):
        raise Http404

    return render(request, 'go/individual_list.html'), {
        'list': serializers.serialize("json", list),
        'user': request.user.username,
    }


# Skeleton for all the AJAX-operations
def operation(request):
    try:
        object = request.POST['object']  # type (list or item)
        action = request.POST['action']  # action (delete|rename|weight|add|check)
        if object == 'list':
            if action == 'add':
                return add_list(
                    request,
                    request.POST['title'],
                    request.POST['public'])
            elif action == 'delete':
                return delete_list(
                    request,
                    request.POST['id'])
            elif action == 'rename':
                return rename_list(
                    request,
                    request.POST['id'],
                    request.POST['newTitle'])
        elif object == 'item':
            if action == 'add':
                return add_item(
                    request,
                    request.POST['parentid'],
                    request.POST['title'],
                    request.POST['nextstep'],
                    request.POST['weight'])
            elif action == 'delete':
                return delete_list(
                    request,
                    request.POST['id'])
            elif action == 'rename':
                return rename_list(
                    request,
                    request.POST['id'],
                    request.POST['newTitle'])
            elif action == 'change_weight':
                return change_item_weight(
                    request,
                    request.POST['id'],
                    request.POST['weight'])
            elif action == 'check':
                return check_item(
                    request,
                    request.POST['id'],
                    request.POST['uncheck'])
        return 0  # Somewhere, something went wrong. Returns 0
    except:
        return 0  # 0 - the undefined error


# Adds list
def add_list(request, title, public=False):
    if request.user.is_authenticated():
        try:
            list = List.objects.create(
                title=title,
                user=request.user,
                public=public)
            list.save()
            return list.pk  # List added successfully
        except:
            return 0  # Error
    else:
        return -1  # User not authenticated


# Removing a list | POST: key, op: delete
def delete_list(request, key):
    list = find_list(key)
    if (list):
        if (list.user == request.user):
            list.remove()
            return key  # List was deleted
        else:
            return -1  # User is not authenticated
    return 0  # List could not be found


# For renaming a list | POST: op: rename_list, key, newTitle
def rename_list(request, key, newTitle):
    list = find_list(key)
    if (list):
        if (list.user == request.user):
            list.title = newTitle
            list.save()
            return key  # List was renamed
        else:
            return -1  # User is not authenticated
    return 0  # List could not be found


# Adds an item to an existing list
def add_item(request, parentkey, title, nextstep=None, weight=0):
    item = find_item(parentkey)
    if (item):
        if (item.user == request.user):
            item = ListItem.objects.create(
                title=title,
                user=request.user,
                nextstep=nextstep,
                weight=weight)
            item.save()
            return item.pk  # List was renamed
        else:
            return -1  # User is not authenticated
    return 0  # List could not be found


# (Un)checks an item
def check_item(request, key, uncheck=False):
    item = find_item(key)
    if (item):
        if (item.parent.user == request.user):
            if (uncheck):
                item.uncheck()
            else:
                item.check()
            item.save()
        else:
            return -1  # User is not authenticated
    return 0  # Item could not be found


# Changes the weight of a given item
def change_item_weight(request, key, weight):
    item = find_item(key)
    if not item or abs(weight) > 100000:
        return 0  # Item could not be found (or redundant weightcheck kicks)
    else:
        if (item.parent.user == request.user):
            item.setWeight(weight)
            return item.pk
        else:
            return -1  # User is not authenticated


# Deletes a given item
def delete_item(request, key):
    item = find_item(key)
    if (item):
        if (item.parent.user == request.user):
            item.remove()
            return key  # Item deleted successfully
        else:
            return -1  # User is not authenticated
    return 0  # Item could not be found


# Renames an item
def rename_item(request, key, newTitle):
    item = find_item(key)
    if (item):
        if (item.parent.user == request.user):
            item.title = newTitle
            item.save()
            return key  # Item deleted successfully
        else:
            return -1  # User is not authenticated
    return 0  # Item could not be found


# # INTERNAL FUNCTIONS
# Returns listitem-object or False (if doesn't exists) | Internal
def find_item(key):
    item = ListItem.objects.filter(pk=key)
    if (item):
        return item[0]  # returns the object from the queryset
    return False  # returns False if item cannot be found


# Returns list-object or False (if doesn't exists) | Internal
def find_list(key):
    list = List.objects.filter(pk=key)
    if (list):
        return list[0]  # returns the object from the queryset
    return False  # returns False if item cannot be found


# Creates and adds an example list to the requesting user
def createDefaultList(request):
    defaultlist = List.objects.create(title="Example list", user=request.user)
    ListItem.objects.create(title="Paint the living room",
                            nextstep="Pick out sample colors at George's Paint.",
                            parent=defaultlist.pk)
    ListItem.objects.create(title="Fix the car",
                            nextstep="Pick it up at the station.",
                            weight=1,
                            parent=defaultlist.pk).check()
    return defaultlist
