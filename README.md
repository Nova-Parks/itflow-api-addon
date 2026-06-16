# ITFlow API Addon

Currently, this project adds additional REST endpoints for ITFlow.

This is kind of a fly-by-the-seat-of-my-pants project required for an ITSM migration with an imminent deadline.

I do at some point plan to implement this in ITFlow directly through PRs using the built-in PHP post backend.

eh /shrug

## !! This is not a secure REST API. There is no authentication. At all. It exposes the ITFlow database and is designed to be used as a helper for a one-time data import !!

endpoints configured:

### GET /ping
```
heartbeat endpoint
```

### POST /ticket_replies
```
{
    ticket_reply: 'ticket reply body',
    ticket_reply_by: contact or user id,
    ticket_reply_type: Client | Internal
    ticket_reply_ticket_id: ticket id,
}
```

... more