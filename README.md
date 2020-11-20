Twitter Bot Service with Raindrop Integration
===

Service to automatically tweet selection of [raindrop.io](raindrop.io) items at regular intervals.


Features
---

Configurable:
- twitter account to tweet from: [@lcptuk](https://www.twitter.com/lcptuk)
- raindrop account to take from: X
- raindrop tag to select from: default #post-to-twitter
- frequency: [default] every 10 minutes
- start / stop: ?
- tweet content: [default] title, url, link to read-only raindrop library, description if space


How to run
---

The following instructions require knowing how to type commands into the terminal.

It assumes Python version >3.8 is already installed.
You can check with:

```shell
$ python --version
```

### Locally

You may want to run this bot locally to test it, or if you don't need the features of a dedicated production server.

1. Import the project:

  ```shell
  $ git clone git@github.com:nwspk/lcpt_twitter_bot.git
  $ cd lcpt_twitter_bot
  ```

2. Create a `credential.txt` file with the twitter and raindrop authentication required inside the `lcpt_twitter_bot` folder.

  ```shell
  $ touch ./credentials.txt
  ```

  The `credential.txt` file should be laid out like this:

  ```yaml
  raindrop:
    client_id: '<paste here>'
    client_secret: '<paste here>'
    token: '<paste here>'

  twitter:
    consumer_key: '<paste here>'
    consumer_secret: '<paste here>'
    access_token:
      key: '<paste here>'
      secret: '<paste here>'
  ```

3. Install required external libraries.

  ```shell
  $ pip3 install -r ./requirements.txt
  ```

4. To do a test run:

  ```shell
  $ python3 ./fetch_from_raindrop.py
  ```

  Stop by pressing `Ctrl-c`.

5. To run locally in the background (only works as long as you don't turn your computer off):

  Check `screen` is installed:

  ```shell
  $ screen --version
  ```

  If it returns `Screen version <etc>` you're good to go.

  ```shell
  $ screen -S my_twitter_bot
  $ python3 ./fetch_from_raindrop.py
  ```

  Wait a few seconds to check it's running fine. You shouldn't see any `Error`s returned.

  Press `Ctrl-a` then `d` to let the bot run in the background.

  The bot will be stopped automatically if its process is killed, if you turn your computer off for example, and it won't start again until you follow the above step 5 again.
  One way to stop the bot while your computer is still running is to type:

  ```shell
  $ screen -r my_twitter_bot
  ```

  Then press `Ctrl-c` to stop the bot, and press `Ctrl-a` then `b` to return to normal.


Where to configure main features:
---

TODO

