# ITFlow API Addon

Currently, this project adds additional REST endpoints for ITFlow.

This is kind of a fly-by-the-seat-of-my-pants project required for an ITSM migration with an imminent deadline.

I do at some point plan to implement this in ITFlow directly through PRs using the built-in PHP post backend.

eh /shrug

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
    ticket_reply_ticket_id: ticket id,
}
```

... more