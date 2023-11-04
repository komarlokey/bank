from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .seriazlizers import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from django.core.exceptions import *
from bank.models import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CategoryApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="имя категории товаров")
            },
        ),
        responses={
            403: "У вас не достаточно прав",
            201: CategorySerializer(),
            400: "Ошибка сериалайзера",
        }
    )
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name="ordering", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
        responses={
            200: GoodsSerializer()
        },
    )
    def get(self, request):
        if request.GET.get("ordering"):
            goods = Good.objects.all().order_by(request.GET.get("ordering"))
        else:
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

    def delete(self, request):
        index = request.data["index"]
        try:
            request.session["cart"].pop(index)
            request.session.modified = True
            return self.get(request)
        except KeyError:
            return Response({"msg": "Такого индекса не существует"}, status=HTTP_404_NOT_FOUND)

    def patch(self, request):
        index = request.data["index"]
        count = request.data["count"]
        try:
            request.session["cart"][index][1] = count
            request.session.modified = True
            return self.get(request)
        except IndexError:
            return Response({"msg": "Такого индекса не существует"}, status=HTTP_404_NOT_FOUND)


class OrderApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = OrderGoodsSerializer

    def get(self, request):
        order = Order.objects.filter(buyer=request.user).order_by("-date_time")
        data = OrderSerializer(order, many=True).data
        return Response(data=data, status=HTTP_200_OK)

    def post(self, request):
        if "cart" in request.session:
            cart = request.session["cart"]
            if cart:
                order = Order(buyer=request.user, final_sum=0)
                order.save()
                order_sum = 0
                for elem in cart:
                    good = Good.objects.get(id=elem[0])
                    order_good = OrderGoods(good=good, count=elem[1])
                    order_sum += good.price * elem[1]
                    order_good.save()
                    order.goods.add(order_good)
                order.final_sum = order_sum
                bonus = request.data["bonus"]
                if bonus:
                    if bonus >= order.final_sum:
                        request.user.bonus -= order.final_sum
                        order.final_sum = 0
                    else:
                        order.final_sum -= request.user.bonus
                        request.user.bonus = 0
                card = Card.objects.get(owner=request.user)
                if card.balance >= order.final_sum:
                    card.balance -= order.final_sum
                    request.user.bonus += round(order.final_sum * 0.05)
                    for elem in cart:
                        good = Good.objects.get(id=elem[0])
                        good.bought += elem[1]
                        good.save()
                    request.user.save()
                    card.save()
                    order.save()
                    del request.session["cart"]
                    return Response(data={"msg": "Покупка оформлена успешно"}, status=HTTP_201_CREATED)
                else:
                    return Response(data={"msg": "Не хватает средств на карте"}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"msg": "Корзина пуста"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"msg": "Корзина не найдена в сессий"}, status=HTTP_400_BAD_REQUEST)


class CartIncreaseApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, index):
        try:
            request.session["cart"][index][1] += 1
            request.session.modified = True
            return CartApiView().get(request)
        except IndexError:
            return Response({"msg": "Такого индекса не сущетсвует"}, status=HTTP_404_NOT_FOUND)


class CartDecreaseApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, index):
        try:
            request.session["cart"][index][1] -= 1
            request.session.modified = True
            return CartApiView().get(request)
        except IndexError:
            return Response({"msg": "Такого индекса не сущетсвует"}, status=HTTP_404_NOT_FOUND)