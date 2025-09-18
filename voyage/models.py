from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Category(models.Model):
    name = models.CharField(max_length=267, verbose_name='Имя категории')
    slug = models.SlugField(max_length=267, unique=True, verbose_name="URL-адрес (slug)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ["name"]


class Tour(models.Model):
    CONTINENTS = [
        ('Africa', 'Африка'),
        ('Europe', 'Европа'),
        ('North America', 'Северная Америка'),
        ('South America', 'Южная Америка'),
        ('Asia', 'Азия'),
        ('Australia', 'Австралия'),
        ('Antarctica', 'Антарктида')
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tours', verbose_name='Категория')
    title = models.CharField(max_length=199, verbose_name='Название')
    continent = models.CharField(max_length=47, choices=CONTINENTS, blank=True, verbose_name='Континент')

    slogan = models.CharField(max_length=199, blank=True, verbose_name='Слоган')
    country = models.CharField(max_length=101, blank=True, verbose_name='Страна')
    start_date = models.DateField(null=True, blank=True, verbose_name='Дата начала')
    seats = models.PositiveIntegerField(default=0, verbose_name='Количество мест')
    total_seats = models.PositiveIntegerField(default=0, verbose_name='Всего мест')
    departure = models.CharField(max_length=199, blank=True, verbose_name='Отправление')
    duration = models.IntegerField(help_text='Количество дней', verbose_name='Длительность')
    difficulty = models.CharField(max_length=99, blank=True, verbose_name='Сложность')
    program = models.TextField(blank=True, verbose_name='Программа тура')
    included = models.TextField(blank=True, verbose_name='Что включено')
    price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='tours/', blank=True, null=True, verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'
        ordering = ['title']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'tour')

    def __str__(self):
        return f'{self.user.username} -> {self.tour.title}'


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Пользователь')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Тур')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f"{self.tour.title} * {self.quantity}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        unique_together = ('user', 'tour')


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f"{self.user.username} → {self.tour.title}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']


class FAQ(models.Model):
    question = models.CharField(max_length=256, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1, verbose_name='Сумма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    status = models.CharField(max_length=24, default='pending', verbose_name='Статус')

    def __str__(self):
        return f'Оплата {self.amount} $ за {self.tour.title}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        unique_together = [('user', 'tour')]
        ordering = ['-created_at']


class Comment(models.Model):
    tour = models.ForeignKey("Tour", on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.tour.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fio = models.CharField(max_length=255, blank=True, verbose_name="ФИО")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Возраст")
    photo = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Фото")
    married = models.BooleanField(default=False, verbose_name="В браке")
    license = models.BooleanField(default=False, verbose_name="Права")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Билет {self.tour.title} для {self.user.username}"
