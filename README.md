# RokuApp
Python script for Roku with UI and keyboard controls. Optionally can also include a Spotify controller
 (I added this so playing music on Chromecast didn't require switching to the Spotify app to skip tracks)

Lots of Spotify behavior not implemented\n
Buttons icon change dynamically based on play state still needs to completed, only works for play button\n

To use Spotify, there needs to be a `res/client_id.json` formatted like:
```json
{
    "client_id" : "123...xyz",
    "client_secret" : "123..xyz"
}
```
After being authenticated, the refresh token will also get stored here to avoid having to login repeatedly.\n

Spotify usage is basically forced right now, it will eventually be configurable in settings so that on launch the
Spotify authentication isn't forced on the user\n

Disabling spotify controller in settings requires relaunching app for change to take effect

Bug: Skip forward/back doesn't trigger current playing song to update immediately, update timer will take care of this 
later but there's some latency there