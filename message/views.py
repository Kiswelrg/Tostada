from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
import json
from .models import ChatMessage

# Create your views here.
def send_Msg(
        request,
        content,
        channel,
        user_from,
        user_mentioned = None,
        edited = False,
        tool_used = None,
        is_private = False,
    ):
    pass


@require_http_methods(["GET"])
def list_rooms(request):
    """GET /api/messages/rooms/ - List all rooms for user"""
    dummy_rooms = [
        {
            "channel_id": "123456789",
            "room_type": "channel",
            "name": "General",
            "last_message": "Hello everyone!",
            "last_message_time": timezone.now().isoformat(),
            "unread_count": 3,
            "participants": [
                {"id": 1, "username": "user1", "avatar": None, "is_online": True},
                {"id": 2, "username": "user2", "avatar": None, "is_online": False}
            ]
        },
        {
            "channel_id": "987654321",
            "room_type": "direct",
            "name": "Direct Message",
            "last_message": "How are you?",
            "last_message_time": timezone.now().isoformat(),
            "unread_count": 1,
            "participants": [
                {"id": 2, "username": "user2", "avatar": None, "is_online": True}
            ]
        }
    ]
    return JsonResponse({"rooms": dummy_rooms})


@csrf_exempt
@require_http_methods(["POST"])
def create_room(request):
    """POST /api/messages/rooms/ - Create new room"""
    try:
        data = json.loads(request.body)
        room_name = data.get('name', 'New Room')
        room_type = data.get('type', 'channel')
        
        dummy_room = {
            "channel_id": "111222333",
            "room_type": room_type,
            "name": room_name,
            "last_message": None,
            "last_message_time": None,
            "unread_count": 0,
            "participants": []
        }
        return JsonResponse({"room": dummy_room}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@require_http_methods(["GET"])
def get_room_details(request, cid):
    """GET /api/messages/rooms/{cid}/ - Get room details"""
    dummy_room = {
        "channel_id": cid,
        "room_type": "channel",
        "name": f"Room {cid}",
        "description": "This is a sample room",
        "created_at": timezone.now().isoformat(),
        "participants": [
            {"id": 1, "username": "user1", "avatar": None, "is_online": True},
            {"id": 2, "username": "user2", "avatar": None, "is_online": False}
        ]
    }
    return JsonResponse({"room": dummy_room})


@require_http_methods(["GET"])
def get_room_messages(request, cid):
    """GET /api/messages/rooms/{cid}/messages/ - Get paginated messages"""
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 50))
    
    dummy_messages = []
    for i in range(limit):
        message_id = 100000 + i + ((page - 1) * limit)
        dummy_messages.append({
            "urlCode": str(message_id),
            "contents": {"version": "0.10.0", "block": [{"type": "text", "content": f"Sample message {message_id}"}]},
            "time_sent": timezone.now().isoformat(),
            "is_read": i % 3 == 0,
            "is_edited": False,
            "sender": {
                "id": (i % 2) + 1,
                "username": f"user{(i % 2) + 1}",
                "avatar": None,
                "is_online": True
            },
            "mentioned_user": None,
            "is_private": False,
            "channel": cid,
            "tool_used": None,
            "state": "1"
        })
    
    return JsonResponse({
        "messages": dummy_messages,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": 1000,
            "has_next": page * limit < 1000
        }
    })


@csrf_exempt
@require_http_methods(["POST"])
def mark_messages_read(request, cid):
    """POST /api/messages/rooms/{cid}/mark_read/ - Mark messages as read"""
    try:
        data = json.loads(request.body)
        message_ids = data.get('message_ids', [])
        
        return JsonResponse({
            "success": True,
            "marked_count": len(message_ids),
            "channel_id": cid
        })
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@require_http_methods(["GET"])
def search_messages(request):
    """GET /api/messages/search/?q=query&channel_id=123 - Search messages"""
    query = request.GET.get('q', '')
    channel_id = request.GET.get('channel_id', None)
    page = int(request.GET.get('page', 1))
    limit = 25  # Fixed to 25 per page as expected by frontend
    
    if not query:
        return JsonResponse({"error": "Query parameter 'q' is required"}, status=400)
    
    # Build search query
    search_filter = Q(content_text__icontains=query) & Q(state='1')  # Only active messages
    
    # Add channel filter if specified
    if channel_id:
        search_filter &= Q(channel__urlCode=channel_id)
    
    # Get total count
    total_results = ChatMessage.objects.filter(search_filter).count()
    
    # Calculate pagination
    start_index = (page - 1) * limit
    end_index = start_index + limit
    
    # Get paginated results
    messages = ChatMessage.objects.filter(search_filter).select_related(
        'sender', 'channel'
    ).order_by('-time_sent')[start_index:end_index]
    
    # Format results
    results = []
    for msg in messages:
        # Create highlight text
        content_lower = msg.content_text.lower()
        query_lower = query.lower()
        
        highlight = msg.content_text
        if query_lower in content_lower:
            # Simple highlighting - find first occurrence
            start_pos = content_lower.find(query_lower)
            context_start = max(0, start_pos - 30)
            context_end = min(len(msg.content_text), start_pos + len(query) + 30)
            highlight = f"...{msg.content_text[context_start:context_end]}..."
        
        results.append({
            "id": msg.urlCode,
            "urlCode": str(msg.urlCode),
            "nickname": msg.sender.username if msg.sender else "Unknown",
            "date_sent": msg.time_sent.isoformat(),
            "contents": msg.content_text[:200] + ("..." if len(msg.content_text) > 200 else ""),
            "avatar_src": msg.sender.avatar.url if msg.sender and msg.sender.avatar else "/static/@me/1F955.svg",
            "attachments": [],  # TODO: Add attachment support
            "channel": str(msg.channel.urlCode) if msg.channel else channel_id,
            "highlight": highlight
        })
    
    return JsonResponse({
        "results": results,
        "count": total_results,
        "query": query,
        "channel_id": channel_id,
        "page": page,
        "per_page": limit
    })


@require_http_methods(["GET"])
def get_message_history(request, cid):
    """GET /api/messages/rooms/{cid}/history/?before=456 - Load older messages"""
    before = request.GET.get('before', None)
    limit = int(request.GET.get('limit', 50))
    
    dummy_messages = []
    start_id = int(before) - 1 if before else 50000
    
    for i in range(limit):
        message_id = start_id - i
        if message_id <= 0:
            break
            
        dummy_messages.append({
            "urlCode": str(message_id),
            "contents": {"version": "0.10.0", "block": [{"type": "text", "content": f"Historical message {message_id}"}]},
            "time_sent": timezone.now().isoformat(),
            "is_read": True,
            "is_edited": False,
            "sender": {
                "id": (i % 2) + 1,
                "username": f"user{(i % 2) + 1}",
                "avatar": None,
                "is_online": False
            },
            "channel": cid
        })
    
    return JsonResponse({
        "messages": dummy_messages,
        "channel_id": cid,
        "has_more": message_id > 1
    })