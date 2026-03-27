from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from subroutines.rss_feed_monitor import FeedWatcher
from subroutines.article_synchronisation import ArticleSyncService
from subroutines.review_processor import Reviewer
from subroutines.database_manager import DatabaseManager
from pathlib import Path

import config as CONFIG

router = APIRouter(prefix="/api")

@router.post("/scan")
def scan_rss():
    """
    Scans the RSS feed and returns data about articles
    """

    try:
        watchman = FeedWatcher()
        stats = watchman.check_feed()
        
        return {
            "status": "success",
            "message": "RSS feed scanned successfully.",
            "stats": stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/proceed")
async def proceed_sync():
    """
    Triggers the synchronization of articles from the cache.json file to MongoDB.
    """
    try:
        service = ArticleSyncService(json_path=Path(CONFIG.CACHE_FILE))

        stats = await service.sync_all()
        
        return {
            "status": "success",
            "message": "Articles synchronized successfully.",
            "stats": stats
        }
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/ping")
def test_endpoint():
    return {
        "status": "ok",
        "message": "Test endpoint is working!"
    }

@router.post("/review")
def review_article(
    action: str = Query(..., description="Action to perform on the article "),
    url: str | None = Query(None, description="URL of the article to review"),
    category: str | None = Query(None, description="Category for insert_prebuilt")
):
    """
    This endpoint is called by the Android application to perform aspecific review action chosen by the user

    Handles review actions:
        - get_next
        - discard
        - insert_prebuilt
        - insert_special
    """
    try:
        review_processor = Reviewer()
        result = review_processor.process_review_api(
            action=action,
            url=url,
            category=category
        )
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "status": "success",
            "message": "Review action processed successfully.",
            "data": result["data"],
            "state": result["status"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_articles")
def get_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(60, ge=1, le=100)
):
    """Returns a paginated list of articles for the Android App"""

    try:
        dbMan = DatabaseManager()

        offset = (page-1)*limit
        articles = dbMan.paginate_articles(limit, offset)

        return {
            "status" : "success",
            "page" : page,
            "limit" : limit,
            "count" : len(articles),
            "articles" : articles
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Request body models
class RatingUpdate(BaseModel):
    hash_id: str
    rating: int


@router.put("/update_rating")
def update_rating(data: RatingUpdate):
    dbMan = DatabaseManager()

    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 & 5"
                            )
    success = dbMan.update_rating(data.hash_id, data.rating)
    if success:
        return True
    raise HTTPException(status_code=404, detail="Article not found")

class StatusUpdate(BaseModel):
    hash_id: str


@router.put("/mark completed")
def mark_completed(data: StatusUpdate):
    dbMan = DatabaseManager()

    success = dbMan.update_status(data.hash_id)
    if success:
        return True
    raise HTTPException(status_code=404, detail="Article not found")
