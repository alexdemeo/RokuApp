# RokuApp
Python script for Roku with UI and keyboard controls. Optionally can also include a Spotify controller (I added this so playing music on Chromecast didn't require using Spotify app to flip back and forth)

Lots of spotify behavior not implemented
Planning to have spotify buttons change icons dynamically based on play state

To use Spotify, there needs to be a `client_id.json` in `/res` formatted like:
```json
{
    "client_id": "123...xyz",
    "client_secret": "123..xyz"
}
```
After being authenticated, the refresh token will also get stored here to avoid having to login repeatedly. 

Spotify usage is basically forced right now, it will eventually be configurable in settings so that on launch the
Spotify authentication isn't forced on the user