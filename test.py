import unittest
from unittest.mock import patch, Mock
from datetime import date
import sys, os

import main

class TestWeChatPush(unittest.TestCase):

    @patch('requests.get')
    def test_get_access_token(self, mock_get):
        # 模拟成功获取access_token的情况
        mock_get.return_value = Mock(status_code=200)
        #mock_get.return_value.json.return_value = {"access_token": "test_access_token"}
        
        #main.config = {"app_id": "wxaf8a866f51f95760", "app_secret": "ce216d479fb0bcf9fe936c040668ecc3"}
        app_id = "wxaf8a866f51f95760"
        app_secret = "ce216d479fb0bcf9fe936c040668ecc3"
        access_token = main.get_access_token(app_id, app_secret)
        #self.assertEqual(access_token, "test_access_token")
        print(access_token)
        
        # 模拟获取失败的情况
        # mock_get.return_value.json.return_value = {}
        # with self.assertRaises(SystemExit):
        #     main.get_access_token()

    @patch('requests.get')
    def test_get_weather(self, mock_get):
        # 模拟成功获取城市ID
        # mock_get.side_effect = [
        #     Mock(status_code=200, json=Mock(return_value={
        #         "code": "200",
        #         "location": [{"id": "test_location_id"}]
        #     })),
        #     Mock(status_code=200, json=Mock(return_value={
        #         "daily": [{
        #             "textDay": "Sunny",
        #             "iconDay": "100",
        #             "textNight": "Clear",
        #             "iconNight": "150",
        #             "tempMax": "30",
        #             "tempMin": "20"
        #         }]
        #     }))
        # ]
        
        #main.config = {"weather_key": "test_weather_key"}
        weather_key = "b43344eac12c473db1eb007df62a4547"
        region = "合肥"
        # 调用函数
        weather_day_text, weather_day_icon, weather_night_text, weather_night_icon, temp_max, temp_min = main.get_weather(weather_key, region)

        # 打印结果
        print("白天天气情况:", weather_day_text, "图标:", weather_day_icon)
        print("夜间天气情况:", weather_night_text, "图标:", weather_night_icon)
        print("最高气温:", temp_max)
        print("最低气温:", temp_min)
        #self.assertEqual(weather, ("Sunny", "100", "Clear", "150", "30°C", "20°C"))
        
        
        # 模拟城市查询失败
        # mock_get.side_effect = [
        #     Mock(status_code=200, json=Mock(return_value={"code": "404"}))
        # ]
        # with self.assertRaises(SystemExit):
        #     main.get_weather("wrong_region")
        
        # 模拟API key错误
        # mock_get.side_effect = [
        #     Mock(status_code=200, json=Mock(return_value={"code": "401"}))
        # ]
        # with self.assertRaises(SystemExit):
        #     main.get_weather("test_region")

    def test_get_day_left(self):
        today = date(2024, 6, 5)
        
        # 测试当日是倒数日
        self.assertEqual(main.get_day_left("2024-06-05", 2024, today), 0)
        
        # 测试未来日期
        self.assertEqual(main.get_day_left("2024-06-10", 2024, today), 5)
        
        # 测试过去日期
        self.assertEqual(main.get_day_left("2024-05-30", 2024, today), 360)

    @patch('requests.get')
    def test_get_ciba(self, mock_get):
        # mock_get.return_value = Mock(status_code=200)
        # mock_get.return_value.json.return_value = {
        #     "content": "This is a test sentence.",
        #     "note": "这是一个测试句子。"
        # }
        
        note_en1, note_en2, note_ch1, note_ch2 = main.get_ciba()
        # self.assertEqual(note_en1, "This is a ")
        # self.assertEqual(note_en2, "test sentence.")
        # self.assertEqual(note_ch1, "这是一个")
        # self.assertEqual(note_ch2, "测试句子。")
        print(note_ch1 + note_ch2)
        print(note_en1 + note_en2)

    @patch('requests.post')
    def test_send_message(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = {"errcode": 0}
        
        # Mocking data for send_message
        to_user = "test_user"
        access_token = "test_access_token"
        region_name = "test_region"
        weather_day_text = "Sunny"
        weather_day_icon = "100"
        weather_night_text = "Clear"
        weather_night_icon = "150"
        temp_max = "30°C"
        temp_min = "20°C"
        note_ch1 = "这是"
        note_ch2 = "测试"
        note_en1 = "This is"
        note_en2 = "a test"
        note_de1 = ""
        note_de2 = ""
        
        main.send_message(to_user, access_token, region_name, weather_day_text, weather_day_icon, weather_night_text, weather_night_icon, temp_max, temp_min, note_ch1, note_ch2, note_en1, note_en2, note_de1, note_de2)
        self.assertTrue(mock_post.called)
        
        # 模拟发送消息失败
        mock_post.return_value.json.return_value = {"errcode": 40037}
        main.send_message(to_user, access_token, region_name, weather_day_text, weather_day_icon, weather_night_text, weather_night_icon, temp_max, temp_min, note_ch1, note_ch2, note_en1, note_en2, note_de1, note_de2)
        self.assertTrue(mock_post.called)

    @patch('main.get_access_token')
    @patch('main.get_weather')
    @patch('main.get_ciba')
    @patch('main.send_message')
    def test_main(self, mock_send_message, mock_get_ciba, mock_get_weather, mock_get_access_token):
        mock_get_access_token.return_value = "test_access_token"
        mock_get_weather.return_value = ("Sunny", "100", "Clear", "150", "30°C", "20°C")
        mock_get_ciba.return_value = ("This is", "a test", "这是", "测试")
        
        config = {
            "app_id": "test_app_id",
            "app_secret": "test_app_secret",
            "weather_key": "test_weather_key",
            "region": "test_region",
            "user": ["test_user"],
            "template_id": "test_template_id",
            "love_date": "2020-01-01",
            "note_ch1": "",
            "note_ch2": "",
            "note_en1": "",
            "note_en2": "",
            "note_de1": "",
            "note_de2": ""
        }
        
        with patch('builtins.open', unittest.mock.mock_open(read_data=str(config))):
            with patch('sys.exit') as mock_exit:
                main.main()
                self.assertFalse(mock_exit.called)

if __name__ == '__main__':
    unittest.main()
