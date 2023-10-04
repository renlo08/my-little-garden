from django.test import TestCase
from django.utils.text import slugify

from gardens.models import Garden
from gardens.utils import slugify_instance_name


class GardenTestCase(TestCase):

    def setUp(self) -> None:
        self.number_of_garden = 500
        for i in range(0, self.number_of_garden):
            Garden.objects.create(name='my little garden', description='description of the garden')

    def test_queryset_exists(self):
        qs = Garden.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Garden.objects.all()
        self.assertEqual(self.number_of_garden, qs.count())

    def test_my_little_garden_slug(self):
        obj = Garden.objects.all().order_by("id").first()
        name = obj.name
        slug = obj.slug
        slugfield_name = slugify(name)
        self.assertEqual(slugfield_name, slug)

    def test_my_little_garden_unique_slug(self):
        qs = Garden.objects.exclude(slug__iexact='my-little-garden')
        for obj in qs:
            name = obj.name
            slug = obj.slug
            slugfield_name = slugify(name)
            self.assertNotEquals(slugfield_name, slug)

    def test_slugify_instance_name(self):
        obj = Garden.objects.all().last()
        new_slugs = []
        for i in range(0, 25):
            instance = slugify_instance_name(obj, save=False)
            new_slugs.append(instance.slug)
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(unique_slugs), len(new_slugs))

    def test_slugify_garden_name(self):
        slug_list = Garden.objects.all().values_list('slug', flat=True)
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(slug_list), len(unique_slug_list))

    def test_garden_search_manager(self):
        qs = Garden.objects.search(query='my little garden')
        self.assertEqual(qs.count(), self.number_of_garden)
        qs = Garden.objects.search(query='little')
        self.assertEqual(qs.count(), self.number_of_garden)
        qs = Garden.objects.search(query='description of')
        self.assertEqual(qs.count(), self.number_of_garden)