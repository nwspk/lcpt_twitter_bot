Twitter Bot Service with Raindrop Integration
===

Service to automatically tweet selection of [raindrop.io](raindrop.io) items at regular intervals.


How to configure
---

The following features are customisable by changing their values in the [config file](https://github.com/nwspk/lcpt_twitter_bot/blob/main/config.yml):

- **interval**: an integer, the amount of minutes between posting tweets. eg. `60`
- **raindrop_tag**: a string, only library items with this tag will be selected in the Raindrop collection. eg. `'post-to-twitter'`
- **tweet_format**: a string, the content of the tweet with placeholders with the library item attributes.

### Tweet format

The tweet will always display the raindrop cover image of the raindrop library item when possible.

Available library item attributes are:
  - `{title}`
  - `{url}`
  - `{description}`
  - `{tags}` that will show as `#tag1 #tag2 #tag3`

The most up-to-date available library item attributes can be seen in the [`content` dictionary](https://github.com/nwspk/lcpt_twitter_bot/blob/a0681d91434cb187693a108b011c569ee936a0e3/fetch_from_raindrop.py#L97-L102)

The `tweet_format` string follows the rules of python**3** string formatting: https://pyformat.info/.

A `tweet_format` example is `'{title:.100}\n\n{url}'` where the title is **truncated** after 100 characters.

> :warning: A tweet won't be posted if it is over 280 characters.


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

