# build
> 🔩🛠️ brief notes on the build, optimised for junk/materials on hand..

The metal frame base was up-cycled from a junk treadmill and paired with galvanised (M8)
threaded rod using M8 nuts and washers. Modified [Zevro KCH-06139] wall mounted cereal
dispenser was used as main payload delivery, secured to [offset slotted steel angle] with
three eight millimetre pop rivets. See [images] for how the servos are coupled to the
dispenser knobs. The rest of the delivery was hacked together from 45 degree elbows and
central vacuum PVC pipe, cut at 45 degree angle at the end touching the bowls and attached
to the vertical rods with some more threaded rod and clamps. [Servos] are held in place
with left over car roof awning brackets, secured onto vertical shafts (threaded rod) with
nuts and washers and padded with some packaging foam.

The center dispenser was modified to hold water by gluing the bottom plug shut with pour
resin and adding a 1/4" push-fit tube bulkhead (drill in the bulkhead first, before
pouring). Water is then gravity fed via [12VDC 1/4" push-fit solenoid valve] and
[water level sensor relay board]. The [water sensor] is a length of 1/4" HVAC copper pipe
flared on one end, covered with corrugated electrical conduit with three copper wire rings
for connection to the relay board and a 1/4" compression coupling to solenoid valve.

All electronics, buttons and switches fit in between the slotted angles. Aside from RPi
Zero W and case left over from [another] project, I used a common step-down buck converter
to bring 12VDC down to 5VDC for the RPi. Everything was soldered onto a breadboard, which
was installed in old hair product plastic box with holes drilled in for cabling. The
camera is an old RPi module (~ v1.3) with a fish eye lens replacing the stock lens. It's
housed in an old dental floss box and secured under the slotted steel angle with velcro
tape. The light was the last minute addition, up-cycled from a bicycle light found on a
street a decade or so ago.

The main [ifeed] software is written in Python and held together with Bash scrips and
"balenafied" Docker compose. Servos can be controlled by momentary switches as well as Linux `SIGUSR`
signals. I used `USR1` for snack and `USR2` for meal. The only difference between the two
is the amount of time the servos run, defined in [config.py]. The [iwait] scheduler execs
into the `ifeed` container on a cron schedule and dispenses by sending an appropriate
signal to the Python process. My [istream] solution can stream to an RTMP sink as well
as take timelapse stills. Streaming on RPi Zero is marginal and doesn't leave enough
compute to run the servos properly. I left it there as an option to use on higher powered
devices, but for RPi Zero(s), I set `ISTREAM_STILL` environment variable instead.

The solution is deployed to balenaCloud for convenience. Because `RPi Zero` is weak, I
used a tiny `nweb` HTTP server, as well as `netcat` to serve images/pages and `Traefic`
for reverse proxying it. Since balenaCloud offers public device URLs, HTTPS certificates
are handled for me.

[ifeed]: #ifeed "ifeed container service"
[another]: https://github.com/balena-labs-projects/inkyshot
[Zevro KCH-06139]: https://www.amazon.ca/KCH-06139-Indispensable-SmartSpace-Dry-Food-Dispenser/dp/B0009MGQUM
[12VDC 1/4" push-fit solenoid valve]: https://www.aliexpress.com/item/4000976038622.html
[offset slotted steel angle]: https://www.canadiantire.ca/en/pdp/steelworks-plated-steel-offset-angle-adjustable-14-gauge-zinc-plated-assorted-sizes-0616198p.0616199.html
[water level sensor relay board]: https://www.aliexpress.com/item/32978205921.html
[images]: images
[water sensor]: images/water-level-sensor.png "close up of the water sensor assembly"
[config.py]: ifeed/config.py
[iwait]: iwait/main.sh
[istream]: docker-compose.yml "balenafied composition"
[Servos]: https://www.aliexpress.com/item/1005003256573988.html