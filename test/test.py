#!/usr/bin/env python3
from glob import glob
from subprocess import run

import yaml
from yaml import Loader as YamlLoader
import plumbum as pb

CODE_EXT = '.hvm'
BASE_CMD = ['hvm', 'run']

def run_test(code_path, args) -> str: 
  p = run(
    [*BASE_CMD, code_path, *args],
    capture_output=True,
  )
  output = p.stdout
  return output.decode('utf-8')

def main():
  tests_folder = pb.local.path("./test/tests")
  config_files = tests_folder.glob("*.yml")
  for config_file_path in config_files:
    basename = config_file_path.name.rstrip('.yml')
    with open(config_file_path, 'r') as f:
      config = yaml.load(f, YamlLoader)
    
    for test in config['tests']:
      print(test)
      input_args = test['input']
      expected_output = test['output']
      code_path = tests_folder / basename / CODE_EXT

      input_args = map(str, input_args)
      output = run_test(code_path, input_args)

      print(output)

  pass
 
if __name__ == "__main__":
  main()
