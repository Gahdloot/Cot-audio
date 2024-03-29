from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .randomizing import one_random_content_from_tag
from .models import Minister, Events, Content
from .serializers import ContentSerializer, AuthorSerializer, EventSerializer, HomePageMinisters
from django.db.models import Q


class ListUsers(APIView):

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        data = {}
        usernames = [user.name for user in Minister.objects.all()]
        data['user'] = usernames
        data['content'] = [content.name for content in Content.objects.all()]
        cont = Content.objects.all()
        data['content'] += [p.content.url for p in cont]
        return Response(data)



class TrendingList(APIView):
    '''
    Home page returns the latest content, trending content(by number of plays), and top ministers by number of plays
    '''

    def get(self, request, format=None):
        data = {}

        # fetching for newest content top 2
        latest_6 = Content.objects.order_by('-date_created')[:9]

        # fetching for contents by the amount of listens
        most_listened = Content.objects.order_by('times_played')

        # For Quick picks
        '''
                this gets one content from each tag and fetches them out in a shuffled method
            '''
        quick_pick_tag = Events.objects.all()
        quick_pick_content = Content.objects.all()

        quick_pick = one_random_content_from_tag(quick_pick_tag,quick_pick_content)
        quick_pick = ContentSerializer(quick_pick, many=True)
        data['quick picks'] = quick_pick.data

        # fetching for most listened Authors
        minister = Minister.objects.order_by('times_played')

        # fetching all Ministers
        ministers = Minister.objects.all()

        # serializing all the data
        minister = AuthorSerializer(minister, many=True)
        serializer = ContentSerializer(latest_6, many=True)
        most_listened = ContentSerializer(most_listened, many=True)
        ministers = HomePageMinisters(ministers, many=True)

        # adding them to the data dictionary
        data['latest'] = serializer.data
        data['most_listened'] = most_listened.data
        data['top ministers'] = minister.data
        data['All Ministers'] = ministers.data
        return Response(data)


class MinistersPage(APIView):
    '''Returns all Ministers, the Ministers content, and other authors'''

    def get(self, request, format=None):
        data = {}
        ministers = Minister.objects.all()
        ministers = AuthorSerializer(ministers)
        data['All Ministers'] = ministers.data

class MinisterPage(APIView):
    """
    Retruns a specific author, the authors content, and other authors
    """

    def get(self, request, id, format=None):
        data = {}

        # trying to fetch authors by their id
        try:
            Main_minister = Minister.objects.get(id=id)
        except Minister.DoesNotExist:
            data = {'message': 'failed'}
            return Response(data)
        #print(type(Main_author.name))

        # getting all the authors content, quersyset by author's name
        minister_content = Content.objects.filter(minister__name=Main_minister.name)

        # serializing all authors contents from the author
        minister_content = ContentSerializer(minister_content, many=True)

        # serilaizing author by id
        Main_minister = AuthorSerializer(Main_minister)

        # fetching all authours excluding the main author
        Other_authors = Minister.objects.all().exclude(id=id)

        # serilaizing other authors
        Other_authors = AuthorSerializer(Other_authors, many=True)

        # adding them to the data dictionary
        data['main author'] = Main_minister.data
        data['author Content'] = minister_content.data
        data['other author'] = Other_authors.data

        return Response(data)


class ContentPage(APIView):
    """The Content page this to view the content in full, with description
        the contents also suggests similar content based on tags
    """

    '''
    The post method is to increment times played on content
    '''

    def get(self, request, id, format=None):
        data = {}

        # quering main content by ID
        Main_content = Content.objects.get(id=id)

        # creating a variable to track the tag name of the content
        content_tag = Main_content.tag.name
        data['content_tag'] = content_tag

        # Serializing main content
        Main_content = ContentSerializer(Main_content)

        # adding main contents to api
        data['main_content'] = Main_content.data

        # Querying the Content the while filtering the for the same tag as main event
        other_Content = Content.objects.filter(tag__name=content_tag).exclude(id=id)

        # Serializing other content
        other_Content = ContentSerializer(other_Content, many=True)

        # adding main contents to api
        data['other_content_on_the_same_tag'] = other_Content.data

        return Response(data)

    def post(self, request, id, format=None):
        """
        this is to ensure that when a content is played, the times played is incremented by one(1)

        :param request: httprequest
        :param id: collect the id of a content
        :param format:
        :return: a success when the content has been incremented by one(1)
        """

        data = {}
        # querying main content by ID
        Main_content = Content.objects.get(id=id)

        # creating a variable to track the times played of the content
        content_tag = Main_content.tag.times_played
        main_content_times_played = Main_content.times_played
        minister_profile_times_played = Main_content.minister.times_played


        # incrementing the times played
        content_tag += 1
        main_content_times_played += 1
        minister_profile_times_played += 1

        Main_content.save()

        data['message'] = 'success'

        return Response(data)


class Explore(APIView):
    '''The Tag Page returns a dictionary of name of all tags
    '''

    def get(self, request, format=None):
        data = {}

        all_tag = Events.objects.all()
        all_tag = EventSerializer(all_tag, many=True)
        return Response(all_tag.data)


class TagPage(APIView):
    '''The Tag Page returns a dictionary of name of all episodes in a tag
    '''

    def get(self, request, tag, format=None):
        data = {}

        tag = Content.objects.filter(tag__name=tag)
        tagged_content = ContentSerializer(tag, many=True)

        data['tagged_content'] = tagged_content.data

        return Response(data)


class SearchContent(APIView):
    '''
    to search for content by minister name, tag/Eventname, title and description
    '''
    def get(self, request, query, format=None):
        data = {}
        contents = Content.objects.filter(Q(minister__name__icontains=query) | Q(name__icontains=query) | Q(tag__name__icontains=query) | Q(description__icontains=query))
        contents = ContentSerializer(contents, many=True)
        data['results'] = contents.data

        return Response(data)