from rest_framework import serializers
from websites.models import Website, APIKey
from analytics.models import Visitor, PageView


class WebsiteSerializer(serializers.ModelSerializer):
    total_views = serializers.SerializerMethodField()
    total_visitors = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = ['id', 'name', 'domain', 'tracking_id', 'created_at',
                  'total_views', 'total_visitors']

    def get_total_views(self, obj):
        return obj.pageviews.count()

    def get_total_visitors(self, obj):
        return obj.visitors.count()


class PageViewSerializer(serializers.ModelSerializer):
    visitor_id = serializers.CharField(source='visitor.visitor_id', read_only=True)

    class Meta:
        model = PageView
        fields = ['id', 'url', 'page_title', 'referrer',
                  'visitor_id', 'timestamp']


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['visitor_id', 'country', 'city', 'browser', 'os',
                  'device', 'first_visit', 'last_visit']
        # IP address excluded for privacy (optional)