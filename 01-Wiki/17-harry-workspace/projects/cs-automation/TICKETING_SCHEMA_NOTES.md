# Supabase Ticketing Schema Deployment Notes

## Deployment Status
- **SQL Migration File**: Created at `C:\Users\gemc\clawd\projects\cs-automation\supabase-ticketing-schema.sql`.
- **Deployment Status**: FAILED/PENDING.
  - Management API (sbp_...) returned 403 Forbidden.
  - Service Role Key returned 401 Invalid API Key for REST access (likely project ref mismatch or key expiry).
  - Direct `psql` access is required but not available in this environment.

## Schema Summary
The schema includes:
1. **Tables**:
   - `tickets`: Main ticket storage with `ticket_number` (serial), status, priority, channel, and customer details.
   - `ticket_messages`: Threaded messages for each ticket (customer/agent/system).
   - `ticket_tags`: Master list of tags with colors.
2. **Views**:
   - `v_open_tickets`: Filtered view for active tickets.
   - `v_ticket_summary`: Joined view with message counts and last activity timestamps.
3. **Automation (Triggers)**:
   - `updated_at`: Auto-updates on ticket modification.
   - `first_response_at`: Captured on the first agent message.
   - `resolved_at`: Automatically set/cleared based on status transitions.

## Next Steps
- Manual deployment via Supabase SQL Editor using the generated `.sql` file.
- Verify Management Token permissions.
- Verify Project Reference in the provided Service Role Key.
