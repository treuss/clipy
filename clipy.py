#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import re
import sys
from enum import Enum


__author__ = "Thomas Reuß"
__email__ = "thomas@domain.tld"
__version__ = "0.01"
__lastupdate__ = "2023-11-14"

"""
Pattern passt auf sed-typische Scriplets, wie s/alt/neu/ oder auch
s#/tmp/file1#/tmp/file2#
"""

class CommandParser:
	
	class Command(Enum):
		SUBSTITUTE = 1
		DELETE = 2

	script_pattern = (
			r'^(?P<com>[sd])(?P<sep>[\/#~_])'
			r'(?P<needle>.*)\2(?P<rep>.*)\2(?P<mod>[mgi]*)$'
			)

	def __init__(self, scriptlet: str):
		reg = re.search(self.script_pattern, scriptlet, flags=0)
		if None != reg:
			self.set_command(reg["com"])
			self.set_needle(reg["needle"])
			self.set_replacement(reg["rep"])
			self.set_modifiers(reg["mod"])
		else:
			raise ValueError(f"Fehler in Scriptlet: {scriptlet}")

	def get_command(self):
		if 'S' == self._command:
			return self.Command.SUBSTITUTE
		elif 'D' == self._command:
			return self.Command.DELETE
		else:
			raise NotImplementedError

	def set_command(self, value):
		self._command = value.upper()

	def get_needle(self):
		return self._needle

	def set_needle(self, value):
		self._needle = value

	def get_replacement(self):
		return self._replacement

	def set_replacement(self, value):
		self._replacement = value

	def get_modifiers(self):
		return self._modifiers

	def set_modifiers(self, value):
		self._modifiers = value



def main() -> int:
	parser = argparse.ArgumentParser(
			prog = 'clipy',
			description = 'Eine rudimentäre  Implementierung von sed in Python'
		)
	parser.add_argument("-v", "--verbose", help="Erweiterte Ausgabe",
						action="store_true", required=False, default=False)
	parser.add_argument('-V', '--version', action='version',
						version=f'%(prog)s {__version__} ({__lastupdate__})')
	parser.add_argument("-i", "--in-place", help="Sollen Änderungen an der Quelldatei " \
				   "direkt in der Quelldatei stattfinden?", required=False, default=False)
	parser.add_argument('scriptlet', type=str, nargs="?",
					 help='sed-artiges Scriptlet')
	parser.add_argument('infiles', nargs='*', type=argparse.FileType('r'),
                    default=sys.stdin,
					 help='Eine oder mehrere Dateien')

	args = parser.parse_args()

	if args.verbose:
		print("Verbosity: ON")
	if not args.scriptlet:
		parser.print_help(sys.stderr)
		sys.exit(1)

	cmd_par = CommandParser(args.scriptlet)

	if CommandParser.Command.SUBSTITUTE == cmd_par.get_command():
		if type(args.infiles) is list:
			for f in args.infiles:
				haystack = f.read()
				result = re.sub(cmd_par.get_needle(),
						  cmd_par.get_replacement(),
						  haystack)
				print(result)
		else:
			haystack = args.infiles.read()
			result = re.sub(cmd_par.get_needle(),
					  cmd_par.get_replacement(),
					  haystack)
			print(result)
	else:
		raise NotImplementedError()

	if not os.isatty(0):
		for line in sys.stdin:
			print(f"{line.rstrip()}")
	return 0

if __name__ == '__main__':
	# Den Return-Code der Main-Funktion an die Shell geben
	sys.exit(main())
