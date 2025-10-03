from rest_framework import serializers
from .models import Skill, UserSkill, CV


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'category']


class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), write_only=True)

    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'skill_id', 'level', 'years_experience', 'details']

    def create(self, validated_data):
        skill = validated_data.pop('skill_id')
        user_profile = self.context['request'].user.profile
        return UserSkill.objects.create(profile=user_profile, skill=skill, **validated_data)

    def update(self, instance, validated_data):
        skill = validated_data.pop('skill_id', None)
        if skill is not None:
            instance.skill = skill
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CVSerializer(serializers.ModelSerializer):
    # Pour afficher l'URL complète du fichier uploadé
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = CV
        fields = ['id', 'file', 'file_url', 'uploaded_at', 'description']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
