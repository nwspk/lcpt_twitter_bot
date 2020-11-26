Twitter Bot Service with Raindrop Integration
===

Service to automatically tweet selection of [raindrop.io](raindrop.io) items at regular intervals via the [@lcptuk](https://twitter.com/lcptuk) twitter account.


How to configure
---

The following features are customisable by changing their values in the [config file](https://github.com/nwspk/lcpt_twitter_bot/blob/main/config.yml):

- **running**: a boolean, `true` or `false`, turns the bot on and off
- **interval**: an integer, the amount of minutes between posting tweets. eg. `60`. Minimum is every `5` minutes; Bot won't take into account a tweeting interval shorter than the polling interval (5min)
- **raindrop_tag**: a string, only library items with this tag will be selected in the Raindrop collection. eg. `'post-to-twitter'`
- **tweet_format**: a string, the content of the tweet with placeholders with the library item attributes.
- **default_image_url**: a string, the link to the image to display with the tweet if the library item doesn't have a corresponding image. The image will be reframed by twitter. If the image url doesn't work, the bot will gracefully fall back onto not displaying an image with the tweet.

> The bot polls the config to check for changes every 5 minutes. Therefore there may be up to 5 minutes before any change is implemented. If the tweeting interval has changed to `X` min and there are `<X` min since the last tweet before the config was changed, the next tweet will be `X` min after the latest tweet.

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

2. Create a `credentials.sh` file with the twitter and raindrop authentication required inside the `lcpt_twitter_bot` folder.

  ```shell
  $ touch ./credentials.sh
  ```

  The `credential.sh` file should be laid out like this:

  ```sh
  export RAINDROP_CLIENT_ID=<paste here>
  export RAINDROP_CLIENT_SECRET=<paste here>
  export RAINDROP_TOKEN=<paste here>

  export TWITTER_KEY=<paste here> # twitter consumer key
  export TWITTER_SECRET=<paste here> # twitter consumer secret
  export TWITTER_ACCESS_TOKEN=<paste here> # twitter access token key
  export TWITTER_ACCESS_SECRET=<paste here> # twitter access token secret
  ```

3. Install required external libraries.

  ```shell
  $ pip3 install -r ./requirements.txt
  ```

4. Start the bot.

  ```shell
  $ python3 ./run.py
  ```

  Stop the bot by pressing `Ctrl-c`.

5. To run locally in the background (only works as long as you don't turn your computer off):

  Check `screen` is installed:

  ```shell
  $ screen --version
  ```

  If it returns `Screen version <etc>` you're good to go.

  ```shell
  $ screen -S bot
  $ python3 ./run.py
  ```

  Wait a few seconds to check it's running fine. You shouldn't see any `Error`s returned.

  Press `Ctrl-a` then `d` to let the bot run in the background.

  The bot will be stopped automatically if its process is killed, if you turn your computer off for example, and it won't start again until you follow the above step 5 again.
  One way to stop the bot while your computer is still running is to type:

  ```shell
  $ screen -r bot
  ```

  Then press `Ctrl-c` to stop the bot, and press `Ctrl-a` then `b` to return to normal.


Remotely on a server
---

These are instructions on how to admin the already running bot instance that is currently hosted on DigitalOcean.

1. Find the remote host (=server) IP address:

  Sign in to your Digital Ocean account and under **Projects** click on **raindrop twitter bot**. Under **Resources**, you should see **DROPLETS (1)** with the IP address. Keep track of the IP address.

2. Open a terminal and connect to the remote server:

  ```shell
  $ ssh webmaster@<ip address>
  ```

  Enter the password when asked.

3. The bot is running in a `screen`.

  ```shell
  $ screen -r bot
  ```

