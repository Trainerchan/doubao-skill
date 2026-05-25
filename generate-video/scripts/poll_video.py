#!/usr/bin/env python3
"""Seedance 视频生成 — 创建任务 → 轮询 → 下载 MP4

用法:
    python poll_video.py "提示词"
    python poll_video.py "提示词" --image https://example.com/frame.jpg
    python poll_video.py "提示词" --duration 10 --ratio 1:1 --no-audio

前置:
    pip install volcengine-python-sdk python-dotenv requests
    .env 中配置 ARK_API_KEY=your-key
"""

import os, time, argparse, sys
import requests
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
if not API_KEY:
    print("错误: 未设置 ARK_API_KEY，请在 .env 文件中配置或设置环境变量")
    sys.exit(1)

MODEL = os.getenv("DOUBAO_VIDEO_MODEL", "doubao-seedance-2-0-260128")
client = Ark(api_key=API_KEY)


def generate_video(
    prompt: str,
    image_url: str | None = None,
    duration: int = 5,
    ratio: str = "16:9",
    generate_audio: bool = True,
    max_wait: int = 600,
) -> str | None:
    """生成视频，返回下载的文件路径，失败返回 None"""
    content: list = [{"type": "text", "text": prompt}]
    if image_url:
        content.append({"type": "image_url", "image_url": {"url": image_url}})

    print(f"模型: {MODEL}")
    print(f"时长: {duration}s | 比例: {ratio} | 音频: {generate_audio}")
    print("创建任务...")

    resp = client.content_generation.tasks.create(
        model=MODEL,
        content=content,
        duration=duration,
        ratio=ratio,
        generate_audio=generate_audio,
    )
    task_id = resp.id
    print(f"任务 ID: {task_id}")

    elapsed = 0
    while elapsed < max_wait:
        time.sleep(10)
        elapsed += 10
        task = client.content_generation.tasks.get(task_id)
        print(f"  [{elapsed}s] 状态: {task.status}")

        if task.status == "succeeded":
            video_url = task.content.video_url
            print(f"生成成功! 下载中...")
            r = requests.get(video_url, timeout=120)
            r.raise_for_status()
            filename = f"seedance_{task_id}.mp4"
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"下载完成: {filename}")
            return filename

        elif task.status == "failed":
            print(f"任务失败: {task.error}")
            return None

    print(f"任务超时（{max_wait}s），可稍后手动查询: {task_id}")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seedance 视频生成工具")
    parser.add_argument("prompt", help="视频描述提示词")
    parser.add_argument("--image", default=None, help="首帧参考图 URL")
    parser.add_argument("--duration", type=int, default=5, help="时长(秒), [4,15]")
    parser.add_argument("--ratio", default="16:9", help="宽高比: 16:9/4:3/1:1/3:4/9:16/21:9")
    parser.add_argument("--no-audio", action="store_true", help="禁用音画同生")
    parser.add_argument("--max-wait", type=int, default=600, help="最长等待秒数")
    args = parser.parse_args()

    generate_video(
        prompt=args.prompt,
        image_url=args.image,
        duration=args.duration,
        ratio=args.ratio,
        generate_audio=not args.no_audio,
        max_wait=args.max_wait,
    )
