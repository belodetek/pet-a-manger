# pet-a-manger

<head>
  <meta name="google-site-verification" content="3dUMQhIoNee09W-bUaFKWruLzBBFWq4Wz5JrTroHr40" />
</head>

> 🐈‍⬛🐈‍⬛ iwait, ifeed, istream while iwatch...

Opinionated cat feeder, [optimised for RPi Zero W] and [other materials on hand].

[![balena deploy button](https://www.balena.io/deploy.svg)](https://dashboard.balena-cloud.com/deploy?repoUrl=https://github.com/belodetek/pet-a-manger)

## [iwait](https://github.com/mcuadros/ofelia)
> trigger dispensation on a [cron schedule]

* `IWAIT_MEAL_SCHEDULE` controls cron schedule (e.g. `15 2 6 * * *` to dispense `@06:02:15`)
* `IWAIT_SNACK_SCHEDULES` controls cron (snack) schedules
* `TZ` sets timezone (e.g. `US/Pacific`)
* `IWAIT_SLACK_{WEBHOOK_URL.ERRORS_ONLY}` controls Slack integration parameters


## [ifeed]
> dispense on `GPIO` (physical push buttons) or `USR{1,2}` Linux signals

* `IFEED_{MEAL,SNACK}_RUNSECS` controls dispensation duration in seconds on `USR{1,2}` events
* `IFEED_BUTTON{1,2}_GPIO` sets button pins (physical board [pin numbering scheme]
* `IFEED_PWM{1,2}_GPIO` sets servo motor pins
* `IFEED_HEARTBEAT_URL` send an empty HTTP request to [reset alert trigger]
* `IFEED_ALERT_RESET_SIGNALS` reset trigger on specific signals only


## [istream]
> stream video to RTMP sink (poorly on RPi Zero W) with `raspivid` or serve timelapse stills (better) with `raspistill` and `nweb`

* `ISTREAM_RTMP_URL` controls where `raspivid` streams to (e.g. YouTube, Restream, etc.); **or**
* `ISTREAM_STILL` image name for `raspistill` timelapse (e.g. somewhere on `tmpfs` ideally)
* `ISTREAM_VIDEO_{H264_PROFILE,WIDTH,HEIGHT,FRAMERATE,BITRATE,KEYFRAME}` sets video parameters
* `ISTREAM_AUDIO_SAMPLE_RATE` (ffmpeg) sets empty audio stream bitrate
* `ISTREAM_IMAGE_{WIDTH,HEIGHT,ROTATE,ANNOTATE}` still image parameters


## [iwatch]
> serve a HTTP redirect or static HTML with `netcat` as well as `/health` endpoint

* `IWATCH_STATIC_HTML` controls static HTML content (e.g. YouTube iframe/embed)
* `IWATCH_REDIRECT_URL` controls redirect URL if no static HTML specified

[ifeed]: https://github.com/belodetek/pet-a-manger/tree/master/ifeed "ifeed container service"
[istream]: https://github.com/belodetek/pet-a-manger/tree/master/istream "istream container service"
[iwatch]: https://github.com/belodetek/pet-a-manger/tree/master/iwatch "iwatch container service"
[optimised for RPi Zero W]: docs/BUILD.md "my build"
[other materials on hand]: https://github.com/belodetek/pet-a-manger/tree/master/docs/images "link to images folder"
[reset alert trigger]: https://healthchecks.io "cron monitoring link"
[pin numbering scheme]: https://pinout.xyz "GPIO pin reference"
[cron schedule]: https://pkg.go.dev/github.com/robfig/cron "Go cron expression reference"
