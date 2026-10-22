#!/usr/bin/env python3
"""Replay only the local browser extraction boundary; never call a translator."""
import functools,http.server,json,pathlib,threading
from playwright.sync_api import sync_playwright
repo=pathlib.Path(__file__).resolve().parents[1]
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(repo))
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
origin=f'http://127.0.0.1:{server.server_port}'
external=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome',headless=True)
  page=browser.new_page()
  def route(request):
   if request.request.url.startswith(origin+'/'):request.continue_()
   else:external.append(request.request.url);request.abort()
  page.route('**/*',route)
  page.goto(origin+'/docs/local-boundary.html')
  page.wait_for_function('window.lessonResult !== undefined',timeout=10000)
  result=page.evaluate('window.lessonResult')
  assert all(result[k] for k in ['eligibleTextQueued','ignoredClassExcluded','codeTagExcluded','originalDOMUnchanged']),result
  assert external==[],external
  print(json.dumps({'result':result,'observed_external_request_attempts':len(external),'browser':browser.version},indent=2))
  browser.close()
finally:
 server.shutdown();server.server_close()
