# --- Ollama Fallback Test ---
import pytest
from unittest.mock import patch

def test_ollama_fallback():
    # Import dispatch from main
    from main import dispatch
    with patch('main.ollama_query', return_value="Ollama says hi") as mock_ollama, \
         patch('handlers.listener.speak') as mock_speak, \
         patch('builtins.quit'):
        # Use a query that does NOT match any handler keywords
        dispatch("foobar unmatched query")
        mock_ollama.assert_called_once()
        mock_speak.assert_called_with("Ollama says hi")

# --- Guidance for fixing handler mocks ---
# For AssertionError: Expected 'open_new_tab' to have been called once:
# - Ensure you patch the correct function (e.g., 'webbrowser.open_new_tab' or your wrapper).
# - Make sure your test input triggers the handler logic.
#
# For AssertionError: Expected 'handle' to have been called once:
# - Patch/mock the correct handler (e.g., 'handlers.search.handle').
# - Ensure the test input matches the new dispatch logic.
import pytest
import sys
from unittest.mock import patch, MagicMock, mock_open

# ── Mock heavy imports before any handler is loaded ──────────────────────────
sys.modules['pyttsx3'] = MagicMock()
sys.modules['speech_recognition'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()
sys.modules['psutil'] = MagicMock()
sys.modules['pyjokes'] = MagicMock()
sys.modules['wikipedia'] = MagicMock()
sys.modules['webbrowser'] = MagicMock()
sys.modules['smtplib'] = MagicMock()
sys.modules['requests'] = MagicMock()

# ── Patch speak globally so no TTS fires during tests ────────────────────────
SPEAK = 'handlers.voice.speak'


# =============================================================================
# datetime_handler
# =============================================================================
class TestDatetimeHandler:
    def test_time_query(self):
        import handlers.datetime_handler as dh
        with patch('handlers.datetime_handler.speak') as mock_speak:
            dh.handle('what is the current time')
            calls = [c.args[0] for c in mock_speak.call_args_list]
            assert 'The current time is' in calls

    def test_date_query(self):
        import handlers.datetime_handler as dh
        with patch('handlers.datetime_handler.speak') as mock_speak:
            dh.handle('what is the current date')
            calls = [c.args[0] for c in mock_speak.call_args_list]
            assert 'The current date is' in calls

    def test_time_takes_priority_over_date(self):
        import handlers.datetime_handler as dh
        with patch('handlers.datetime_handler.speak') as mock_speak:
            dh.handle('time and date')
            calls = [c.args[0] for c in mock_speak.call_args_list]
            assert 'The current time is' in calls


# =============================================================================
# personal
# =============================================================================
class TestPersonal:
    def test_who_are_you(self):
        # Patch the correct speak function and ensure handler calls it
        with patch('handlers.personal.speak') as mock_speak:
            from handlers import personal
            personal.handle('who are you')
            mock_speak.assert_called()
            assert any('myPA' in str(c) for c in mock_speak.call_args_list)

    def test_developer_query_reads_file(self):
        import handlers.personal as personal_mod
        with patch('handlers.personal.speak') as mock_speak, \
             patch('builtins.open', mock_open(read_data='Praveen Kumar')):
            personal_mod.handle('tell me about your developer')
            mock_speak.assert_called()
            assert any('Praveen Kumar' in str(c) for c in mock_speak.call_args_list)

    def test_father_query_reads_file(self):
        with patch(SPEAK), \
             patch('builtins.open', mock_open(read_data='dev info')):
            from handlers import personal
            personal.handle('who is your father')  # should not raise


# =============================================================================
# search
# =============================================================================
class TestSearch:
    def test_wikipedia_search(self):
        import handlers.voice as voice_mod
        voice_mod.speak = MagicMock()
        with patch('handlers.search.wikipedia') as mock_wiki, \
             patch('handlers.search.speak'):
            mock_wiki.summary.return_value = 'Python is a language.'
            from handlers import search
            search.handle('what is python')
            mock_wiki.summary.assert_called_once()

    def test_google_search(self):
        with patch('handlers.search.speak'), \
             patch('handlers.search.takeCommand', return_value='youtube'), \
             patch('handlers.search.wb.open_new_tab') as mock_open:
            from handlers import search
            search.handle('search on google for something')
            mock_open.assert_called_once_with('youtube.com')

    def test_open_website(self):
        with patch('handlers.search.speak'), \
             patch('handlers.search.takeCommand', return_value='github'), \
             patch('handlers.search.wb.open_new_tab') as mock_open:
            from handlers import search
            search.handle('open website')
            mock_open.assert_called_once_with('github.com')

    def test_wikipedia_page_not_found(self):
        with patch('handlers.search.wikipedia') as mock_wiki, \
             patch('handlers.search.speak') as mock_speak:
            mock_wiki.exceptions.PageError = Exception
            mock_wiki.summary.side_effect = Exception('Page not found')
            from handlers import search
            search.handle('what is fine pages for bullets')
            assert any('could not find' in str(c).lower() for c in mock_speak.call_args_list)

    def test_wikipedia_disambiguation(self):
        with patch('handlers.search.wikipedia') as mock_wiki, \
             patch('handlers.search.speak') as mock_speak:
            mock_wiki.exceptions.PageError = type('PageError', (Exception,), {})
            disambiguation = type('DisambiguationError', (Exception,), {'options': ['Python (language)', 'Python (snake)']})
            mock_wiki.exceptions.DisambiguationError = disambiguation
            mock_wiki.summary.side_effect = disambiguation('ambiguous')
            from handlers import search
            search.handle('what is python')
            assert any('specific' in str(c).lower() for c in mock_speak.call_args_list)
        with patch('handlers.search.wikipedia') as mock_wiki, \
             patch('handlers.search.speak'):
            mock_wiki.summary.return_value = 'Result.'
            from handlers import search
            search.handle('who is iron man')
            call_query = mock_wiki.summary.call_args[0][0]
            assert 'who' not in call_query


# =============================================================================
# email_handler
# =============================================================================
class TestEmailHandler:
    def test_send_email_success(self):
        with patch('handlers.email_handler.speak') as mock_speak, \
             patch('handlers.email_handler.takeCommand', return_value='hello boss'), \
             patch('handlers.email_handler._sendEmail') as mock_send:
            from handlers import email_handler
            email_handler.handle('send email')
            mock_send.assert_called_once_with('reciever@xyz.com', 'hello boss')
            assert any('sent' in str(c).lower() for c in mock_speak.call_args_list)

    def test_send_email_failure(self):
        with patch('handlers.email_handler.speak') as mock_speak, \
             patch('handlers.email_handler.takeCommand', return_value='hello'), \
             patch('handlers.email_handler._sendEmail', side_effect=Exception('SMTP error')):
            from handlers import email_handler
            email_handler.handle('send email')
            assert any('Unable' in str(c) for c in mock_speak.call_args_list)


# =============================================================================
# system
# =============================================================================
class TestSystem:
    def test_logout(self):
        with patch('handlers.system.os.system') as mock_os:
            from handlers import system
            system.handle('logout')
            mock_os.assert_called_once_with('shutdown -1')

    def test_restart(self):
        with patch('handlers.system.os.system') as mock_os:
            from handlers import system
            system.handle('restart')
            mock_os.assert_called_once_with('shutdown /r /t 1')

    def test_shutdown(self):
        with patch('handlers.system.os.system') as mock_os:
            from handlers import system
            system.handle('shut down')
            mock_os.assert_called_once_with('shutdown /r /t 1')

    def test_play_songs(self):
        with patch('handlers.system.speak'), \
             patch('handlers.system.os.listdir', return_value=['song0.mp3', 'song1.mp3']), \
             patch('handlers.system.os.startfile') as mock_start, \
             patch('builtins.quit'):
            from handlers import system
            system.handle('play songs')
            mock_start.assert_called_once()


# =============================================================================
# reminder
# =============================================================================
class TestReminder:
    def test_create_reminder(self):
        with patch('handlers.reminder.speak'), \
             patch('handlers.reminder.takeCommand', return_value='buy eggs'), \
             patch('builtins.open', mock_open()) as mock_file:
            from handlers import reminder
            reminder.handle('reminder')
            mock_file().write.assert_called()

    def test_read_reminder(self):
        with patch('handlers.reminder.speak') as mock_speak, \
             patch('builtins.open', mock_open(read_data='buy eggs')):
            from handlers import reminder
            reminder.handle('do you know anything')
            assert any('buy eggs' in str(c) for c in mock_speak.call_args_list)

    def test_create_reminder_list_trigger(self):
        with patch('handlers.reminder.speak'), \
             patch('handlers.reminder.takeCommand', return_value='call mom'), \
             patch('builtins.open', mock_open()) as mock_file:
            from handlers import reminder
            reminder.handle('create a reminder list')
            mock_file().write.assert_called()


# =============================================================================
# screenshot
# =============================================================================
class TestScreenshot:
    def test_screenshot_taken(self):
        with patch('handlers.screenshot.speak') as mock_speak, \
             patch('handlers.screenshot.pyautogui') as mock_pg:
            mock_img = MagicMock()
            mock_pg.screenshot.return_value = mock_img
            from handlers import screenshot
            screenshot.handle('take a screenshot')
            mock_pg.screenshot.assert_called_once()
            mock_img.save.assert_called_once()
            mock_speak.assert_called_with('Done!')


# =============================================================================
# system_info
# =============================================================================
class TestSystemInfo:
    def test_cpu_and_battery(self):
        with patch('handlers.system_info.speak') as mock_speak, \
             patch('handlers.system_info.psutil') as mock_psutil:
            mock_psutil.cpu_percent.return_value = 42.0
            mock_battery = MagicMock()
            mock_battery.percent = 85
            mock_psutil.sensors_battery.return_value = mock_battery
            from handlers import system_info
            system_info.handle('cpu and battery')
            assert any('42.0' in str(c) for c in mock_speak.call_args_list)
            assert any('85' in str(c) for c in mock_speak.call_args_list)


# =============================================================================
# jokes
# =============================================================================
class TestJokes:
    def test_joke_spoken(self):
        with patch('handlers.jokes.speak') as mock_speak, \
             patch('handlers.jokes.pyjokes') as mock_pyjokes:
            mock_pyjokes.get_joke.return_value = 'Why do programmers prefer dark mode?'
            from handlers import jokes
            jokes.handle('tell me a joke')
            mock_speak.assert_called_once_with('Why do programmers prefer dark mode?')


# =============================================================================
# weather
# =============================================================================
class TestWeather:
    def setup_method(self):
        pass

    def _mock_geo_response(self, city='London', lat=51.5074, lon=-0.1278):
        return {
            'results': [
                {'name': city, 'latitude': lat, 'longitude': lon}
            ]
        }

    def _mock_weather_response(self, temp=20, code=0):
        return {
            'current_weather': {
                'temperature': temp,
                'weathercode': code
            }
        }

    def test_weather_found(self):
        with patch('handlers.weather.speak') as mock_speak, \
             patch('handlers.weather.takeCommand', return_value='London'), \
             patch('handlers.weather.requests') as mock_req:
            # First call: geocoding, Second call: weather
            mock_req.get.side_effect = [
                MagicMock(json=lambda: self._mock_geo_response(city='London', lat=51.5074, lon=-0.1278)),
                MagicMock(json=lambda: self._mock_weather_response(temp=22, code=1))
            ]
            from handlers import weather
            weather.handle('what is the weather')
            assert any('London' in str(c) and '22' in str(c) and 'mainly clear' in str(c)
                       for c in mock_speak.call_args_list)

    def test_weather_city_not_found(self):
        with patch('handlers.weather.speak') as mock_speak, \
             patch('handlers.weather.takeCommand', return_value='xyz123'), \
             patch('handlers.weather.requests') as mock_req:
            mock_req.get.return_value.json.return_value = {'results': []}
            from handlers import weather
            weather.handle('temperature')
            assert any("couldn't find the weather" in str(c).lower() for c in mock_speak.call_args_list)

    def test_weather_service_error(self):
        with patch('handlers.weather.speak') as mock_speak, \
             patch('handlers.weather.takeCommand', return_value='Paris'), \
             patch('handlers.weather.requests.get') as mock_get:
            mock_get.side_effect = Exception('Network error')
            from handlers import weather
            weather.handle('temperature')
            assert any('trouble connecting' in str(c).lower() for c in mock_speak.call_args_list)

    def test_weather_condition_unknown(self):
        with patch('handlers.weather.speak') as mock_speak, \
             patch('handlers.weather.takeCommand', return_value='Berlin'), \
             patch('handlers.weather.requests') as mock_req:
            mock_req.get.side_effect = [
                MagicMock(json=lambda: self._mock_geo_response(city='Berlin', lat=52.52, lon=13.405)),
                MagicMock(json=lambda: self._mock_weather_response(temp=15, code=123))  # unknown code
            ]
            from handlers import weather
            weather.handle('weather')
            assert any('unknown conditions' in str(c).lower() for c in mock_speak.call_args_list)


# =============================================================================
# features
# =============================================================================
class TestFeatures:
    def test_features_spoken(self):
        with patch('handlers.features.speak') as mock_speak:
            from handlers import features
            features.handle('help')
            mock_speak.assert_called_once_with(features.FEATURES)

    def test_features_printed(self, capsys):
        with patch('handlers.features.speak'):
            from handlers import features
            features.handle('features')
            captured = capsys.readouterr()
            assert 'wikipedia' in captured.out


# =============================================================================
# greeting
# =============================================================================
class TestGreeting:
    def test_hello_no_time(self):
        with patch('handlers.greeting.speak') as mock_speak:
            from handlers import greeting
            greeting.handle('hello mypa')
            mock_speak.assert_called_with('what can i do for you')

    def test_good_morning(self):
        with patch('handlers.greeting.speak') as mock_speak, \
             patch('handlers.greeting.datetime') as mock_dt:
            mock_dt.datetime.now.return_value.hour = 9
            from handlers import greeting
            greeting.handle('good morning mypa')
            assert any('morning' in str(c).lower() for c in mock_speak.call_args_list)

    def test_good_afternoon(self):
        with patch('handlers.greeting.speak') as mock_speak, \
             patch('handlers.greeting.datetime') as mock_dt:
            mock_dt.datetime.now.return_value.hour = 14
            from handlers import greeting
            greeting.handle('good afternoon')
            assert any('afternoon' in str(c).lower() for c in mock_speak.call_args_list)

    def test_good_night(self):
        with patch('handlers.greeting.speak') as mock_speak, \
             patch('handlers.greeting.datetime') as mock_dt:
            mock_dt.datetime.now.return_value.hour = 21
            from handlers import greeting
            greeting.handle('goodnight')
            assert any('evening' in str(c).lower() or 'night' in str(c).lower()
                       for c in mock_speak.call_args_list)


# =============================================================================
# voice
# =============================================================================
class TestVoice:
    def test_change_to_female(self):
        import handlers.voice as voice_mod
        voice_mod.voices = [MagicMock(), MagicMock()]
        with patch('handlers.voice.speak'), \
             patch.object(voice_mod, 'voice_change') as mock_vc:
            voice_mod.handle('change to female')
            mock_vc.assert_called_with(1)

    def test_change_to_male(self):
        import handlers.voice as voice_mod
        voice_mod.voices = [MagicMock(), MagicMock()]
        with patch('handlers.voice.speak'), \
             patch.object(voice_mod, 'voice_change') as mock_vc:
            voice_mod.handle('change to male')
            mock_vc.assert_called_with(0)

    def test_voice_prompt_female_response(self):
        with patch('handlers.voice.speak'), \
             patch('handlers.voice.engine'), \
             patch('handlers.listener.takeCommand', return_value='female'):
            from handlers import voice
            voice.voices = [MagicMock(), MagicMock()]
            with patch.object(voice, 'voice_change') as mock_vc:
                voice.handle('change voice')
                mock_vc.assert_called_with(1)


# =============================================================================
# dispatcher (main.dispatch)
# =============================================================================
class TestDispatch:
    def setup_method(self):
        # patch all handlers before importing dispatch
        self.patches = {
            'datetime_handler': patch('main.datetime_handler.handle'),
            'personal':         patch('main.personal.handle'),
            'search':           patch('main.search.handle'),
            'email':            patch('main.email_handler.handle'),
            'system':           patch('main.system.handle'),
            'reminder':         patch('main.reminder.handle'),
            'screenshot':       patch('main.screenshot.handle'),
            'system_info':      patch('main.system_info.handle'),
            'jokes':            patch('main.jokes.handle'),
            'weather':          patch('main.weather.handle'),
            'features':         patch('main.features.handle'),
            'greeting':         patch('main.greeting.handle'),
            'voice':            patch('main.voice.handle'),
            'wishme_end':       patch('main.wishme_end'),
        }
        self.mocks = {k: v.start() for k, v in self.patches.items()}

    def teardown_method(self):
        for p in self.patches.values():
            p.stop()

    def _dispatch(self, query):
        from main import dispatch
        dispatch(query)

    def test_routes_time(self):
        self._dispatch('what is the current time')
        self.mocks['datetime_handler'].assert_called_once()

    def test_routes_date(self):
        self._dispatch('what is the current date')
        self.mocks['datetime_handler'].assert_called_once()

    def test_routes_personal_who_are_you(self):
        self._dispatch('who are you')
        self.mocks['personal'].assert_called_once()

    def test_routes_personal_developer(self):
        self._dispatch('tell me about your developer')
        self.mocks['personal'].assert_called_once()

    def test_routes_wikipedia(self):
        self._dispatch('search wikipedia for python')
        self.mocks['search'].assert_called_once()

    def test_routes_google(self):
        self._dispatch('search on google for something')
        self.mocks['search'].assert_called_once()

    def test_routes_email(self):
        self._dispatch('send email to my boss')
        self.mocks['email'].assert_called_once()

    def test_routes_logout(self):
        self._dispatch('logout of my account')
        self.mocks['system'].assert_called_once()

    def test_routes_restart(self):
        self._dispatch('restart my computer')
        self.mocks['system'].assert_called_once()

    def test_routes_shutdown(self):
        self._dispatch('shut down my computer')
        self.mocks['system'].assert_called_once()

    def test_routes_play_songs(self):
        self._dispatch('play songs')
        self.mocks['system'].assert_called_once()

    def test_routes_reminder(self):
        self._dispatch('reminder buy eggs')
        self.mocks['reminder'].assert_called_once()

    def test_routes_read_reminder(self):
        self._dispatch('do you know anything')
        self.mocks['reminder'].assert_called_once()

    def test_routes_screenshot(self):
        self._dispatch('take a screenshot')
        self.mocks['screenshot'].assert_called_once()

    def test_routes_cpu(self):
        self._dispatch('cpu and battery usage')
        self.mocks['system_info'].assert_called_once()

    def test_routes_joke(self):
        self._dispatch('tell me a joke')
        self.mocks['jokes'].assert_called_once()

    def test_routes_weather(self):
        self._dispatch('weather today')
        self.mocks['weather'].assert_called_once()

    def test_routes_features(self):
        self._dispatch('help')
        self.mocks['features'].assert_called_once()

    def test_routes_greeting(self):
        self._dispatch('hello mypa')
        self.mocks['greeting'].assert_called_once()

    def test_routes_voice(self):
        self._dispatch('change voice to female')
        self.mocks['voice'].assert_called_once()

    def test_routes_bye(self):
        self._dispatch('bye bye mypa')
        self.mocks['wishme_end'].assert_called_once()

    def test_routes_i_am_done(self):
        self._dispatch('i am done')
        self.mocks['wishme_end'].assert_called_once()

    def test_unknown_query_no_crash(self):
        self._dispatch('something completely unknown')
        # none of the handlers should be called
        for name, mock in self.mocks.items():
            mock.assert_not_called(), f"{name} should not have been called"
