from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from users.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from django.db.models import Sum, When, Case, IntegerField

from wp_core.models import *
from wp_core.serializers import *
from wp_core.permissions import OnlyStaffCanModify, StaffOrOwnerCanModify, OnlyStaffAndPoliticianCanModify
from wp_core.pagination import NewestQuestionsSetPagination
# Create your views here.

class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, OnlyStaffAndPoliticianCanModify]
    queryset = Answer.objects.annotate(
                upvotes=Sum(
                    Case(
                        When(voteanswer__up=True, then=1),
                        output_field=IntegerField()
                    )
                )
            )
    serializer_class = AnswerSerializer
     
    def get_serializer_class(self):
        print(self.action)
        if self.action == 'create' or self.action == 'update':
            return AnswerPostSerializer
        return self.serializer_class # I dont' know what you want for create/destroy/update.                
    
    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def upvote(self, request, pk=None):
        try:
            answer = self.get_queryset().get(pk=pk)
        except Question.DoesNotExist:
            raise NotFound(detail='Answer with the id %s does not exist' % pk)
        VoteAnswer.objects.update_or_create(
                answer=answer, 
                user=request.user, 
                defaults={
                    'up':True
                    }
                )
        return Response(self.get_serializer(answer).data)

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def downvote(self, request, pk=None):
        try:
            answer = self.get_queryset().get(pk=pk)
        except Question.DoesNotExist:
            raise NotFound(detail='Answer with the id %s does not exist' % pk)
        VoteAnswer.objects.update_or_create(
                answer=answer, 
                user=request.user, 
                defaults={
                    'up':False
                    }
                )
        return Response(self.get_serializer(answer).data)
