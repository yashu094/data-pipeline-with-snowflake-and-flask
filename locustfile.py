from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_translations(self):
        self.client.get('/translations?language=en')

    @task
    def add_translation(self):
        self.client.post('/translations', json={
            "TALK_ID": 1003,
            "NATIVE_LANG": "de",
            "TRANSCRIPT": "Beispieltext",
            "SPEAKER_1": "Max Mustermann",
            "RECORDED_DATE": "2024-01-02",
            "TITLE": "Beispiel Titel",
            "VIEWS": 7000,
            "DURATION": 1500
        })
