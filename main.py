#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
from authentication import auth, cleanupsessions
from controllers import main, plan, dashboard
from config import *

app = webapp2.WSGIApplication([
    (REGISTER_URI, auth.RegisterResponseHandler),
    (LOGIN_URI, auth.LoginResponseHandler),
    (LOGOUT_URI, auth.LogoutResponseHandler),
    (PLAN_URI, plan.MainHandler),
    (DASHBOARD_URI, dashboard.MainHandler),
    (ADD_MAJOR_URI, dashboard.AddMajorHandler),
    (CLEAR_MAJORS_URI, dashboard.ClearMajorsHandler),
    (DELETE_ACCOUNT_URI, auth.DeleteAccountHandler),
    (ERROR_URI, main.ErrorHandler),
    (LOAD_DATA_URI, main.LoadDataHandler),
    ('/cleanupsessions', cleanupsessions.CleanupSessionsHandler),
    ('/', main.MainHandler)
], debug=DEBUG)
