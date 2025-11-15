# TickTick API - Important Information & Rate Limits

## What We Experienced

### Our Usage Today:
- **Total tasks created**: 192 successfully (180+ attempted)
- **Projects created**: 2
- **Time taken**: Approximately 15-20 minutes
- **Result**: API started returning "unknown_exception" errors after ~180 tasks

### Error Pattern:
After creating approximately 180 tasks, the API started consistently returning:
```json
{
  "errorId": "...",
  "errorCode": "unknown_exception",
  "errorMessage": "Unknown exception",
  "data": null
}
```

This suggests we hit a rate limit, though TickTick returns a generic error instead of a specific 429 (Too Many Requests) status.

## Rate Limiting Information

### Official Documentation:
- TickTick does NOT publicly document specific rate limit numbers
- Documentation is at: https://developer.ticktick.com/api (requires login)
- The API uses OAuth 2.0 for authentication

### What We Know:
Based on our experience and common API patterns:

**Likely Limits:**
- **Per-minute limit**: Unknown, but errors started after rapid task creation
- **Daily quota**: Possibly around 200-300 requests per day for free tier
- **Burst limit**: API can handle quick successive requests initially, then throttles

**Our Strategy:**
- Used 0.1 second delays between tasks initially (worked fine)
- Hit limits after ~180-190 tasks total
- Increasing delays to 2 seconds didn't help (quota already exceeded)

## Best Practices

### For Bulk Operations:
1. **Batch in smaller groups**: Create 50-100 tasks at a time, then wait
2. **Add delays**: Use 0.5-1 second delays between requests
3. **Monitor for errors**: Watch for "unknown_exception" errors
4. **Retry logic**: Wait 60 seconds before retrying on errors
5. **Daily planning**: Spread bulk imports across multiple days if needed

### Rate Limit Recovery:
- **Wait time**: Likely 24 hours for quota reset
- **Retry strategy**: Exponential backoff (wait 1min, 5min, 15min, etc.)
- **Alternative**: Add remaining tasks manually through the app

## Our Token Information

### Access Token Details:
- **Token**: Stored in `ticktick_token.json`
- **Type**: Bearer token (OAuth 2.0)
- **Expires in**: ~180 days (15,551,866 seconds)
- **Scope**: `tasks:write`
- **Created**: November 14, 2024

### Token Management:
- Token will expire in approximately 6 months
- Need to re-authorize when token expires
- Keep `client_id` and `client_secret` safe (in ticktick_get_token.py)

## What's Missing

**Tivaleo Tasks (21 tasks):**
All under "Special Considerations" section - see `missing_tivaleo_tasks.txt`

**Options to complete:**
1. **Wait 24 hours**: Run `add_missing_tasks.py` tomorrow
2. **Manual entry**: Add from the text file (organized by category)
3. **TickTick web interface**: Faster than mobile app for bulk entry

## API Endpoints We Used

### Successfully Used:
- `POST /open/v1/project` - Create project/list
- `POST /open/v1/task` - Create task with optional parent

### Structure:
```python
# Create task
{
  "title": "Task name",
  "projectId": "project_id",
  "parentId": "parent_task_id"  # Optional, for subtasks
}
```

## Recommendations Going Forward

### For Future Imports:
1. **Plan ahead**: Split large imports (100+ tasks) across multiple days
2. **Use delays**: 0.5-1 second between requests is safe
3. **Monitor usage**: Keep track of daily API calls
4. **Have backup**: Keep txt files of tasks for manual entry if needed

### Account Type Considerations:
- **Free account**: May have stricter limits
- **Premium account**: Might have higher quotas (not confirmed)
- Contact TickTick support for exact limits based on account type

## Files in This Project

### Created Files:
1. `ticktick_get_token.py` - OAuth token retrieval
2. `ticktick_token.json` - Stored access token
3. `add_tasks_to_ticktick.py` - Main bulk import script
4. `add_missing_tasks.py` - Script for remaining tasks
5. `missing_tivaleo_tasks.txt` - Manual task list
6. `ticktick_swadha_bangles.txt` - Source task list
7. `ticktick_tivaleo.txt` - Source task list

### Security Notes:
- Keep `ticktick_token.json` private (contains access token)
- Keep `ticktick_get_token.py` private (contains client secret)
- Add these to .gitignore if sharing repository

## Summary

**What worked:**
- Successfully imported 192 tasks with parent-child hierarchy
- OAuth authentication flow
- Automated bulk task creation

**What to improve:**
- Need to spread large imports across multiple days
- Add better error handling for rate limits
- Implement retry logic with exponential backoff

**Current status:**
- 192/213 tasks imported (90% complete)
- 21 tasks remaining (documented for manual entry or retry tomorrow)
- Both projects set up with proper structure in TickTick

---
*Last updated: November 14, 2024*
