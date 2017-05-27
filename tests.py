import os
import needle_drop
import unittest
import tempfile

class NeedleTestCase(unittest.TestCase):

    def setUp(self):
        self.app = needle_drop.app.test_client()

    def tearDown(self):
        pass

    def test_get_video_info(self):
        # REO Speedwagon Can't Fight This Feeling
        video_id = "zpOULjyy-n8"
        data = needle_drop.get_video_info(video_id)
        self.assertEquals(data['duration'], 294)
        self.assertEquals(data['name'], 'REO Speedwagon - Can\'t Fight This Feeling')

        # Toto Africa
        video_id = "FTQbiNvZqaY"
        data = needle_drop.get_video_info(video_id)
        self.assertEquals(data['duration'], 275)
        self.assertEquals(data['name'], 'Toto - Africa')

    def test_get_playlist_videos(self):
        # 80s hits
        playlist_id = "PLCD0445C57F2B7F41"
        playlist_videos = needle_drop.get_playlist_videos(playlist_id)
        # checks that True Colors video id is in the list
        self.assertIn("LPn0KFlbqX8", playlist_videos)
        self.assertNotIn("GLvohMXgcBo", playlist_videos)
        self.assertEqual(len(playlist_videos), 201)

        # 90s hits
        playlist_id = "PL8B6CD2520590127F"
        playlist_videos = needle_drop.get_playlist_videos(playlist_id)
        # checks that Under the Bridge video id is in the list
        self.assertIn("GLvohMXgcBo", playlist_videos)
        self.assertNotIn("LPn0KFlbqX8", playlist_videos)
        self.assertEqual(len(playlist_videos), 136)


if __name__ == "__main__":
    unittest.main()
