from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import validate_video_url, validate_text_links


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[validate_video_url])
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True,
        validators=[validate_text_links],
    )

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True,
        validators=[validate_text_links],
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.subscriptions.filter(user=user).exists()


class CourseDetailSerializer(CourseSerializer):
    lessons = LessonSerializer(many=True, read_only=True)



