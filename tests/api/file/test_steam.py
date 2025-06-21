from unittest.mock import patch

def dummy_iter(content: bytes):
    return (chunk for chunk in [content])


class TestFileStream:
    def test_stream_video_file(self, test_client):
        with patch("src.api.file.stream.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.stream.folder_destination", return_value="/videos"), \
             patch("src.api.file.stream.iterfile", return_value=dummy_iter(b"\x00\x00\x00\x20ftypisom")), \
             patch("pathlib.Path.exists", return_value=True):

            response = test_client.get("/file/stream/?file_name=video.mp4")
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("video/")
            assert response.content == b"\x00\x00\x00\x20ftypisom"

    def test_stream_photo_file(self, test_client):
        with patch("src.api.file.stream.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.stream.folder_destination", return_value="/photos"), \
             patch("src.api.file.stream.iterfile", return_value=dummy_iter(b"\xff\xd8\xff\xe0")), \
             patch("pathlib.Path.exists", return_value=True):

            response = test_client.get("/file/stream/?file_name=photo.jpg")
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("image/")
            assert response.content == b"\xff\xd8\xff\xe0"

    def test_file_not_found(self, test_client):
        with patch("src.api.file.stream.get_external_drive_path", return_value="/fake_drive/"), \
             patch("src.api.file.stream.folder_destination", return_value="/photos"), \
             patch("pathlib.Path.exists", return_value=False):

            response = test_client.get("/file/stream/?file_name=missing.jpg")
            assert response.status_code == 404
            assert response.json() == {"detail": "File not found"}
