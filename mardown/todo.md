### Archived

|Type|Detail|1|2|Finished|
|---|---|---|---|---|
|code template|stoppable watcher|@/util/watcher.js|   |✅|
|msg|msg block|with head/avatar|   |✅|
|msg|msg block|without|   |✅|
|msg|reaction part|   |   ||
|Channel Input|Function Selection Dropdown|   |   |✅|
|FunctionList|Default Button|Find Servers|   ||
|msg|database msg|store msg in db||✅|

### ToDo

|Type|Detail|1|2|Finished|
|---|---|---|---|---|
|django|database PK|change some models to use snowflake ID and modify PK scheme (using compound ones)||
|msg|database msg|before ws connection, check channel/server permission||
|msg|delete msg|be able to delete||
|channel|create invite|invite user to `Channel`||
|msg|mention|create `mention` in msg||
|urls|serve media with permission|||
|user|`timeout` user|||
|user|`ban` user|||
|user|`kick` user|||



### Tips

 - don't forget ending slash in .vue url that starts with `api`, it will cause django to return redirections