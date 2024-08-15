### Archived

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

### InProgress

|Type|Detail|1|2|Finished|
|---|---|---|---|---|
|msg|parser|inputking use multiple `items` for each line of msg||*|
|msg|parser|1msg sent and received in 1 content not a list|||
|inputking|files|show selected files above inputking|||
|msg|files|show attachments as files|||
|Auth|User|change site auth user to my custom AUser|||


* 没有selection时，input检测具体span
* 没有selection时，input检测具体span的caret position
* 有selection时，input检测具体span
* 有selection时，input检测具体span的caret position
* click检测具体span及位置



### ToDo

|Type|Detail|1|2|Finished|
|---|---|---|---|---|
|msg|socket|change socket to handle multiple channels||🤺|
|django|database PK|change some models to use compound PK||
|msg|database msg|before ws connection, check channel/server permission||
|channel|create invite|invite user to `Channel`||
|msg|mention|create `mention` in msg||
|msg|reaction part|   |   ||
|FunctionList|Default Button|Find Servers functionality|||
|user|`timeout` user|||
|user|`ban` user|||
|user|`kick` user|||



### Tips

 - don't forget ending slash in .vue url that starts with `api`, it will cause django to return redirections