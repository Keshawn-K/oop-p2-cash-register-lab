#!/usr/bin/env python3
import importlib.util
import inspect
import os
import sys

ROOT = os.path.dirname(__file__)
LIB = os.path.join(ROOT, 'lib')
sys.path.insert(0, LIB)

test_path = os.path.join(LIB, 'testing', 'cash_register_test.py')
spec = importlib.util.spec_from_file_location('cash_register_test', test_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

TestClass = None
for name, obj in inspect.getmembers(mod, inspect.isclass):
  if name == 'TestCashRegister':
    TestClass = obj
    break

if TestClass is None:
  print('No TestCashRegister class found in tests')
  sys.exit(1)

passed = 0
failed = 0
for name, func in inspect.getmembers(TestClass, predicate=inspect.isfunction):
  if name.startswith('test_'):
    # reset class-level registers to fresh instances before each test
    if hasattr(TestClass, 'cash_register') and hasattr(mod, 'CashRegister'):
      setattr(TestClass, 'cash_register', mod.CashRegister())
    if hasattr(TestClass, 'cash_register_with_discount') and hasattr(mod, 'CashRegister'):
      setattr(TestClass, 'cash_register_with_discount', mod.CashRegister(20))
    inst = TestClass()
    method = getattr(inst, name)
    try:
      method()
      print(f'PASS: {name}')
      passed += 1
    except AssertionError:
      print(f'FAIL: {name} (AssertionError)')
      failed += 1
    except Exception as e:
      print(f'ERROR: {name} ({e})')
      failed += 1

print(f'Passed: {passed}, Failed: {failed}')
sys.exit(0 if failed == 0 else 1)
