import random
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

# from django.db import transaction
from slunic.models import Comment, Page, Question, Tutorial, Category

from faker import Faker

fake = Faker(["id"])
fake_en = Faker(["en"])

User = get_user_model()


def generate_fake_users(number):

    for _ in range(number):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = "_".join([first_name.lower(), last_name.lower()])
        email = "%s@gmail.com" % username
        password = "fake_user"
        fake_user = User(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        fake_user.save()


def generate_fake_tuts(number):
    # get Users
    users = User.objects.all()
    users_total = users.count()
    categories = ["Technology", "Money", "Business", "Productivity", "Psychology", "Mindfulness", "Art"]
    tags = [
        "Internet",
        "Computer",
        "Programming",
        "Bank",
        "Stock",
        "Invest",
        "Healt",
        "Happy",
        "Music",
        "Design",
    ]

    # Generate Categorie
    for cat in categories:
        Category.objects.get_or_create(name=cat, defaults={"description": fake_en.paragraph()})

    category_objects = Category.objects.all()
    category_total = category_objects.count()
    for _ in range(number):
        user = users[random.randrange(start=0, stop=(users_total - 1))]
        category = category_objects[random.randrange(start=0, stop=(category_total - 1))]
        title = fake_en.sentence(nb_words=10)
        content = " ".join(fake_en.paragraphs(nb=5))
        summary = fake_en.paragraph()
        tut = Tutorial(
            author=user,
            title=title,
            category=category,
            summary=summary,
            content=content,
        )
        tut.save()
        for _ in range(random.randrange(start=2, stop=4)):
            tut.tags.add(tags[random.randrange(start=0, stop=(len(tags) - 1))])


def generate_fake_comments(number):
    # get Users
    users = User.objects.all()
    users_total = users.count()
    tutorials = Page.objects.filter(real_model__in=["tutorial", "comment"])
    tutorial_total = tutorials.count()
    for _ in range(number):
        user = users[random.randrange(start=0, stop=(users_total - 1))]
        tutorial = tutorials[random.randrange(start=0, stop=(tutorial_total - 1))]
        content = " ".join(fake_en.paragraphs(nb=2))
        comment = Comment(
            author=user,
            parent=tutorial.get_real_instance(),
            content=content,
        )
        comment.save()


def generate_fake_questions(number):
    # get Users
    users = User.objects.all()
    users_total = users.count()
    tags = [
        "Internet",
        "Computer",
        "Programming",
        "Bank",
        "Stock",
        "Invest",
        "Healt",
        "Happy",
        "Music",
        "Design",
    ]

    for _ in range(number):
        user = users[random.randrange(start=0, stop=(users_total - 1))]
        title = fake_en.sentence(nb_words=10) + "?"
        content = " ".join(fake_en.paragraphs(nb=5))
        quest = Question(
            author=user,
            title=title,
            content=content,
        )
        quest.save()
        for _ in range(random.randrange(start=2, stop=4)):
            quest.tags.add(tags[random.randrange(start=0, stop=(len(tags) - 1))])


class Command(BaseCommand):
    help = "Seed fake data .."

    def add_arguments(self, parser):
        parser.add_argument("model", type=str)
        parser.add_argument("number", type=int)

    def handle(self, *args, **options):
        model_type = options.get("model")
        number = options.get("number")
        if model_type == "users":
            generate_fake_users(number)
        elif model_type == "tutorials":
            generate_fake_tuts(number)
        elif model_type == "comments":
            generate_fake_comments(number)
        elif model_type == "questions":
            generate_fake_questions(number)
        else:
            raise CommandError("Options not found")
