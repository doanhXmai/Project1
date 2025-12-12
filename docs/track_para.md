|                    | Banner            | Poster            | Lyrics            | Audio                                |
|--------------------|-------------------|-------------------|-------------------|--------------------------------------|
| Yêu cầu            | 1 file Default    | 1 file Default    | đuôi file là .txt | định dạng bài hát TenBai_TenCaSi.mp3 |
| có cần thiết không | có cx đc ko cx đc | có cx đc ko cx đc | có cx đc ko cx đc | bắt buộc                             |

```python
class TrackRequestCreateSchema(BaseModel):
    track_title: str
    track_info: Optional[str] = None
    track_duration: Optional[str] = None
    track_lyric: Optional[str] = None
    track_total_view: Optional[int] = 0

class SingerCreateSchema(BaseModel):
    singer_name: str
    singer_info: Optional[str] = None
    singer_view: Optional[str] = 0

class GenreCreateSchema(BaseModel):
    genre_name: str
    genre_info: Optional[str] = None
```
