# -*- coding: utf-8 -*-
import pyonmttok
import sys
import logging

def create_logger(logfile, loglevel):
  numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
      logging.error("Invalid log level={}".format(loglevel))
      sys.exit()
    if logfile is None or logfile == 'stderr':
      logging.basicConfig(format='[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s', datefmt='%Y-%m-%d_%H:%M:%S', level=numeric_level)
      logging.debug('Created Logger level={}'.format(loglevel))
    else:
      logging.basicConfig(filename=logfile, format='[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s', datefmt='%Y-%m-%d_%H:%M:%S', level=numeric_level)
      logging.debug('Created Logger level={} file={}'.format(loglevel, logfile))

sp_model = None
log_level = 'info'
prog = sys.argv.pop(0)
usage = '''usage: {} -sp_model_path FILE [-log_level LEVEL] < stdin
   -sp_model_path FILE : SentencePiece model file
   -log_level   STRING : log level [debug, info, warning, critical, error] (info)
'''.format(prog)

while len(sys.argv):
  tok = sys.argv.pop(0)
  if tok=='-h':
    sys.stderr.write(usage)
    sys.exit()
  elif tok=='-sp_model' and len(sys.argv)>=0:
    sp_model = sys.argv.pop(0)
  elif tok=="-log_level":
    log_level = sys.argv.pop(0)
  else:
    sys.stderr.write('error: unparsed {} option\n'.format(tok))
    sys.stderr.write(usage)
    sys.exit()

create_logger(None, log_level)

if sp_model is None:		
  logging.error('error: missing -sp_model option')    
  sys.exit()


token = pyonmttok.Tokenizer(mode = 'space', sp_model_path = sp_model, joiner_annotate = True)
#token = pyonmttok.Tokenizer(mode = 'space', sp_model_path = sp_model, spacer_annotate = True)
for l in sys.stdin:
  t, _ = token.tokenize(l.rstrip())
  print(' '.join(t))
