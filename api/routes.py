from fastapi import APIRouter, HTTPException
from subroutines.rss_feed_monitor import FeedWatcher

router = APIRouter(prefix="/api")

@router.post("/scan")
# Scans the RSS feed and returns data about articles.
def scan_rss():
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