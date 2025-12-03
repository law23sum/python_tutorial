from django.contrib import admin

from .models import Chat, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ("created_at", "updated_at", "message_type", "content")
    fields = ("message_type", "content", "created_at")
    ordering = ("created_at",)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")
    search_fields = ("user__username", "name")
    list_filter = ("user",)
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chat",
        "created_at",
        "message_type",
        "short_content",
    )
    search_fields = ("chat__name", "message_type", "content")
    list_filter = (
        "chat",
        "message_type",
        "created_at",
    )

    def short_content(self, obj):
        return obj.content[:50]
