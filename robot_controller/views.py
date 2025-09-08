import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# In-memory signaling state
STREAM_STATE = {
    "offer": None,
    "answer": None,
    "candidates": []
    
}

COMMAND_STATE = {
    "offer": None,
    "answer": None,
    "candidates": []
}


def stream_page(request):
    return render(request, "stream.html")

# Helper function for validating SDP payloads
def validate_sdp(data):
    return "sdp" in data and "type" in data

# Helper function for validating ICE candidates
def validate_candidate(data):
    return all(k in data for k in ("candidate", "sdpMid", "sdpMLineIndex"))

@csrf_exempt
def streaming_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        action = data.get("action")
        if action == "send_offer":
            if validate_sdp(data):
                STREAM_STATE["offer"] = {"sdp": data["sdp"], "type": data["type"]}
                return JsonResponse({"status": "stream offer stored"})
            return JsonResponse({"error": "Missing SDP or type"}, status=400)

        elif action == "send_answer":
            if validate_sdp(data):
                STREAM_STATE["answer"] = {"sdp": data["sdp"], "type": data["type"]}
                return JsonResponse({"status": "stream answer stored"})
            return JsonResponse({"error": "Missing SDP or type"}, status=400)

        elif action == "send_candidate":
            if validate_candidate(data):
                STREAM_STATE["candidates"].append({
                    "candidate": data["candidate"],
                    "sdpMid": data["sdpMid"],
                    "sdpMLineIndex": data["sdpMLineIndex"]
                })
                return JsonResponse({"status": "stream candidate stored"})
            return JsonResponse({"error": "Incomplete ICE candidate"}, status=400)

        return JsonResponse({"error": "Unknown action"}, status=400)

    elif request.method == "GET":
        action = request.GET.get("action")
        if action == "get_offer":
            return JsonResponse(STREAM_STATE.get("offer") or {})
        elif action == "get_answer":
            return JsonResponse(STREAM_STATE.get("answer") or {})
        elif action == "get_candidates":
            return JsonResponse({"candidates": STREAM_STATE["candidates"]})
        return JsonResponse({"error": "Unknown action"}, status=400)

    return JsonResponse({"error": "Invalid stream request"}, status=400)

@csrf_exempt
def command_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        action = data.get("action")
        if action == "send_offer":
            if validate_sdp(data):
                COMMAND_STATE["offer"] = {"sdp": data["sdp"], "type": data["type"]}
                return JsonResponse({"status": "command offer stored"})
            return JsonResponse({"error": "Missing SDP or type"}, status=400)

        elif action == "send_answer":
            if validate_sdp(data):
                COMMAND_STATE["answer"] = {"sdp": data["sdp"], "type": data["type"]}
                return JsonResponse({"status": "command answer stored"})
            return JsonResponse({"error": "Missing SDP or type"}, status=400)

        elif action == "send_candidate":
            if validate_candidate(data):
                COMMAND_STATE["candidates"].append({
                    "candidate": data["candidate"],
                    "sdpMid": data["sdpMid"],
                    "sdpMLineIndex": data["sdpMLineIndex"]
                })
                return JsonResponse({"status": "command candidate stored"})
            return JsonResponse({"error": "Incomplete ICE candidate"}, status=400)

        return JsonResponse({"error": "Unknown action"}, status=400)

    elif request.method == "GET":
        action = request.GET.get("action")
        if action == "get_offer":
            return JsonResponse(COMMAND_STATE.get("offer") or {})
        elif action == "get_answer":
            return JsonResponse(COMMAND_STATE.get("answer") or {})
        elif action == "get_candidates":
            return JsonResponse({"candidates": COMMAND_STATE["candidates"]})
        return JsonResponse({"error": "Unknown action"}, status=400)

    return JsonResponse({"error": "Invalid command request"}, status=400)

@csrf_exempt
def reset_signaling(request):
    STREAM_STATE.update({"offer": None, "answer": None, "candidates": []})
    COMMAND_STATE.update({"offer": None, "answer": None, "candidates": []})
    return JsonResponse({"status": "reset"})
