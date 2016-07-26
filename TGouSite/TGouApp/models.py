from django.db import models
from django.contrib.auth.models import User


class Consumer (models.Model):
    user = models.OneToOneField(User, null=True, related_name='ConsumerProf')
    nickName = models.CharField(max_length=200, blank=True, null=True)  # 用户昵称
    dftAddress = models.TextField(blank=True, null=True)  # 默认收货地址
    dftPayType = models.IntegerField(blank=True, null=True)  # 默认付款方式
    contact = models.TextField(blank=True, null=True)  # 联系方式


class ShopCategory (models.Model):
    name = models.CharField(max_length=200)  # 类别名称
    # parent = models.ForeignKey(ShopCategory, on_delete=models.CASCADE)
    # #       父类别标识符


class Shop (models.Model):
    name = models.CharField(max_length=200)  # 店名
    category = models.ForeignKey(
        ShopCategory, on_delete=models.CASCADE, blank=True, null=True)  # 类别标识符
    location = models.CharField(max_length=200)  # 位置
    intro = models.TextField()  # 简介
    createDate = models.DateTimeField()  # 开店日期


class ShopKeeper (models.Model):
    user = models.OneToOneField(User, null=True, related_name='ShopKeeperProf')
    nickName = models.CharField(max_length=200, null=True, blank=True)  # 用户昵称
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, null=True)  # 店铺标识符
    contact = models.TextField(null=True)  # 联系方式
    account = models.CharField(max_length=200, null=True)  # 收款账号


class CommodityCategory (models.Model):
    name = models.CharField(max_length=200)  # 类别名称
    parent = models.ForeignKey(
        ShopCategory, on_delete=models.CASCADE)  # 父类别标识符


class Commodity (models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # 所属店铺标识符
    name = models.CharField(max_length=200)  # 商品名
    category = models.ForeignKey(
        CommodityCategory, on_delete=models.CASCADE, blank=True, null=True)  # 类别标识符
    price = models.DecimalField(max_digits=8, decimal_places=2)  # 售价
    inventory = models.IntegerField()  # 库存余量
    grade = models.CharField(max_length=200)  # 评分
    gradedBy = models.IntegerField()  # 评分数量
    state = models.IntegerField()  # 商品状态


class Order (models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)  # 创建用户标识符
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # 负责店铺标识符
    address = models.CharField(max_length=200)  # 送货地址
    payType = models.IntegerField()  # 购买方式
    message = models.TextField()  # 留言
    price = models.DecimalField(max_digits=8, decimal_places=2)  # 订单总价
    time = models.DateTimeField()  # 创建时间
    state = models.IntegerField()  # 订单状态


class OrderItem (models.Model):
    cmd = models.ForeignKey(Commodity, on_delete=models.CASCADE)  # 商品标识符
    quantity = models.IntegerField()  # 购买数量
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # 所属订单标识符


class Cart (models.Model):
    consumer = models.ForeignKey(
        Consumer, on_delete=models.CASCADE)  # 所属消费者标识符


class CartItem (models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)  # 商品标识符
    quantity = models.IntegerField()  # 购买数量
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)  # 所属购物车标识符


class Comment (models.Model):
    commodity = models.ForeignKey(
        Commodity, on_delete=models.CASCADE)  # 被评论商品标识符
    grade = models.DecimalField(max_digits=3, decimal_places=2)  # 评分
    message = models.TextField()  # 评论内容
    time = models.DateTimeField()  # 创建时间


class Grading (models.Model):
    consumer = models.ForeignKey(
        Consumer, on_delete=models.CASCADE)  # 关联消费者标识符
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # 关联商户标识符
    direction = models.IntegerField()  # 评分朝向（店铺->消费者还是消费者->店铺）
    time = models.DateTimeField()  # 创建时间
    grade = models.DecimalField(max_digits=3, decimal_places=2)  # 评分
