from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group, ContentType
from apps.news.models import NewsPub, Carousel, AddNewsCategory
from apps.courses.models import Course, CourseCategory
from apps.cms.models import Teacher


class Command(BaseCommand):
    help = 'Init Permission Groups'

    def handle(self, *args, **options):
        edit_content_type = ContentType.objects.get_for_models(NewsPub,Carousel,AddNewsCategory,CourseCategory,Course,Teacher)
        edit_content_type = edit_content_type.values()
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_type)
        edit_group = Group.objects.create(name='编辑')
        edit_group.permissions.set(edit_permissions)

        self.stdout.write(self.style.SUCCESS('编辑权限创建完成'))
