# coding: spec

# The noy plugin for nosetests (enabled by the --with-noy option)
# will register the "spec" codec, which means any file that has
# "# coding: sepc" as the first line, like this file, will be parsed
# by the spec codec before it is imported.

# The codec will then turn what you have written into proper
# , executable python code!

# The test can then be specified using describes and its

# TRY:
# nosetests --with-spec --spec-color --with-noy spec

import logging
import json
import server
from expects import *
from noseOfYeti.tokeniser.support import noy_sup_setUp, noy_sup_tearDown

describe "Test Pet Server":

    before_each:
        # Only log criticl errors
        server.app.debug = False
        server.initialize_logging(logging.ERROR)
        server.Pet.remove_all()
        server.Pet(0, 'fido', 'dog').save()
        server.Pet(0, 'kitty', 'cat').save()
        self.app = server.app.test_client()

    after_each:
        server.Pet.remove_all()

    it "should response to index page":
        resp = self.app.get('/')
        expect(resp.status_code).to(equal(200))
        expect('Pet Demo REST API Service' in resp.data).to(be_true)

    it "should return a list of pets":
        resp = self.app.get('/pets')
        expect(resp.status_code).to(equal(200))
        expect(len(resp.data)).to(be_above(0))

    it "should return a single pet":
        resp = self.app.get('/pets/2')
        expect(resp.status_code).to(equal(200))
        data = json.loads(resp.data)
        expect(data).to(have_key('name', match('kitty')))

    it "should not be found":
        resp = self.app.get('/pets/0')
        expect(resp.status_code).to(equal(404))

    ignore "should add a new pet":
        pass
