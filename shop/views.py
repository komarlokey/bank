from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .seriazlizers import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from django.core.exceptions import *


class CategoryApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=HTTP_200_OK)

    def post(self, request):
        if not request.user.is_staff:
            return Response(data={"msg": "У вас не достаточно прав"}, status=HTTP_403_FORBIDDEN)
        # name = request.data["name"]
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class ReviewApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = ReviewSerializer

    def get(self, request):
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=HTTP_200_OK)

    def post(self, request):
        # if not request.user:
        #     return Response(data={"msg": "Вы не авторизованы"}, status=HTTP_401_UNAUTHORIZED)
        good = Good.objects.get(id=request.data["good"])
        request.data["author"] = request.user.id
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            good.reviews.add(Review.objects.get(id=serializer.data["id"]))
            good.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class GoodApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = GoodsSerializer

    def get(self, request):
        goods = Good.objects.all()
        data = GoodsSerializer(goods, many=True).data
        return Response(data=data, status=HTTP_200_OK)

    def post(self, request):
        if not request.user.is_staff:
            return Response(data={"msg": "У вас не достаточно прав"}, status=HTTP_403_FORBIDDEN)
        try:
            name = request.data["name"]
            description = request.data["description"]
            price = request.data["price"]
            category = Category.objects.get(id=request.data["category"])
        except ObjectDoesNotExist:
            return Response(data={"msg": "Такой категорий нет"}, status=HTTP_404_NOT_FOUND)
        except KeyError:
            return Response(data={"msg": "Заполните поля(name, description, price, category)"},
                            status=HTTP_400_BAD_REQUEST)

        new_good = Good(name=name, description=description, price=price, category=category)
        new_good.save()
        return Response(data={"msg": "Все прошло успешно"}, status=HTTP_201_CREATED)


class GoodDetailApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = GoodsSerializer

    def get(self, request, pk):
        try:
            goods = Good.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(data={"msg": "Такого товара не существует"}, status=HTTP_404_NOT_FOUND)
        data = GoodDetailSerializer(goods).data
        return Response(data=data, status=HTTP_200_OK)


class GoodsByCategoryApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = GoodsSerializer

    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        goods = Good.objects.filter(category=category)
        data = GoodsSerializer(goods, many=True).data
        return Response(data=data, status=HTTP_200_OK)


class CartApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        if "cart" in request.session.keys():
            data = {"cart": request.session["cart"]}
        else:
            data = {"cart": []}
        return Response(data=data, status=HTTP_200_OK)

    def post(self, request):
        good_id = request.data["id"]
        count = request.data["count"]
        if "cart" in request.session.keys():
            is_new = True
            for i in range(len(request.session["cart"])):
                if request.session["cart"][i][0] == good_id:
                    request.session["cart"][i][1] += count
                    is_new = False
                    break
            if is_new:
                request.session["cart"].append((good_id, count))
        else:
            request.session["cart"] = [(good_id, count)]
        request.session.modified = True
        return Response(data={"msg": "Товар был добавлен в корзину"}, status=HTTP_200_OK)
