# needle_drop
A name that tune app using YouTube playlists. You select a YouTube playlist, and the app randomly picks a song from the playlist, and starts playing the song at a random time. It hides the title info and reveals it when you click a button. You can think of it as a game of who can name the song first ("name that tune"). You can also mute your computer and try to guess the song from the music video alone.

## Running locally

### YouTube API Key
To run this locally, you will need a YouTube API Key (this allows the app to get playlist info and song info). Follow directions [here](https://developers.google.com/youtube/registering_an_application). You do not need OAuth, just an API Key. It should be about 40 characters. You should note the key, as you will be using it later.

### Download and Running
If you don't have it, install virtualenv
```bash
pip install virtualenv
```
or use your favorite virtual environment wrapper.

Download the repo, install requirements.
```bash
git clone https://github.com/lonoffd/needle_drop.git
cd needle_drop
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Now, you will either need to add your YouTube API Key as an environment variable (better if you are sharing the code publicly, e.g. on github) or you can hard code it in the python file (fine if you are just running locally).

To add as an environment variable:
```bash
export YOUTUBE_API_KEY="<your key goes here>"
```
For example, if the key was Abcd123456789, you would enter
```bash
export YOUTUBE_API_KEY="Abcd123456789"
```
Alternatively, you can hard code (again, only if you aren't sharing/commiting it anywhere publicly) it by replacing the line
```python
API_KEY = os.environ["YOUTUBE_API_KEY"]
```
with
```python
API_KEY = "Abcd123456789"
```

Now, you can run it:
```bash
python needle_drop.py
```
And opening a browser to localhost:5000

There are a few default playlists. You can look up playlists on YouTube (they have IDs in the URL of the form PL#######), and add them to the needle_drop.py PLAYLISTS list, or you can use a playlist by dropping it into the URL localhost:5000/PL########.
