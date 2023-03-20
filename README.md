# pet-a-manger
> 🐈‍⬛🐈‍⬛ iwait, ifeed, istream while iwatch...

Automated cat feeder on RPi Zero W with Python.

[![balena deploy button](https://www.balena.io/deploy.svg)](https://dashboard.balena-cloud.com/deploy?repoUrl=https://github.com/belodetek/pet-a-manger)

## [iwait](https://github.com/mcuadros/ofelia)
> trigger dispensation on a [cron schedule](https://pkg.go.dev/github.com/robfig/cron)

* `IFEED_MEAL_SCHEDULE` controls cron schedule (e.g. `15 2 6 * * *` to dispense `@06:02:15`)
* `IFEED_SNACK_SCHEDULE{1,2}` controls cron (snack) schedules
* `TZ` sets timezone (e.g. `US/Pacific`)
* `IFEED_SLACK_WEBHOOK_URL` controls where scheduling errors go in Slack
* `IFEED_SLACK_ERRORS_ONLY` controls Slack logging verbosity (e.g. `true` or `false`)
* `IFEED_HEARTBEAT_URL` send an empty HTTP request to [reset alert trigger](https://healthchecks.io/)


## ifeed
> dispense on `GPIO` (physical buttons or momentary switches) or `SIGUSR{1,2}` Linux signals

* `IFEED_{MEAL,SNACK}_RUNSECS` controls dispensation duration in seconds on `SIGUSR{1,2}` events
* `IFEED_BUTTON{1,2}_GPIO` sets button pins (physical board [pin numbering scheme](https://pinout.xyz/))
* `IFEED_PWM{1,2}_GPIO` sets servo motor pins


## istream
> stream video to RTMP sink (poorly on RPi Zero W) or serve timelapse stills (better)

* `RTMP_STREAM_URL` controls where to stream (e.g. YouTube, Restream, etc.); or
* `ISTREAM_STILL` image name for timelapse (e.g. on `tmpfs`)
* `H264_PROFILE` sets H.264 profile (e.g. main, baseline, etc.)
* `VIDEO_{WIDTH,HEIGHT}` sets resolution
* `VIDEO_{FRAMERATE,BITRATE}` sets video frame-rate and quality
* `KEYFRAME_RATE` sets control frame every X video rates
* `AUDIO_SAMPLE_RATE` sets empty audio stream bitrate


## iwatch
> simple HTTP redirect with `netcat` or static HTML

* `IWATCH_HTML` controls static HTML content (e.g. YouTube iframe/embed)
* `IWATCH_URL` controls redirect URL if no static HTML specified
