from django.contrib.auth.models import User
from news_portal.models import Author, Category, Post, PostCategory, Comment

# 1. Создаем пользователей с проверкой на существование
if not User.objects.filter(username='ivan').exists():
    user1 = User.objects.create_user('ivan', password='123')
else:
    user1 = User.objects.get(username='ivan')

if not User.objects.filter(username='maria').exists():
    user2 = User.objects.create_user('maria', password='456')
else:
    user2 = User.objects.get(username='maria')

# 2. Создаем авторов с проверкой
if not Author.objects.filter(user=user1).exists():
    author1 = Author.objects.create(user=user1)
else:
    author1 = Author.objects.get(user=user1)

if not Author.objects.filter(user=user2).exists():
    author2 = Author.objects.create(user=user2)
else:
    author2 = Author.objects.get(user=user2)

# 3. Создаем категории с проверкой
for cat_name in ['Спорт', 'Политика', 'Образование', 'Технологии']:
    if not Category.objects.filter(name=cat_name).exists():
        Category.objects.create(name=cat_name)

cat_sport = Category.objects.get(name='Спорт')
cat_politics = Category.objects.get(name='Политика')
cat_edu = Category.objects.get(name='Образование')
cat_tech = Category.objects.get(name='Технологии')

# 4. Создаем посты
post1, created = Post.objects.get_or_create(
    author=author1, post_type='article',
    title='Как выиграть в спорте',
    text='Спорт — это здоровье, дисциплина и упорство.',
    defaults={'rating': 0}
)

post2, created = Post.objects.get_or_create(
    author=author2, post_type='article',
    title='Политика 2025',
    text='Что нас ждет в будущем? Анализ событий.',
    defaults={'rating': 0}
)

news1, created = Post.objects.get_or_create(
    author=author1, post_type='news',
    title='Новый гаджет',
    text='Компания X выпустила революционный девайс.',
    defaults={'rating': 0}
)

# 5. Присваиваем категории
PostCategory.objects.get_or_create(post=post1, category=cat_sport)
PostCategory.objects.get_or_create(post=post1, category=cat_edu)
PostCategory.objects.get_or_create(post=post2, category=cat_politics)
PostCategory.objects.get_or_create(post=news1, category=cat_tech)

# 6. Создаем комментарии
Comment.objects.get_or_create(
    post=post1, user=user1, text='Классная статья!', defaults={'rating': 0}
)
Comment.objects.get_or_create(
    post=post1, user=user2, text='Согласна, полезно.', defaults={'rating': 0}
)
Comment.objects.get_or_create(
    post=post2, user=user1, text='Интересный взгляд.', defaults={'rating': 0}
)
Comment.objects.get_or_create(
    post=news1, user=user2, text='Жду обзор!', defaults={'rating': 0}
)

# 7. Меняем рейтинги
post1.rating = 0  # Сбрасываем, чтобы начать с чистого листа
post1.like()      # +1
post1.like()      # +1 (итого 2)
post1.save()

post2.rating = 0
post2.dislike()   # -1
post2.save()

news1.rating = 0
news1.like()      # +1
news1.save()

comment1 = Comment.objects.get(post=post1, user=user1, text='Классная статья!')
comment1.rating = 0
comment1.like()   # +1
comment1.save()

comment3 = Comment.objects.get(post=post2, user=user1, text='Интересный взгляд.')
comment3.rating = 0
comment3.dislike()  # -1
comment3.save()

# 8. Обновляем рейтинг авторов
author1.update_rating()
author2.update_rating()

# 9. Выводим лучшего автора
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший автор: {best_author.user.username}, рейтинг: {best_author.rating}")

# 10. Выводим лучший пост
best_post = Post.objects.order_by('-rating').first()
print(f"Лучший пост: {best_post.title}, Автор: {best_post.author.user.username}, "
      f"Рейтинг: {best_post.rating}, Дата: {best_post.created_at}, Превью: {best_post.preview()}")

# 11. Выводим комментарии к лучшему посту
for comment in best_post.comment_set.all():
    print(f"Комментарий: {comment.text}, Автор: {comment.user.username}, "
          f"Рейтинг: {comment.rating}, Дата: {comment.created_at}")