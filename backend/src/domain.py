from dataclasses import dataclass
from typing import Optional
from googleapiclient.discovery import build
import datetime
import error

VideoId = str
CommentId = str


@dataclass(frozen=True)
class Comment:
    video_id: VideoId
    comment_id: CommentId
    text: str
    like_count: int


@dataclass(frozen=True)
class Thumbnail:
    url: str
    width: int
    height: int


@dataclass(frozen=True)
class Video:
    video_id: VideoId
    title: str
    description: str
    thumbnail_default: Thumbnail
    thumbnail_standard: Thumbnail
    like_count: int
    view_count: int
    comment_count: int
    published_at: datetime.datetime


@dataclass(frozen=True)
class VideoError(error.Error):
    video_id: VideoId
    error_message: str


class Youtube:
    def __init__(self, google_api_key: str):
        self._youtube = build('youtube', 'v3',
                              developerKey=google_api_key)

    def video_comments(self, video_id: VideoId) -> list[Comment]:
        video_response = self._youtube.commentThreads().list(
            part='snippet',
            videoId=video_id
        ).execute()

        comments: list[Comment] = []
        while video_response:
            comments += [
                Comment(
                    video_id=video_id,
                    comment_id=item["id"],
                    text=item['snippet']['topLevelComment']['snippet'],
                    like_count=item["likeCount"]
                ) for item in video_response['items']]

            # Again repeat
            if 'nextPageToken' in video_response:
                video_response = self._youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    pageToken=video_response['nextPageToken']
                ).execute()
            else:
                break

        return comments

    def video_summary(self, video_id: VideoId | list[VideoId]) -> list[Video] | VideoError:
        if not isinstance(video_id, list):
            video_id = [video_id]

        assert len(video_id) > 0
        print(",".join(video_id))

        response = self._youtube.videos().list(
            part='snippet,statistics',
            id=",".join(video_id)
        ).execute()

        items = response.get("items")
        if items is None or len(items) == 0:
            return [VideoError(video_id=_video_id, error_message="TODO: api error") for _video_id in video_id]

        return [
            Video(
                video_id=item["id"],
                title=item["snippet"]["title"],
                description=item["snippet"]["description"],
                thumbnail_default=Thumbnail(item["snippet"]["thumbnails"]["default"]["url"],
                                    int(item["snippet"]["thumbnails"]["default"]["width"]),
                                    int(item["snippet"]["thumbnails"]["default"]["height"])),
                thumbnail_standard=Thumbnail(item["snippet"]["thumbnails"]["standard"]["url"],
                                    int(item["snippet"]["thumbnails"]["standard"]["width"]),
                                    int(item["snippet"]["thumbnails"]["standard"]["height"])),
                like_count=int(item["statistics"]["likeCount"]),
                view_count=int(item["statistics"]["viewCount"]),
                comment_count=int(item["statistics"]["commentCount"]),
                published_at=datetime.datetime.strptime(
                    item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            ) for item in items]
