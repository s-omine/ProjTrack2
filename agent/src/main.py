
from agent import agent, StateDeps, ProverbsState
from database import init_pool, close_pool, get_proverbs_from_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Startup
    try:
        # Try to initialize the database
        await init_pool()
        
        # Load proverbs from database
        db_proverbs = await get_proverbs_from_db()
        if db_proverbs:
            print(f"📚 Loaded {len(db_proverbs)} proverbs from database")
    except Exception as e:
        print(f"⚠️  Database not configured or unavailable: {e}")
        print("   The app will continue with in-memory state only.")
    
    yield
    
    # Shutdown
    try:
        await close_pool()
    except Exception as e:
        print(f"Error closing database: {e}")

app = agent.to_ag_ui(deps=StateDeps(ProverbsState()), lifespan=lifespan)

if __name__ == "__main__":
    # run the app
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
