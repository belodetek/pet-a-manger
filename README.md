# pet-a-manger
> 🐈‍⬛🐈‍⬛ iwait, ifeed, istream while iwatch...

Automated cat feeder on RPi Zero W with Python.

## iwait
> trigger dispensation on a [cron schedule](https://pkg.go.dev/github.com/robfig/cron)

* `IFEED_SCHEDULE` controls cron schedule (e.g. `15 2 6 * * *` to dispense `@06:02:15`)
* `TZ` sets timezone (e.g. `US/Pacific`)
* `IFEED_SLACK_WEBHOOK_URL` controls where scheduling errors go in Slack
* `IFEED_SLACK_ERRORS_ONLY` controls Slack logging verbosity (e.g. `true` or `false`)
* `IFEED_HEARTBEAT_URL` send an empty HTTP request to [reset alert trigger](https://healthchecks.io/)


## ifeed
> dispense on `GPIO` or `SIGUSR2` events

* `IFEED_RUNSECS` controls dispensation duration on `USR2` event
* `IFEED_BUTTON{1,2}_GPIO` sets button pins (physical board [pin numbering scheme](https://pinout.xyz/))
* `IFEED_PWM{1,2}_GPIO` sets servo motor pins


## istream
> stream video to RTMP URL, poorly

* `RTMP_STREAM_URL` controls where to stream
* `H264_PROFILE` sets H.264 profile (e.g. main, baseline)
* `VIDEO_{WIDTH,HEIGHT}` sets resolution
* `VIDEO_{FRAMERATE,BITRATE}` sets video frame-rate and quality
* `KEYFRAME_RATE` sets control frame every X video rates
* `AUDIO_SAMPLE_RATE` sets empty audio stream bitrate


## iwatch
> simple HTTP redirect or static HTML

* `IWATCH_HTML` controls static HTML content (e.g. iframe/embed)
* `IWATCH_URL` controls redirect URL if no static HTML specified
