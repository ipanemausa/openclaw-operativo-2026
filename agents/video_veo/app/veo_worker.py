import redis
import time
from veo_client import generate_video

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

while True:
    job = redis_client.brpop("queue:video_veo", timeout=5)
    if not job:
        continue

    job_id = job[1]
    data = redis_client.hgetall(f"veo:{job_id}")

    redis_client.hset(f"veo:{job_id}", "status", "processing")

    try:
        video_url = generate_video(
            prompt=data["prompt"],
            duration=int(data["duration"]),
            resolution=data["resolution"],
            style=data["style"]
        )

        redis_client.hset(f"veo:{job_id}", mapping={
            "status": "completed",
            "video_url": video_url
        })

    except Exception as e:
        redis_client.hset(f"veo:{job_id}", "status", f"error: {str(e)}")
