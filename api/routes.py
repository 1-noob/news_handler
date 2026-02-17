from fastapi import APIRouter, HTTPException
from subroutines.rss_feed_monitor import FeedWatcher
from subroutines.article_synchronisation import ArticleSyncService
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