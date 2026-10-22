#!/usr/bin/env python3
"""Replay only the local browser extraction boundary; never call a translator."""
import argparse,functools,http.server,json,pathlib,threading
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser()
parser.add_argument('--prove-ignore-control',action='store_true',help='Remove only the fixture ignore class in the browser response and require the exclusion check to fail.')
args=parser.parse_args()
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
   if args.prove_ignore_control and request.request.url==origin+'/docs/local-boundary.html':
    response=request.fetch();body=response.text();assert 'class="ignore"' in body
    request.fulfill(response=response,body=body.replace('class="ignore"','class="not-protected"'))
   elif request.request.url.startswith(origin+'/'):request.continue_()
   else:external.append(request.request.url);request.abort()
  page.route('**/*',route)
  page.goto(origin+'/docs/local-boundary.html')
  page.wait_for_function('window.lessonResult !== undefined',timeout=10000)
  result=page.evaluate('window.lessonResult')
  assert all(result[k] for k in ['eligibleTextQueued','codeTagExcluded','originalDOMUnchanged']),result
  assert result['ignoredClassExcluded'] is (not args.prove_ignore_control),result
  assert external==[],external
  print(json.dumps({'result':result,'observed_external_request_attempts':len(external),'browser':browser.version},indent=2))
  if args.prove_ignore_control:print('PROTECTION_REMOVAL_CAUGHT')
  browser.close()
finally:
 server.shutdown();server.server_close()
