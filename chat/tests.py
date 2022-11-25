from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            cls.driver = webdriver.Chrome()
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_when_chat_message_sent_seen_by_everyone_in_room(self):
        try:
            self._enter_chat_room("room_1")

            self._open_new_window()
            self._enter_chat_room("room_1")

            self._switch_to_window(0)
            self._post_message('Meow')

            WebDriverWait(self.driver, 2).until(
                lambda _: "Meow" in self._chat_log_value,
                "Message not received by window 1 from window 1"
            )
            self.switch_to_window(1)
            WebDriverWait(self.driver, 2).until(
                labda _: "Meow" in self._chat_log_value,
                "Message not received in window 2 from window 1"
            )
        finally:
            self.close_all_new_windows()


    # === Utilities === #

    def enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + "/chat/")
