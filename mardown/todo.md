### <div style="color:green;">Archived</div>

|Type|Detail|1|2|Finished|
|---|---|---|---|---|
|code template|stoppable watcher|@/util/watcher.js|   |✅|
|msg|msg block|with head/avatar|   |✅|
|msg|msg block|without|   |✅|
|Channel Input|Function Selection Dropdown|   |   |✅|
|msg|database msg|store msg in db||✅|
|django|database PK|change some models to use snowflake ID||✅|
|msg|group_head|auto change msg to group_head||✅|
|msg|msg menu|open and close robustly||✅|
|msg|delete msg|be able to delete||✅|
|msg|image|upload files||✅|
|media|serve|serve media using view||✅|
|media|serve|add media service signature to url||✅|
|msg|parser|inputking use multiple `items` for each line of msg||✅|
|msg|parser|1msg sent and received in 1 content not a list||✅|
|msg|images|show images preview(organized)||✅|
|inputking|scroll|show jump to bottom when new msgs arrive||✅|
|msg|files|show attachments as files||✅|
|msg|input|input bug when typing Chinese||✅|
|avatar|image|save blured(❎)/scaled(✅) image as a `field` to speed up static rendering|||


### <div style="color:#E6E600;">InProgress</div>

|Type|Detail|1|2|Finished|
|---|---|---|---|---|
|msg|attachment|delete single attachment in a msg||✅|
|server|category|show empty category anyway|||
|view|error|build a 403 page|||
|inputking|scroll|show jump to bottom button when viewing old msgs|||
|inputking|code|clean it up|||
|Auth|User|change site auth user to my custom AUser|||


### <div style="color:#FF0000;">Bugs</div>

|Type|Detail|1|2|Finished|
|---|---|---|---|---|
|inputking|method|first time entering the site, automatically select a tool, which is not intended|||


### <div style="color:#00E6E6;">ToDo</div>

|Type|Detail|1|2|Finished|
|---|---|---|---|---|
|msg|socket|change socket to handle multiple channels|||
|msg|pagination|implement message pagination in channels||✅|
|django|database PK|change some models to use compound PK||
|msg|database msg|before ws connection, check channel/server permission||
|channel|create invite|invite user to `Channel`|||
|msg|mention|create `mention` in msg||
|msg|reaction part|   |   ||
|FunctionList|Default Button|Find Servers functionality|||
|user|`timeout` user|||
|user|`ban` user|||
|user|`kick` user|||
|server|invite management|create/delete/track invite codes usage||✅|
|msg|edit message|allow users to edit their own messages||
|msg|search|search messages within channels/servers||
|server|settings|server settings management UI||
|channel|settings|channel settings and permissions UI||
|user|profile|user profile customization and bio||
|notification|system|real-time notifications for mentions/DMs||
|server|discovery|public server browsing/discovery feature||
|role|management|role creation and permission management UI||



### Tips

 - don't forget ending slash in .vue url that starts with `api`, it will cause django to return redirections