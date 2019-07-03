from django.shortcuts import render, HttpResponse
from app01.models import *
# Create your views here.
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import json

class PublisherSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    email = serializers.CharField()


# class BookSerializers(serializers.Serializer):
#     title =  serializers.CharField()
#     price = serializers.CharField()
#     pub_date = serializers.DateField()
#     publish =serializers.CharField()
#     # authors = serializers.CharField(source="authors.all")
#     authors = serializers.SerializerMethodField()
#
#     def get_authors(self,obj):
#         temp = []
#         for author in obj.authors.all():
#             temp.append(author.name)
#         return temp


class BookSerializers(serializers.ModelSerializer):
    publish = serializers.HyperlinkedIdentityField(
        view_name='publish_detail',
        lookup_field="publish_id",
        lookup_url_kwarg="pk")
    class Meta:
        model = Book
        fields = "__all__"

    # authors = serializers.SerializerMethodField()
    # publish = serializers.CharField(source="publish.name")  # 外键字段用 source 显示 关联对象
    # def get_authors(self, obj):
    #     """
    #     处理多对多字段
    #     :param obj:
    #     :return:
    #     """
    #     temp = []
    #     for author in obj.authors.all():
    #         temp.append(author.name)
    #     return temp
    #
    # def create(self, validated_data):
    #     authors = validated_data.pop('authors')
    #     obj = Book.objects.create(**validated_data)
    #     obj.authors.add(*authors)
    #     return obj


class  Publisher(APIView):

    def get(self,request):
        publishers = Publish.objects.all()

        bs = PublisherSerializers(publishers,many=True)

        return HttpResponse(bs.data)


class BooksView(APIView):

    def get(self,request):
        book =  Book.objects.all()
        bs  = BookSerializers(book,many=True,context={'request': request})

        return  Response(bs.data)
    def post(self,request):
        print("books>>>>>",request.data)
        bs = BookSerializers(data=request.data, many=False)
        if bs.is_valid():
            print("validated_data>>>>>",bs.validated_data)
            bs.save()
            return Response(bs.data)
        else:
            return HttpResponse(bs.errors)


class BookdetailView(APIView):
    def get(self,request,pk):
        """
        get方式查询某条数据
        :param request:
        :param pk:
        :return:
        """
        book_obj = Book.objects.filter(pk=pk).first()
        bs = BookSerializers(book_obj,context={'request': request})

        return Response(bs.data)

    def put(self,request,pk):
        """
        更新某本书籍
        :param request:
        :param pk:
        :return:
        """
        book_obj = Book.objects.filter(pk=pk).first()
        bs = BookSerializers(book_obj, data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)

    def post(self,request,pk):
        print("post>>>>",request.data)

        return HttpResponse("post")

    def delete(self,request,pk):
        Book.objects.filter(pk=pk).delete()

        return Response("删除成功")


#############################################################################
#第二种方式
# from rest_framework import mixins
# from rest_framework import generics
#
# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = "__all__"
#
#
#
# class AuthorView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#
#     def get(self,request, *args, **kwargs):
#         """
#         查询所有作者信息
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         return self.list(self, request, *args, **kwargs)
#     def post(self, request, *args, **kwargs):
#         """
#         创建作者信息
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         return self.create(request, *args, **kwargs)
# class  AuthorDetailView(mixins.DestroyModelMixin,mixins.RetrieveModelMixin,
#                         mixins.UpdateModelMixin,generics.GenericAPIView):
#
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

###############################################################################
# 终极形式viewsets.ModelViewSet
from rest_framework import viewsets

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer




def get_random_str(user):
    """
    通过时间加盐生成token
    :param user:
    :return:
    """
    import hashlib,time
    ctime=str(time.time())

    md5=hashlib.md5(bytes(user,encoding="utf8"))
    md5.update(bytes(ctime,encoding="utf8"))

    return md5.hexdigest()


class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        res = {"code": 1000, "msg": None}
        user = request.data.get("user")
        pwd = request.data.get("pwd")
        # user_obj = UserInfo.objects.filter(user=user, pwd=pwd).first()
        print(user, pwd)
        user_obj = User.objects.filter(name=user,pwd=pwd).first()
        if not user_obj:
            res["code"] = 1001
            res["msg"] = "用户名或者密码错误"
        else:
            token = get_random_str(user)          # 调用生成token函数
            Token.objects.update_or_create(user=user_obj, defaults={"token": token})   # 存在则更新token ,不存在则创建
            res["token"] = token

        return JsonResponse(res)









