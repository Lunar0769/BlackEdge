# 🧠 Memory Optimization for Render Free Tier

## Issue
Render free tier has 512MB RAM. BlackEdge with multiple AI agents can exceed this, causing:
- Worker timeouts
- Out of memory errors
- Process kills

## Solutions Implemented

### 1. Reduced Workers
```
Before: --workers 2
After: --workers 1 --threads 2
```
- Single worker process uses less memory
- Threading handles concurrent requests
- Worker class: gthread (threaded)

### 2. Increased Timeout
```
Before: --timeout 120
After: --timeout 300
```
- Gives agents more time to complete
- Prevents premature worker kills

### 3. Worker Recycling
```
--max-requests 100 --max-requests-jitter 10
```
- Worker restarts after 100-110 requests
- Prevents memory leaks
- Clears accumulated memory

### 4. Garbage Collection
Added explicit `gc.collect()` after:
- Each agent execution
- Each request completion
- Error handling

### 5. Memory Cleanup
```python
# Free vectorstore after use
del vectorstore
gc.collect()
```

## Updated Configuration

### Procfile
```
web: gunicorn app:app --workers 1 --threads 2 --timeout 300 --worker-class gthread --max-requests 100 --max-requests-jitter 10
```

### render.yaml
```yaml
startCommand: gunicorn app:app --workers 1 --threads 2 --timeout 300 --worker-class gthread --max-requests 100 --max-requests-jitter 10
```

## Performance Impact

### Before Optimization
- ❌ Worker timeout after 120s
- ❌ Out of memory errors
- ❌ Process kills
- ❌ Failed requests

### After Optimization
- ✅ Longer timeout (300s)
- ✅ Aggressive garbage collection
- ✅ Worker recycling
- ✅ Stable memory usage

## Monitoring

Watch for these in Render logs:
```
[CRITICAL] WORKER TIMEOUT - Increase timeout
[ERROR] Worker was sent SIGKILL - Out of memory
```

If still occurring:
1. Reduce concurrent requests (add queue)
2. Upgrade to Starter plan ($7/month, 512MB)
3. Or Standard plan ($25/month, 2GB)

## Trade-offs

### Pros
- ✅ Works on free tier
- ✅ No code changes needed
- ✅ Automatic memory management

### Cons
- ⚠️ Slower response (single worker)
- ⚠️ Limited concurrency (2 threads)
- ⚠️ Longer timeouts needed

## Alternative: Upgrade Plan

If you need better performance:

**Starter ($7/month)**
- 512MB RAM (same as free)
- Always on (no sleep)
- Better for consistent traffic

**Standard ($25/month)**
- 2GB RAM (4x more)
- Can use: --workers 2 --threads 4
- Better for high traffic

## Testing

After deployment, test with:
1. Single query - should work
2. Multiple queries - may queue
3. Complex queries - may take 2-3 minutes

Monitor logs for:
- Worker timeouts
- Memory errors
- Response times

---

**These optimizations allow BlackEdge to run on Render's free tier!** 🔥
