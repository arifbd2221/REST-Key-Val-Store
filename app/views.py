from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from rest_framework import status
from memcached_stats import MemcachedStats
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import JsonResponse


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
mem = MemcachedStats()


class KeyVal(APIView):

    @method_decorator(cache_page(CACHE_TTL))
    def get(self,request,format=None):
        keys = request.query_params.get('keys')
        allcaches = dict()

        for k in mem.keys(): # getting all keys
            key = k.split(':')[2]
            allcaches[key] = cache.get(key) # populating all cache values

        if keys is not None:
            keyList = keys.split(',') # extracting keys from query string
            result = cache.get_many(keyList) # getting key value pairs according to the queries

            if result is None:
                return Response('No keys found',status=status.HTTP_404_NOT_FOUND) # nothing found

            for k in keyList: # reset the TTL of those keys
                cache.touch(k,CACHE_TTL) # reset TTL

            return HttpResponse(JsonResponse(result),status=status.HTTP_200_OK)
        
        
        if allcaches is None:
            return Response('No keys found',status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(JsonResponse(allcaches),status=status.HTTP_200_OK)

        
    
    @method_decorator(cache_page(CACHE_TTL))
    def post(self,request,format=None):
        values = request.data

        if values is None:
            return Response("Bad Request",status=status.HTTP_400_BAD_REQUEST)

        for k,v in values.items():
            cache.set(k,v,CACHE_TTL) # setting up the key values into cache

        return Response("Created",status=status.HTTP_201_CREATED)
    

    def patch(self,request,format=None):
        values = request.data

        if values is None:
            return Response("Bad Request",status=status.HTTP_400_BAD_REQUEST)

        cache.set_many(values,CACHE_TTL) # updating key values and reseting TTL

        return Response("Updated",status=status.HTTP_200_OK)

    