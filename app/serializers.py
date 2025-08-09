from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MemberModel, AttendanceModel, EventModel

class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = MemberModel
        fields = [
            'id',
            'user',
            'username',
            'department',
            'first_name',
            'last_name',
            'year',
            'club',
            'role',
            'position',
            'user_role',
            'event_counts',
            'present_days',
        ]
        read_only_fields = ('event_counts', 'present_days')

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        if not user_data:
            username = self.initial_data.get('username', {})
            # username = self.initial_data.get('user', {}).get('username')
            user = User.objects.get(username=username)
            validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Avoid changing user on update
        validated_data.pop('user', None)
        return super().update(instance, validated_data)
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceModel
        fields = '__all__'
        read_only_fields = ('member', 'date')
        
class EventSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    members_participated = serializers.PrimaryKeyRelatedField(queryset=MemberModel.objects.all(), many=True, required=False)

    class Meta:
        model = EventModel
        fields = '__all__'
        read_only_fields = ('club', 'created_at', 'updated_at')

    def create(self, validated_data):
        members_participated_data = validated_data.pop('members_participated', [])
        event = EventModel.objects.create(**validated_data)
        event.members_participated.set(members_participated_data)

        # Increment the event count for each participating member
        for member in members_participated_data:
            member.event_counts += 1
            member.save()

        return event
    
