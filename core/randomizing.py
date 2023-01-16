'''This is a file of functions for randomizing the Query set'''
import random
from .models import Minister, Events, Content
from .serializers import ContentSerializer, AuthorSerializer, EventSerializer

def one_random_content_from_tag(tag, content) -> list:
    '''The parameter for this function are 2 queryset e.g example.objects.all
        this gets one content from each tag and fetches them out in a shuffled method
    '''
    tags = list(tag)
    content = list(content)
    random.shuffle(content)
    new_list = []
    def check_data(x):
        return x.name
    for tag in tags:
        for cont in content:
            if tag.name == cont.event_name:

                new_list.append(cont)
        '''A Test with list comprehension'''
        #new_list = [cont.event_name for cont in content if tag.name == cont.event_name]
    random.shuffle(new_list)
    return new_list



# tag = Events.objects.all()
# content = Content.object.all()
#
#
# one_random_content_from_tag(tag, content)
